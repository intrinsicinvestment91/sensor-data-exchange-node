# Contributing to SDEN

Thank you for your interest in contributing to SDEN! This document covers contributions to the
**protocol specification**. For contributions to the code, see
[CONTRIBUTING.md](../CONTRIBUTING.md) at the repository root.

## Current Status

The protocol specification is frozen at RIS v1.0 and the reference implementation exists in
[`sden/`](../sden/) and [`sden-client/`](../sden-client/). The focus of this document is:

- Protocol specification review and refinement
- Specification contributions and improvements
- Keeping the implementation aligned with the specification

## How to Contribute

### 1. Review Protocol Specifications

The most valuable contribution at this stage is reviewing the protocol specifications:

- **Read the Specifications**: Start with the [Protocol Overview](spec/overview.md) and explore the [Protocol Specifications](spec/)
- **Provide Feedback**: Identify ambiguities, potential issues, or areas that need clarification
- **Ask Questions**: Submit questions about protocol behavior or design decisions

**Where to Provide Feedback**: Open issues or discussions on the GitHub repository

### 2. Contribute to Protocol Specifications

Contributions to the protocol specification are welcome:

#### Types of Contributions

- **Clarifications**: Improve specification clarity and remove ambiguities
- **Corrections**: Fix errors or inconsistencies in the specification
- **Improvements**: Propose enhancements that align with protocol principles
- **Documentation**: Improve specification documentation and examples

#### Contribution Process

1. **Review Governance**: Understand the [Governance](spec/governance.md) process for protocol changes
2. **Propose Changes**: Submit proposals as written specification changes
3. **Public Review**: Proposals undergo public review and discussion
4. **Acceptance**: Changes are accepted based on governance criteria

#### Proposal Requirements

Proposals SHOULD include:

- Clear motivation for the change
- Scope and impact analysis
- Backward compatibility assessment
- Security and threat implications
- Specification text changes

See [Governance - Change Process](spec/governance.md#4-change-process) for details.

#### Governance Principles

All contributions must align with SDEN's governance principles:

- **Stability Over Velocity**: Changes should be rare, deliberate, and conservative
- **Minimal Authority**: No single entity has special protocol authority
- **Capture Resistance**: Mechanisms resist economic capture and vendor lock-in

See [Governance](spec/governance.md) for complete governance details.

### 3. Contribute to Reference Implementation

The reference implementation is available in [`sden/`](../sden/) and [`sden-client/`](../sden-client/):

- **Implementation Contributions**: Contribute code to the reference implementation
- **Testing**: Help test protocol compliance
- **Documentation**: Improve implementation documentation

See [CONTRIBUTING.md](../CONTRIBUTING.md) at the repository root for development setup, and the
[Reference Implementation README](../reference-implementation/README.md) for what is implemented,
what is validated, and what remains planned.

#### Reference Implementation Principles

The reference implementation:

- Demonstrates protocol compliance
- Maintains minimalism and clarity over optimization
- Includes tests that validate specification requirements
- Documents any deviations or limitations clearly

See [Reference Implementation README](../reference-implementation/README.md) for details.

### 4. Create Alternative Implementations

SDEN encourages alternative implementations that adhere to the protocol rules:

- **Independent Implementations**: Build your own SDEN-compliant implementation
- **Protocol Compliance**: Ensure your implementation follows the protocol specifications
- **Community Sharing**: Share your implementation experiences and learnings

The protocol specification is authoritative; implementations validate it, not define it.

## Contribution Guidelines

### Specification Contributions

- **Follow Specification Style**: Maintain consistency with existing specification documents
- **Reference Protocol Principles**: Align contributions with protocol design principles
- **Consider Threat Model**: Ensure changes don't weaken security guarantees
- **Maintain Minimalism**: Avoid adding unnecessary complexity

### Code Contributions

- **Follow Code Style**: Adhere to project coding standards
- **Write Tests**: Include tests that validate specification requirements
- **Document Changes**: Clearly document what your code does and why
- **Protocol Compliance**: Ensure code implements protocol requirements correctly

## Getting Started

1. **Read the Documentation**: Start with the [Protocol Overview](spec/overview.md)
2. **Understand the Protocol**: Review relevant [Protocol Specifications](spec/)
3. **Review Governance**: Understand the [Governance](spec/governance.md) process
4. **Choose Your Contribution**: Decide whether to review, propose changes, or plan implementation
5. **Engage**: Open issues, submit proposals, or start discussions

## Questions?

- **Protocol Questions**: Open an issue or discussion on GitHub
- **Specification Ambiguities**: Report them as issues for clarification
- **Implementation Questions**: See [Reference Implementation README](../reference-implementation/README.md)

## Related Documentation

- [Protocol Specifications](spec/) — Complete protocol definitions
- [Governance](spec/governance.md) — Protocol governance and change process
- [Reference Implementation README](../reference-implementation/README.md) — Reference implementation status
- [Protocol Overview](spec/overview.md) — Protocol purpose and scope
