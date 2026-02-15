# Governance

## 1. Overview

SDEN defines a minimal governance model focused on protocol stability, long-term interoperability, and resistance to capture.

The governance process exists to manage protocol evolution, not to coordinate economic activity, enforce compliance, or arbitrate disputes.

SDEN explicitly avoids on-chain governance, token voting, or centralized control bodies.

This specification defines protocol behavior only and does not mandate implementation, deployment, or economic models.

---

## 2. Governance Principles

SDEN governance is guided by the following principles:

### 2.1 Stability Over Velocity

Protocol changes SHOULD be rare, deliberate, and conservative.

Backward compatibility is prioritized over rapid iteration.  
Breaking changes are treated as exceptional events.

---

### 2.2 Minimal Authority

No single entity, foundation, company, or maintainer is granted special protocol authority by default.

Governance decisions derive from documented process and public review, not ownership or branding.

---

### 2.3 Capture Resistance

Governance mechanisms are designed to resist:

- Economic capture
- Vendor lock-in
- Regulatory centralization
- Spec drift driven by short-term incentives

No mechanism is assumed to be permanently capture-proof.

---

## 3. Specification Authority

The authoritative definition of SDEN is the published protocol specification contained in this repository.

Reference implementations, deployments, or network effects do not override the written specification.

Where ambiguity exists, the specification text takes precedence.

---

## 4. Change Process

### 4.1 Proposal Submission

Protocol changes MUST be proposed as written specification changes.

Proposals SHOULD include:

- Clear motivation
- Scope and impact analysis
- Backward compatibility assessment
- Security and threat implications

---

### 4.2 Review and Discussion

Proposals MUST undergo public review.

Review is intended to identify:

- Specification ambiguity
- Threat model regressions
- Centralization risks
- Implementation complexity

Consensus is preferred but not strictly required.

---

### 4.3 Acceptance Criteria

A proposal MAY be accepted if:

- It does not violate existing non-goals
- It preserves or improves verification guarantees
- It does not introduce mandatory dependencies
- It maintains protocol minimalism

Non-Goals and Threat Model documents are normative constraints on governance decisions.

Acceptance does not imply endorsement of any implementation.

---

## 5. Versioning

SDEN follows semantic versioning principles at the specification level.

- **Patch versions** clarify language or fix errors without changing behavior
- **Minor versions** add backward-compatible features
- **Major versions** introduce breaking changes

Breaking changes MUST be explicitly labeled and justified.

---

## 6. Backward Compatibility

Backward compatibility SHOULD be maintained wherever possible.

When compatibility cannot be preserved:

- The break MUST be explicitly documented
- Migration paths SHOULD be described
- The rationale MUST be compelling and defensible

Silent incompatibility is unacceptable.

---

## 7. Governance and Implementation Independence

Governance decisions do not mandate implementation behavior.

Governance does NOT enforce, control, or compel implementation behavior. Governance manages specification evolution only.

Implementations MAY choose to:

- Adopt changes immediately
- Delay adoption
- Remain on older versions

Protocol compliance is version-scoped.

---

## 8. No Economic Governance

SDEN governance does not include:

- Fee setting
- Incentive tuning
- Token issuance
- Treasury management
- Reward distribution

Economic models are external to the protocol.

---

## 9. No Dispute Resolution

SDEN governance does not resolve disputes between:

- Node operators
- Data consumers
- Settlement participants
- Implementers

Disputes are out of scope and MUST be handled externally.

---

## 10. Forking and Divergence

Specifications MAY be forked.

Competing or divergent specifications MUST clearly identify themselves to avoid confusion.

The SDEN name does not imply exclusivity.

---

## 11. Summary

SDEN governance exists to preserve protocol integrity, not to control outcomes.

By minimizing authority, resisting capture, and prioritizing stability, SDEN aims to remain a durable foundation for verifiable, hardware-anchored sensor data exchange over the long term.

