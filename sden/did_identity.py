import base64
import json
import logging
import os

import base58
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)

logger = logging.getLogger(__name__)

# Multicodec prefix for Ed25519 public key: 0xed01
_ED25519_MULTICODEC_PREFIX = bytes([0xED, 0x01])


class DIDIdentity:
    """Ed25519 identity with did:key encoding.

    The DID URI is: did:key:z + base58btc(0xed01 || pubkey_bytes)
    The 'z' prefix is the multibase indicator for base58btc.
    """

    def __init__(self, private_key: Ed25519PrivateKey | None = None) -> None:
        self._private_key = private_key or Ed25519PrivateKey.generate()
        self._public_key: Ed25519PublicKey = self._private_key.public_key()
        self._pubkey_bytes: bytes = self._public_key.public_bytes(
            Encoding.Raw, PublicFormat.Raw
        )
        self.did: str = self._encode_did(self._pubkey_bytes)

    @staticmethod
    def _encode_did(pubkey_bytes: bytes) -> str:
        payload = _ED25519_MULTICODEC_PREFIX + pubkey_bytes
        return "did:key:z" + base58.b58encode(payload).decode()

    def sign(self, data: bytes) -> str:
        """Sign data, return base64-encoded signature."""
        signature = self._private_key.sign(data)
        return base64.b64encode(signature).decode()

    def verify(self, data: bytes, signature_b64: str) -> bool:
        """Verify a base64-encoded signature against data."""
        try:
            sig = base64.b64decode(signature_b64)
            self._public_key.verify(sig, data)
            return True
        except Exception:
            return False

    def sign_json(self, obj: dict) -> str:
        """Canonically serialize a dict and sign it."""
        canonical = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
        return self.sign(canonical)

    def verify_json(self, obj: dict, signature_b64: str) -> bool:
        canonical = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
        return self.verify(canonical, signature_b64)

    def export_private_key_pem(self) -> str:
        return self._private_key.private_bytes(
            Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()
        ).decode()

    @classmethod
    def from_pem(cls, pem: str) -> "DIDIdentity":
        from cryptography.hazmat.primitives.serialization import load_pem_private_key

        key = load_pem_private_key(pem.encode(), password=None)
        assert isinstance(key, Ed25519PrivateKey)
        return cls(private_key=key)

    @classmethod
    def load_or_generate(cls, key_path: str = "identity.pem") -> "DIDIdentity":
        """Load identity from env var or file; generate and save if neither exists.

        Priority:
          1. DID_PRIVATE_KEY_PEM env var (best for containers / secrets managers)
          2. PEM file at key_path (default: identity.pem)
          3. Generate new key and persist to key_path
        """
        pem_env = os.environ.get("DID_PRIVATE_KEY_PEM")
        if pem_env:
            identity = cls.from_pem(pem_env)
            logger.info("Loaded Ed25519 identity from DID_PRIVATE_KEY_PEM: %s", identity.did)
            return identity

        if os.path.exists(key_path):
            with open(key_path) as f:
                identity = cls.from_pem(f.read())
            logger.info("Loaded Ed25519 identity from %s: %s", key_path, identity.did)
            return identity

        identity = cls()
        os.makedirs(os.path.dirname(os.path.abspath(key_path)), exist_ok=True)
        with open(key_path, "w") as f:
            f.write(identity.export_private_key_pem())
        logger.info("Generated new Ed25519 identity: %s → saved to %s", identity.did, key_path)
        return identity


def verify_did_signature(did: str, data: bytes, signature_b64: str) -> bool:
    """Verify a signature given only the producer's DID (no private key needed)."""
    try:
        # Strip "did:key:z" prefix, base58-decode, strip multicodec prefix
        encoded = did.removeprefix("did:key:z")
        payload = base58.b58decode(encoded)
        pubkey_bytes = payload[len(_ED25519_MULTICODEC_PREFIX):]
        pub = Ed25519PublicKey.from_public_bytes(pubkey_bytes)
        sig = base64.b64decode(signature_b64)
        pub.verify(sig, data)
        return True
    except Exception:
        return False
