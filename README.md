# NomaanOS-Core v6.0
> Sovereign AI Stack (SAS) - Fail-Closed Execution & Cryptographic Evidence Ledger.

## Repository Structure
```text
NomaanOS-Core/
├── src/
│   ├── __init__.py
│   └── engine.py        # Core fail-closed execution logic
├── tests/
│   └── test_exec.py     # Automated unit & security test suite
├── config/
│   └── security_policy.json # Strict execution allowlists & policies
├── docs/                # Architecture notes & specs
└── SECURITY.md          # Vulnerability reporting guidelines

Architecture Overview
L1 Host Substrate: Hardened Linux baseline with strict access controls.
L2 NOS Exec: Deterministic execution engine (shell=False, strict allowlists, shlex sanitization).
L3 Sentinel Proxy: Gatekeeper enforcing invariant security policies.
L4 AEGIS: On-device local LLM orchestration (Zero-leakage).
L5 Neural Lock: Continuous behavioral validation.
Security & Compliance
Append-only Merkle-tree audit logging.
Designed for edge environments and high-security research.
