# Third-Party Notices

SDEN is licensed under the Apache License, Version 2.0 (see [`LICENSE`](LICENSE)).

This repository additionally contains files copied from a separately licensed project. Those files
are listed below and are **not** covered by SDEN's Apache-2.0 licence — each is governed by the
licence reproduced with it.

---

## BitAgent

Two files are vendored from the **BitAgent** project into the [`bitagent/`](bitagent/) directory so
that SDEN's producer node can create and check Lightning invoices through LNbits without requiring a
separate BitAgent checkout.

| File in this repository | Upstream path in BitAgent | Modification |
|---|---|---|
| `bitagent/agent_wallet.py` | `agent_wallet.py` (root-level layout) | Executable code body unchanged; provenance and licence comments added |
| `bitagent/lnbits_client.py` | `lnbits_client.py` (root-level layout) | Executable code body unchanged; provenance and licence comments added |

Both files were taken from BitAgent's root-level module layout. The only SDEN-side change to either
file is the comment header at the top; no executable behavior was changed. They are imported at
runtime by `sden/sensor_agent.py`, which places the `bitagent/` directory on `sys.path`.

BitAgent is an independent project by the same author as SDEN. It is not a contributor to SDEN, and
its inclusion here does not imply any endorsement or joint maintenance.

### Licence

```
MIT License

Copyright (c) 2025 intrinsicinvestment91

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
