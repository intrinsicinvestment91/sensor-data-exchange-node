import base64
import json

import base58
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from pydantic import BaseModel, Field

_ED25519_PREFIX_LEN = 2  # 0xed01 multicodec prefix


def _verify_did_signature(did: str, data: bytes, signature_b64: str) -> bool:
    """Verify an Ed25519 signature using a did:key DID as the verifying key."""
    try:
        encoded = did.removeprefix("did:key:z")
        payload = base58.b58decode(encoded)
        pubkey_bytes = payload[_ED25519_PREFIX_LEN:]
        pub = Ed25519PublicKey.from_public_bytes(pubkey_bytes)
        sig = base64.b64decode(signature_b64)
        pub.verify(sig, data)
        return True
    except Exception:
        return False


class SensorReading(BaseModel):
    producer_did: str
    sensor_type: str
    timestamp_utc: str
    value: float
    units: str
    quality_score: float = Field(ge=0.0, le=1.0)
    signature: str

    def verify(self) -> bool:
        """Verify the producer's Ed25519 signature over this reading.

        The signed payload is the reading fields (excluding signature),
        canonically serialized as compact sorted JSON — matching exactly
        what the producer signs in sden/sensor_agent.py.
        """
        payload = {
            "producer_did": self.producer_did,
            "sensor_type": self.sensor_type,
            "timestamp_utc": self.timestamp_utc,
            "value": self.value,
            "units": self.units,
            "quality_score": self.quality_score,
        }
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        return _verify_did_signature(self.producer_did, canonical, self.signature)
