# Verification Model

## 1. Overview

SDEN defines a verification-first model for evaluating sensor data produced by independently operated, physically anchored nodes.

The protocol makes a strict distinction between:

- **Data authenticity** — whether data originated from a specific node identity
- **Data integrity** — whether data was altered after publication
- **Data correctness** — whether data accurately reflects physical reality

SDEN guarantees authenticity and integrity at the protocol level.  
Correctness is contextual, probabilistic, and explicitly not guaranteed.

Node identity and signature requirements are defined in the Node Identity Model.

---

## 2. Verification Goals

The SDEN verification model is designed to enable data consumers to:

- Attribute data to a specific node identity
- Detect tampering or forgery
- Reason about physical plausibility
- Evaluate risk without relying on centralized authorities

Verification in SDEN is consumer-driven.  
The protocol provides evidence, not conclusions.

---

## 3. Authenticity Verification

### 3.1 Signed Data Publication

All sensor data published under the SDEN protocol MUST be cryptographically signed using the Node Identity Key.

A valid signature establishes that:

- The data originated from the holder of the Node Identity Key
- The data has not been modified since signing

Authenticity verification does not imply correctness or trustworthiness.

---

### 3.2 Identity Continuity

Consumers MAY track identity continuity over time to establish long-term behavioral context.

Continuity is an observation, not a guarantee, and MAY be broken intentionally or maliciously.

---

## 4. Integrity Verification

### 4.1 Data Integrity Guarantees

SDEN ensures integrity through:

- Cryptographic signatures
- Optional content addressing or hashing
- Immutable publication semantics once data is released

Any modification to published data MUST invalidate prior integrity guarantees.

---

### 4.2 Transport Independence

Integrity verification is independent of transport.

Data MAY be transmitted, cached, relayed, or mirrored by untrusted intermediaries without compromising integrity.

---

## 5. Verification Classes

SDEN defines multiple verification classes to reflect varying levels of confidence and context.

These classes are descriptive, not prescriptive.

### 5.1 Class I — Identity-Only Verification

- Data is signed by a valid node identity
- No additional claims or corroboration are present

This class establishes provenance only.

---

### 5.2 Class II — Self-Asserted Context

- Data includes signed metadata describing hardware, sensors, or environment
- Assertions are self-reported by the node

Consumers MUST treat these claims as unverified.

---

### 5.3 Class III — Corroborated Verification

- Data is corroborated by external sources
- Corroboration MAY include:
  - Cross-node agreement
  - Third-party attestations
  - Environmental constraints

Corroboration increases confidence but does not eliminate uncertainty.

Nodes MAY collude to produce coordinated false data. Corroboration from multiple sources does not guarantee correctness if sources are colluding.

---

### 5.4 Class IV — Contextual Confidence

- Data has historical consistency
- Physical constraints are respected
- Behavior aligns with observed norms

Confidence emerges over time and usage, not at publication.

---

## 6. Physical-World Constraints

SDEN explicitly models the physical world as uncertain.

Verification MUST account for:

- Sensor drift and failure
- Environmental interference
- Adversarial manipulation of physical conditions
- Limited observability
- Physical sensors that MAY lie or report false data without detection

No protocol mechanism can fully eliminate these factors.

---

## 7. Failure and Adversarial Scenarios

SDEN assumes:

- Nodes MAY publish false or misleading data
- Nodes MAY be compromised
- Sensors MAY fail silently
- Networks MAY be unreliable

The verification model is designed to limit blast radius rather than guarantee correctness.

---

## 8. Verification vs Settlement

Verification and settlement are orthogonal concerns.

- Settlement does not imply data correctness
- Verification does not imply entitlement to settlement
- Verification does NOT require settlement or payment
- Settlement does NOT validate or verify data correctness

Consumers MUST evaluate verification independently of settlement outcomes.

---

## 9. Consumer Responsibility

Data consumers are responsible for:

- Selecting verification thresholds
- Interpreting verification classes
- Combining SDEN evidence with external context

SDEN provides tools for reasoning, not final judgments.

---

## 10. Non-Goals

The verification model explicitly does not:

- Certify truth
- Guarantee accuracy
- Prevent coordinated false reporting
- Replace domain-specific validation

These limitations are fundamental to physical sensing.

---

## 11. Summary

SDEN’s verification model prioritizes transparency, provenance, and integrity over claims of truth.

By making uncertainty explicit and verifiable evidence portable, SDEN enables informed decision-making without centralized trust.
