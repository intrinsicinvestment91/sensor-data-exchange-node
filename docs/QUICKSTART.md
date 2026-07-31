# Quick Start

The shortest path is the [root README quickstart](../README.md#quickstart). This page summarises it
and points at the reference material.

## Run a producer node

Requires Python 3.12+ and an [LNbits](https://lnbits.com) wallet. Mock sensor mode is the default —
no hardware needed.

```bash
git clone https://github.com/intrinsicinvestment91/sensor-data-exchange-node
cd sensor-data-exchange-node
cp .env.example .env          # set LNBITS_URL and LNBITS_API_KEY
docker-compose up
```

The node listens on `http://localhost:8080`. `GET /info` returns its DID, sensor type, and price.

## Buy a reading

`sden-client` is not yet published to PyPI — install it from source:

```bash
pip install -e ./sden-client
sden-buy --url http://localhost:8080 --type temperature
```

The [root README](../README.md) shows the Python SDK and raw `curl` equivalents.

## Validation boundary

Validation currently uses a mock wallet and mock sensor; no end-to-end run against a live wallet
and physical sensor is evidenced. See the
[reference implementation status](../reference-implementation/README.md) for the full breakdown of
what is implemented, what is validated, and what remains planned.

## Related Documentation

- [Protocol Specifications](spec/) — protocol definitions
- [Reference Implementation Spec (RIS v1.0)](ris/SDEN_RIS_v1.md) — the frozen implementation baseline
- [Installation](INSTALLATION.md) — installation options
- [Configuration](CONFIGURATION.md) — environment variable reference
