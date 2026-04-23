"""Assert RIS v1.0 timing targets on minimum hardware."""

import time
import uuid
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from sden.pricing import FlatPricingEngine
from sden.sensor_agent import SensorAgent, build_app
from sden.sensor_reader import MockSensorReader


@pytest.fixture()
def timed_client(tmp_path):
    mock_wallet = MagicMock()
    mock_wallet.create_invoice.return_value = {
        "bolt11": "lnbc150n1bench",
        "checking_id": "bench-checking-id",
    }
    mock_wallet.check_invoice.return_value = True

    reader = MockSensorReader("temperature", seed=7)
    pricing = FlatPricingEngine(price_sats=150)
    with (
        patch("sden.sensor_agent.AgentWallet", return_value=mock_wallet),
        patch.object(SensorAgent, "_announce_nostr"),
    ):
        agent = SensorAgent(
            sensor_reader=reader,
            pricing_engine=pricing,
            audit_db_path=str(tmp_path / "bench.db"),
        )
    return TestClient(build_app(agent))


def test_quote_under_500ms(timed_client):
    request_id = str(uuid.uuid4())
    start = time.perf_counter()
    resp = timed_client.post("/quote", json={
        "request_id": request_id,
        "sensor_type": "temperature",
        "quantity": 1,
        "timestamp_utc": "2026-04-22T00:00:00Z",
        "signature": "sig",
    })
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert resp.status_code == 200
    assert elapsed_ms < 500, f"Quote took {elapsed_ms:.1f}ms (limit 500ms)"


def test_end_to_end_under_3500ms(timed_client):
    request_id = str(uuid.uuid4())
    start = time.perf_counter()

    r1 = timed_client.post("/quote", json={
        "request_id": request_id,
        "sensor_type": "temperature",
        "quantity": 1,
        "timestamp_utc": "2026-04-22T00:00:00Z",
        "signature": "sig",
    })
    checking_id = r1.json()["checking_id"]

    timed_client.post("/verify_payment", json={
        "request_id": request_id,
        "checking_id": checking_id,
    })
    timed_client.get("/data")

    elapsed_ms = (time.perf_counter() - start) * 1000
    assert elapsed_ms < 3500, f"End-to-end took {elapsed_ms:.1f}ms (limit 3500ms)"
