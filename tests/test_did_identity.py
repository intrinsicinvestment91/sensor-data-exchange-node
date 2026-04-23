import json
import os

import pytest

from sden.did_identity import DIDIdentity, verify_did_signature


def test_did_format():
    identity = DIDIdentity()
    assert identity.did.startswith("did:key:z6Mk"), f"Got: {identity.did}"


def test_sign_verify_roundtrip():
    identity = DIDIdentity()
    data = b"hello sden"
    sig = identity.sign(data)
    assert identity.verify(data, sig)


def test_verify_rejects_tampered_data():
    identity = DIDIdentity()
    sig = identity.sign(b"original")
    assert not identity.verify(b"tampered", sig)


def test_sign_verify_json():
    identity = DIDIdentity()
    obj = {"value": 22.4, "units": "celsius"}
    sig = identity.sign_json(obj)
    assert identity.verify_json(obj, sig)
    assert not identity.verify_json({"value": 99.9, "units": "celsius"}, sig)


def test_verify_did_signature_standalone():
    identity = DIDIdentity()
    data = b"standalone verify"
    sig = identity.sign(data)
    assert verify_did_signature(identity.did, data, sig)
    assert not verify_did_signature(identity.did, b"wrong", sig)


def test_pem_export_import_roundtrip():
    identity = DIDIdentity()
    pem = identity.export_private_key_pem()
    restored = DIDIdentity.from_pem(pem)
    assert restored.did == identity.did
    sig = identity.sign(b"test")
    assert restored.verify(b"test", sig)


def test_different_keys_produce_different_dids():
    a = DIDIdentity()
    b = DIDIdentity()
    assert a.did != b.did


# --- load_or_generate ---

def test_load_or_generate_creates_pem_file(tmp_path):
    key_file = str(tmp_path / "identity.pem")
    identity = DIDIdentity.load_or_generate(key_file)
    assert os.path.exists(key_file)
    assert identity.did.startswith("did:key:z6Mk")


def test_load_or_generate_reuses_existing_key(tmp_path):
    key_file = str(tmp_path / "identity.pem")
    id1 = DIDIdentity.load_or_generate(key_file)
    id2 = DIDIdentity.load_or_generate(key_file)
    assert id1.did == id2.did


def test_load_or_generate_env_var_takes_priority(tmp_path, monkeypatch):
    # Generate a known identity and inject its PEM via env var
    known = DIDIdentity()
    monkeypatch.setenv("DID_PRIVATE_KEY_PEM", known.export_private_key_pem())

    # Even with a different file present, env var wins
    key_file = str(tmp_path / "identity.pem")
    loaded = DIDIdentity.load_or_generate(key_file)
    assert loaded.did == known.did
    assert not os.path.exists(key_file)  # no file written when using env var


def test_load_or_generate_env_var_does_not_write_file(tmp_path, monkeypatch):
    identity = DIDIdentity()
    monkeypatch.setenv("DID_PRIVATE_KEY_PEM", identity.export_private_key_pem())
    key_file = str(tmp_path / "should_not_exist.pem")
    DIDIdentity.load_or_generate(key_file)
    assert not os.path.exists(key_file)
