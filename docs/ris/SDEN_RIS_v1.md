# Sensor Data Exchange Node (SDEN)
## Reference Implementation Specification (RIS) v1.0

**Status:** Frozen / Implementation-ready  
**Derived from:** SDEN Whitepaper v1.0 (Frozen)

---

## Table of Contents
1. Purpose and Intent
2. Scope and Non-Scope
3. System Roles
4. Hardware Baselines
5. Software Stack
6. Identity and Key Management
7. Data Model
8. Protocol Flow Summary
9. Request Lifecycle — Deterministic State Machine
10. API Surface — Endpoints, Schemas, Error Codes
11. Error Handling, Logging, and Local Audit Model
12. Security & Cryptography Model
13. Performance Targets & Deterministic Timing Constraints
14. Deployment Modes
15. Roadmap Alignment
16. Compliance and Licensing

---

## 1. Purpose and Intent

This RIS defines the authoritative implementation baseline for SDEN, translating the frozen whitepaper into a deterministic, testable, and auditable system.

**Audience**
- Software engineers
- Security reviewers
- Grant evaluators

**Focus**
Minimal production-capable node, explicitly avoiding speculative or optional features outside v1.0.

---

## 2. Scope and Non-Scope

### In Scope
- Single producer node
- Single buyer agent
- Optional relay node
- Lightning-based settlement
- Signed sensor data delivery

### Out of Scope
- Global consensus mechanisms
- Token issuance or staking
- On-chain data storage
- Anonymity guarantees

---

## 3. System Roles

### Producer Node
- Collects sensor data
- Signs data with DID-bound keys
- Advertises data availability
- Accepts Lightning payments
- Delivers verified data

### Buyer Agent
- Discovers available data
- Requests quotes
- Pays Lightning invoices
- Verifies signatures

### Relay Node (Optional)
- Indexes producer metadata
- Responds to discovery queries
- Does not custody funds or data

---

## 4. Hardware Baselines

### Producer (Minimum)
| Component | Requirement |
|---------|-------------|
| CPU | 2-core ARMv8 / x86_64 |
| RAM | 2 GB |
| Storage | 32 GB (encrypted) |
| OS | Linux |
| Network | Ethernet or LTE |

### Relay (Minimum)
| Component | Requirement |
|---------|-------------|
| CPU | 4 cores |
| RAM | 8 GB |
| Storage | 128 GB |

---

## 5. Software Stack

- **OS:** Debian or Fedora IoT
- **Container Runtime:** Docker or Podman
- **Core Language:** Rust
- **Agent / Integration:** Python
- **Database:** SQLite (Producer), PostgreSQL (Relay)
- **Transport:** HTTPS (TLS 1.3)

---

## 6. Identity and Key Management

- **DID Method:** `did:key` (Ed25519)
- **Key Hierarchy**
  - Root identity key (long-lived)
  - Optional session keys (rotated)

All messages and audit entries **must be signed**.

---

## 7. Data Model

### Canonical Sensor Record
- Producer DID
- Sensor type
- Timestamp (UTC)
- Value + units
- Quality score
- Signature

### Storage Model
- Raw data stored locally
- Metadata optionally exposed via relay

---

## 8. Protocol Flow Summary

1. Producer boots and registers identity
2. Producer advertises data availability
3. Buyer discovers data
4. Buyer requests quote
5. Producer issues Lightning invoice
6. Buyer pays invoice
7. Producer verifies payment
8. Producer delivers signed data

---

## 9. Request Lifecycle — Deterministic State Machine

**Producer Node States**

```
IDLE
  |
  v
REQUEST_RECEIVED
  |
  +-- invalid --> TERMINATED
  |
  v
VALIDATED
  |
  v
PRICED
  |
  v
INVOICED
  |
  +-- timeout --> TERMINATED
  |
  v
PAID
  |
  v
DELIVERED
  |
  v
TERMINATED
```

**Rules**
- Deterministic flow
- No retries or partial payments
- All failures are terminal

---

## 10. API Surface — Endpoints, Schemas, Error Codes

### Endpoints
- `/quote` — Request price and invoice
- `/verify_payment` — Confirm settlement
- `/data` — Retrieve signed sensor data

### Example Schema (Quote Request)
```json
{
  "request_id": "uuid-v4",
  "sensor_type": "temperature",
  "quantity": 1,
  "timestamp_utc": "ISO8601",
  "signature": "base64"
}
```

### Example Schema (Quote Response)
```json
{
  "request_id": "uuid-v4",
  "price_sats": 150,
  "invoice": "lnbc1...",
  "invoice_expiry": 3600
}
```

### Error Codes
| Code | Meaning |
|-----|--------|
| 100 | Invalid request format |
| 101 | Sensor type not available |
| 102 | Invoice not found |
| 103 | Payment not verified |
| 104 | Invoice expired |
| 105 | Data unavailable |

---

## 11. Error Handling, Logging, and Local Audit Model

- All failures are terminal
- Audit logs are append-only and signed

### Audit Log Fields
- timestamp_utc
- request_id
- event_type
- details
- error_code
- signature

---

## 12. Security & Cryptography Model

- **Keys:** Ed25519, DID-bound
- **Signatures:** Required on all data and audit entries
- **Integrity:** Unique request IDs + timestamps
- **Transport:** HTTPS / TLS 1.3

**Threats Addressed**
- Data spoofing
- Replay attacks
- Unauthorized requests
- Payment circumvention
- Audit tampering

---

## 13. Performance Targets & Deterministic Timing

| Operation | Target |
|---------|--------|
| Quote response | < 500 ms |
| Invoice generation | < 100 ms |
| Invoice verification | < 1 s |
| Data retrieval & signing | < 2 s |
| Total request → delivery | < 3.5 s |

Measured on minimum hardware baselines using UTC clocks.

---

## 14. Deployment Modes

- **Single Node:** Producer + Buyer (minimal)
- **Production Pilot:** Producer + Buyer
- **Indexed Deployment:** Producer + Relay + Buyer

---

## 15. Roadmap Alignment

| Version | Scope |
|--------|-------|
| v1.0 | Minimal node, deterministic lifecycle, signed data, Lightning, local audit |
| v1.1 | Optional relay, batch requests, concurrent handling |
| v2.0 | Multi-node federation, standardized discovery, optional SLAs |

Backward compatibility is mandatory; optional features are never required for v1.0 compliance.

---

## 16. Compliance and Licensing

- Open-source license: MIT or Apache-2.0
- No proprietary runtime dependencies
- Public Ed25519 cryptography only
- Signed, append-only local audit logs
- Lightning Network payments only (non-custodial)

---

**End of RIS v1.0 — Fully Frozen**
