[![NomaanOS Core CI](https://github.com/NomaanOS-Dev/NomaanOS-Core/actions/workflows/tests.yml/badge.svg)](https://github.com/NomaanOS-Dev/NomaanOS-Core/actions/workflows/tests.yml)
[![Release](https://img.shields.io/badge/Release-v0.1.0--alpha-blue.svg?style=for-the-badge)](https://github.com/NomaanOS-Dev/NomaanOS-Core)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

# ⚡ NomaanOS Core — Sovereign AI Stack (SAS)
> **An experimental, zero-cloud, zero-cloud execution kernel designed to run AI workloads completely offline with cryptographic verification and real-time host telemetry.**

---

### 💡 What is NomaanOS Core? (In 10 Seconds)
Most AI tools send private data and prompts to third-party cloud APIs. **NomaanOS Core is a local sovereign operating kernel**:
- **Offline & Bare-Metal**: Runs directly on Linux, Raspberry Pi, and Android/Termux environments.
- **Zero-Cloud Leakage**: Zero outbound telemetry, tracking, or cloud dependencies.
- **Cryptographic Audit Trail**: Every operation is sealed using append-only keyed HMAC-SHA256 hash chains.
- **Integrated SOC Telemetry**: Real-time browser-accessible dashboard for CPU, memory, and probe diagnostics.

---

## 🏗️ System Architecture

```text
       +-------------------------------------------------------+
       |             NomaanOS Host Telemetry & SOC             |
       |     [CPU Temp / Memory / Process / Cryptographic ID]  |
       +---------------------------+---------------------------+
                                   |
                     Raw Linux Sysfs & Kernel IPC
                                   |
       +---------------------------v---------------------------+
       |               Sovereign Core Kernel                   |
       |       - Execution Engine & Memory Enclave             |
       |       - Keyed HMAC Node Authentication                |
       |       - Red-Team & Fault-Tolerance Monitor            |
       +---------------------------+---------------------------+
                                   |
                  Tamper-Proof Audit Pipeline
                                   |
       +---------------------------v---------------------------+
       |          Immutable Evidence Hash Ledger               |
       |   [Cryptographic Verification Chain & State Seals]    |
       +-------------------------------------------------------+

🚀 Quickstart
​1. Launch Core CLI
git clone [https://github.com/NomaanOS-Dev/NomaanOS-Core.git](https://github.com/NomaanOS-Dev/NomaanOS-Core.git)
cd NomaanOS-Core
python nomaanos_cli.py

2. Launch Local SOC Console
​Open web/index.html in any browser, or serve it locally:
python -m http.server 8080 -d web/

Navigate to http://localhost:8080 to access the live operations interface.

​3. Docker Deployment
docker compose up -d

🛡️ Key Components
ComponentResponsibility
nomaanos.pyCore kernel execution engine and secure state manager.
mobile_node.pyEdge telemetry adapter tailored for mobile/ARM devices.
redteam_benchmark.jsonThreat vectors and cryptographic stress test benchmarks.
web/index.htmlInteractive SOC operator cockpit and health probe endpoint.
