# NomaanOS-Core v6.0 - Technical & API Specification
> Architect & Founder: Nomaan Khan | Scholar @ IHFC – IIT Delhi

## 🖥️ Master CLI Commands Reference
Run all operations through the unified enterprise entrypoint (`nomaanos.py`):

| Command | Description | Output Format |
| :--- | :--- | :--- |
| `python nomaanos.py telemetry` | Renders real-time SOC security dashboard & Merkle chain stats. | ANSI Terminal UI |
| `python nomaanos.py verify` | Triggers Phoenix auto-remediation & ledger cryptographic chain audit. | JSON |
| `python nomaanos.py lock` | Generates L5 Neural Lock behavioral biometrics attestation token. | JSON |
| `python nomaanos.py audit` | Runs automated compliance checks against Section 65B baselines. | JSON |
| `python nomaanos.py simulate` | Executes automated red-team threat payload injection suite. | Terminal Log |
| `python nomaanos.py sbom` | Generates CycloneDX Software Bill of Materials inventory. | JSON |
| `python nomaanos.py harden` | Executes pre-flight system lockdown and environment hardening. | JSON |
| `python nomaanos.py release` | Generates cryptographically signed v6.0 release manifest bundle. | JSON |
| `python nomaanos.py server` | Launches FastAPI local security REST API server on port 8000. | Uvicorn Server |

## 🌐 REST API Endpoints Reference
When running `python nomaanos.py server`:
- `GET /` - Node health and architectural metadata.
- `GET /verify` - Phoenix cryptographic integrity verification.
- `GET /lock` - L5 Neural Lock attestation token generation.
- `GET /audit` - Automated compliance and security report.
- `POST /run` - Secure orchestrated pipeline execution (`intent` & `command`).
