"""Shared fixtures for sden-client tests.

Generates real Ed25519 keys and valid signed readings without importing
the sden package — keeping sden-client truly standalone in tests.
"""

import base64
import json
from unittest.mock import MagicMock

import base58
import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from sden_client.models import SensorReading

_ED25519_PREFIX = bytes([0xED, 0x01])


@pytest.fixture
def test_key() -> Ed25519PrivateKey:
    return Ed25519PrivateKey.generate()


@pytest.fixture
def test_did(test_key: Ed25519PrivateKey) -> str:
    pub_bytes = test_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    return "did:key:z" + base58.b58encode(_ED25519_PREFIX + pub_bytes).decode()


def _sign(key: Ed25519PrivateKey, payload: dict) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return base64.b64encode(key.sign(canonical)).decode()


@pytest.fixture
def valid_reading(test_key: Ed25519PrivateKey, test_did: str) -> SensorReading:
    payload = {
        "producer_did": test_did,
        "sensor_type": "temperature",
        "timestamp_utc": "2026-04-22T00:00:00Z",
        "value": 22.4,
        "units": "celsius",
        "quality_score": 0.98,
    }
    return SensorReading(**payload, signature=_sign(test_key, payload))


@pytest.fixture
def mock_wallet() -> MagicMock:
    wallet = MagicMock()
    wallet.pay_invoice.return_value = None
    return wallet
