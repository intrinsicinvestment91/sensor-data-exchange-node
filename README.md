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

Sensor Data Exchange Node (SDEN) is an **open protocol specification** for hardware-anchored, self-hosted sensor infrastructure.

SDEN defines how independently operated sensor nodes can:

- Cryptographically identify themselves  
- Publish **verifiable live data**  
- Exchange that data directly with AI systems, autonomous agents, and external buyers  

—all **without reliance on centralized cloud intermediaries**.

---

## Protocol Status

**Status: Draft Protocol Specification**

The SDEN specification is considered internally stable but subject to external review and implementation feedback.

**Current Phase: Protocol/Spec Maturity**

This repository is currently focused on protocol specification and definition. Reference implementation is in planning. See [Reference Implementation Status](reference-implementation/README.md) for details.

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

1. [Features](docs/FEATURES.md)  
2. [Architecture](docs/ARCHITECTURE.md)  
3. [Installation](docs/INSTALLATION.md)  
4. [Quick Start](docs/QUICKSTART.md)  
5. [Configuration](docs/CONFIGURATION.md)  
6. [Use Cases](docs/USE_CASES.md)  
7. [Contributing](docs/CONTRIBUTING.md)  
8. [License](LICENSE)  
9. [Contact & Links](#contact--links)

---

## 🚀 How to Engage

### Review Protocol Specifications

SDEN is currently in **protocol/spec maturity** phase. The authoritative protocol specifications are available in:

- **[Protocol Specifications](docs/spec/)** — Core protocol definitions
- **[Reference Implementation Spec (RIS)](docs/ris/)** — Build contract for reference implementation
- **[Documentation Index](docs/README.md)** — Overview of all documentation

### Contribute

Contributions are welcome at this stage:

- **Protocol Review**: Review and provide feedback on protocol specifications in `docs/spec/`
- **Spec Contributions**: Propose improvements or clarifications to the protocol definition
- **Reference Implementation**: Contribute to the reference implementation (see [Reference Implementation Status](reference-implementation/README.md))

See [Contributing Guidelines](docs/CONTRIBUTING.md) for details.

### Implement

The SDEN protocol specification is designed to enable independent implementations. To implement SDEN:

1. Review the [Protocol Specifications](docs/spec/) to understand the protocol requirements
2. Consult the [Reference Implementation Spec](docs/ris/) for implementation guidance
3. Build your implementation following the protocol rules defined in the specifications

Alternative implementations are encouraged, provided they adhere to the protocol rules defined in the specification.

---

## 📞 Contact & Links

- **GitHub Repository**: [intrinsicinvestment91/sensor-data-exchange-node](https://github.com/intrinsicinvestment91/sensor-data-exchange-node)
- **License**: [LICENSE](LICENSE)
- **Documentation**: [docs/README.md](docs/README.md)
- **Protocol Specifications**: [docs/spec/](docs/spec/)
- **Reference Implementation Spec**: [docs/ris/](docs/ris/)
