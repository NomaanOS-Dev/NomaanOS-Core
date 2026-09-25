import sys
import json
from src.orchestrator import NomaanOSOrchestrator
from src.telemetry_dashboard import render_dashboard
from src.phoenix_engine import PhoenixEngine
from src.neural_lock import NeuralLock
from src.compliance_auditor import ComplianceAuditor
from src.threat_simulator import ThreatSimulator

def print_help():
    print("\033[1;36m" + "="*50)
    print("      NOMAANOS SOVEREIGN AI STACK - MASTER CLI")
    print("="*50 + "\033[0m")
    print("Usage: python nomaanos.py [command]\n")
    print("Available Commands:")
    print("  telemetry   - Render real-time SOC security telemetry dashboard")
    print("  verify      - Run Phoenix auto-remediation & integrity check")
    print("  lock        - Generate L5 Neural Lock attestation token")
    print("  audit       - Generate automated compliance & security report")
    print("  simulate    - Run automated red-team threat simulation suite")
    print("  run         - Execute sample orchestrator pipeline request")
    print("  help        - Show this help menu\n")

def main():
    if len(sys.argv) < 2:
        print_help()
        return

    cmd = sys.argv[1].lower()

    if cmd == "telemetry":
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
    elif cmd == "run":
        os_core = NomaanOSOrchestrator()
        res = os_core.process_request("Execute secure file check", ["ls"])
        print(json.dumps(res, indent=2))
    else:
        print_help()

if __name__ == "__main__":
    main()
