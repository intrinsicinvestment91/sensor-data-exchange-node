# Installation

Requires **Python 3.12+**. No sensor hardware is needed — mock sensor mode is the default.

## Producer node

**Docker (recommended):**

```bash
git clone https://github.com/intrinsicinvestment91/sensor-data-exchange-node
cd sensor-data-exchange-node
cp .env.example .env          # set LNBITS_URL and LNBITS_API_KEY
docker-compose up
```

`docker-compose` stores the Ed25519 identity key and the audit log in a named volume (`sden_data`),
so the producer DID is stable across restarts.

**From source:**

```bash
pip install -r requirements.txt
cp .env.example .env
python -m sden.main
```

## Buyer SDK

`sden-client` is **not yet published to PyPI**. Install it from source:

```bash
pip install -e ./sden-client
```

This also installs the `sden-buy` CLI.

## Development install

```bash
pip install -r requirements-dev.txt

make test        # ruff + mypy + pytest
make benchmark   # RIS v1.0 timing targets
```

Tests substitute a mock wallet and skip Nostr announcement, so no LNbits instance is required.

## Validation boundary

Validation currently uses a mock wallet and mock sensor; no end-to-end run against a live wallet
and physical sensor is evidenced.

## Related Documentation

- [Configuration](CONFIGURATION.md) — environment variable reference
- [Quick Start](QUICKSTART.md) — shortest path to a running node
- [Architecture](ARCHITECTURE.md) — system architecture
- [Reference Implementation Spec (RIS v1.0)](ris/SDEN_RIS_v1.md) — implementation requirements
