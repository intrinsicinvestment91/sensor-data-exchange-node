import json
import sqlite3
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sden.did_identity import DIDIdentity

_SCHEMA = """
CREATE TABLE IF NOT EXISTS audit_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp_utc TEXT NOT NULL,
    request_id  TEXT NOT NULL,
    event_type  TEXT NOT NULL,
    details     TEXT NOT NULL,
    error_code  INTEGER,
    signature   TEXT NOT NULL
);
-- request_ids table for replay-attack deduplication
CREATE TABLE IF NOT EXISTS seen_request_ids (
    request_id TEXT PRIMARY KEY,
    first_seen TEXT NOT NULL
);
-- Append-only guarantee is upheld by never calling UPDATE/DELETE in this module.
"""


class AuditDB:
    def __init__(self, db_path: str, identity: "DIDIdentity") -> None:
        self._identity = identity
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    def log(
        self,
        request_id: str,
        event_type: str,
        details: dict,
        error_code: int | None = None,
    ) -> None:
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        row_content = {
            "timestamp_utc": ts,
            "request_id": request_id,
            "event_type": event_type,
            "details": details,
            "error_code": error_code,
        }
        signature = self._identity.sign_json(row_content)
        self._conn.execute(
            """
            INSERT INTO audit_log
                (timestamp_utc, request_id, event_type, details, error_code, signature)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                ts,
                request_id,
                event_type,
                json.dumps(details, separators=(",", ":")),
                error_code,
                signature,
            ),
        )
        self._conn.commit()

    def is_seen_request_id(self, request_id: str) -> bool:
        row = self._conn.execute(
            "SELECT 1 FROM seen_request_ids WHERE request_id = ?", (request_id,)
        ).fetchone()
        return row is not None

    def mark_request_id_seen(self, request_id: str) -> None:
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        self._conn.execute(
            "INSERT OR IGNORE INTO seen_request_ids (request_id, first_seen) VALUES (?, ?)",
            (request_id, ts),
        )
        self._conn.commit()

    def verify_all(self) -> list[dict]:
        """Return list of rows with a 'valid' bool field indicating signature integrity."""
        results = []
        for row in self._conn.execute("SELECT * FROM audit_log ORDER BY id"):
            row_content = {
                "timestamp_utc": row["timestamp_utc"],
                "request_id": row["request_id"],
                "event_type": row["event_type"],
                "details": json.loads(row["details"]),
                "error_code": row["error_code"],
            }
            valid = self._identity.verify_json(row_content, row["signature"])
            results.append({**dict(row), "valid": valid})
        return results

    def close(self) -> None:
        self._conn.close()
