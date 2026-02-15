# SDEN Reference Implementation

## Purpose

This reference implementation demonstrates SDEN protocol compliance through minimal, illustrative code.

## What This Will Demonstrate

The reference implementation will demonstrate:

- **Node Identity Key generation and management** — how nodes generate and control their Node Identity Key
- **Cryptographic signing** — how nodes sign published sensor data using the Node Identity Key
- **Data publication** — how nodes publish signed, integrity-preserving data streams
- **Settlement abstraction** — how nodes integrate with settlement backends (e.g., Bitcoin Lightning)
- **Verification evaluation** — how consumers evaluate data authenticity, integrity, and contextual validity
- **Protocol compliance** — adherence to all MUST, SHOULD, and MAY requirements defined in the specification

## What This Will NOT Define

The reference implementation will NOT define:

- **Protocol behavior** — the specification is authoritative, not the implementation
- **Deployment models** — how nodes are deployed or operated in practice
- **Economic models** — pricing strategies, fee structures, or incentive mechanisms
- **Hardware requirements** — specific hardware components or configurations
- **Network topology** — how nodes discover or connect to each other
- **User interfaces** — how operators or consumers interact with the system

## Non-Authoritative Status

**This reference implementation is non-authoritative.**

The authoritative definition of SDEN is the published protocol specification contained in `docs/spec/`.

- Reference implementations exist to **validate** the specification, not to define it
- Where ambiguity exists, the **specification text takes precedence**
- Alternative implementations are encouraged, provided they adhere to the protocol rules
- This implementation may contain bugs, inefficiencies, or non-optimal design choices
- This implementation does not represent the only valid way to implement SDEN

## Specification Authority

Reference implementations, deployments, or network effects do not override the written specification.

If this implementation diverges from the specification, the specification is correct and the implementation must be fixed.

## Contributing

Contributions to the reference implementation should:

- Focus on demonstrating protocol compliance
- Maintain minimalism and clarity over optimization
- Include tests that validate specification requirements
- Document any deviations or limitations clearly

---

**Remember:** The specification defines the protocol. This implementation demonstrates it.
