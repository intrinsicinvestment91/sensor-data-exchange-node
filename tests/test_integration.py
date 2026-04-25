"""End-to-end buy cycle tests using FastAPI TestClient with a mocked AgentWallet."""

import uuid
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from sden.models import ErrorCode
from sden.pricing import FlatPricingEngine
from sden.sensor_agent import SensorAgent, build_app
from sden.sensor_reader import MockSensorReader


@pytest.fixture()
def mock_wallet():
    wallet = MagicMock()
    wallet.create_invoice.return_value = {
        "bolt11": "lnbc150n1test",
        "checking_id": "test-checking-id-123",
    }
    wallet.check_invoice.return_value = True
    return wallet


@pytest.fixture()
def client(mock_wallet, tmp_path):
    reader = MockSensorReader("temperature", seed=1)
    pricing = FlatPricingEngine(price_sats=150)
    with (
        patch("sden.sensor_agent.AgentWallet", return_value=mock_wallet),
        patch.object(SensorAgent, "_announce_nostr"),  # skip Nostr in tests
    ):
        agent = SensorAgent(
            sensor_reader=reader,
            pricing_engine=pricing,
            audit_db_path=str(tmp_path / "test_audit.db"),
        )
    app = build_app(agent)
    return TestClient(app), agent


def test_health(client):
    tc, _ = client
    resp = tc.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_info(client):
    tc, agent = client
    resp = tc.get("/info")
    assert resp.status_code == 200
    data = resp.json()
    assert data["producer_did"].startswith("did:key:z6Mk")
    assert data["sensor_type"] == "temperature"
    assert data["price_sats"] == 150


def test_full_buy_cycle(client):
    tc, agent = client
    request_id = str(uuid.uuid4())

    # POST /quote
    quote_resp = tc.post("/quote", json={
        "request_id": request_id,
        "sensor_type": "temperature",
        "quantity": 1,
        "timestamp_utc": "2026-04-22T00:00:00Z",
        "signature": "dummysig",
    })
    assert quote_resp.status_code == 200, quote_resp.text
    quote = quote_resp.json()
    assert quote["price_sats"] == 150
    assert quote["invoice"] == "lnbc150n1test"
    checking_id = quote["checking_id"]

    # POST /verify_payment
    verify_resp = tc.post("/verify_payment", json={
        "request_id": request_id,
        "checking_id": checking_id,
    })
    assert verify_resp.status_code == 200, verify_resp.text
    assert verify_resp.json()["paid"] is True

    # GET /data
    data_resp = tc.get("/data")
    assert data_resp.status_code == 200, data_resp.text
    reading = data_resp.json()
    assert reading["sensor_type"] == "temperature"
    assert reading["units"] == "celsius"
    assert "signature" in reading
    assert reading["producer_did"].startswith("did:key:z6Mk")

    # Verify the signature is valid
    from sden.did_identity import verify_did_signature
    import json

    sig_payload = {k: reading[k] for k in reading if k != "signature"}
    canonical = json.dumps(sig_payload, sort_keys=True, separators=(",", ":")).encode()
    assert verify_did_signature(reading["producer_did"], canonical, reading["signature"])


def test_wrong_sensor_type_returns_101(client):
    tc, _ = client
    resp = tc.post("/quote", json={
        "request_id": str(uuid.uuid4()),
        "sensor_type": "humidity",
        "quantity": 1,
        "timestamp_utc": "2026-04-22T00:00:00Z",
        "signature": "sig",
    })
    assert resp.status_code == 400
    assert resp.json()["error_code"] == ErrorCode.SENSOR_TYPE_NOT_AVAILABLE


def test_data_without_payment_returns_409(client):
    tc, _ = client
    resp = tc.get("/data")
    assert resp.status_code == 409


def test_verify_payment_without_quote_returns_409(client):
    tc, _ = client
    resp = tc.post("/verify_payment", json={
        "request_id": str(uuid.uuid4()),
        "checking_id": "some-id",
    })
    assert resp.status_code == 409


def test_audit_log_entries_are_signed(client):
    tc, agent = client
    request_id = str(uuid.uuid4())

    tc.post("/quote", json={
        "request_id": request_id,
        "sensor_type": "temperature",
        "quantity": 1,
        "timestamp_utc": "2026-04-22T00:00:00Z",
        "signature": "sig",
    })

    entries = agent._audit.verify_all()
    assert len(entries) > 0
    for entry in entries:
        assert entry["valid"], f"Invalid signature on audit row id={entry['id']}"
