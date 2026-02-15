# Node Identity Model

## 1. Overview

SDEN defines a cryptographic node identity model designed to uniquely identify independently operated nodes and bind that identity to physical hardware.

Node identity in SDEN is not an account, username, or platform registration.  
It is a cryptographic construct used to establish provenance, accountability, and verifiability for published sensor data.

The protocol assumes that node identities may be created, operated, compromised, or retired without centralized coordination.

---

## 2. Cryptographic Identity

### 2.1 Node Identity Key Pair

Each SDEN node MUST generate and control a long-lived asymmetric key pair, referred to as the **Node Identity Key**.

- The public key serves as the node’s canonical identifier
- The private key MUST remain under the node operator’s control
- All protocol-relevant messages originating from the node MUST be signed using this key

The protocol does not mandate a specific cryptographic algorithm, but implementations SHOULD use widely reviewed, modern primitives.

---

### 2.2 Identity Persistence

A node’s identity persists across restarts, network changes, and data publications.

Changing a node's Node Identity Key constitutes the creation of a new node identity and MUST be treated as such by data consumers.

---

## 3. Hardware Anchoring

### 3.1 Physical Binding

SDEN explicitly recognizes that nodes exist in the physical world.

Nodes SHOULD bind their cryptographic identity to physical hardware characteristics using one or more of the following mechanisms:

- Secure elements or hardware security modules
- TPM-derived measurements
- Hardware serials or fused identifiers
- Measured boot attestations

The protocol does not mandate specific hardware components but provides a framework for declaring and verifying hardware bindings.

---

### 3.2 Hardware Trust Levels

SDEN defines multiple hardware trust levels rather than a binary trusted/untrusted model.

Nodes MAY declare their hardware anchoring capabilities, including:

- No hardware anchoring
- Software-only identity
- Secure element-backed key storage
- Attested boot or runtime environment

Data consumers MUST evaluate these declarations independently and SHOULD treat them as claims rather than guarantees.

---

## 4. Identity Claims and Attestations

Nodes MAY publish signed identity metadata describing:

- Hardware characteristics
- Sensor capabilities
- Deployment context
- Operator-provided assertions

These claims:

- MUST be cryptographically signed by the Node Identity Key
- MUST be treated as self-asserted unless externally verified
- MAY be corroborated by third-party attestations or measurements

SDEN does not define a centralized attestation authority.

---

## 5. Node Lifecycle

### 5.1 Creation

Node identity creation is local and permissionless.

There is no global registration process or approval authority.

---

### 5.2 Operation

During operation, nodes MUST:

- Sign published sensor data
- Sign identity and capability claims
- Maintain continuity of identity across data publications

Nodes MAY be malicious or compromised. The protocol does not prevent nodes from publishing false data, making false claims, or breaking identity continuity.

---

### 5.3 Key Rotation

Nodes MAY rotate identity keys.

Key rotation SHOULD be accompanied by:

- A signed declaration linking the old and new keys
- A clear indication that continuity is asserted, not guaranteed

Consumers MAY choose whether to honor such continuity claims.

---

### 5.4 Revocation and Decommissioning

SDEN does not provide a global revocation mechanism.

Nodes MAY publish signed revocation or decommissioning statements indicating that an identity should no longer be considered active.

Consumers are responsible for interpreting and enforcing revocation semantics according to their risk tolerance.

---

## 6. Identity and Accountability

Node identity establishes accountability for data publication, not truthfulness.

A valid signature proves that data originated from a specific node identity but does not guarantee:

- Sensor correctness
- Environmental accuracy
- Operator honesty
- Trustworthiness
- Data truthfulness

Identity does NOT imply trustworthiness. Identity establishes provenance and accountability only.

These concerns are addressed by the Verification Model.

Data authenticity guarantees are defined in the Verification Model.

---

## 7. Privacy Considerations

SDEN does not require node identities to be human-readable or linked to real-world identities.

Operators MAY choose to operate nodes pseudonymously.

Persistent node identities MAY allow long-term correlation of published data; operators and consumers SHOULD account for this when designing deployments.

---

## 8. Non-Goals

The SDEN node identity model explicitly does not attempt to:

- Prove real-world location
- Guarantee hardware authenticity
- Prevent identity cloning
- Enforce operator behavior
- Provide centralized identity resolution

These limitations are intentional and reflect the realities of physical-world sensing.

---

## 9. Summary

SDEN node identity is a cryptographic, hardware-aware construct designed to support verifiable data provenance without centralized control.

It provides a stable foundation for accountability and verification while explicitly acknowledging the limits of trust in physical systems.
