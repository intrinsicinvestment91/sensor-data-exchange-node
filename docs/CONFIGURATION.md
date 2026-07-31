# Configuration

All settings are read from environment variables. Copy [`.env.example`](../.env.example) to `.env`
and edit it.

The canonical variable reference — names, defaults, and descriptions — is the
[Configuration table in the root README](../README.md#configuration). It is not duplicated here so
the two cannot drift apart.

## Required

`LNBITS_URL` and `LNBITS_API_KEY` are required; the producer refuses to start without them. Use an
LNbits **invoice/read** key for the producer. The buyer SDK's `SDENWallet` needs an **admin** key,
because it pays outgoing invoices.

## Node identity

On first boot the node generates an Ed25519 keypair and writes it to `DID_KEY_PATH`
(`identity.pem` by default). The resulting `did:key:z6Mk…` is stable across restarts as long as
that key persists.

For containers and secrets managers, prefer injecting the key directly:

```bash
export DID_PRIVATE_KEY_PEM="$(cat identity.pem)"
docker-compose up
```

The `docker-compose` setup keeps both the key and the audit database in the `sden_data` named
volume. Neither `identity.pem` nor `audit.db` is tracked in Git — both are listed in
[`.gitignore`](../.gitignore).

## Sensors

`USE_MOCK_SENSOR=true` (the default) uses `MockSensorReader`, which needs no hardware and supports
`temperature`, `humidity`, `pressure`, and `co2`. Set it to `false` only on a node with a real
DHT22 attached.

## Validation boundary

Validation currently uses a mock wallet and mock sensor; no end-to-end run against a live wallet
and physical sensor is evidenced.

## Related Documentation

- [Installation](INSTALLATION.md) — installation options
- [Quick Start](QUICKSTART.md) — shortest path to a running node
- [Architecture](ARCHITECTURE.md) — system architecture
- [Reference Implementation Spec (RIS v1.0)](ris/SDEN_RIS_v1.md) — implementation requirements
