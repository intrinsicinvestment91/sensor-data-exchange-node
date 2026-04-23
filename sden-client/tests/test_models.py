import base64
import json

import pytest

from sden_client.models import SensorReading


def test_verify_valid_signature(valid_reading):
    assert valid_reading.verify() is True


def test_verify_tampered_value(valid_reading):
    tampered = valid_reading.model_copy(update={"value": 99.9})
    assert tampered.verify() is False


def test_verify_tampered_units(valid_reading):
    tampered = valid_reading.model_copy(update={"units": "fahrenheit"})
    assert tampered.verify() is False


def test_verify_tampered_quality_score(valid_reading):
    tampered = valid_reading.model_copy(update={"quality_score": 1.0})
    assert tampered.verify() is False


def test_verify_wrong_did(valid_reading, test_did):
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
    import base58, base64

    other_key = Ed25519PrivateKey.generate()
    pub_bytes = other_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    other_did = "did:key:z" + base58.b58encode(bytes([0xED, 0x01]) + pub_bytes).decode()

    # same signature but different DID — verification should fail
    wrong = valid_reading.model_copy(update={"producer_did": other_did})
    assert wrong.verify() is False


def test_verify_bad_signature_b64(valid_reading):
    bad = valid_reading.model_copy(update={"signature": "not-valid-base64!!!"})
    assert bad.verify() is False


def test_verify_corrupted_signature(valid_reading):
    # Flip a byte in the middle of the signature
    sig_bytes = base64.b64decode(valid_reading.signature)
    corrupted = bytearray(sig_bytes)
    corrupted[32] ^= 0xFF
    bad = valid_reading.model_copy(update={"signature": base64.b64encode(bytes(corrupted)).decode()})
    assert bad.verify() is False


def test_reading_from_dict(valid_reading):
    data = valid_reading.model_dump()
    restored = SensorReading(**data)
    assert restored.verify() is True
    assert restored.value == valid_reading.value
