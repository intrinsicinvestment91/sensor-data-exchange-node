"""SensorAgent — FastAPI app + state machine + Lightning payment flow.

Note: BitAgent's Agent type is an abstract base class intended for subclassing, but
direct reuse across repositories is complicated by constructor side effects and
package-relative import assumptions. SensorAgent is therefore standalone and reuses
only AgentWallet, which is vendored under bitagent/ (see THIRD_PARTY_NOTICES.md).
"""

import logging
import os
import sys
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from sden.audit_db import AuditDB
from sden.did_identity import DIDIdentity
from sden.did_identity import verify_did_signature
from sden.models import (
    ErrorCode,
    ErrorResponse,
    HealthResponse,
    ProducerInfo,
    QuoteRequest,
    QuoteResponse,
    SensorReading,
    VerifyPaymentRequest,
    VerifyPaymentResponse,
)
from sden.pricing import FlatPricingEngine, PricingEngine
from sden.sensor_reader import SensorReader
from sden.state_machine import State, StateMachine

# Bring vendored bitagent/ onto sys.path so AgentWallet is importable
_BITAGENT = os.path.join(os.path.dirname(__file__), "..", "bitagent")
if os.path.isdir(_BITAGENT) and _BITAGENT not in sys.path:
    sys.path.insert(0, _BITAGENT)

from agent_wallet import AgentWallet  # noqa: E402

logger = logging.getLogger(__name__)


class SensorAgent:
    def __init__(
        self,
        sensor_reader: SensorReader,
        pricing_engine: PricingEngine | None = None,
        audit_db_path: str = "audit.db",
        identity: DIDIdentity | None = None,
    ) -> None:
        self._sensor_reader = sensor_reader
        self._pricing = pricing_engine or FlatPricingEngine()
        self._wallet = AgentWallet()
        self._did_identity = identity or DIDIdentity()
        self.did = self._did_identity.did
        self._audit = AuditDB(audit_db_path, self._did_identity)
        self._sm = StateMachine()

        self._invoice_expiry_secs: int = int(os.environ.get("INVOICE_EXPIRY_SECS", "3600"))

        # Per-transaction ephemeral state (single-session model per RIS v1.0)
        self._current_request_id: str | None = None
        self._current_checking_id: str | None = None
        self._invoice_issued_at: float | None = None

        logger.info("SensorAgent started. DID: %s", self.did)
        self._announce_nostr()

    # ------------------------------------------------------------------
    # Boot
    # ------------------------------------------------------------------

    def _announce_nostr(self) -> None:
        """Publish Kind 30078 producer announcement on Nostr."""
        try:
            import json

            from nostr.event import Event
            from nostr.key import PrivateKey
            from nostr.relay_manager import RelayManager

            relay_manager = RelayManager()
            relay_manager.add_relay("wss://relay.damus.io")
            relay_manager.add_relay("wss://nos.lol")

            pk = PrivateKey()
            content = {
                "did": self.did,
                "sensor_type": self._sensor_reader.sensor_type,
                "price_sats": self._pricing.get_price(self._sensor_reader.sensor_type),
                "protocol": "SDEN/1.0",
            }
            event = Event(
                content=json.dumps(content),
                public_key=pk.public_key.hex(),
                kind=30078,
                tags=[["d", self.did]],
            )
            pk.sign_event(event)
            relay_manager.publish_event(event)
            relay_manager.close_connections()
            logger.info("Nostr announcement published")
        except Exception as exc:
            # Non-fatal: discovery is best-effort
            logger.warning("Nostr announcement failed (non-fatal): %s", exc)

    # ------------------------------------------------------------------
    # Endpoint handlers
    # ------------------------------------------------------------------

    def quote(self, req: QuoteRequest) -> QuoteResponse:
        # Replay attack prevention — reject reused request_ids
        request_id_str = str(req.request_id)
        if self._audit.is_seen_request_id(request_id_str):
            raise HTTPException(
                status_code=400,
                detail={
                    "error_code": ErrorCode.INVALID_REQUEST_FORMAT,
                    "message": "Duplicate request_id — replay rejected",
                },
            )

        # Verify buyer's Ed25519 signature over the request body (if buyer_did provided)
        if req.buyer_did:
            import json as _json

            payload = {
                "request_id": request_id_str,
                "sensor_type": req.sensor_type,
                "quantity": req.quantity,
                "timestamp_utc": req.timestamp_utc,
            }
            canonical = _json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
            if not verify_did_signature(req.buyer_did, canonical, req.signature):
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error_code": ErrorCode.INVALID_REQUEST_FORMAT,
                        "message": "Invalid buyer signature",
                    },
                )

        # Allow re-entry after a completed or terminated transaction
        if self._sm.state in (State.DELIVERED, State.TERMINATED):
            self._sm = StateMachine()

        if self._sm.state != State.IDLE:
            raise HTTPException(
                status_code=409,
                detail=f"Node busy, current state: {self._sm.state}",
            )

        self._sm.advance(State.IDLE)  # → REQUEST_RECEIVED
        self._audit.mark_request_id_seen(request_id_str)

        sensor_type = req.sensor_type
        if sensor_type != self._sensor_reader.sensor_type:
            self._sm.terminate()
            self._audit.log(
                str(req.request_id),
                "quote_rejected",
                {"reason": "sensor_type_not_available", "requested": sensor_type},
                error_code=ErrorCode.SENSOR_TYPE_NOT_AVAILABLE,
            )
            raise HTTPException(
                status_code=400,
                detail={
                    "error_code": ErrorCode.SENSOR_TYPE_NOT_AVAILABLE,
                    "message": "Sensor type not available",
                },
            )

        self._sm.advance(State.REQUEST_RECEIVED)  # → VALIDATED
        self._sm.advance(State.VALIDATED)          # → PRICED

        price_sats = self._pricing.get_price(sensor_type, req.quantity)
        self._current_request_id = str(req.request_id)

        invoice_data = self._wallet.create_invoice(
            price_sats, memo=f"SDEN {sensor_type} reading"
        )
        if not invoice_data:
            self._sm.terminate()
            raise HTTPException(status_code=502, detail="Failed to create Lightning invoice")

        self._current_checking_id = invoice_data["checking_id"]
        self._invoice_issued_at = time.monotonic()
        self._sm.advance(State.PRICED)  # → INVOICED

        self._audit.log(
            str(req.request_id),
            "invoice_issued",
            {"price_sats": price_sats, "checking_id": self._current_checking_id},
        )

        return QuoteResponse(
            request_id=req.request_id,
            price_sats=price_sats,
            invoice=invoice_data["bolt11"],
            checking_id=invoice_data["checking_id"],
        )

    def verify_payment(self, req: VerifyPaymentRequest) -> VerifyPaymentResponse:
        self._sm.require(State.INVOICED)

        # Invoice expiry check
        if (
            self._invoice_issued_at is not None
            and (time.monotonic() - self._invoice_issued_at) > self._invoice_expiry_secs
        ):
            self._sm.terminate()
            self._audit.log(
                str(req.request_id),
                "invoice_expired",
                {"checking_id": req.checking_id},
                error_code=ErrorCode.INVOICE_EXPIRED,
            )
            raise HTTPException(
                status_code=410,
                detail={
                    "error_code": ErrorCode.INVOICE_EXPIRED,
                    "message": "Invoice expired",
                },
            )

        if str(req.request_id) != self._current_request_id:
            raise HTTPException(
                status_code=400,
                detail={
                    "error_code": ErrorCode.INVOICE_NOT_FOUND,
                    "message": "Invoice not found",
                },
            )

        paid = self._wallet.check_invoice(req.checking_id)
        if not paid:
            raise HTTPException(
                status_code=402,
                detail={
                    "error_code": ErrorCode.PAYMENT_NOT_VERIFIED,
                    "message": "Payment not verified",
                },
            )

        self._sm.advance(State.INVOICED)  # → PAID
        self._audit.log(
            str(req.request_id), "payment_verified", {"checking_id": req.checking_id}
        )

        return VerifyPaymentResponse(request_id=req.request_id, paid=True)

    def get_data(self) -> SensorReading:
        self._sm.require(State.PAID)

        try:
            raw = self._sensor_reader.read()
        except Exception as exc:
            self._sm.terminate()
            raise HTTPException(
                status_code=503,
                detail={
                    "error_code": ErrorCode.DATA_UNAVAILABLE,
                    "message": "Sensor read failed",
                },
            ) from exc

        reading_dict = {
            "producer_did": self.did,
            "sensor_type": self._sensor_reader.sensor_type,
            "timestamp_utc": raw.timestamp_utc,
            "value": raw.value,
            "units": raw.units,
            "quality_score": raw.quality_score,
        }
        signature = self._did_identity.sign_json(reading_dict)

        self._sm.advance(State.PAID)  # → DELIVERED
        self._audit.log(
            self._current_request_id or "unknown",
            "data_delivered",
            {"value": raw.value, "units": raw.units},
        )

        return SensorReading(
            producer_did=self.did,
            sensor_type=self._sensor_reader.sensor_type,
            timestamp_utc=raw.timestamp_utc,
            value=raw.value,
            units=raw.units,
            quality_score=raw.quality_score,
            signature=signature,
        )


def build_app(agent: SensorAgent) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):  # noqa: ARG001
        yield

    app = FastAPI(title="SDEN Producer Node", version="1.0", lifespan=lifespan)

    @app.get("/td")
    def thing_description():
        """W3C WoT 1.1 Thing Description — makes SDEN interoperable with Azure IoT, Mozilla WebThings, etc."""
        sensor_type = agent._sensor_reader.sensor_type
        price_sats = agent._pricing.get_price(sensor_type)
        return {
            "@context": [
                "https://www.w3.org/2019/wot/td/v1",
                {"sden": "https://github.com/Intrinsicinvestment91/sensor-data-exchange-node#"},
            ],
            "id": agent.did,
            "title": f"SDEN {sensor_type.capitalize()} Producer",
            "description": f"Sells signed {sensor_type} readings via Bitcoin Lightning micropayments",
            "version": {"instance": "1.0"},
            "securityDefinitions": {
                "lightning": {
                    "scheme": "apikey",
                    "in": "header",
                    "name": "X-Checking-Id",
                    "description": f"Pay {price_sats} sats via Lightning; provide checking_id after payment",
                }
            },
            "security": "lightning",
            "properties": {
                sensor_type: {
                    "type": "number",
                    "unit": agent._sensor_reader.read().units if hasattr(agent._sensor_reader, "read") else "unknown",
                    "readOnly": True,
                    "description": f"Verified {sensor_type} reading signed with producer DID",
                    "forms": [
                        {
                            "href": "/data",
                            "op": "readproperty",
                            "htv:methodName": "GET",
                        }
                    ],
                }
            },
            "actions": {
                "quote": {
                    "description": f"Request a Lightning invoice for {price_sats} sats",
                    "input": {
                        "type": "object",
                        "properties": {
                            "request_id": {"type": "string", "format": "uuid"},
                            "sensor_type": {"type": "string"},
                            "quantity": {"type": "integer"},
                            "timestamp_utc": {"type": "string", "format": "date-time"},
                            "signature": {"type": "string"},
                        },
                        "required": ["request_id", "sensor_type", "quantity", "timestamp_utc", "signature"],
                    },
                    "forms": [{"href": "/quote", "htv:methodName": "POST"}],
                },
                "verify_payment": {
                    "description": "Confirm Lightning payment settlement",
                    "forms": [{"href": "/verify_payment", "htv:methodName": "POST"}],
                },
            },
            "sden:pricesSats": price_sats,
            "sden:protocol": "SDEN/1.0",
        }

    @app.get("/health", response_model=HealthResponse)
    def health():
        return HealthResponse()

    @app.get("/info", response_model=ProducerInfo)
    def info():
        return ProducerInfo(
            producer_did=agent.did,
            sensor_type=agent._sensor_reader.sensor_type,
            price_sats=agent._pricing.get_price(agent._sensor_reader.sensor_type),
        )

    @app.post("/quote", response_model=QuoteResponse)
    def quote(req: QuoteRequest):
        return agent.quote(req)

    @app.post("/verify_payment", response_model=VerifyPaymentResponse)
    def verify_payment(req: VerifyPaymentRequest):
        return agent.verify_payment(req)

    @app.get("/data", response_model=SensorReading)
    def data():
        return agent.get_data()

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):  # noqa: ARG001
        detail = exc.detail
        if isinstance(detail, dict) and "error_code" in detail:
            return JSONResponse(status_code=exc.status_code, content=detail)
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error_code=exc.status_code, message=str(detail)
            ).model_dump(),
        )

    return app
