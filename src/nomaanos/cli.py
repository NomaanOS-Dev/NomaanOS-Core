from __future__ import annotations

import sys


def print_banner() -> None:
    print("\033[1;36m")
    print(r"""
 _  _                     _    ___  ____     ____          
| \| |___ _ __  __ _ _ _ /_\  / __|/ __|   /  _  \ ___ _ _ 
| .` / _ \ ' \/ _` | ' \ _ \ \__ \\__ \  | (_) |/ -_) '|
|_|\_\___/_|_|_\__,_|_||_/_/ \_|___/___/   \____/ \___|_|  
    """)
    print("\033[1;32m[+] Sovereign AI Stack (SAS) - Interactive Security CLI v6.0")
    print("\033[1;33m[+] Architect: Nomaan Khan | IHFC-IITD Scholar\033[0m\n")


def print_help() -> None:
    print("Usage: nomaanos [COMMAND]")
    print("\nAvailable Commands:")
    print("  status    Display live telemetry counters and node health")
    print("  verify    Validate cryptographic Evidence Ledger audit chain")
    print("  test-exec Execute fail-closed sandbox probe via NoseExec")
    print("  --help    Show this help message\n")


def main_cli() -> int:
    print_banner()
    args = sys.argv[1:]

    if not args or args[0] in ("--help", "-h"):
        print_help()
        return 0

    cmd = args[0].lower()

    if cmd == "status":
        from nomaanos.soc.telemetry import HostTelemetryProbe
        probe = HostTelemetryProbe()
        metrics = probe.sample_telemetry() if hasattr(probe, "sample_telemetry") else probe.collect_metrics()
        print("[+] Sovereign SOC Host Telemetry:")
        for k, v in metrics.items():
            print(f"    - {k}: {v}")
        return 0

    if cmd == "verify":
        from nomaanos.ledger.engine import EvidenceLedger
        ledger = EvidenceLedger()
        status = ledger.verify_integrity()
        chain_label = "VALID" if status else "COMPROMISED"
        print(f"[+] Audit Ledger Chain Verification: {chain_label}")
        return 0

    if cmd == "test-exec":
        from nomaanos.engine import NoseExec
        engine = NoseExec(["echo", "uname", "ls", "cat"])
        print("Sentinel Engine Active. Running sandbox probe: uname -s")
        res = engine.execute(["uname", "-s"])
        status_val = res.get("status")
        stdout_val = res.get("stdout")
        print(f"Kernel Attestation: {status_val} | stdout: {stdout_val}")
        return 0

    print(f"[-] Unknown command: {cmd}")
    print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main_cli())
