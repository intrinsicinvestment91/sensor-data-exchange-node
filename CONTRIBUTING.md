# Contributing to SDEN

SDEN is an open protocol. Contributions to the reference implementation, buyer SDK, documentation, and the protocol spec itself are all welcome.

## What to work on

Browse [open issues](https://github.com/Intrinsicinvestment91/sensor-data-exchange-node/issues) — issues tagged [`good first issue`](https://github.com/Intrinsicinvestment91/sensor-data-exchange-node/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) are explicitly scoped for contributors new to the codebase.

Good areas to contribute right now:
- **`sden-client` Python SDK** — buyer-side library (`SDENBuyer`, `SensorReading.verify()`) described in Phase 3 of `docs/PLAN.md`
- **`sden-buy` CLI** — `pip install sden-client` command-line buyer
- **Bruno / Postman collection** — zero-code exploration of the three API endpoints
- **GitHub Codespaces devcontainer** — one-click development environment
- **`docs/wot-integration.md`** — how SDEN maps to W3C WoT concepts
- **Hardware testing** — running SDEN on a Raspberry Pi and reporting results

## Development setup

```bash
git clone https://github.com/Intrinsicinvestment91/sensor-data-exchange-node
cd sensor-data-exchange-node

# Install bitagent (provides AgentWallet — SDEN's only runtime dependency on it)
cd /path/to/bitagent && pip install -r requirements.txt && cd -

pip install -r requirements-dev.txt
cp .env.example .env   # fill in LNBITS_URL and LNBITS_API_KEY; USE_MOCK_SENSOR=true works without hardware
```

## Running tests

```bash
make test        # lint (ruff) + type-check (mypy) + full test suite
make benchmark   # assert RIS v1.0 timing targets
pytest tests/test_integration.py -v   # integration tests only
pytest tests/test_foo.py::TestClass::test_method -v   # single test
```

All 36 tests must pass before opening a PR. CI enforces the same checks.

## Protocol changes

The protocol spec (`docs/ris/SDEN_RIS_v1.md`) is frozen at v1.0. Changes that affect the wire format, state machine transitions, or cryptographic requirements require opening a protocol issue first for discussion before any code is written.

Implementation improvements, performance optimizations, additional sensor types, and buyer SDK features do not require spec changes.

## Pull request process

1. Fork the repo and create a branch from `main`.
2. Make your changes. Add or update tests as appropriate.
3. Run `make test` — all checks must pass locally.
4. Open a PR with a clear description of what the change does and why.

PRs are reviewed within 48 hours during the initial community-building period.

## Code style

- Python 3.12+, typed (`mypy --ignore-missing-imports`)
- `ruff` for linting (config inherits from `pyproject.toml` defaults — no configuration file means ruff defaults apply)
- No comments that describe what the code does; only comments that explain non-obvious *why*
- No new dependencies without discussion in an issue first
