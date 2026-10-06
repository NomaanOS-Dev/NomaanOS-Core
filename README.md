<div align="center">

# NomaanOS-Core
### Local-First Edge AI Security Kernel

[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg?style=flat-square)](https://github.com/NomaanOS-Dev/NomaanOS-Core/actions)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?style=flat-square)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Research%20Prototype-orange.svg?style=flat-square)](#status)

</div>

## Status

**This is a research-stage experimental prototype.** It is not a certified production security platform. Use for local experimentation, research, and learning only. Independent validation required before any high-assurance deployment.

## What is NomaanOS-Core?

NomaanOS-Core is an experimental local orchestration and execution kernel designed for:

- **Offline AI execution** — run workloads completely locally without cloud dependencies
- **Cryptographic audit logging** — append-only tamper-evident records of all operations
- **Host telemetry** — real-time system health and anomaly monitoring
- **Air-gapped coordination** — peer-to-peer sync in disconnected environments

## Quick Start

### Prerequisites

- Python 3.8+
- Linux, macOS, or Android (Termux)
- Git

### Installation

```bash
git clone https://github.com/NomaanOS-Dev/NomaanOS-Core.git
cd NomaanOS-Core
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements-dev.txt
```

### Validation

```bash
# Run system status check
python nomaanos.py --status

# Check cryptographic audit chain
python nomaanos.py chain-verify

# View live telemetry
python nomaanos.py telemetry

# Run test suite
pytest -v
```

## Architecture

```
Host Kernel (Linux/POSIX)
    ↓
ShieldSOC (Telemetry & Monitoring)
    ↓
NomaanOS-Core (Orchestration & Execution)
    ↓
EvidenceLedger (Cryptographic Audit)
    ↓
GhostNode (P2P Coordination)
```

## Key Components

| Component | Purpose | Status |
|-----------|---------|--------|
| `nomaanos.py` | CLI dispatcher and main entry point | Working |
| `api_server.py` | REST API for status and telemetry | Experimental |
| `tui_dashboard.py` | Terminal UI for monitoring | Experimental |
| `src/engine.py` | Execution engine with allowlist control | Working |
| `src/orchestrator.py` | Workload orchestration | Experimental |
| `tests/` | Unit test suite | Partial coverage |

## Known Limitations

- ❌ No external security audit
- ❌ Not tested in production environments
- ❌ Limited error recovery mechanisms
- ❌ Local-only operation (no cloud integration planned)
- ⚠️ Cryptographic assumptions based on SHA-256 (not post-quantum)
- ⚠️ Single-node operation (multi-node coordination is experimental)

## Development

### Running Tests

```bash
pytest -q
```

### Code Quality

```bash
# Lint with ruff
ruff check .

# Type check
mypy src/

# Security scan
bandit -r src/

# Compile check
python -m py_compile nomaanos.py api_server.py
```

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Security

See [SECURITY.md](SECURITY.md) for vulnerability reporting and threat model details.

## License

MIT License — see [LICENSE](LICENSE) for details.

## Authors

- **Nomaan Khan** — Architect, IHFC IIT Delhi

## Contact

- GitHub: [@NomaanOS-Dev](https://github.com/NomaanOS-Dev)
- Email: nomaanos@duck.com (for general inquiries)

## Disclaimer

This project is provided as-is for research and educational purposes. Security controls are intentionally designed as defense-in-depth examples, not production-grade security guarantees. Do not rely on this software for protecting sensitive data without independent security review and validation for your specific threat model.
