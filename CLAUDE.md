# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

SDEN (Sensor Data Exchange Node) is a protocol and reference implementation for IoT devices that sell signed sensor data via Bitcoin Lightning micropayments. A SDEN producer node collects sensor readings, signs them with an Ed25519 DID, issues Lightning invoices, and delivers verified data after payment.

The protocol spec is frozen at RIS v1.0. See `docs/ris/SDEN_RIS_v1.md` for the authoritative implementation reference.  
The overhaul plan is in `docs/PLAN.md` — consult it before starting any implementation work.

## Current Status

**Phase 2 (protocol hardening) complete. Phase 3 (developer experience) is next.**

All core modules exist under `sden/`. 32 tests pass (`pytest tests/`). The plan in `docs/PLAN.md` defines the full phase-by-phase roadmap. The competitive positioning is: *"DePIN on Bitcoin. No new token. No new blockchain."*

## Development Setup

Install BitAgent's dependencies first (SDEN depends on `bitagent/agent_wallet.py` at runtime):

```bash
cd /home/charlie/bitagent
pip install -r requirements.txt
```

Then install SDEN's own dev dependencies and create a `.env` in the project root:

```bash
cd /home/charlie/sensor-data-exchange-node
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
make test           # runs ruff + mypy + pytest
make benchmark      # assert RIS timing targets

ruff check sden/ tests/                                          # linter only
mypy sden/ --ignore-missing-imports                              # type-check only
pytest tests/                                                    # full test suite
pytest tests/test_integration.py::test_full_buy_cycle -v        # single test
```

## The Bigger Picture — BitAgent

**This project does not stand alone.** SDEN draws on BitAgent infrastructure. BitAgent (`/home/charlie/bitagent`) provides:
- Lightning payment infrastructure — `AgentWallet` (`bitagent/agent_wallet.py`) wraps `LNbitsClient` — **this is the only bitagent component SDEN uses at runtime**
- Base `Agent` class (`bitagent/src/core/agent.py`) — **do not extend; it cannot be instantiated** (see caveat below)
- DID identity management (`bitagent/src/identity/enhanced_did.py`) — RSA, not usable for SDEN
- Audit logging (`bitagent/src/monitoring/audit_logger.py`) — unsigned, not usable for SDEN
- A2A JSON-RPC pattern (see `src/agents/streamfinder/` as reference)

The `.claude/settings.json` in this repo grants Claude Code read access to `/home/charlie/bitagent` so both codebases are in scope.

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

**`SensorAgent` is standalone** — it does **not** extend `bitagent/src/core/agent.py:Agent`. The bitagent `Agent` base class cannot be instantiated (see caveat below). `SensorAgent` owns its own `AuditDB`, `DIDIdentity`, `StateMachine`, and `AgentWallet` directly.

**MockSensorReader** supports: `temperature`, `humidity`, `pressure`, `co2`. Seeded with a fixed `seed` int for deterministic tests.

**`sden-client/`** (buyer SDK, published to PyPI as `sden-client`) — to be created in Phase 3:
```
sden-client/
  sden_client/
    buyer.py    # SDENBuyer class
    models.py   # SensorReading with .verify()
    cli.py      # `sden-buy` CLI command
```

## BitAgent Integration — Critical Caveats

### 1. Payment: use inline logic, not `@require_payment`

The `@require_payment` decorator in `bitagent/src/core/payment.py` is **not connected to the real LNbits wallet**. All working BitAgent agents use inline logic:

```python
from bitagent.agent_wallet import AgentWallet

wallet = AgentWallet()  # reads LNBITS_URL + LNBITS_API_KEY from env

# In /quote handler:
invoice = wallet.create_invoice(price_sats, memo=f"SDEN {sensor_type}")
return {"invoice": invoice["bolt11"], "checking_id": invoice["checking_id"]}

# In /verify_payment handler:
paid = wallet.check_invoice(checking_id)
if not paid:
    raise HTTPException(status_code=402, detail="Payment not verified")
```

### 2. DID identity: Ed25519 from scratch — do not use `EnhancedDIDManager`

`bitagent/src/identity/enhanced_did.py` generates RSA-2048 — not Ed25519. RIS v1.0 requires `did:key:z6Mk...` (multibase base58btc of an Ed25519 public key). Implemented in `sden/did_identity.py`:

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import base58
# DID URI: "did:key:z" + base58btc(0xed01 || pubkey_bytes)
```

**`Agent` base class is broken — do not extend it.** `Agent.__init__` calls `SecureCommunicationManager.__init__`, which tries to construct `SecureMessage` as a utility object. `SecureMessage` is a dataclass requiring 6 positional args — this raises `TypeError` unconditionally.

### 3. Audit log: entries must be signed

`AuditLogger` (bitagent) logs JSON but does **not sign entries**. `sden/audit_db.py` uses SQLite with a `signature TEXT NOT NULL` column. Every INSERT computes an Ed25519 signature over the serialized row content. Append-only is enforced by never calling UPDATE/DELETE (not via DB permissions). The `seen_request_ids` table provides replay-attack deduplication.

### 4. Nostr discovery: implemented but best-effort

`bitagent/src/network/nostr.py` is empty. `SensorAgent._announce_nostr()` implements Kind 30078 producer announcement using `python-nostr`. Failures are caught and logged as warnings — discovery is non-fatal.

### 5. Mock sensor mode is mandatory

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

The strongest talking point vs. every competitor: **no new token, no new blockchain, runs on existing Bitcoin Lightning infrastructure**. When writing docs, READMEs, grant applications, or blog posts, lead with this. See `docs/PLAN.md` for the full competitor analysis and `docs/comparisons.md` (to be created in Phase 0) for detailed technical comparisons.

## BitAgent Live State

BitAgent is deployed at `https://bitagent-production.up.railway.app`. Full Lightning payment flow verified in production. Available agents: PriceOracleAgent (2 sats), WebFetchAgent (25 sats), SearchAgent (10 sats), PolyglotAgent (100 sats), StreamfinderAgent (100 sats — A2A JSON-RPC reference).

BitAgent ships `mcp_server.py` — a Claude MCP stdio server exposing agents as tools (configured via `.mcp.json` in this repo and in the bitagent root).
