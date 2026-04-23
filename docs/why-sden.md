# Why SDEN: The Case for Bitcoin-Native IoT Data Markets

## The problem

Sensor data is valuable. A temperature reading from a cold-chain shipment, a CO₂ measurement from an air quality monitor, a soil humidity reading from a precision agriculture deployment — these have direct economic value to buyers who cannot generate them locally.

The problem is monetization. Today, if you want to sell sensor data, you have three options, all of which require giving something up:

1. **Upload to a centralized platform** (AWS IoT, Google Cloud IoT, Azure IoT Hub). The platform stores your data, sets your price, takes a cut, and can revoke your access at any time. You are a data supplier to a marketplace you don't control.

2. **Join a token-gated data network** (Ocean Protocol, Streamr, DIMO). You acquire a network token, stake it, and participate in the network's economics. The value of your data is now entangled with the value of a token you didn't issue and can't control.

3. **Build custom infrastructure**. Expensive, takes months, and the result is a closed silo that no buyer can discover or trust.

None of these options are available to a Raspberry Pi operator in a remote location with a DHT22 wired up. None of them work for a single sensor.

## Why Bitcoin Lightning is the right substrate

Bitcoin Lightning solves a specific problem: micropayments between two parties who don't trust each other, settled instantly, with no third party required.

This is exactly the problem SDEN needs to solve. A buyer wants to pay 150 satoshis for a temperature reading. The producer wants to be paid before delivering the data. Neither party trusts the other, and neither should have to.

Lightning's properties match the requirement precisely:

- **No new token.** Satoshis are the unit of account. Producers price in sats, buyers pay in sats. There is no protocol token, no staking requirement, no gas fee denominated in something the producer doesn't hold.
- **Non-custodial.** The producer controls their own Lightning wallet. The buyer controls theirs. No intermediary holds funds at any point.
- **Instant settlement.** Invoice payment is verified in real time — the producer does not deliver data until the payment is confirmed, and the payment is confirmed before the buyer waits more than a second.
- **Global reach.** A producer in a location with no banking infrastructure can receive satoshis from a buyer anywhere in the world. The payment rails already exist.
- **Runs on commodity hardware.** Lightning nodes and LNbits wallets run on the same Raspberry Pi that reads the sensor. There is no specialized hardware requirement.

## Why not a new token?

Every token-gated data network has the same cold-start problem: the token must have value before the network has users, and the network needs users before the token has value. Projects solve this with venture funding and token sales — which creates a different problem, because the token price becomes the thing investors track, not data volume or quality.

SDEN has no token to pump and no token to dump. A producer earns sats when a buyer pays for their data. A buyer pays sats when they want the data. That is the entire economic model.

## Why not a new blockchain?

On-chain data storage is expensive. A single signed temperature reading — 200 bytes of JSON — costs real money to store on any EVM chain. Gas fees fluctuate unpredictably. Smart contracts add attack surface and introduce latency.

SDEN stores nothing on-chain. The producer keeps a local signed audit log. The buyer verifies the Ed25519 signature against the producer's DID. Trust is established cryptographically, not through a blockchain's consensus mechanism.

## The role of cryptographic identity

The piece that makes this work without a platform is Ed25519 signing with a decentralized identifier (DID).

Every SDEN producer has a `did:key:z6Mk...` identifier derived directly from their Ed25519 public key. No registry. No issuer. No certificate authority. The DID is self-sovereign — the producer generates it, owns it, and uses it to sign every reading they produce.

A buyer who receives a sensor reading can verify the Ed25519 signature using only the producer's DID — which is embedded in the reading itself. If the signature is valid, the reading is authentic. If it's tampered with, the signature fails. No oracle, no third party, no phone home.

This is what "cryptographically verifiable" means in practice: the buyer's trust in the data does not depend on trusting the producer personally, or trusting a platform the producer belongs to. It depends only on mathematics.

## The DePIN framing

SDEN is DePIN — Decentralized Physical Infrastructure Networks — without the infrastructure overhead that makes most DePIN projects inaccessible.

The typical DePIN project requires: a custom L1 or L2 blockchain, a native token for staking and rewards, a network of validators or oracles to attest hardware readings, and significant coordination overhead to bootstrap the network.

SDEN requires: a Raspberry Pi, a sensor, a LNbits wallet, and a copy of this repository.

The tradeoff is scale. SDEN v1.0 is a single producer, single buyer protocol. There is no global indexing layer, no automatic discovery at scale, no cross-producer aggregation. These are explicit non-goals for v1.0 — they are addressed in the v1.1+ roadmap with the relay node and batch request work.

What v1.0 does have is something no complex DePIN project has: a working demo that a developer can run in five minutes with no prior Lightning knowledge, on a $35 computer, with no token purchase required.

That is the wedge. The complexity can come later.
