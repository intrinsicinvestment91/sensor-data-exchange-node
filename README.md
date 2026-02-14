<div align="center">
  <img src="docs/diagrams/logo.png" alt="SDEN Logo" width="180" />
  <h1>Sensor Data Exchange Node (SDEN)</h1>
  <p>
    A decentralized, self-hosted data commerce infrastructure for live sensor signals.
  </p>
  <p>
    <a href="https://github.com/intrinsicinvestment91/sensor-data-exchange-node/stargazers">
      <img src="https://img.shields.io/github/stars/intrinsicinvestment91/sensor-data-exchange-node?style=social" alt="GitHub stars" />
    </a>
    <a href="LICENSE">
      <img src="https://img.shields.io/github/license/intrinsicinvestment91/sensor-data-exchange-node" alt="License" />
    </a>
    <a href="https://github.com/intrinsicinvestment91/sensor-data-exchange-node/actions">
      <img src="https://img.shields.io/github/workflow/status/intrinsicinvestment91/sensor-data-exchange-node/CI" alt="CI status" />
    </a>
  </p>
</div>

---

## 📌 What is SDEN?

# Sensor Data Exchange Node (SDEN)

Sensor Data Exchange Node (SDEN) is an **open protocol specification** for hardware-anchored, self-hosted sensor infrastructure.

SDEN defines how independently operated sensor nodes can:

- Cryptographically identify themselves  
- Publish **verifiable live data**  
- Exchange that data directly with AI systems, autonomous agents, and external buyers  

—all **without reliance on centralized cloud intermediaries**.

---

## Key Protocol Principles

- **Cryptographic node identity**  
- **Hardware anchoring and physical verification**  
- **Integrity-preserving data publication**  
- **Trust-minimized settlement**  
- **Long-term infrastructure durability**

---

## Settlement and Payments

SDEN introduces a **settlement abstraction layer** that allows nodes to receive micropayments across multiple payment systems.  

- **Bitcoin Lightning** is the primary reference implementation for instant, uncensorable, low-friction settlement.  
- The protocol remains compatible with alternative enterprise or blockchain payment backends.

---

## Project Positioning

- **Not a product or SaaS platform**  
- **Foundational infrastructure thesis** and protocol definition  
- Supports a new class of **verifiable, machine-to-machine data markets**

---

## Development Stages

1. **Protocol Specification** — defines identity, verification, settlement, and governance models  
2. **Reference Implementation** — minimal open implementations of core protocol components  
3. **Network Deployment** — infrastructure scaling and ecosystem growth

---

The goal is to establish **durable, self-hosted data infrastructure** where **physical nodes, not centralized platforms, anchor trust**.

---

## 🧠 Why SDEN Matters

Traditional IoT ecosystems centralize ownership and monetization — locking producers out of their own data. SDEN changes this by empowering local operators to:

- ✊ Retain **full control of their sensor data**
- 🔐 Provide **provable, signed live signals**
- ⚡ Monetize through **machine-to-machine payments**
- 📡 Support **AI and automated agents** with fresh inputs

---

## 🔍 Table of Contents

1. [Features](#features)  
2. [Architecture](#architecture)  
3. [Installation](#installation)  
4. [Quick Start](#quick-start)  
5. [Configuration](#configuration)  
6. [Use Cases](#use-cases)  
7. [Contributing](#contributing)  
8. [License](#license)  
9. [Contact & Links](#contact--links)

---

## ✨ Features

- 📡 Self-hosted live sensor ingestion and processing  
- 🔒 Cryptographically signed datasets with verifiable provenance  
- ⚖️ Lightning Network micropayment settlement  
- 🧪 Modular node types: Producer, Buyer, Relay  
- 🔄 Extensible API interface (see RIS documentation)

---

## 🏗 Architecture

View detailed designs and protocol flows in the `docs/` folder.  
Key artifacts include:

- **Whitepaper (Frozen v1.0)** — Vision and economic grounding  
- **Reference Implementation Spec (RIS v1.0)** — Build contract  
- **Diagrams** — Architecture, state machines, interactions

---

## 📥 Installation

> *Coming soon — detailed installation scripts and automation.*

In general:

1. Clone the repository  
2. Install runtime dependencies  
3. Review config samples in `configs/`  
4. Run demo scripts from `examples/`

---

## ▶️ Quick Start

```bash
git clone https://github.com/intrinsicinvestment91/sensor-data-exchange-node.git
cd sensor-data-exchange-node
./scripts/setup-env.sh
./scripts/run-demo.sh
