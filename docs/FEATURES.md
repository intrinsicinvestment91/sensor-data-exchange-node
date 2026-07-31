# SDEN Protocol Features

> **Note**: These are **protocol features** defined in the SDEN specification, not product features. The protocol defines the capabilities that implementations must support, but specific implementations may vary in how they realize these features.

## Core Protocol Features

### 📡 Self-Hosted Live Sensor Ingestion and Processing

SDEN enables independently operated sensor nodes to:
- Collect sensor data from physical hardware
- Process and prepare data for publication
- Maintain full control over data collection and processing

**Specification Reference**: [Protocol Overview](spec/overview.md), [Node Identity](spec/node-identity.md)

### 🔒 Cryptographically Signed Datasets with Verifiable Provenance

All published sensor data in SDEN is:
- Cryptographically signed using the node's identity key
- Linked to the node's hardware-anchored identity
- Verifiable by any consumer without relying on intermediaries

**Specification Reference**: [Node Identity](spec/node-identity.md), [Verification Model](spec/verification-model.md)

### ⚖️ Lightning Network Micropayment Settlement

SDEN includes a settlement abstraction layer that supports:
- Bitcoin Lightning Network as the primary reference implementation
- Micropayments for data access
- Trust-minimized, instant settlement
- Compatibility with alternative payment backends

**Specification Reference**: [Settlement Layer](spec/settlement-layer.md)

### 🧪 Modular Node Types: Producer, Buyer, Relay

SDEN defines three primary node roles:

- **Producer Node**: Collects sensor data, signs it, and makes it available for purchase
- **Buyer Agent**: Discovers available data, requests quotes, pays for access, and verifies data
- **Relay Node** (Optional): Indexes producer metadata and responds to discovery queries without custodial responsibilities

**Specification Reference**: [Protocol Overview](spec/overview.md), [Reference Implementation Spec](ris/SDEN_RIS_v1.md)

### 🔄 Extensible API Interface

SDEN defines protocol-level APIs that implementations must support, while allowing flexibility in:
- API surface design
- Transport protocols
- Data formats (within protocol constraints)

**Specification Reference**: [Reference Implementation Spec (RIS)](ris/SDEN_RIS_v1.md)

## Protocol Design Features

### Hardware Anchoring

SDEN explicitly acknowledges that sensor data originates in the physical world and provides mechanisms to:
- Bind node identity to physical hardware
- Reason about physical constraints and environmental uncertainty
- Verify hardware authenticity

**Specification Reference**: [Node Identity](spec/node-identity.md), [Verification Model](spec/verification-model.md)

### Decentralized Operation

SDEN assumes no global coordinator, registry authority, or required cloud service:
- Nodes operate independently
- No single entity controls onboarding or data publication
- Trust-minimized through cryptographic verification

**Specification Reference**: [Protocol Overview](spec/overview.md), [Threat Model](spec/threat-model.md)

### Verification Before Trust

SDEN prioritizes verifiability over authority:
- Consumers can independently evaluate data provenance and integrity
- No reliance on centralized intermediaries for trust
- Explicit trust boundaries and minimal assumptions

**Specification Reference**: [Verification Model](spec/verification-model.md), [Threat Model](spec/threat-model.md)

## Implementation Status

**Protocol Features**: Defined and specified in `docs/spec/`

**Reference Implementation**: Implemented in [`sden/`](../sden/) (producer node) and [`sden-client/`](../sden-client/) (buyer SDK). Validation currently uses a mock wallet and mock sensor; no end-to-end run against a live wallet and physical sensor is evidenced. See [Reference Implementation Status](../reference-implementation/README.md) for the full breakdown.

## Related Documentation

- [Protocol Specifications](spec/) — Complete protocol definitions
- [Reference Implementation Spec](ris/) — Implementation requirements
- [Architecture](ARCHITECTURE.md) — System architecture overview
- [Use Cases](USE_CASES.md) — Example applications
