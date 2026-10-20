from __future__ import annotations

import sys

try:
    from nomaanos.engine import NoseExec
except ImportError:
    try:
        from src.engine import NoseExec
    except ImportError:
        from engine import NoseExec


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


def main_cli() -> int:
    print_banner()
    if len(sys.argv) > 1 and sys.argv[1] in ("--help", "-h"):
        print("Usage: nomaanos [COMMAND]")
        print("Fail-Closed Sentinel Engine for Sovereign AI Workloads.")
        return 0

    engine = NoseExec(["echo", "uname", "ls", "cat"])
    print("Sentinel Engine Active. Allowed binaries: echo, uname, ls, cat")
    res = engine.execute(["uname", "-s"])
    status_val = res.get("status")
    stdout_val = res.get("stdout")
    print(f"Kernel Attestation: {status_val} | stdout: {stdout_val}")
    return 0


if __name__ == "__main__":
    sys.exit(main_cli())
