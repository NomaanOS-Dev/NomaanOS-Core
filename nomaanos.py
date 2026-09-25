import sys
import json
from src.orchestrator import NomaanOSOrchestrator
from src.telemetry_dashboard import render_dashboard
from src.phoenix_engine import PhoenixEngine
from src.neural_lock import NeuralLock
from src.compliance_auditor import ComplianceAuditor
from src.threat_simulator import ThreatSimulator
from src.sbom_generator import SBOMGenerator
from src.hardening import SystemHardening
from src.release_manifest import ReleaseManifest
from src.swarm_sync import SwarmSyncProtocol
from src.health_check import MasterHealthCheck
from src.fuzzer import SecurityFuzzer
from src.snapshot_manager import SnapshotManager
from src.banner import render_banner
from src.deploy_verifier import DeploymentVerifier
from src.attestation_issuer import AttestationIssuer
from src.streamer import TelemetryStreamer
from src.diagnostics import MasterDiagnostics
from src.report_exporter import SecurityReportExporter
from src.stress_test import MasterStressTest
from src.chain_verifier import CryptographicChainVerifier

def print_help():
    render_banner()
    print("\033[1;36m" + "="*60)
    print("      NOMAANOS SOVEREIGN AI STACK - MASTER CLI REFERENCE")
    print("="*60 + "\033[0m")
    print("Usage: python nomaanos.py [command]\n")
    print("Available Commands:")
    print("  chain-verify - Verify cryptographic append-only audit chain integrity")
    print("  stress      - Run master high-concurrency stress & durability test")
    print("  export-report - Export master enterprise security audit report")
    print("  diagnostics - Run deep enclave diagnostics & kernel inspection")
    print("  stream      - Stream real-time node security telemetry & heartbeat")
    print("  cert-issue  - Issue cryptographic root attestation certificate")
    print("  deploy-check - Verify production deployment readiness & artifacts")
    print("  snapshot    - Create cryptographic state snapshot & backup bundle")
    print("  health      - Run master node health & subsystem attestation")
    print("  fuzz        - Run automated security fuzzing & payload mutation suite")
    print("  telemetry   - Render real-time SOC security telemetry dashboard")
    print("  verify      - Run Phoenix auto-remediation & integrity check")
    print("  lock        - Generate L5 Neural Lock attestation token")
    print("  audit       - Generate automated compliance & security report")
    print("  simulate    - Run automated red-team threat simulation suite")
    print("  sbom        - Generate Software Bill of Materials (SBOM) inventory")
    print("  harden      - Run automated system hardening & pre-flight lockdown")
    print("  release     - Generate secure release manifest bundle")
    print("  swarm       - Broadcast P2P swarm heartbeat & sync state")
    print("  server      - Launch FastAPI local security REST API server")
    print("  run         - Execute sample orchestrator pipeline request")
    print("  help        - Show this help menu\n")

def main():
    if len(sys.argv) < 2:
        print_help()
        return

    cmd = sys.argv[1].lower()

    if cmd == "chain-verify":
        cv = CryptographicChainVerifier()
        print(json.dumps(cv.verify_full_chain(), indent=2))
    elif cmd == "stress":
        st = MasterStressTest()
        print(json.dumps(st.run_stress_test(), indent=2))
    elif cmd == "export-report":
        exporter = SecurityReportExporter()
        print(json.dumps(exporter.export_master_report(), indent=2))
    elif cmd == "diagnostics":
        diag = MasterDiagnostics()
        print(json.dumps(diag.run_deep_diagnostics(), indent=2))
    elif cmd == "stream":
        streamer = TelemetryStreamer()
        print(json.dumps(streamer.stream_telemetry(), indent=2))
    elif cmd == "cert-issue":
        issuer = AttestationIssuer()
        print(json.dumps(issuer.issue_certificate(), indent=2))
    elif cmd == "deploy-check":
        dv = DeploymentVerifier()
        print(json.dumps(dv.verify_deployment_readiness(), indent=2))
    elif cmd == "snapshot":
        sm = SnapshotManager()
        print(json.dumps(sm.create_snapshot(), indent=2))
    elif cmd == "health":
        hc = MasterHealthCheck()
        print(json.dumps(hc.run_full_attestation(), indent=2))
    elif cmd == "fuzz":
        fuzzer = SecurityFuzzer()
        print(json.dumps(fuzzer.run_fuzz_test(), indent=2))
    elif cmd == "telemetry":
        render_dashboard()
    elif cmd == "verify":
        phoenix = PhoenixEngine()
        print(json.dumps(phoenix.verify_and_heal(), indent=2))
    elif cmd == "lock":
        lock = NeuralLock()
        print(json.dumps(lock.generate_attestation_token("MASTER_CLI_EXEC"), indent=2))
    elif cmd == "audit":
        auditor = ComplianceAuditor()
        print(json.dumps(auditor.generate_compliance_report(), indent=2))
    elif cmd == "simulate":
        sim = ThreatSimulator()
        sim.run_simulation()
    elif cmd == "sbom":
        gen = SBOMGenerator()
        print(json.dumps(gen.generate_sbom(), indent=2))
    elif cmd == "harden":
        hardener = SystemHardening()
        print(json.dumps(hardener.run_hardening_audit(), indent=2))
    elif cmd == "release":
        rm = ReleaseManifest()
        print(json.dumps(rm.generate_manifest(), indent=2))
    elif cmd == "swarm":
        swarm = SwarmSyncProtocol()
        print(json.dumps(swarm.broadcast_heartbeat(), indent=2))
    elif cmd == "server":
        import uvicorn
        from src.server import app
        print("\033[1;32m[+] Launching NomaanOS REST API Server on http://127.0.0.1:8000\033[0m")
        uvicorn.run(app, host="127.0.0.1", port=8000)
    elif cmd == "run":
        os_core = NomaanOSOrchestrator()
        res = os_core.process_request("Execute secure file check", ["ls"])
        print(json.dumps(res, indent=2))
    else:
        print_help()

if __name__ == "__main__":
    main()
