"""Security tests — RIS v1.0 compliance: replay, expiry, signature bypass, payment skip."""

import json
import uuid
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from sden.did_identity import DIDIdentity
from sden.models import ErrorCode
from sden.pricing import FlatPricingEngine
from sden.sensor_agent import SensorAgent, build_app
from sden.sensor_reader import MockSensorReader


@pytest.fixture()
def agent_and_client(tmp_path):
    mock_wallet = MagicMock()
    mock_wallet.create_invoice.return_value = {
        "bolt11": "lnbc150n1sec",
        "checking_id": "sec-checking-id",
    }
    mock_wallet.check_invoice.return_value = True

    reader = MockSensorReader("temperature", seed=99)
    pricing = FlatPricingEngine(price_sats=150)
    with (
        patch("sden.sensor_agent.AgentWallet", return_value=mock_wallet),
        patch.object(SensorAgent, "_announce_nostr"),
    ):
        agent = SensorAgent(
            sensor_reader=reader,
            pricing_engine=pricing,
            audit_db_path=str(tmp_path / "security.db"),
        )
    return agent, TestClient(build_app(agent))


def _quote_payload(sensor_type="temperature", request_id=None):
    return {
        "request_id": request_id or str(uuid.uuid4()),
        "sensor_type": sensor_type,
        "quantity": 1,
        "timestamp_utc": "2026-04-22T00:00:00Z",
        "signature": "dummysig",
    }


# --- Replay attack ---

def test_replay_attack_rejected(agent_and_client):
    _, tc = agent_and_client
    request_id = str(uuid.uuid4())
    payload = _quote_payload(request_id=request_id)

    r1 = tc.post("/quote", json=payload)
    assert r1.status_code == 200

    # Reset state so node is IDLE again for the replay attempt
    # (complete the transaction first)
    checking_id = r1.json()["checking_id"]
    tc.post("/verify_payment", json={"request_id": request_id, "checking_id": checking_id})
    tc.get("/data")

    # Replay the same request_id
    r2 = tc.post("/quote", json=payload)
    assert r2.status_code == 400
    assert r2.json()["error_code"] == ErrorCode.INVALID_REQUEST_FORMAT


# --- Invoice expiry ---

def test_expired_invoice_returns_410(agent_and_client):
    agent, tc = agent_and_client
    agent._invoice_expiry_secs = 0  # expire immediately

    request_id = str(uuid.uuid4())
    r1 = tc.post("/quote", json=_quote_payload(request_id=request_id))
    assert r1.status_code == 200

    r2 = tc.post("/verify_payment", json={
        "request_id": request_id,
        "checking_id": r1.json()["checking_id"],
    })
    assert r2.status_code == 410
    assert r2.json()["error_code"] == ErrorCode.INVOICE_EXPIRED


def test_expired_invoice_advances_to_terminated(agent_and_client):
    agent, tc = agent_and_client
    agent._invoice_expiry_secs = 0

    request_id = str(uuid.uuid4())
    tc.post("/quote", json=_quote_payload(request_id=request_id))
    tc.post("/verify_payment", json={
        "request_id": request_id,
        "checking_id": "sec-checking-id",
    })
    from sden.state_machine import State
    assert agent._sm.state == State.TERMINATED


# --- Payment bypass: call /data without /verify_payment ---

def test_data_without_verify_payment_rejected(agent_and_client):
    _, tc = agent_and_client
    request_id = str(uuid.uuid4())
    tc.post("/quote", json=_quote_payload(request_id=request_id))
    # Skip verify_payment, try to get data directly
    r = tc.get("/data")
    assert r.status_code == 409  # INVOICED ≠ PAID


# --- Buyer signature verification ---

def test_valid_buyer_signature_accepted(agent_and_client):
    _, tc = agent_and_client
    buyer = DIDIdentity()
    request_id = str(uuid.uuid4())

    payload_for_sig = {
        "request_id": request_id,
        "sensor_type": "temperature",
        "quantity": 1,
        "timestamp_utc": "2026-04-22T00:00:00Z",
    }
    canonical = json.dumps(payload_for_sig, sort_keys=True, separators=(",", ":")).encode()
    sig = buyer.sign(canonical)

    r = tc.post("/quote", json={
        **payload_for_sig,
        "buyer_did": buyer.did,
        "signature": sig,
    })
    assert r.status_code == 200


def test_invalid_buyer_signature_rejected(agent_and_client):
    _, tc = agent_and_client
    buyer = DIDIdentity()
    other_buyer = DIDIdentity()  # wrong key

    request_id = str(uuid.uuid4())
    payload_for_sig = {
        "request_id": request_id,
        "sensor_type": "temperature",
        "quantity": 1,
        "timestamp_utc": "2026-04-22T00:00:00Z",
    }
    canonical = json.dumps(payload_for_sig, sort_keys=True, separators=(",", ":")).encode()
    wrong_sig = other_buyer.sign(canonical)  # signed with the wrong key

    r = tc.post("/quote", json={
        **payload_for_sig,
        "buyer_did": buyer.did,  # claims to be buyer but sig is from other_buyer
        "signature": wrong_sig,
    })
    assert r.status_code == 400
    assert r.json()["error_code"] == ErrorCode.INVALID_REQUEST_FORMAT


# --- W3C WoT Thing Description ---

def test_td_endpoint_structure(agent_and_client):
    _, tc = agent_and_client
    r = tc.get("/td")
    assert r.status_code == 200
    td = r.json()
    assert td["id"].startswith("did:key:z6Mk")
    assert "properties" in td
    assert "actions" in td
    assert "quote" in td["actions"]
    assert "lightning" in td["securityDefinitions"]
    assert td["security"] == "lightning"
