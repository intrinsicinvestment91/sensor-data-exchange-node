import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

import httpx

from sden_client.models import SensorReading

if TYPE_CHECKING:
    from sden_client.wallet import SDENWallet


class SDENBuyer:
    """Orchestrates the full SDEN buy cycle against a producer node.

    After each successful buy(), last_price_sats holds the price paid.
    """

    def __init__(self, producer_url: str, wallet: "SDENWallet") -> None:
        self._url = producer_url.rstrip("/")
        self._wallet = wallet
        self._client = httpx.Client(timeout=30.0)
        self.last_price_sats: int | None = None

    def buy(self, sensor_type: str = "temperature", quantity: int = 1) -> SensorReading:
        """Execute a full buy cycle: quote → pay → verify → data.

        Returns a SensorReading whose .verify() has already passed.
        Raises ValueError if the producer's signature is invalid.
        Raises httpx.HTTPStatusError on any HTTP failure.
        """
        request_id = str(uuid.uuid4())
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        # 1. POST /quote
        quote_resp = self._client.post(
            f"{self._url}/quote",
            json={
                "request_id": request_id,
                "sensor_type": sensor_type,
                "quantity": quantity,
                "timestamp_utc": ts,
                "signature": "open",  # no buyer_did → producer skips sig check
            },
        )
        quote_resp.raise_for_status()
        quote = quote_resp.json()
        self.last_price_sats = quote["price_sats"]

        # 2. Pay invoice
        self._wallet.pay_invoice(quote["invoice"])

        # 3. POST /verify_payment
        verify_resp = self._client.post(
            f"{self._url}/verify_payment",
            json={"request_id": request_id, "checking_id": quote["checking_id"]},
        )
        verify_resp.raise_for_status()

        # 4. GET /data
        data_resp = self._client.get(f"{self._url}/data")
        data_resp.raise_for_status()

        reading = SensorReading(**data_resp.json())
        if not reading.verify():
            raise ValueError(
                f"Ed25519 signature verification failed for producer {reading.producer_did!r}. "
                "The reading may have been tampered with."
            )
        return reading

    def info(self) -> dict:
        """GET /info — producer DID, sensor type, and price."""
        resp = self._client.get(f"{self._url}/info")
        resp.raise_for_status()
        return resp.json()

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "SDENBuyer":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
