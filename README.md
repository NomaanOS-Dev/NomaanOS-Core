<div align="center">

# NomaanOS-Core
### Local-first edge AI security research kernel

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?style=flat-square)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Research%20Prototype-orange.svg?style=flat-square)](#status)

</div>

## Status

This project is an experimental research prototype. It is not a certified production security platform and should not be deployed as one without independent validation, threat modeling, and environment-specific testing.

## What this project is

NomaanOS-Core provides a local-first execution and orchestration layer for research experiments focused on:

- offline AI execution
- host telemetry and anomaly observation
- cryptographic audit trails
- disconnected or low-trust coordination patterns

## Quick start

### Prerequisites

- Python 3.8+
- Linux, macOS, or Android/Termux
- Git

### Setup

```bash
git clone https://github.com/NomaanOS-Dev/NomaanOS-Core.git
cd NomaanOS-Core
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

### Validate the stack

```bash
python nomaanos.py --status
python nomaanos.py telemetry
python nomaanos.py chain-verify
pytest -q
```

## Architecture

```text
Linux / POSIX host
    ↓
ShieldSOC telemetry layer
    ↓
NomaanOS-Core orchestration/runtime
    ↓
EvidenceLedger audit chain
    ↓
GhostNode / disconnected coordination layer
```

## Key components

- `nomaanos.py` — CLI and operational entry point
- `api_server.py` — local HTTP service for status and telemetry endpoints
- `tui_dashboard.py` — terminal dashboard for interactive viewing
- `src/engine.py` — fail-closed execution layer
- `src/orchestrator.py` — orchestration logic for request processing
- `tests/` — validation and behavior checks

## Known limitations

- no external security audit or formal compliance review
- not a validated enterprise deployment platform
- cryptographic assumptions are local and experimental
- multi-node role testing is still limited
- some modules are research scaffolding rather than hardened production services

## Development

### Run tests

```bash
pytest -q
```

### Compile and lint checks

```bash
python -m py_compile nomaanos.py api_server.py tui_dashboard.py
ruff check .
```

## Security

See [SECURITY.md](SECURITY.md) for responsible disclosure expectations and threat-model notes.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development expectations and review workflow.

## License

MIT License — see [LICENSE](LICENSE).

## Maintainer

- Nomaan Khan
- GitHub: https://github.com/NomaanOS-Dev

## Disclaimer

This repository is distributed as an experimental research project. It is provided as-is for local experimentation and engineering exploration. It should not be treated as a deployable production security platform without independent validation.
