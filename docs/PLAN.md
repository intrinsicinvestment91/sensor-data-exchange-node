# SDEN Overhaul Plan
## Achieving a Popular, Well-Starred Protocol Repository

**Created:** 2026-04-22  
**Research basis:** DePIN sector analysis, competitor audit (Ocean Protocol, Streamr, DIMO, peaq, IOTA Marketplace), GitHub growth patterns, grant landscape (OpenSats, HRF), W3C WoT standards, Lightning + IoT academic literature  
**Spec version:** RIS v1.0 (frozen)

> **Historical planning document.** Some milestones, implementation assumptions, and positioning
> in this plan have been superseded. See the [root README](../README.md) and the
> [reference implementation README](../reference-implementation/README.md) for the current
> implementation and validation status.

---

## Vision

SDEN becomes the canonical answer to "how do I sell sensor data on Bitcoin Lightning." It is the only DePIN-adjacent protocol that is:
- **Bitcoin-native** — no new token, no new blockchain, no gas fees
- **Non-custodial** — producer and buyer each control their own Lightning wallet
- **Resource-constrained friendly** — runs on a Raspberry Pi Zero (2-core ARMv8, 2 GB RAM)
- **Cryptographically verifiable** — every reading is Ed25519-signed and auditable
- **Standards-aligned** — W3C WoT Thing Description compatible

**12-month success markers:**
- 500–1000 GitHub stars
- Referenced in at least one academic paper (cite IEEE Lightning+IoT papers to seed the citation chain)
- At least one real deployed producer run by a community member
- One active grant (OpenSats or HRF)
- A working buyer CLI (`sden-buy`) that is the top Google result for "buy sensor data lightning bitcoin"

---

## Competitive Context

| Competitor | Fatal weakness SDEN exploits |
|---|---|
| Ocean Protocol | Token-gated (`OCEAN`), cold-start problem, no real-time streaming, EVM gas fees |
| Streamr | Requires `DATA` token economy, EVM-based, node operator churn, overkill for single sensor |
| DIMO | Vehicle-only, proprietary hardware dongle, `$DIMO` token |
| peaq | Polkadot L1 smart contracts, gas fees, not Bitcoin-native |
| IOTA Marketplace | Not battle-tested, no Lightning, no Bitcoin alignment |

**SDEN's positioning tagline:** *"DePIN on Bitcoin. No new token. No new blockchain."*

---

## Phase 0 — Repository Presence
**Timeline:** Week 1  
**Goal:** A stranger landing on the repo understands the value in 30 seconds without reading a line of code.

### Tasks

- [ ] **README overhaul**
  - First 3 lines: hook sentence, mechanism sentence, differentiation sentence
  - Mermaid architecture diagram (renders natively on GitHub — no image hosting needed)
  - "What makes SDEN different" comparison table vs Ocean/Streamr/peaq
  - Terminal GIF showing a buyer purchasing sensor data (`asciinema` → `svg-term`)
  - Badges: CI status, license (MIT), spec version, "Built on Bitcoin"
  - Links: RIS spec, quickstart, buyer SDK, grant/sponsor section

- [ ] **Repo metadata**
  - GitHub Topics: `depin`, `bitcoin`, `lightning-network`, `iot`, `micropayments`, `did`, `nostr`, `sensor`, `raspberry-pi`, `python`
  - Description: "Buy and sell verifiable sensor data with Bitcoin Lightning — no token, no platform, no middleman"
  - Website field: point to GitHub Pages or a deployed demo

- [ ] **Supporting repository docs**
  - `CONTRIBUTING.md` — clear path for first-time contributors; label issues "good first issue"
  - `.github/ISSUE_TEMPLATE/bug_report.md`
  - `.github/ISSUE_TEMPLATE/feature_request.md`
  - `.github/ISSUE_TEMPLATE/protocol_question.md`
  - `docs/why-sden.md` — prose argument for Bitcoin-native IoT data markets vs token alternatives
  - `docs/comparisons.md` — technical comparison with Ocean, Streamr, DIMO

- [ ] **GitHub Actions CI skeleton**
  - Workflow: lint (ruff), type-check (mypy), test (pytest) on push
  - Badge in README

---

## Phase 1 — Core Reference Implementation
**Timeline:** Weeks 2–6  
**Goal:** `docker-compose up` delivers a running, spec-compliant producer node in under 5 minutes.

### Architecture

```
sden/
  __init__.py
  main.py              # uvicorn entry point; reads env vars
  sensor_agent.py      # SensorAgent(Agent) — FastAPI app, state machine, endpoints
  sensor_reader.py     # Hardware abstraction: DHT22 driver + MockSensorReader
  did_identity.py      # Ed25519 did:key creation + data signing (replaces RSA EnhancedDIDManager)
  audit_db.py          # SQLite append-only log; every row has an Ed25519 signature field
  pricing.py           # Pluggable pricing engine: flat, time-of-day, quality-weighted
  state_machine.py     # IDLE→DELIVERED enum + transition guard
  models.py            # Pydantic request/response schemas matching RIS v1.0
```

### Critical Implementation Decisions

- **Ed25519 DID (not RSA):** SDEN uses its own DID implementation rather than reusing BitAgent's, because the projects have different integration and packaging boundaries and RIS v1.0 requires Ed25519 specifically. Implement `did:key:z6Mk...` encoding in `did_identity.py` using:
  - `cryptography.hazmat.primitives.asymmetric.ed25519.Ed25519PrivateKey`
  - Multibase base58btc encoding of the public key bytes for the DID URI
  - Sign each sensor reading with the producer's Ed25519 private key

- **Payment pattern (inline, not decorator):** The `@require_payment` decorator in BitAgent's `src/core/payment.py` is not wired to the real LNbits wallet. Use inline `AgentWallet` calls:
  ```python
  wallet = AgentWallet()  # LNBITS_URL + LNBITS_API_KEY from env
  invoice = wallet.create_invoice(price_sats, memo=f"SDEN {sensor_type} reading")
  paid = wallet.check_invoice(checking_id)
  ```

- **Signed audit log:** SQLite schema must include a `signature` column. Every INSERT must be signed with the producer's Ed25519 key. No UPDATE or DELETE ever — append-only enforced at the DB layer.

- **Nostr announcement on boot:** `bitagent/src/network/nostr.py` is currently empty. Implement Kind 30078 producer announcement using `python-nostr` (already in BitAgent's `requirements.txt`).

### Tasks

- [ ] `did_identity.py` — Ed25519 key generation, `did:key:z6Mk...` encoding, sign/verify
- [ ] `audit_db.py` — SQLite schema, signed append-only INSERT, read/verify methods
- [ ] `state_machine.py` — state enum, transition guard, terminal state handling
- [ ] `models.py` — Pydantic schemas for all RIS v1.0 request/response bodies and error codes
- [ ] `sensor_reader.py` — `MockSensorReader` (deterministic fake data) + `DHT22Reader` stub
- [ ] `pricing.py` — flat pricing engine (v1.0); pluggable interface for future strategies
- [ ] `sensor_agent.py` — `SensorAgent(Agent)` class with:
  - `POST /quote` — validate request signature, create invoice, advance state
  - `POST /verify_payment` — check LNbits, advance to PAID
  - `GET /data` — return signed sensor reading, advance to DELIVERED
  - `GET /health` — liveness probe
  - `GET /info` — producer DID, sensor type, price
  - State machine enforcement on every transition
- [ ] `main.py` — uvicorn entry point, env-driven config
- [ ] `requirements.txt` — pin versions; include cryptography, fastapi, uvicorn, python-nostr, python-dotenv
- [ ] `Dockerfile` — minimal Python 3.12 slim image
- [ ] `docker-compose.yml` — producer + mock sensor mode; `USE_MOCK_SENSOR=true`
- [ ] `.env.example` — `LNBITS_URL`, `LNBITS_API_KEY`, `SENSOR_TYPE`, `PRICE_SATS`, `USE_MOCK_SENSOR`
- [ ] End-to-end integration test: full buy cycle against LNbits testnet

### Mock Sensor Mode

**Non-negotiable for adoption.** Grant evaluators, reviewers, and contributors will not have a DHT22 wired up. `USE_MOCK_SENSOR=true` in the env produces realistic randomized readings with configurable drift. This is the only way to evaluate SDEN without hardware.

```bash
# Evaluator experience — no hardware required
git clone https://github.com/Intrinsicinvestment91/sensor-data-exchange-node
cp .env.example .env  # fill in LNbits creds
docker-compose up     # producer running on :8080
sden-buy --url http://localhost:8080 --type temperature
# → Paid 150 sats. Temperature: 22.4°C (quality: 0.98) [signature verified ✓]
```

---

## Phase 2 — Protocol Hardening
**Timeline:** Weeks 7–10  
**Goal:** Spec-compliant, security-auditable, and interoperable with existing IoT standards.

### RIS v1.0 Compliance Checklist

- [ ] All 6 error codes (100–105) implemented, tested, and documented
- [ ] State machine: no out-of-order transitions possible (guard at every endpoint)
- [ ] Invoice expiry enforced — `TERMINATED` state when timeout exceeded
- [ ] Request IDs are UUID v4, validated on receipt, stored in audit log
- [ ] All buyer quote requests require Ed25519 signature over the request body
- [ ] Signature verification rejects replayed requests (timestamp + nonce check)
- [ ] Performance benchmarks pass on minimum hardware (automated in CI)

### W3C WoT Thing Description Endpoint

Add `GET /td` returning a W3C Web of Things Thing Description (WoT 1.1). This makes SDEN interoperable with Azure IoT Operations, Mozilla WebThings, and any WoT broker — no competitor in the Lightning space has done this. It is a major differentiator for enterprise evaluators and grant reviewers.

```json
// GET /td
{
  "@context": ["https://www.w3.org/2019/wot/td/v1"],
  "id": "did:key:z6Mk...",
  "title": "SDEN Temperature Producer",
  "securityDefinitions": { "lightning": { "scheme": "apikey", "in": "header" } },
  "security": "lightning",
  "properties": {
    "temperature": {
      "type": "number",
      "unit": "celsius",
      "readOnly": true,
      "forms": [{ "href": "/data", "op": "readproperty", "htv:methodName": "GET" }]
    }
  },
  "actions": {
    "quote": { "forms": [{ "href": "/quote", "htv:methodName": "POST" }] }
  }
}
```

- [ ] `GET /td` endpoint — WoT Thing Description with Lightning payment metadata
- [ ] `docs/wot-integration.md` — how SDEN maps to WoT concepts

### Test Suite

- [ ] Unit tests: Ed25519 sign/verify, DID encoding, state machine transitions, all error codes
- [ ] Integration tests: full buy cycle against real LNbits (testnet or regtest)
- [ ] Security tests:
  - Replay attack rejection (reused request_id)
  - Expired invoice rejection (TERMINATED state)
  - Invalid signature rejection (tampered request body)
  - Payment bypass attempt (call `/data` without going through `/verify_payment`)
- [ ] Performance tests: assert each operation against RIS timing targets
- [ ] `Makefile` with `make test`, `make lint`, `make benchmark`

### BOLT12 Offers (forward-looking hook)

Add `GET /offer` returning a BOLT12 offer for recurring data purchases. This enables subscription-style access without per-request invoice roundtrips. Annotate as `# v1.1 feature` but implement now so the architecture supports it.

---

## Phase 3 — Developer Experience
**Timeline:** Weeks 11–14  
**Goal:** A developer integrates SDEN into their project in an afternoon with no prior Lightning knowledge.

### Python Buyer SDK (`sden-client`)

Publish to PyPI as `sden-client`. Minimal, no dependencies beyond `httpx` and `cryptography`.

```python
from sden_client import SDENBuyer, SDENWallet

wallet = SDENWallet(lnbits_url=..., api_key=...)
buyer = SDENBuyer("https://producer.example.com", wallet=wallet)

reading = buyer.buy(sensor_type="temperature")
assert reading.verify()   # checks Ed25519 signature against producer's DID
print(f"{reading.value}{reading.units}")  # 22.4°C
```

- [ ] `sden-client/` package — `SDENBuyer`, `SDENWallet`, `SensorReading` with `.verify()`
- [ ] `sden-client/tests/` — full test suite including signature verification
- [ ] Publish to PyPI (`sden-client`)
- [ ] `examples/buy_temperature.py` — 15-line complete example

### CLI Tool (`sden-buy`)

Installed with `pip install sden-client`. The single most viral artifact for social sharing.

```bash
sden-buy --url https://producer.example.com \
         --type temperature \
         --wallet $LNBITS_API_KEY
# → Paid 150 sats. Temperature: 22.4°C (quality: 0.98) [✓ signature verified]
```

- [ ] `sden-buy` CLI using Click or Typer
- [ ] `--verify-only` flag (verify a previously fetched reading without paying)
- [ ] `--output json` flag for pipeline use
- [ ] Tab completion

### TypeScript/Node SDK (`sden-client-js`)

Secondary priority. Model after DIMO's TypeScript-first data SDK. Publish to npm as `sden-client`.

- [ ] `sden-client-js/` package — `SDENBuyer`, `SensorReading` with `.verify()`
- [ ] Publish to npm

### Interactive Demo

- [ ] Replit template — one-click environment with mock producer + buyer pre-configured
- [ ] OR GitHub Codespaces devcontainer — same result
- [ ] Bruno/Postman collection for all three API endpoints — enables zero-code exploration

### Documentation Site

- [ ] `docs/` → GitHub Pages via `mkdocs` or `mdBook`
- [ ] Pages: Getting Started, Protocol Spec, API Reference, Buyer SDK, Running on Hardware, Security Model
- [ ] Auto-generated API docs from Pydantic models (FastAPI `/docs` is a start; export OpenAPI spec)

---

## Phase 4 — Positioning and Community
**Timeline:** Weeks 15–20  
**Goal:** SDEN is findable, shareable, and has an active contributor loop.

### Grant Applications

**OpenSats** (apply as soon as Phase 1 is working):
- Category: Bitcoin/Lightning infrastructure
- Frame: open-source reference implementation for Lightning-native IoT data markets
- Deliverables: working reference node, buyer SDK, published spec, CI/CD, docs

**HRF Bitcoin Development Fund** (quarterly cycle):
- Frame: censorship-resistant data economy — sensors in restricted environments selling data without government-controlled intermediaries
- Deliverables: same as above + Nostr discovery layer (decentralized, censorship-resistant)

**EU NGI Zero / Horizon** (longer cycle):
- Frame: W3C WoT standards-compliant open protocol for IoT interoperability
- W3C Thing Description endpoint makes this a legitimate standards-track submission

- [ ] OpenSats application drafted and submitted
- [ ] HRF application drafted and submitted
- [ ] `FUNDING.yml` in `.github/` (GitHub Sponsors / OpenSats link)

### Publishing Sequence

**Order matters.** Publish in this sequence — not before:

1. **Technical blog post** (publish when Phase 1 is working):  
   Title: *"Why we built a sensor data marketplace on Bitcoin Lightning instead of a new blockchain"*  
   Publish on: GitHub Pages, cross-post to Stacker News, Primal (Nostr), Bitcoin Magazine dev track, HackerNoon  
   
2. **Hacker News "Show HN"** (publish when Docker quickstart works):  
   Title: *"Show HN: SDEN – buy and sell verifiable sensor data with Bitcoin Lightning"*  
   Timing: Tuesday–Thursday, 9am ET. Do not post until the Docker demo works flawlessly.

3. **Nostr announcement** (dogfoods the discovery layer):  
   Post from the project's Nostr npub. Link to the repo and the demo.

4. **Conference talks** (submit CFPs now for 2026 cycle):
   - TABConf (Atlanta) — Bitcoin + Lightning developer conference
   - Bitcoin++ (Austin or Berlin) — developer-focused, protocol talks welcome
   - Lightning Conference — direct audience
   - IoT Tech Expo (London/Amsterdam) — enterprise IoT audience, unique positioning

- [ ] Blog post drafted
- [ ] HN post draft ready (submit only after Docker demo works)
- [ ] Project Nostr npub created
- [ ] CFPs submitted to TABConf, Bitcoin++

### Community Infrastructure

- [ ] GitHub Discussions enabled (not Discord — keeps everything indexed and searchable)
- [ ] "Sensor Registry" concept: a public Nostr-based list of known SDEN producers (like a relay list for producers)
- [ ] "good first issue" label applied to 5+ issues before any promotion
- [ ] Response SLA: answer all issues within 48 hours during the first 3 months (this is the single biggest star-retention factor)

### Academic Positioning

- [ ] Add references to IEEE Lightning+IoT papers in README and docs:
  - "Enabling Micro-payments on IoT Devices using Bitcoin Lightning Network" (IEEE 2021)
  - "LNGate: Secure Bidirectional IoT Micro-Payments Using Bitcoin's Lightning Network" (IEEE 2023)
- [ ] "Cite this protocol" section in README (BibTeX format)
- [ ] Submit to arXiv as a technical report once the spec + implementation are complete

---

## Phase 5 — Protocol Extensions
**Timeline:** Month 6+  
**Goal:** Keep the roadmap credible without over-promising for v1.0.

### v1.1 — Relay Node + Batch Requests

- Relay node implementation (indexes producer metadata, responds to discovery queries)
- Batch request: multiple readings per invoice
- Concurrent request handling

### v1.2 — Streaming Mode

- WebSocket subscription model for continuous data feed
- Buyer pays a streaming invoice (keysend or AMP) for a time-bounded feed
- Aligns with BitAgent Phase 3 (WebSocket + MQTT support)

### v2.0 — TEE Attestation

Integrate Trusted Execution Environment attestation for high-stakes sensor data (supply chain, environmental compliance, regulatory reporting). The producer node runs inside an ARM TrustZone or RISC-V enclave; buyers receive a cryptographic proof that the firmware is unmodified alongside the sensor reading.

This is cutting-edge (active 2025 research, RISC-V TEE survey published 2024, AP-TEE standardization ongoing). It would be the first Lightning-native implementation of hardware-attested sensor data — a significant academic and enterprise credibility signal.

### v2.1 — ZK Data Quality Proofs

Allow a producer to prove a sensor reading falls within a claimed range (e.g., "temperature is above freezing") without revealing the exact value. Uses zk-SNARKs or Bulletproofs. Relevant for privacy-sensitive deployments.

---

## Implementation Reference — BitAgent Integration Points

| SDEN requirement | BitAgent component | File | Caveat |
|---|---|---|---|
| Lightning invoices | `AgentWallet` | `bitagent/agent_wallet.py` | Call inline; SDEN implements its payment boundary locally rather than importing BitAgent's `@require_payment` decorator, which is coupled to BitAgent's own runtime assumptions |
| Base agent class | `Agent` | `bitagent/src/core/agent.py` | Extend this; it wires monitoring and audit |
| DID creation | — | custom `did_identity.py` | Implemented in SDEN; RIS v1.0 requires Ed25519 `did:key`, and BitAgent's identity module generates RSA keys |
| Audit logging | `AuditLogger` | `bitagent/src/monitoring/audit_logger.py` | Extend to add Ed25519 signature per entry |
| Nostr announcement | — | implement in `sensor_agent.py` | `bitagent/src/network/nostr.py` is empty |
| Performance tracking | `AgentPerformanceTracker` | `bitagent/src/monitoring/performance_monitor.py` | Use directly; assert against RIS targets |

---

## Success Metrics by Phase

| Phase | Metric | Target |
|---|---|---|
| 0 | README quality | All critical sections present; diagram renders; no broken links |
| 1 | End-to-end test | Full buy cycle passing in CI against LNbits testnet |
| 2 | RIS compliance | All checklist items green; security tests pass |
| 3 | Developer onboarding | New contributor can run mock demo in < 5 minutes |
| 4 | Community | ≥ 5 external contributors; OpenSats application submitted |
| 4 | Stars | 200+ stars within 30 days of HN post |
| 12 months | Stars | 500–1000 stars |
| 12 months | Deployments | ≥ 1 real sensor running in production by a community member |

---

## Files to Create (ordered by impact)

```
README.md                          # complete overhaul — highest priority
docs/why-sden.md                   # prose argument for Bitcoin-native IoT
docs/comparisons.md                # technical vs Ocean/Streamr/DIMO/peaq
docs/wot-integration.md            # W3C WoT compatibility guide
sden/__init__.py
sden/main.py
sden/sensor_agent.py
sden/did_identity.py               # Ed25519 — do not reuse EnhancedDIDManager
sden/audit_db.py
sden/state_machine.py
sden/models.py
sden/sensor_reader.py
sden/pricing.py
sden-client/                       # buyer SDK (PyPI)
  sden_client/__init__.py
  sden_client/buyer.py
  sden_client/models.py
  sden_client/cli.py               # sden-buy command
requirements.txt
requirements-dev.txt
Dockerfile
docker-compose.yml
.env.example
Makefile
.github/workflows/ci.yml
.github/ISSUE_TEMPLATE/
CONTRIBUTING.md
FUNDING.yml
```
