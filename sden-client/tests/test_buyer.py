import uuid
from unittest.mock import MagicMock, patch

import httpx
import pytest

from sden_client.buyer import SDENBuyer


def _mock_response(status_code: int, data: dict) -> MagicMock:
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.json.return_value = data
    if status_code >= 400:
        resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "error", request=MagicMock(), response=resp
        )
    else:
        resp.raise_for_status.return_value = None
    return resp


@pytest.fixture
def buyer(mock_wallet):
    b = SDENBuyer("http://test.producer", wallet=mock_wallet)
    yield b
    b.close()


def test_buy_full_cycle(buyer, valid_reading, mock_wallet):
    request_id = str(uuid.uuid4())
    quote_data = {
        "request_id": request_id,
        "price_sats": 150,
        "invoice": "lnbc150n1test",
        "checking_id": "test-checking-id",
        "invoice_expiry": 3600,
    }

    with patch.object(buyer._client, "post", side_effect=[
        _mock_response(200, quote_data),
        _mock_response(200, {"request_id": request_id, "paid": True}),
    ]), patch.object(buyer._client, "get", return_value=_mock_response(200, valid_reading.model_dump())):
        reading = buyer.buy(sensor_type="temperature")

    assert reading.sensor_type == "temperature"
    assert reading.value == valid_reading.value
    assert reading.verify() is True
    assert buyer.last_price_sats == 150
    mock_wallet.pay_invoice.assert_called_once_with("lnbc150n1test")


def test_buy_raises_on_invalid_signature(buyer, valid_reading, mock_wallet):
    request_id = str(uuid.uuid4())
    quote_data = {
        "request_id": request_id,
        "price_sats": 150,
        "invoice": "lnbc150n1test",
        "checking_id": "test-checking-id",
        "invoice_expiry": 3600,
    }
    tampered = valid_reading.model_copy(update={"value": 999.9})

    with patch.object(buyer._client, "post", side_effect=[
        _mock_response(200, quote_data),
        _mock_response(200, {"request_id": request_id, "paid": True}),
    ]), patch.object(buyer._client, "get", return_value=_mock_response(200, tampered.model_dump())):
        with pytest.raises(ValueError, match="signature verification failed"):
            buyer.buy(sensor_type="temperature")


def test_buy_raises_on_quote_http_error(buyer, mock_wallet):
    with patch.object(buyer._client, "post", return_value=_mock_response(400, {"error": "bad request"})):
        with pytest.raises(httpx.HTTPStatusError):
            buyer.buy(sensor_type="unknown")


def test_buy_raises_on_verify_payment_error(buyer, valid_reading, mock_wallet):
    request_id = str(uuid.uuid4())
    quote_data = {
        "request_id": request_id,
        "price_sats": 150,
        "invoice": "lnbc150n1test",
        "checking_id": "test-checking-id",
        "invoice_expiry": 3600,
    }

    with patch.object(buyer._client, "post", side_effect=[
        _mock_response(200, quote_data),
        _mock_response(402, {"error_code": 103, "message": "Payment not verified"}),
    ]):
        with pytest.raises(httpx.HTTPStatusError):
            buyer.buy(sensor_type="temperature")


def test_info_returns_producer_info(buyer):
    info_data = {"producer_did": "did:key:z6Mk...", "sensor_type": "temperature", "price_sats": 150}
    with patch.object(buyer._client, "get", return_value=_mock_response(200, info_data)):
        info = buyer.info()
    assert info["price_sats"] == 150
    assert info["sensor_type"] == "temperature"


def test_buyer_context_manager(mock_wallet):
    with SDENBuyer("http://test.producer", wallet=mock_wallet) as buyer:
        assert buyer._url == "http://test.producer"
    # close() should have been called — client should be closed
    assert buyer._client.is_closed
