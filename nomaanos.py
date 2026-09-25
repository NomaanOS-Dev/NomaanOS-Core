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
from src.badge_generator import SecurityBadgeGenerator
from src.tui import SecurityTUI
from src.benchmark import MasterBenchmark
from src.bootstrapper import MasterBootstrapper
from src.health_inspector import MasterHealthInspector
from src.packager import ReleasePackager
from src.webhook_hub import MasterWebhookHub
from src.log_rotator import MasterLogRotator
from src.deployment_shield import DeploymentShield
from src.summary_exporter import MasterSummaryExporter
from src.master_verifier import MasterCodeVerifier
from src.master_seal import MasterProductionSeal

def print_help():
    render_banner()
    print("\033[1;36m" + "="*60)
    print("      NOMAANOS SOVEREIGN AI STACK - MASTER CLI REFERENCE")
    print("="*60 + "\033[0m")
    print("Usage: python nomaanos.py [command]\n")
    print("Available Commands:")
    print("  seal        - Apply master production cryptographic sign-off seal")
    print("  verify-repo - Run master repository code & syntax integrity verifier")
    print("  summary     - Export master sovereign stack telemetry summary report")
    print("  shield      - Run automated production deployment integrity shield")
    print("  rotate      - Rotate and archive master audit logs & telemetry")
    print("  webhook     - Broadcast real-time security alert webhook to SOC sink")
    print("  package     - Package entire core ecosystem into release ZIP archive")
    print("  inspect     - Run deep master health & runtime enclave inspection")
    print("  boot        - Run master boot sequence & subsystem initialization")
    print("  benchmark   - Run full-stack master security & integration benchmark")
    print("  tui         - Launch interactive terminal user interface (TUI) dashboard")
    print("  badges      - Generate professional SVG security shield badges")
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

    if cmd == "seal":
        seal = MasterProductionSeal()
        print(json.dumps(seal.apply_seal(), indent=2))
    elif cmd == "verify-repo":
        verifier = MasterCodeVerifier()
        print(json.dumps(verifier.verify_all_modules(), indent=2))
    elif cmd == "summary":
        exporter = MasterSummaryExporter()
        print(json.dumps(exporter.export_summary(), indent=2))
    elif cmd == "shield":
        shield = DeploymentShield()
        print(json.dumps(shield.verify_shield(), indent=2))
    elif cmd == "rotate":
        rotator = MasterLogRotator()
        print(json.dumps(rotator.rotate_logs(), indent=2))
    elif cmd == "webhook":
        hub = MasterWebhookHub()
        print(json.dumps(hub.dispatch_alert(), indent=2))
    elif cmd == "package":
        pkg = ReleasePackager()
        print(json.dumps(pkg.package_release(), indent=2))
    elif cmd == "inspect":
        inspector = MasterHealthInspector()
        print(json.dumps(inspector.inspect_health(), indent=2))
    elif cmd == "boot":
        boot = MasterBootstrapper()
        print(json.dumps(boot.boot_sequence(), indent=2))
    elif cmd == "benchmark":
        bm = MasterBenchmark()
        print(json.dumps(bm.run_master_benchmark(), indent=2))
    elif cmd == "tui":
        tui = SecurityTUI()
        tui.render_tui()
    elif cmd == "badges":
        bg = SecurityBadgeGenerator()
        print(json.dumps(bg.generate_badges(), indent=2))
    elif cmd == "chain-verify":
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
