# ⚡ NomaanOS Core — Sovereign AI Stack (SAS)
> **An enterprise-hardened, zero-cloud execution kernel designed to run AI workloads completely offline with cryptographic verification and real-time host telemetry.**

---

### 💡 What is NomaanOS Core? (In 10 Seconds)
Most AI tools send your private data and prompts to public cloud servers. **NomaanOS Core is a self-sovereign operating environment**:
- Runs entirely on local bare-metal / edge hardware (Linux, Raspberry Pi, Android/Termux).
- Zero external cloud dependencies or telemetry leaks.
- Cryptographically signs and audits every operation with tamper-proof ledgers.
- Features a built-in real-time SOC web console for hardware and security metrics.

---

## 🏗️ System Architecture

```text
       +-------------------------------------------------------+
       |             NomaanOS Host Telemetry & SOC             |
       |     [CPU Temp / Memory / Process / Cryptographic ID]   |
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

🚀 Quickstart & Interactive SOC Console
​Run the full local environment and interactive web telemetry in under 30 seconds:
​1. Run Core CLI
# Clone the repository
git clone [https://github.com/NomaanOS-Dev/NomaanOS-Core.git](https://github.com/NomaanOS-Dev/NomaanOS-Core.git)
cd NomaanOS-Core

# Launch Core Engine CLI
python nomaanos_cli.py

2. Launch Local SOC Console
​Open web/index.html directly in your browser, or serve it locally:
python -m http.server 8080 -d web/

Visit http://localhost:8080 to interact with real-time telemetry gauges and endpoint probing.
​3. Docker Deployment
docker compose up -d

cat << 'EOF' > README.md
# ⚡ NomaanOS Core — Sovereign AI Stack (SAS)
> **An enterprise-hardened, zero-cloud execution kernel designed to run AI workloads completely offline with cryptographic verification and real-time host telemetry.**

---

### 💡 What is NomaanOS Core? (In 10 Seconds)
Most AI tools send your private data and prompts to public cloud servers. **NomaanOS Core is a self-sovereign operating environment**:
- Runs entirely on local bare-metal / edge hardware (Linux, Raspberry Pi, Android/Termux).
- Zero external cloud dependencies or telemetry leaks.
- Cryptographically signs and audits every operation with tamper-proof ledgers.
- Features a built-in real-time SOC web console for hardware and security metrics.

---

## 🏗️ System Architecture

```text
       +-------------------------------------------------------+
       |             NomaanOS Host Telemetry & SOC             |
       |     [CPU Temp / Memory / Process / Cryptographic ID]   |
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

🚀 Quickstart & Interactive SOC Console
​Run the full local environment and interactive web telemetry in under 30 seconds:
​1. Run Core CLI
# Clone the repository
git clone [https://github.com/NomaanOS-Dev/NomaanOS-Core.git](https://github.com/NomaanOS-Dev/NomaanOS-Core.git)
cd NomaanOS-Core

# Launch Core Engine CLI
python nomaanos_cli.py

2. Launch Local SOC Console
​Open web/index.html directly in your browser, or serve it locally:
python -m http.server 8080 -d web/

Visit http://localhost:8080 to interact with real-time telemetry gauges and endpoint probing.
​3. Docker Deployment
docker compose up -d


🛡️ Key Features & Modules
Module / ComponentReal-World Role
nomaanos.py / nomaanos_cli.pySovereign engine runtime, command execution, and state isolation.
mobile_node.pyEdge node adapter for low-power and mobile edge devices.
redteam_benchmark.jsonSynthetic security threat simulation vectors and resilience tests.
web/index.htmlWeb-based SOC operations interface for live probe monitoring.
Dockerfile & docker-compose.ymlOne-click containerized deployment for air-gapped infrastructure.

📜 Compliance & Security Specs
​Cryptographic Standard: Keyed HMAC SHA-256
​Dependency Model: Python 3.8+ Standard Library Only (Zero third-party attack surface)
​Target Platforms: Linux, Raspberry Pi, POSIX Edge Nodes
