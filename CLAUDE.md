# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

SDEN (Sensor Data Exchange Node) is a protocol and reference implementation for IoT devices that sell signed sensor data via Bitcoin Lightning micropayments. A SDEN producer node collects sensor readings, signs them with an Ed25519 DID, issues Lightning invoices, and delivers verified data after payment.

The protocol spec is frozen at RIS v1.0. See `docs/ris/SDEN_RIS_v1.md` for the authoritative implementation reference.  
The overhaul plan is in `docs/PLAN.md` — consult it before starting any implementation work.

## Current Status

**Phase 3 (developer experience) complete. Phase 4 (positioning and community) is next.**

Core producer modules exist under `sden/`. Buyer SDK exists under `sden-client/`. Tests cover both (`pytest` runs `tests/` and `sden-client/tests/`). The plan in `docs/PLAN.md` defines the full phase-by-phase roadmap. The competitive positioning is: *"DePIN on Bitcoin. No new token. No new blockchain."*

## Development Setup

Requires **Python 3.12+**. The project vendors two files from BitAgent — `bitagent/agent_wallet.py` and `bitagent/lnbits_client.py` — into the `bitagent/` directory at the project root. See `THIRD_PARTY_NOTICES.md` for their provenance and licence. No separate BitAgent checkout is needed for development; their runtime dependencies (`requests`, `python-dotenv`) are pulled in by `requirements.txt`.

Install SDEN's dev dependencies and create a `.env` in the project root:

```bash
cd sensor-data-exchange-node
pip install -r requirements-dev.txt

# .env (copy from .env.example):
LNBITS_URL=https://your-lnbits-instance.com
LNBITS_API_KEY=your-lnbits-api-key
SENSOR_TYPE=temperature
PRICE_SATS=150
USE_MOCK_SENSOR=true    # no hardware needed for development
SDEN_HOST=0.0.0.0
SDEN_PORT=8080
AUDIT_DB_PATH=audit.db
INVOICE_EXPIRY_SECS=3600
```

```bash
# Run producer node
docker-compose up
# or directly:
python -m sden.main

# Lint / type-check / test (CI mirrors these exactly)
make test           # runs ruff + mypy + pytest (does NOT run benchmark)
make benchmark      # runs tests/test_benchmark.py only — asserts RIS timing targets

ruff check sden/ tests/ sden-client/sden_client/ sden-client/tests/  # linter only
mypy sden/ --ignore-missing-imports                                   # type-check sden/ only (sden-client/ not covered)
pytest                                                                # full test suite (both sden/ and sden-client/)
pytest tests/test_integration.py::test_full_buy_cycle -v             # single test
```

## Vendored BitAgent Files

SDEN's only runtime dependency on BitAgent is the Lightning wallet wrapper. Two files are vendored
into `bitagent/` and imported directly:

- `bitagent/agent_wallet.py` — `AgentWallet`, a thin wrapper that reads `LNBITS_URL` and
  `LNBITS_API_KEY` from the environment
- `bitagent/lnbits_client.py` — `LNbitsClient`, the raw LNbits REST client it wraps

They are derived from BitAgent's root-level layout and used under the MIT licence. Their executable
code bodies are unchanged; the only SDEN-side addition is a provenance and licence comment header.
Provenance and the full licence text are recorded in `THIRD_PARTY_NOTICES.md`. Nothing else from
BitAgent is used at runtime, and no BitAgent checkout is required.

If you want a local BitAgent checkout for exploration, set `BITAGENT_PATH` to it in your own
environment — `.mcp.json` expands that variable in the MCP server's `args`, and there is
deliberately no default, so an unset variable fails visibly instead of silently resolving to
someone else's machine path. Grant directory access through your own untracked
`.claude/settings.local.json`; machine-specific paths do not belong in tracked config.

## Protocol Flow (from RIS v1.0)

```
Producer boots → registers DID identity → announces on Nostr
       ↓
Buyer sends quote request (signed)
       ↓
Producer validates → issues Lightning invoice  [POST /quote]
       ↓
Buyer pays invoice
       ↓
Producer verifies payment                      [POST /verify_payment]
       ↓
Producer delivers signed sensor reading        [GET /data]
```

**State machine:** IDLE → REQUEST_RECEIVED → VALIDATED → PRICED → INVOICED → PAID → DELIVERED  
All failures are terminal. No retries. No partial payments.  
After DELIVERED or TERMINATED the state machine resets on the next `/quote` call (single-session model).

## API Surface

| Endpoint | Method | Purpose |
|---|---|---|
| `/quote` | POST | Request price and receive Lightning invoice |
| `/verify_payment` | POST | Confirm settlement before data delivery |
| `/data` | GET | Retrieve signed sensor reading |
| `/td` | GET | W3C WoT Thing Description |
| `/health` | GET | Liveness probe |
| `/info` | GET | Producer DID, sensor type, price |

### Quote Request / Response Schemas

```json
// POST /quote request
{
  "request_id": "uuid-v4",
  "sensor_type": "temperature",
  "quantity": 1,
  "timestamp_utc": "ISO8601",
  "buyer_did": "did:key:z6Mk...",  // optional — if present, signature is verified
  "signature": "base64"
}

// POST /quote response
{
  "request_id": "uuid-v4",
  "price_sats": 150,
  "invoice": "lnbc1...",
  "invoice_expiry": 3600,
  "checking_id": "lnbits-checking-id"   // pass this to /verify_payment
}
```

### Error Codes

| Code | Meaning |
|---|---|
| 100 | Invalid request format |
| 101 | Sensor type not available |
| 102 | Invoice not found |
| 103 | Payment not verified |
| 104 | Invoice expired |
| 105 | Data unavailable |

## Data Model (Canonical Sensor Record)

```json
{
  "producer_did": "did:key:z6Mk...",
  "sensor_type": "temperature",
  "timestamp_utc": "2026-04-22T00:00:00Z",
  "value": 22.4,
  "units": "celsius",
  "quality_score": 0.98,
  "signature": "<Ed25519 base64>"
}
```

## Architecture

```
sden/
  main.py              # uvicorn entry point — reads env, wires reader/pricing/agent/app
  sensor_agent.py      # SensorAgent (standalone class) + build_app() FastAPI factory
  did_identity.py      # Ed25519 key gen, did:key encoding, sign/verify
  audit_db.py          # SQLite append-only signed log + replay-attack deduplication
  state_machine.py     # State enum + advance()/require()/terminate() guard
  models.py            # Pydantic schemas (all RIS v1.0 request/response bodies)
  sensor_reader.py     # MockSensorReader + DHT22Reader; factory: make_reader(type, use_mock)
  pricing.py           # PricingEngine ABC + FlatPricingEngine (PRICE_SATS env var)
```

**`reference-implementation/`** holds specification-conformance notes only (README, no code). The working implementation is `sden/`.

**`SensorAgent` is standalone** — it does not extend BitAgent's `Agent` type. That type is an abstract base class intended for subclassing, but direct reuse across repositories is complicated by constructor side effects and package-relative import assumptions (see the integration notes below). `SensorAgent` owns its own `AuditDB`, `DIDIdentity`, `StateMachine`, and `AgentWallet` directly.

**MockSensorReader** supports: `temperature`, `humidity`, `pressure`, `co2`. Seeded with a fixed `seed` int for deterministic tests.

**`sden-client/`** (buyer SDK; packaged as `sden-client`, not yet published to PyPI — install from source with `pip install -e ./sden-client`):
```
sden-client/
  sden_client/
    buyer.py    # SDENBuyer.buy() — full quote→pay→verify→data cycle; .last_price_sats
    wallet.py   # SDENWallet — wraps LNbits for outbound payments (needs admin key)
    models.py   # SensorReading with .verify() (Ed25519 sig check against producer DID)
    cli.py      # `sden-buy` CLI: --url, --type, --output json|human, --verify-only <file>
  tests/        # pytest suite for the buyer SDK
```

`SDENWallet` requires a **LNbits admin key** (not the invoice/read key) to pay outgoing invoices. `SDENBuyer` accepts any object with a `.pay_invoice(bolt11)` method, so you can substitute a mock in tests.

## Integration Notes

### 1. Payment: inline wallet calls

`SensorAgent` calls the vendored `AgentWallet` directly rather than going through any decorator
or middleware layer. The wallet is constructed once and used inline in the request handlers:

```python
from agent_wallet import AgentWallet   # vendored under bitagent/, added to sys.path

wallet = AgentWallet()  # reads LNBITS_URL + LNBITS_API_KEY from env

# In /quote handler:
invoice = wallet.create_invoice(price_sats, memo=f"SDEN {sensor_type}")
return {"invoice": invoice["bolt11"], "checking_id": invoice["checking_id"]}

# In /verify_payment handler:
paid = wallet.check_invoice(checking_id)
if not paid:
    raise HTTPException(status_code=402, detail="Payment not verified")
```

### 2. DID identity: Ed25519, implemented in SDEN

RIS v1.0 requires `did:key:z6Mk...` — multibase base58btc of an **Ed25519** public key. SDEN
implements this itself in `sden/did_identity.py` rather than reusing any external identity helper:

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import base58
# DID URI: "did:key:z" + base58btc(0xed01 || pubkey_bytes)
```

### 3. Base class: `SensorAgent` does not inherit

BitAgent's `Agent` type is an abstract base class intended for subclassing. SDEN does not build on
it: cross-repository reuse is complicated by constructor side effects and package-relative import
assumptions, so `SensorAgent` is standalone and composes its own collaborators. Only the LNbits
wallet wrapper is reused, and it is vendored (see `THIRD_PARTY_NOTICES.md`).

### 4. Audit log: entries must be signed

`sden/audit_db.py` uses SQLite with a `signature TEXT NOT NULL` column. Every INSERT computes an
Ed25519 signature over the serialized row content. Append-only is enforced by never calling
UPDATE/DELETE (not via DB permissions). The `seen_request_ids` table provides replay-attack
deduplication.

### 5. Nostr discovery: implemented but best-effort

`SensorAgent._announce_nostr()` implements Kind 30078 producer announcement using `python-nostr`.
Failures are caught and logged as warnings — discovery is non-fatal, and no test covers the live
path.

### 6. Mock sensor mode is mandatory

Gate all sensor hardware access behind `USE_MOCK_SENSOR=true` env flag. `MockSensorReader` works without any hardware. This is required for CI, grant evaluators, and contributors without a physical DHT22.

## Testing Patterns

Integration tests patch `AgentWallet` and skip Nostr on construction:

```python
with (
    patch("sden.sensor_agent.AgentWallet", return_value=mock_wallet),
    patch.object(SensorAgent, "_announce_nostr"),
):
    agent = SensorAgent(reader, pricing, audit_db_path=str(tmp_path / "test.db"))
```

Use `tmp_path` (pytest fixture) for all `audit_db_path` values to avoid test pollution.

## Performance Targets (RIS v1.0)

| Operation | Target |
|---|---|
| Quote response | < 500 ms |
| Invoice generation | < 100 ms |
| Invoice verification | < 1 s |
| Data retrieval + signing | < 2 s |
| Total end-to-end | < 3.5 s |

Measured on minimum hardware (2-core ARMv8, 2 GB RAM). Assert these in CI with `make benchmark`.

## Competitive Differentiation

The strongest talking point vs. every competitor: **no new token, no new blockchain, runs on existing Bitcoin Lightning infrastructure**. When writing docs or READMEs, lead with this. See `docs/comparisons.md` for the detailed technical comparison and `docs/PLAN.md` for the roadmap.

## Validation Boundary

Validation currently uses a mock wallet and mock sensor; no end-to-end run against a live wallet
and physical sensor is evidenced. CI runs lint, type-check, the test suite, and the RIS timing
benchmark against mock backends only. Do not describe SDEN as production-ready, live-wallet
validated, or hardware validated.
