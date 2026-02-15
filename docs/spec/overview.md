# SDEN Protocol Overview

## 1. Purpose and Scope

Sensor Data Exchange Node (SDEN) defines an open protocol for the publication, verification, and exchange of sensor data produced by independently operated, physically anchored nodes.

The SDEN protocol specifies how self-hosted nodes:

- Establish cryptographic identity
- Bind that identity to physical hardware
- Publish signed, integrity-preserving data streams
- Enable verifiable access to data by machines, agents, and external consumers
- Receive value in exchange for data without reliance on centralized cloud infrastructure

SDEN is a protocol specification, not a product, platform, or service. It defines interoperability rules and trust boundaries, not deployment requirements or commercial offerings.

This specification defines protocol behavior only and does not mandate implementation, deployment, or economic models.

This specification intentionally separates protocol definition from reference implementation.

---

## 2. Design Philosophy

SDEN is designed around the following principles:

### 2.1 Verification Before Trust

SDEN does not assume sensor data is correct, complete, or truthful by default.  
The protocol prioritizes verifiability over authority.

Consumers of SDEN data MUST be able to independently evaluate the provenance, integrity, and contextual validity of published data without relying on centralized intermediaries.

### 2.2 Physical Anchoring

SDEN explicitly acknowledges that sensor data originates in the physical world.

The protocol therefore treats hardware identity, physical constraints, and environmental uncertainty as first-class design considerations rather than implementation details.

SDEN does not attempt to eliminate physical uncertainty; it provides mechanisms to reason about it.

### 2.3 Decentralized Operation

SDEN assumes no global coordinator, registry authority, or required cloud service.

Nodes MAY be operated by individuals, organizations, or autonomous systems.  
No single entity is assumed to control node onboarding, data publication, or settlement.

### 2.4 Minimal Protocol Surface

SDEN defines the minimum set of rules necessary to enable interoperable, verifiable data exchange.

Functionality that can be implemented off-protocol or via optional extensions is intentionally excluded from the core specification.

---

## 3. What SDEN Defines

The SDEN protocol defines:

- A cryptographic node identity model
- A mechanism for binding identity to physical hardware
- A format and process for publishing signed sensor data
- A verification model for evaluating data provenance and integrity
- A settlement abstraction for exchanging value for data access
- Governance rules for protocol evolution

These definitions are normative where explicitly stated using MUST, SHOULD, and MAY language.

---

## 4. What SDEN Does Not Define

SDEN explicitly does not define:

- A global sensor registry
- A discovery marketplace or listing service
- A pricing model for data
- A requirement to use any specific blockchain or settlement network
- A guarantee of data correctness or truth
- A mandate for specific hardware components
- A deployment topology or operational model

These exclusions are intentional and documented further in the Non-Goals specification.

---

## 5. Protocol vs Reference Implementation

SDEN distinguishes between:

- **Protocol Specification**: The normative rules described in this document set
- **Reference Implementation**: Minimal, illustrative implementations that demonstrate protocol compliance

Reference implementations are non-authoritative and exist to validate the specification, not to define it.

Alternative implementations are encouraged, provided they adhere to the protocol rules.

---

## 6. Settlement and Value Exchange

SDEN includes a settlement abstraction layer that allows nodes to exchange value for data access without embedding a specific settlement backend into the protocol.

Settlement mechanisms MAY include:

- Bitcoin Lightning
- On-chain cryptocurrency transfers
- Enterprise billing systems
- Off-chain escrow or contractual settlement

Bitcoin Lightning is treated as the primary trust-minimized reference Settlement Backend, but it is not mandatory.

Settlement does not imply trust in data correctness; it enables access, not validation.

---

## 7. Threat Model Alignment

SDEN assumes adversarial conditions.

Nodes, consumers, networks, and intermediaries MAY be compromised, dishonest, or unreliable.

The protocol is designed to limit the impact of these failures through cryptographic verification, explicit trust boundaries, and minimal assumptions.

Threats and mitigations are documented in the Threat Model specification.

---

## 8. Intended Use Cases

SDEN is intended to support:

- Machine-to-machine data exchange
- Autonomous agent data consumption
- Scientific and environmental sensing
- Infrastructure monitoring
- Edge-compute and self-hosted sensor deployments

The protocol is not optimized for consumer IoT platforms or centralized data aggregation services.

---

## 9. Evolution and Stability

SDEN prioritizes long-term stability over rapid iteration.

Protocol changes SHOULD be backward-compatible wherever possible.  
Breaking changes MUST require explicit governance approval as defined in the Governance specification.

The goal of SDEN is to establish durable infrastructure rather than short-term experimentation.

---

## 10. Summary

SDEN defines a verification-first, hardware-aware protocol for decentralized sensor data exchange.

By separating identity, verification, and settlement from centralized platforms, SDEN enables new forms of machine-readable, trust-minimized data markets rooted in physical reality rather than abstract authority.
