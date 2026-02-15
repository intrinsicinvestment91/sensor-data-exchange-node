# SDEN Architecture

This document provides a high-level overview of SDEN architecture. For detailed protocol specifications, see the [Protocol Specifications](spec/).

## Architecture Overview

SDEN is designed as a decentralized protocol for sensor data exchange. The architecture emphasizes:

- **Cryptographic identity** — Nodes establish verifiable identity through hardware-anchored keys
- **Direct exchange** — Data flows directly between producers and buyers without mandatory intermediaries
- **Settlement abstraction** — Payment mechanisms are abstracted, allowing multiple settlement backends
- **Verification-first** — Trust is established through cryptographic verification, not authority

## System Components

### Node Types

SDEN defines three primary node roles:

#### Producer Node
- Collects sensor data from physical hardware
- Signs data with node identity keys
- Advertises data availability
- Accepts payments and delivers data

**Specification**: [Protocol Overview](spec/overview.md), [RIS System Roles](ris/SDEN_RIS_v1.md#3-system-roles)

#### Buyer Agent
- Discovers available sensor data
- Requests quotes and negotiates access
- Pays for data access via settlement layer
- Verifies data authenticity and integrity

**Specification**: [Protocol Overview](spec/overview.md), [RIS System Roles](ris/SDEN_RIS_v1.md#3-system-roles)

#### Relay Node (Optional)
- Indexes producer metadata
- Responds to discovery queries
- Does not custody funds or data
- Provides optional network services

**Specification**: [Protocol Overview](spec/overview.md), [RIS System Roles](ris/SDEN_RIS_v1.md#3-system-roles)

## Core Architectural Layers

### Identity Layer

The identity layer establishes cryptographic node identity and binds it to physical hardware:

- **Node Identity Keys**: Cryptographically generated keys that uniquely identify nodes
- **Hardware Anchoring**: Mechanisms to bind identity to physical hardware
- **DID-based Identity**: Decentralized identifier model for node identity

**Specification**: [Node Identity](spec/node-identity.md), [RIS Identity and Key Management](ris/SDEN_RIS_v1.md#6-identity-and-key-management)

### Data Publication Layer

The data publication layer handles signed sensor data:

- **Data Signing**: All published data is cryptographically signed
- **Integrity Preservation**: Data structure maintains integrity guarantees
- **Provenance Tracking**: Data is linked to node identity and hardware

**Specification**: [Verification Model](spec/verification-model.md), [RIS Data Model](ris/SDEN_RIS_v1.md#7-data-model)

### Verification Layer

The verification layer enables consumers to evaluate data:

- **Signature Verification**: Cryptographic verification of data signatures
- **Provenance Evaluation**: Assessment of data origin and authenticity
- **Contextual Validity**: Evaluation of data within physical and temporal context

**Specification**: [Verification Model](spec/verification-model.md)

### Settlement Layer

The settlement layer abstracts payment mechanisms:

- **Settlement Abstraction**: Protocol-agnostic payment interface
- **Lightning Integration**: Bitcoin Lightning as primary reference implementation
- **Alternative Backends**: Support for other payment systems

**Specification**: [Settlement Layer](spec/settlement-layer.md), [RIS](ris/SDEN_RIS_v1.md)

## Protocol Flow

The core SDEN protocol flow involves:

1. **Discovery**: Buyer discovers available data from producers (optionally via relay)
2. **Quote Request**: Buyer requests pricing and access terms
3. **Payment**: Buyer pays via settlement layer (e.g., Lightning invoice)
4. **Data Delivery**: Producer delivers signed sensor data
5. **Verification**: Buyer verifies data authenticity and integrity

**Specification**: [RIS Protocol Flow Summary](ris/SDEN_RIS_v1.md#8-protocol-flow-summary), [RIS Request Lifecycle](ris/SDEN_RIS_v1.md#9-request-lifecycle--deterministic-state-machine)

## Implementation Architecture

### Reference Implementation

The reference implementation follows the architecture defined in the RIS:

- **Hardware Baselines**: Minimum hardware requirements for each node type
- **Software Stack**: Technology stack for reference implementation
- **API Surface**: Protocol-compliant API endpoints
- **Security Model**: Cryptography and security implementation

**Specification**: [Reference Implementation Spec (RIS)](ris/SDEN_RIS_v1.md)

### Deployment Models

SDEN supports various deployment models:

- **Self-Hosted**: Nodes operated independently by data producers
- **Edge Deployment**: Nodes deployed at sensor locations
- **Cloud-Compatible**: Protocol works with cloud infrastructure (but doesn't require it)

**Specification**: [RIS Deployment Modes](ris/SDEN_RIS_v1.md#14-deployment-modes)

## Security Architecture

SDEN's security model is based on:

- **Cryptographic Verification**: All trust established through cryptography
- **Minimal Trust Assumptions**: Explicit trust boundaries
- **Adversarial Model**: Designed to function under adversarial conditions

**Specification**: [Threat Model](spec/threat-model.md), [RIS Security & Cryptography Model](ris/SDEN_RIS_v1.md#12-security--cryptography-model)

## Diagrams

Architecture diagrams and visualizations are available in the [diagrams](diagrams/) directory.

## Related Documentation

- [Protocol Specifications](spec/) — Complete protocol definitions
- [Reference Implementation Spec](ris/) — Implementation architecture details
- [Features](FEATURES.md) — Protocol features and capabilities
- [Use Cases](USE_CASES.md) — Example applications
