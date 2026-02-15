# SDEN Documentation

This directory contains all documentation for the Sensor Data Exchange Node (SDEN) protocol.

## Documentation Structure

### Protocol Specifications

The authoritative protocol specifications define the SDEN protocol rules and requirements:

- **[Overview](spec/overview.md)** — Protocol purpose, scope, and design philosophy
- **[Architecture](spec/architecture.md)** — System architecture and component design
- **[Node Identity](spec/node-identity.md)** — Cryptographic identity model
- **[Verification Model](spec/verification-model.md)** — Data verification and provenance
- **[Settlement Layer](spec/settlement-layer.md)** — Payment and settlement abstraction
- **[Governance](spec/governance.md)** — Protocol evolution and governance
- **[Threat Model](spec/threat-model.md)** — Security assumptions and mitigations
- **[Non-Goals](spec/non-goals.md)** — Explicitly out-of-scope items

### Reference Implementation Specification (RIS)

The RIS defines the build contract for the reference implementation:

- **[RIS v1.0](ris/SDEN_RIS_v1.md)** — Complete reference implementation specification
- **[Requirements](ris/requirements.md)** — Implementation requirements
- **[Assumptions](ris/assumptions.md)** — Implementation assumptions
- **[Open Questions](ris/open-questions.md)** — Unresolved implementation questions
- **[RIS README](ris/README.md)** — Overview of RIS documentation

### Implementation Guides

User-facing documentation for working with SDEN:

- **[Features](FEATURES.md)** — Protocol features and capabilities
- **[Architecture](ARCHITECTURE.md)** — High-level architecture overview
- **[Installation](INSTALLATION.md)** — Installation instructions (when available)
- **[Quick Start](QUICKSTART.md)** — Quick start guide (when available)
- **[Configuration](CONFIGURATION.md)** — Configuration reference (when available)
- **[Use Cases](USE_CASES.md)** — Example use cases and applications
- **[Contributing](CONTRIBUTING.md)** — How to contribute to SDEN

### Reference Implementation

- **[Reference Implementation README](../reference-implementation/README.md)** — Status and purpose of the reference implementation

## Protocol vs Implementation

SDEN distinguishes between:

- **Protocol Specification**: The normative rules described in `docs/spec/`
- **Reference Implementation**: Minimal, illustrative implementations that demonstrate protocol compliance (see `reference-implementation/`)

Reference implementations are non-authoritative and exist to validate the specification, not to define it. Alternative implementations are encouraged, provided they adhere to the protocol rules.

## Current Status

**Protocol Status**: Draft Protocol Specification (internally stable, subject to external review)

**Implementation Status**: Protocol/Spec Maturity — Reference implementation is in planning phase. See [Reference Implementation Status](../reference-implementation/README.md) for details.

## Getting Started

1. **Understanding the Protocol**: Start with the [Protocol Overview](spec/overview.md)
2. **Reviewing Specifications**: Browse the [Protocol Specifications](spec/)
3. **Planning Implementation**: Consult the [Reference Implementation Spec](ris/)
4. **Contributing**: See [Contributing Guidelines](CONTRIBUTING.md)
