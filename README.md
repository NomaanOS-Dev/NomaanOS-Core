# NomaanOS-Core: Sovereign AI Stack (SAS) Kernel

[![CI](https://github.com/NomaanOS-Dev/NomaanOS-Core/actions/workflows/ci.yml/badge.svg)](https://github.com/NomaanOS-Dev/NomaanOS-Core/actions)
[![Release](https://img.shields.io/github/v/release/NomaanOS-Dev/NomaanOS-Core?color=blue)](https://github.com/NomaanOS-Dev/NomaanOS-Core/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![API Standard](https://img.shields.io/badge/OpenAPI-3.0.3-green.svg)](openapi.json)

**Architect & Author:** Nomaan Khan | Scholar @ IHFC - IIT Delhi  
**Kernel Level:** Sovereign Security Kernel v6.0  
**Current Tag:** `v1.1.0` (Production Stable)

---

## Overview

The **Sovereign AI Stack (SAS)** is an immutable, hardware-attested, zero-trust execution environment designed for sovereign edge intelligence and cryptographically verified agent autonomy.

Complete architecture specifications, threat modeling, and formal mathematical proofs are detailed in [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Core Capabilities

* **Unified CLI Engine:** System-wide `nomaanos` command binary providing multi-subsystem attestation, terminal TUI, and telemetry probes.
* **Zero-Dependency REST API:** Built-in HTTP micro-daemon listening on `127.0.0.1:8080` conforming to [OpenAPI 3.0.3](openapi.json).
* **Hardware-Grounded Telemetry:** Direct Linux `sysfs` virtual filesystem binding querying live thermal zones without simulation wrappers.
* **Persistent Evidence Ledger:** Merkle-linked append-only JSONL event journal with automatic cold-boot chain verification.
* **Zero-Trust Identity Enclave:** Cryptographic SHA-256 HMAC nonces for secure inter-agent challenge handshakes.

---

## Quickstart

### 1. Global CLI Usage

```bash
# Health attestation across all modules
nomaanos --status

# Genuine Linux thermal & hardware load probe
nomaanos telemetry

# Verify persistent SHA-256 cryptographic ledger
nomaanos chain-verify

# Launch live visual ANSI terminal console
nomaanos tui

# Run foreground REST API daemon
nomaanos server

REST API Endpoints
# Core attestation
curl -s [http://127.0.0.1:8080/health](http://127.0.0.1:8080/health)

# Hardware telemetry
curl -s [http://127.0.0.1:8080/telemetry](http://127.0.0.1:8080/telemetry)

# Audit chain verification
curl -s [http://127.0.0.1:8080/audit/verify](http://127.0.0.1:8080/audit/verify)


cat << 'EOF' > README.md
# NomaanOS-Core: Sovereign AI Stack (SAS) Kernel

[![CI](https://github.com/NomaanOS-Dev/NomaanOS-Core/actions/workflows/ci.yml/badge.svg)](https://github.com/NomaanOS-Dev/NomaanOS-Core/actions)
[![Release](https://img.shields.io/github/v/release/NomaanOS-Dev/NomaanOS-Core?color=blue)](https://github.com/NomaanOS-Dev/NomaanOS-Core/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![API Standard](https://img.shields.io/badge/OpenAPI-3.0.3-green.svg)](openapi.json)

**Architect & Author:** Nomaan Khan | Scholar @ IHFC - IIT Delhi  
**Kernel Level:** Sovereign Security Kernel v6.0  
**Current Tag:** `v1.1.0` (Production Stable)

---

## Overview

The **Sovereign AI Stack (SAS)** is an immutable, hardware-attested, zero-trust execution environment designed for sovereign edge intelligence and cryptographically verified agent autonomy.

Complete architecture specifications, threat modeling, and formal mathematical proofs are detailed in [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Core Capabilities

* **Unified CLI Engine:** System-wide `nomaanos` command binary providing multi-subsystem attestation, terminal TUI, and telemetry probes.
* **Zero-Dependency REST API:** Built-in HTTP micro-daemon listening on `127.0.0.1:8080` conforming to [OpenAPI 3.0.3](openapi.json).
* **Hardware-Grounded Telemetry:** Direct Linux `sysfs` virtual filesystem binding querying live thermal zones without simulation wrappers.
* **Persistent Evidence Ledger:** Merkle-linked append-only JSONL event journal with automatic cold-boot chain verification.
* **Zero-Trust Identity Enclave:** Cryptographic SHA-256 HMAC nonces for secure inter-agent challenge handshakes.

---

## Quickstart

### 1. Global CLI Usage

```bash
# Health attestation across all modules
nomaanos --status

# Genuine Linux thermal & hardware load probe
nomaanos telemetry

# Verify persistent SHA-256 cryptographic ledger
nomaanos chain-verify

# Launch live visual ANSI terminal console
nomaanos tui

# Run foreground REST API daemon
nomaanos server

REST API Endpoints
# Core attestation
curl -s [http://127.0.0.1:8080/health](http://127.0.0.1:8080/health)

# Hardware telemetry
curl -s [http://127.0.0.1:8080/telemetry](http://127.0.0.1:8080/telemetry)

# Audit chain verification
curl -s [http://127.0.0.1:8080/audit/verify](http://127.0.0.1:8080/audit/verify)

Container Deployment (Docker)
# Run via docker compose
docker compose up -d

# Check live API container logs
docker compose logs -f

Architecture Matrix
Subsystem RepoOperational RoleRelease Target
NomaanOS-CoreControl plane, CLI binary, REST API enginev1.1.0
NomaanOS-ShieldSOCLinux sysfs thermal sensor & telemetry probesv1.1.0
NomaanOS-EvidenceLedgerAppend-only JSONL persistent cryptographic ledgerv1.1.0
NomaanOS-GhostNodeZero-trust enclave identity & keyed HMAC attestationv1.0.0
