# SDEN Reference Implementation

## Where the implementation lives

This directory holds conformance notes only. It contains no code.

The working reference implementation is in the repository root:

| Location | Contents |
|---|---|
| [`sden/`](../sden/) | Producer node — FastAPI app, state machine, Ed25519 DID identity, signed audit log, pricing, sensor abstraction |
| [`sden-client/`](../sden-client/) | Buyer SDK and the `sden-buy` CLI |
| [`tests/`](../tests/), [`sden-client/tests/`](../sden-client/tests/) | Test suites for both sides |

See the [root README](../README.md) for setup and usage.

## What is implemented

The following are implemented and exercised by the test suite:

- **Node identity** — Ed25519 keypair generation, `did:key:z6Mk…` encoding, persistence across restarts via `DID_KEY_PATH` or an injected `DID_PRIVATE_KEY_PEM`
- **Cryptographic signing** — every sensor reading is signed with the producer's Node Identity Key and is verifiable by the buyer SDK
- **Data delivery** — signed readings served over the RIS v1.0 HTTP surface (`/quote`, `/verify_payment`, `/data`, `/td`, `/health`, `/info`)
- **Settlement abstraction** — Lightning invoices created and checked through an LNbits client behind a thin wallet wrapper
- **Request lifecycle** — the deterministic single-session state machine `IDLE → REQUEST_RECEIVED → VALIDATED → PRICED → INVOICED → PAID → DELIVERED`, with terminal failures and RIS error codes 100–105
- **Audit trail** — append-only SQLite log in which every row carries an Ed25519 signature, with replay deduplication by request id
- **W3C WoT 1.1** — a Thing Description endpoint at `/td`

## Validation status

**Validation currently uses a mock wallet and mock sensor; no end-to-end run against a live wallet and physical sensor is evidenced.**

- Continuous integration runs linting, type-checking, the full test suite, and the RIS timing benchmark on every change to `main`.
- Integration tests substitute a mock wallet and skip Nostr announcement, so no LNbits instance is required.
- `MockSensorReader` is the default sensor; `DHT22Reader` exists for real hardware but is not exercised by any automated test.
- Nostr producer announcement is best-effort and non-fatal; it is not covered by the test suite.

## Packaging and release status

- **`sden-client` is not published to PyPI.** Install it from source: `pip install -e ./sden-client`.
- The producer node ships as a `Dockerfile` and `docker-compose.yml` for local use. There is no published container image.

## Planned work

Remaining roadmap items — including PyPI publication, a TypeScript SDK, an interactive demo, and a documentation site — are tracked in [`docs/PLAN.md`](../docs/PLAN.md). Nothing in that list should be read as currently available.

## What this implementation does NOT define

- **Protocol behavior** — the specification is authoritative, not the implementation
- **Deployment models** — how nodes are deployed or operated in practice
- **Economic models** — pricing strategies, fee structures, or incentive mechanisms
- **Hardware requirements** — specific hardware components or configurations
- **Network topology** — how nodes discover or connect to each other
- **User interfaces** — how operators or consumers interact with the system

## Non-authoritative status

**This reference implementation is non-authoritative.**

- [`docs/spec/`](../docs/spec/) is the authoritative definition of the SDEN **protocol**.
- [`docs/ris/SDEN_RIS_v1.md`](../docs/ris/SDEN_RIS_v1.md) is the frozen **implementation baseline** derived from it — the build contract this code is written against.
- Where the code and either document diverge, the documents are correct and the code must be fixed.

Reference implementations exist to **validate** the specification, not to define it. Alternative implementations are encouraged, provided they adhere to the protocol rules. This implementation may contain bugs, inefficiencies, or non-optimal design choices, and it does not represent the only valid way to implement SDEN.

Reference implementations, deployments, or network effects do not override the written specification.

## Contributing

Contributions to the reference implementation should:

- Focus on demonstrating protocol compliance
- Maintain minimalism and clarity over optimization
- Include tests that validate specification requirements
- Document any deviations or limitations clearly

See [CONTRIBUTING.md](../CONTRIBUTING.md) for setup, and [docs/CONTRIBUTING.md](../docs/CONTRIBUTING.md) for protocol change proposals.

---

**Remember:** The specification defines the protocol. This implementation demonstrates it.
