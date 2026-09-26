import os
import sys
import time

BASE_DIR = os.path.expanduser("~/NomaanOS-Work")
sys.path.insert(0, os.path.join(BASE_DIR, "NomaanOS-ShieldSOC"))
sys.path.insert(0, os.path.join(BASE_DIR, "NomaanOS-EvidenceLedger"))

from host_telemetry import get_genuine_telemetry
from ledger_persistent import PersistentEvidenceLedger

def render_tui(iterations=3):
    ledger = PersistentEvidenceLedger(os.path.join(BASE_DIR, "NomaanOS-EvidenceLedger", "audit_store.jsonl"))
    
    for i in range(iterations):
        os.system("clear")
        telemetry = get_genuine_telemetry()
        valid = ledger.verify_chain()
        chain_len = len(ledger._chain)

        print("\033[1;36m====================================================================\033[0m")
        print("\033[1;32m      SOVEREIGN AI STACK (SAS) - LIVE OBSERVABILITY CONSOLE         \033[0m")
        print("\033[1;36m====================================================================\033[0m")
        print(f" Kernel Architecture : {telemetry.get('arch', 'N/A')} ({telemetry.get('os', 'N/A')})")
        print(f" Target Host         : {telemetry.get('host', 'N/A')}")
        print(f" Sensor Interface    : \033[92m{telemetry.get('sensor_source', 'N/A').upper()}\033[0m")
        print("--------------------------------------------------------------------")
        print(f" Core SoC Temperature: \033[1;33m{telemetry.get('temperature_celsius', 'N/A')} °C\033[0m")
        print(f" System Load (1m)    : {telemetry.get('load_1m', 'N/A')}")
        print("--------------------------------------------------------------------")
        print(f" Audit Chain Length  : \033[1;34m{chain_len} blocks\033[0m")
        chain_badge = "\033[92mVERIFIED INTEGRITY [PASS]\033[0m" if valid else "\033[91mCORRUPTED [FAIL]\033[0m"
        print(f" Tamper Verification : {chain_badge}")
        print("\033[1;36m====================================================================\033[0m")
        print(f" Telemetry Tick      : {i + 1}/{iterations} | Refreshing every 1.5s...")
        if i < iterations - 1:
            time.sleep(1.5)

if __name__ == "__main__":
    render_tui(3)
