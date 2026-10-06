# Sovereign AI Stack (SAS) - System Architecture & Engineering Specifications

**Author:** Nomaan Khan  
**Affiliation:** IHFC - Technology Innovation Hub, IIT Delhi  
**Kernel Level:** Sovereign Security Kernel v6.0  
**Current Release:** v1.1.0 (Production Stable)

---

## 1. High-Level System Architecture

The Sovereign AI Stack (SAS) provides an immutable, cryptographically verifiable, and hardware-attested execution environment designed for high-integrity edge computing and zero-trust autonomous agents.

+------------------------------------+
|       Unified CLI & REST API       |
|   (nomaanos CLI / api_server.py)   |
+-----------------+------------------+
|
+----------------------------+----------------------------+
|                                                         |
+--------v--------+                                      +---------v---------+
|  GhostNode      |                                      |   ShieldSOC       |
|  (Zero-Trust)   |                                      |   (Observability) |
+--------+--------+                                      +---------+---------+
|  HMAC Attest    |                                      |  Linux sysfs      |
|  Mutual Auth    |                                      |  Thermal Probes   |
+--------+--------+                                      +---------+---------+
|                                                         |
+----------------------------+----------------------------+
|
+----------v-----------+
|   EvidenceLedger     |
|   (Audit Integrity)  |
+----------+-----------+
|  Append-only JSONL   |
|  SHA-256 Hash Chain  |
+----------------------+

## 2. Core Pillars & Subsystem Specifications

### I. NomaanOS-Core (Master Orchestration & Control Plane)
* **Unified Dispatcher (`nomaanos`):** System-wide CLI utility handling status health attestation, ANSI-colored terminal telemetry consoles (TUI), and foreground API execution.
* **Zero-Dependency API Engine (`api_server.py`):** Python standard library HTTP daemon listening on `127.0.0.1:8080` serving three authoritative routes:
  * `GET /health` - Core engine attestation.
  * `GET /telemetry` - Machine telemetry snapshot.
  * `GET /audit/verify` - Mathematical verification of the persistent hash chain.

### II. ShieldSOC (Hardware Telemetry & Sensor Adaptation)
* **Direct Sysfs Interface (`host_telemetry.py`):** Bypasses mock libraries to query raw Linux kernel thermal zone descriptors (`/sys/class/thermal/thermal_zone*/temp`).
* **Non-Simulated Telemetry:** Reports true operating temperature, architecture (`aarch64`/`x86_64`), and system load directly to the upper orchestrator.

### III. GhostNode (Enclave Identity & Node Attestation)
* **Zero-Trust Challenge Verification:** Employs keyed SHA-256 HMAC handshakes for edge entity authentication without external certificate authorities.
* **Replay-Attack Mitigation:** Implements single-use challenge nonce tokens verified inside the enclave boundary.

### IV. EvidenceLedger (Cryptographic Persistence & Proof of Audit)
* **Merkle-Linked Hash Chain:** Sequential blocks where each state contains $Hash(index + timestamp + payload + PrevHash)$.
* **Append-Only JSONL Store (`ledger_persistent.py`):** Guarantees zero data loss across daemon restarts with automated verification routines upon cold boot.

---

## 3. Cryptographic Verification Guarantees

Every ledger transaction follows strict cryptographic chaining:

$$H_i = \text{SHA-256}\left(\text{Index}_i \mathbin{\Vert} \text{Timestamp}_i \mathbin{\Vert} \text{PayloadHash}_i \mathbin{\Vert} H_{i-1}\right)$$

Any modification to historical block records on disk results in an immediate failure during `chain-verify`, triggering an attestation halt.

---

## 4. Verification & Operational Matrix

| Capability | Module Provider | Verification Command | Implementation State |
| :--- | :--- | :--- | :--- |
| **System Attestation** | `NomaanOS-Core` | `nomaanos --status` | Verified Operational |
| **Hardware Thermals** | `NomaanOS-ShieldSOC`| `nomaanos telemetry` | sysfs Native Probe |
| **Tamper Detection** | `NomaanOS-EvidenceLedger` | `nomaanos chain-verify` | Persistent SHA-256 |
| **Console Display** | `NomaanOS-Core` | `nomaanos tui` | Real-time ANSI Refresh |
| **Network Interface** | `NomaanOS-Core` | `nomaanos server` | Zero-dependency HTTP |

---

## 5. Security & Threat Model

* **Threat:** Root fs file tampering.  
  * **Mitigation:** EvidenceLedger validates recursive hash links upon boot. Altered rows prevent new blocks from being accepted.
* **Threat:** False telemetry spoofing.  
  * **Mitigation:** Thermal probes bind strictly to `/sys/class/` virtual file descriptors, returning graceful fail-safe states if interfaces are unreadable.
* **Threat:** Network overhead in constrained environments.  
  * **Mitigation:** Zero external runtime dependencies; all modules execute purely on top of POSIX-compliant Python 3 internals.
