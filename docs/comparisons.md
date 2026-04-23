# SDEN vs. Alternatives: Technical Comparison

This document compares SDEN to the major sensor data marketplace and DePIN protocols. The goal is not to diminish these projects — several are technically impressive — but to be precise about where SDEN's approach differs and why.

---

## Ocean Protocol

**What it is:** A decentralized data marketplace built on EVM chains. Data assets are tokenized as "datatokens"; buyers purchase datatokens to access datasets.

**How data is sold:**
1. Provider publishes a dataset and mints a datatoken.
2. Buyer purchases the datatoken on a DEX (using OCEAN or ETH for gas).
3. Buyer presents the datatoken to the provider's Compute-to-Data node or directly downloads the dataset.

**Strengths:**
- Mature ecosystem with real data assets published
- Compute-to-Data allows analysis without raw data exposure
- Strong academic and enterprise partnerships

**Where SDEN differs:**

| Dimension | Ocean Protocol | SDEN |
|---|---|---|
| Payment token | OCEAN (ERC-20) + gas (ETH) | Bitcoin satoshis |
| New token required | Yes — must hold OCEAN | No |
| Real-time streaming | No — batch datasets | Yes — per-reading invoices |
| Data integrity | Provider assertion | Ed25519 signature, verifiable by buyer |
| Runs on Raspberry Pi | No — requires cloud or server infrastructure | Yes |
| Single-sensor support | Impractical — dataset overhead | Native use case |
| Settlement time | EVM block time (12s+) + DEX swap | Lightning (< 1s) |

**The core tension:** Ocean is designed for large datasets from institutional providers. The economics of minting datatokens, paying gas, and operating Compute-to-Data infrastructure make it impractical for a single DHT22 sensor selling 150-sat readings. SDEN targets exactly this segment.

---

## Streamr

**What it is:** A decentralized real-time data streaming network. Publishers push data streams; subscribers access them. DATA token is used for network payments and staking.

**How data is sold:**
1. Publisher creates a stream and sets a price in DATA tokens.
2. Subscriber pays DATA tokens to the publisher's node.
3. Data flows via the Streamr P2P network.

**Strengths:**
- Genuine real-time streaming (not batch)
- P2P delivery without centralized storage
- Active developer community

**Where SDEN differs:**

| Dimension | Streamr | SDEN |
|---|---|---|
| Payment token | DATA (ERC-20) | Bitcoin satoshis |
| Network overhead | Requires joining the Streamr P2P network | Direct HTTP to producer |
| Node requirements | Streamr node software + staking | uvicorn + LNbits wallet |
| Data signing | Not built-in | Ed25519, every reading |
| Buyer verification | Trust the network | Verify signature locally |
| Lightning native | No | Yes |

**The core tension:** Streamr's strength is high-throughput streaming at scale. SDEN's strength is the simplest possible path from a single sensor to a paying buyer. For continuous data feeds from thousands of sensors, Streamr's P2P infrastructure makes sense. For "I have one sensor and I want to sell readings," SDEN's overhead is an order of magnitude lower.

Note: Streamr's v1.1 roadmap includes SDEN-compatible streaming via WebSocket — this is explicitly called out in the SDEN v1.2 roadmap.

---

## DIMO

**What it is:** A vehicle data network. Car owners install a DIMO-compatible device (OBD-II dongle or compatible hardware) and earn $DIMO tokens for contributing vehicle telemetry data.

**How data is sold:**
1. Car owner installs DIMO device and connects their vehicle.
2. DIMO's network collects and indexes the telemetry.
3. Data buyers pay $DIMO tokens to access aggregated or raw vehicle data via API.

**Strengths:**
- Purpose-built for automotive data with strong OEM partnerships
- Polished consumer app and device ecosystem
- Real data from millions of vehicles

**Where SDEN differs:**

| Dimension | DIMO | SDEN |
|---|---|---|
| Domain | Vehicle telemetry only | Any sensor type |
| Hardware | Proprietary DIMO dongle or compatible OBD-II device | Any sensor + Raspberry Pi |
| Payment token | $DIMO | Bitcoin satoshis |
| Data custody | DIMO platform | Producer-held, buyer-verified |
| Sensor types | Automotive (speed, RPM, fuel, location) | Temperature, humidity, pressure, CO₂, extensible |
| Self-hosted | No | Yes |

**The core tension:** DIMO is not a general-purpose sensor protocol — it is a vehicle data company that issues a token. Comparing SDEN to DIMO is comparing a protocol to a product. SDEN is what you build when you want the DIMO model for sensors that aren't in a car.

---

## peaq

**What it is:** A Polkadot parachain designed as a DePIN infrastructure layer. Machine identities, data sharing, and payments are implemented as on-chain primitives.

**How data is sold:**
1. Machine registers a machine DID on the peaq chain.
2. Data is published on-chain or via peaq's off-chain data layer.
3. Buyers interact with smart contracts for access control and payment.

**Strengths:**
- Substrate-based, so benefits from Polkadot shared security
- Machine identity primitives are well-designed
- Active grant and ecosystem funding

**Where SDEN differs:**

| Dimension | peaq | SDEN |
|---|---|---|
| Blockchain | Polkadot parachain (peaq) | None |
| Payment | DOT / peaq native token | Bitcoin satoshis |
| Machine identity | On-chain DID registry | Self-sovereign `did:key` (no registry) |
| Settlement | Smart contract execution | Lightning invoice |
| Running cost | Gas fees per transaction | Zero protocol fees |
| Hardware requirements | Server or cloud for parachain interaction | Raspberry Pi Zero |

**The core tension:** peaq is building DePIN infrastructure at the blockchain layer — it requires running or connecting to a Polkadot parachain, paying gas in tokens you must acquire, and operating within the Polkadot ecosystem. SDEN has no blockchain, no gas, and no tokens. The tradeoff is that SDEN v1.0 has no global state — there is no on-chain record of producers or transactions. This is a deliberate choice, not an oversight.

---

## Summary

| | SDEN | Ocean | Streamr | DIMO | peaq |
|---|:---:|:---:|:---:|:---:|:---:|
| **New token required** | No | OCEAN | DATA | $DIMO | DOT |
| **New blockchain** | No | EVM | EVM | EVM | Polkadot |
| **Runs on Raspberry Pi** | ✓ | ✗ | ✗ | ✗ | ✗ |
| **Ed25519 signed readings** | ✓ | ✗ | ✗ | ✗ | ✗ |
| **W3C WoT compatible** | ✓ | ✗ | ✗ | ✗ | ✗ |
| **Non-custodial** | ✓ | ✗ | ✗ | ✗ | ✗ |
| **Single-sensor native** | ✓ | ✗ | Partial | ✗ | ✗ |
| **Lightning native** | ✓ | ✗ | ✗ | ✗ | ✗ |
| **Zero protocol fees** | ✓ | ✗ | ✗ | ✗ | ✗ |

SDEN does not compete with these protocols on their own terms — it does not attempt global data indexing, DEX liquidity, or L1 smart contract composability. It competes on simplicity, Bitcoin alignment, and the ability to run on hardware that costs $35.
