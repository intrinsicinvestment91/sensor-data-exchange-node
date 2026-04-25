import json
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from sden_client.cli import main


@pytest.fixture
def runner():
    return CliRunner()


# --- --verify-only ---

def test_verify_only_valid_reading(runner, valid_reading, tmp_path):
    reading_file = tmp_path / "reading.json"
    reading_file.write_text(json.dumps(valid_reading.model_dump()))

    result = runner.invoke(main, ["--url", "http://unused", "--verify-only", str(reading_file)])
    assert result.exit_code == 0
    assert "✓ signature verified" in result.output


def test_verify_only_invalid_reading(runner, valid_reading, tmp_path):
    tampered = valid_reading.model_copy(update={"value": 999.9})
    reading_file = tmp_path / "reading.json"
    reading_file.write_text(json.dumps(tampered.model_dump()))

    result = runner.invoke(main, ["--url", "http://unused", "--verify-only", str(reading_file)])
    assert result.exit_code == 1
    assert "✗ signature INVALID" in result.output


def test_verify_only_json_output(runner, valid_reading, tmp_path):
    reading_file = tmp_path / "reading.json"
    reading_file.write_text(json.dumps(valid_reading.model_dump()))

    result = runner.invoke(
        main, ["--url", "http://unused", "--verify-only", str(reading_file), "--output", "json"]
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["valid"] is True
    assert "reading" in data
    assert data["reading"]["sensor_type"] == "temperature"


# --- normal buy flow ---

def test_buy_missing_lnbits_credentials(runner, monkeypatch):
    monkeypatch.delenv("LNBITS_URL", raising=False)
    monkeypatch.delenv("LNBITS_API_KEY", raising=False)
    result = runner.invoke(main, ["--url", "http://localhost:8080"])
    assert result.exit_code != 0
    assert "LNBITS_URL" in result.output


def test_buy_human_output(runner, valid_reading):
    with patch("sden_client.cli.SDENWallet"), \
         patch("sden_client.cli.SDENBuyer") as mock_buyer_cls:
        mock_buyer = MagicMock()
        mock_buyer.__enter__ = MagicMock(return_value=mock_buyer)
        mock_buyer.__exit__ = MagicMock(return_value=False)
        mock_buyer.buy.return_value = valid_reading
        mock_buyer.last_price_sats = 150
        mock_buyer_cls.return_value = mock_buyer

        result = runner.invoke(main, [
            "--url", "http://localhost:8080",
            "--type", "temperature",
            "--lnbits-url", "http://lnbits.test",
            "--lnbits-key", "test-key",
        ])

    assert result.exit_code == 0
    assert "150 sats" in result.output
    assert "22.4" in result.output
    assert "✓ signature verified" in result.output


def test_buy_json_output(runner, valid_reading):
    with patch("sden_client.cli.SDENWallet"), \
         patch("sden_client.cli.SDENBuyer") as mock_buyer_cls:
        mock_buyer = MagicMock()
        mock_buyer.__enter__ = MagicMock(return_value=mock_buyer)
        mock_buyer.__exit__ = MagicMock(return_value=False)
        mock_buyer.buy.return_value = valid_reading
        mock_buyer.last_price_sats = 150
        mock_buyer_cls.return_value = mock_buyer

        result = runner.invoke(main, [
            "--url", "http://localhost:8080",
            "--output", "json",
            "--lnbits-url", "http://lnbits.test",
            "--lnbits-key", "test-key",
        ])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["sensor_type"] == "temperature"
    assert data["value"] == 22.4


def test_buy_error_exits_nonzero(runner):
    with patch("sden_client.cli.SDENWallet"), \
         patch("sden_client.cli.SDENBuyer") as mock_buyer_cls:
        mock_buyer = MagicMock()
        mock_buyer.__enter__ = MagicMock(return_value=mock_buyer)
        mock_buyer.__exit__ = MagicMock(return_value=False)
        mock_buyer.buy.side_effect = ValueError("signature verification failed")
        mock_buyer_cls.return_value = mock_buyer

        result = runner.invoke(main, [
            "--url", "http://localhost:8080",
            "--lnbits-url", "http://lnbits.test",
            "--lnbits-key", "test-key",
        ])

    assert result.exit_code == 1
    assert "Error" in result.output
