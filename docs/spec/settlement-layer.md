# Settlement Layer

## 1. Overview

SDEN defines a settlement abstraction for exchanging value in return for access to sensor data.

Settlement in SDEN is intentionally decoupled from identity, verification, and data correctness.  
The protocol treats settlement as an interface, not a mandate.

SDEN does not require the use of any specific settlement network, blockchain, or financial intermediary.

This specification defines protocol behavior only and does not mandate implementation, deployment, or economic models.

---

## 2. Purpose of Settlement

The settlement layer exists to:

- Enable permissionless value exchange between data producers and consumers
- Support machine-to-machine settlement flows
- Allow nodes to control access to data based on settlement outcomes
- Avoid embedding commercial logic into the core protocol

Settlement enables *access*, not *trust*.

---

## 3. Settlement Abstraction

### 3.1 Interface Model

SDEN defines settlement as an abstract interface with the following conceptual stages:

1. **Request** — a consumer requests access to data
2. **Quote** — the node specifies settlement requirements
3. **Execution** — value transfer occurs
4. **Verification** — settlement outcome is evaluated
5. **Fulfillment** — data access is granted or denied

The protocol does not prescribe how these stages are implemented internally.

Nodes MAY be malicious. Consumers MAY be adversarial. Settlement backends MAY fail or be unreliable.

---

### 3.2 Settlement Independence

Settlement mechanisms MUST be independent of:

- Node identity verification
- Data verification and correctness evaluation
- Transport or storage mechanisms

Failure or success of settlement MUST NOT affect the validity of published data.

---

## 4. Reference Settlement Backends

SDEN permits multiple settlement backends.

Nodes MAY support one or more of the following:

- Bitcoin Lightning
- On-chain cryptocurrency transfers
- Traditional settlement processors
- Enterprise billing systems
- Off-chain contractual or escrow arrangements

Bitcoin Lightning is designated as the primary trust-minimized reference Settlement Backend due to its:

- Instant settlement
- Low transaction overhead
- Lack of centralized intermediaries
- Suitability for micropayments

Use of Lightning is optional and non-exclusive.

---

## 5. Settlement Claims and Proofs

Nodes MAY require consumers to present settlement proofs before granting access.

Settlement proofs MAY include:

- Receipt-based proofs
- Cryptographic invoices
- Signed acknowledgments
- External settlement attestations

SDEN does not define a canonical proof format.

Settlement proofs MUST be evaluated by the node according to its declared policy.

Nodes MAY be malicious and consumers MAY be adversarial; settlement proof evaluation MUST account for fraud and dispute scenarios.

---

## 6. Failure Modes

Settlement MAY fail for reasons including:

- Insufficient funds
- Network unavailability
- Timeout or partial execution
- Fraud or dispute

Nodes MUST define their own handling policies for failed or ambiguous settlement outcomes.

The protocol does not enforce retries, refunds, or dispute resolution.

---

## 7. Settlement and Access Control

Nodes MAY use settlement outcomes to:

- Gate access to live data
- Rate-limit consumers
- Provide tiered data access
- Enable pay-per-use models

Nodes MUST NOT retroactively invalidate previously published data based on settlement outcomes.

---

## 8. Settlement Is Not Verification

Settlement does not imply:

- Data correctness
- Data completeness
- Trustworthiness of the node
- Endorsement by the protocol
- Data validation or verification

Settlement does NOT validate, verify, or prove data correctness. Settlement enables access only.

Consumers MUST evaluate data independently of settlement results.

Settlement does not alter or override verification outcomes as defined in the Verification Model.

---

## 9. Privacy Considerations

Settlement mechanisms MAY introduce correlation or identity leakage.

Nodes and consumers SHOULD consider:

- Settlement metadata exposure
- Transaction traceability
- Linkability across sessions

SDEN does not mandate privacy-preserving settlement but permits it.

---

## 10. Non-Goals

The settlement layer explicitly does not:

- Define pricing strategies
- Enforce economic incentives
- Resolve disputes
- Guarantee settlement finality
- Act as a marketplace or broker

These concerns are intentionally left outside the protocol scope.

---

## 11. Summary

SDEN's settlement layer provides a flexible, settlement-agnostic mechanism for exchanging value without embedding economic assumptions into the protocol.

By treating settlement as an interface rather than a dependency, SDEN enables diverse economic models while preserving verification integrity and decentralization.
