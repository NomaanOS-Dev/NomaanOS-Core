# NomaanOS-Core System Architecture

## 1. Zero-Trust Sentinel Model
The core execution engine (`NoseExec`) enforces strict fail-closed boundaries:
- **Binary Allowlisting**: Command execution is restricted to strictly pre-approved system binaries.
- **Path Stripping**: Fully qualified paths and directory traversals (`/bin/`, `../`) are normalized and validated against approved command signatures.
- **POSIX Resource Limits**: Processes operate under hard caps for CPU time (`RLIMIT_CPU`) and memory allocation (`RLIMIT_AS`), preventing resource exhaustion attacks.

## 2. Evidence Ledger & Audit Trails
The `EvidenceLedger` subsystem provides tamper-evident audit logs:
- **HMAC-SHA256 Chaining**: Each audit entry is signed with cryptographic hashes tied to the previous entry signature.
- **Fail-Closed Tamper Detection**: If any historical entry is mutated on disk, subsequent reads trigger immediate chain invalidation and alert telemetry.

## 3. Package Structure (PEP 517/518)
src/
└── nomaanos/
├── init.py          # Package entry points & version exposure
├── cli.py               # Dispatch interface for Sentinel execution
├── engine.py            # NoseExec process isolation & rlimits
├── ledger/
│   └── engine.py        # Cryptographic EvidenceLedger implementation
└── soc/
└── telemetry.py     # System telemetry & integrity metric counters
