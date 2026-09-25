import sys
import time
from src.engine import NoseExec

def print_banner():
    print("\033[1;36m")
    print(r"""
  _  _                     _    ___  ____     ____          
 | \| |___ _ __  __ _ _ _ /_\  / __|/ __|   / mời \ ___ _ _ 
 | .` / _ \ '  \/ _` | ' \ _ \ \__ \\__ \  | ffff |/ -_) '_|
 |_|\_\___/_|_|_\__,_|_||_/_/ \_|___/___/   \____/ \___|_|  
    """)
    print("\033[1;32m[+] Sovereign AI Stack (SAS) - Interactive Security CLI v6.0")
    print("\033[1;33m[+] Architect: Nomaan Khan | IHFC-IITD Scholar\033[0m\n")

def main_cli():
    print_banner()
    engine = NoseExec(["echo", "uname", "ls", "cat"])
    
    print("Type system commands to test against the Fail-Closed Sentinel Engine.")
    print("Type 'exit' to quit, or 'help' for examples.\n")
    
    while True:
        try:
            cmd = input("\033[1;35mnomaanos-cli>\033[0m ").strip()
            if not cmd:
                continue
            if cmd == "exit":
                print("\033[1;31mExiting NomaanOS Shell. Stay Secure.\033[0m")
                break
            if cmd == "help":
                print("\033[1;36mExamples:\033[0m")
                print("  echo Hello NomaanOS    (Allowed)")
                print("  uname -a               (Allowed)")
                print("  rm -rf /               (Blocked by Fail-Closed Engine)")
                continue
            
            # Split command safely
            parts = cmd.split()
            print("[*] Evaluating intent through Sentinel Proxy...")
            time.sleep(0.3)
            
            result = engine.execute(parts)
            if result["status"] == "SUCCESS":
                print(f"\033[1;32m[SUCCESS] Executed safely:\033[0m {result['stdout']}")
            else:
                print(f"\033[1;31m[BLOCKED] Security Invariant Violated:\033[0m {result['reason']}")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main_cli()
