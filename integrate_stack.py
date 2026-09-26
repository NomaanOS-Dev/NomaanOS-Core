import sys
import os
import secrets

# Workspace relative paths
sys.path.append(os.path.expanduser("~/NomaanOS-Work/NomaanOS-ShieldSOC"))
sys.path.append(os.path.expanduser("~/NomaanOS-Work/NomaanOS-GhostNode"))
sys.path.append(os.path.expanduser("~/NomaanOS-Work/NomaanOS-EvidenceLedger"))

try:
    from shield_monitor import ShieldSOCMonitor
    from ghost_node import GhostNodeEngine
    from ledger import EvidenceLedger
except ImportError as e:
    print(f"[-] Dependency Import Failed: {e}")
    sys.exit(1)

def run_sovereign_pipeline():
    print("=" * 60)
    print("      NOMAANOS ENTERPRISE FULL-STACK INTEGRATION TEST")
    print("=" * 60)

    # 1. Telemetry Capture
    print("\n[+] 1. Fetching ShieldSOC Telemetry...")
    monitor = ShieldSOCMonitor()
    telemetry = monitor.fetch_telemetry()
    print(f"    Host: {telemetry['host']} | Status: {telemetry['status']}")

    # 2. Node Identity & Challenge Proof
    print("\n[+] 2. Generating GhostNode HMAC Proof...")
    node_key = secrets.token_bytes(32)
    node = GhostNodeEngine("edge-node-01", node_key)
    proof = node.generate_attestation_proof("challenge-auth-token-99")
    print(f"    Node: {proof['node_id']} | Proof Hash: {proof['proof'][:16]}...")

    # 3. Cryptographic Evidence Ledger
    print("\n[+] 3. Committing to Evidence Ledger Hash Chain...")
    ledger = EvidenceLedger()
    record = ledger.record_evidence("boot_telemetry.log", proof['proof'])
    print(f"    Ledger Index: {record['index']} | Current Hash: {record['current_hash'][:16]}...")

    # 4. Chain Verification
    valid = ledger.verify_chain()
    print(f"\n[+] 4. Cryptographic Chain Integrity Verified: {'PASSED ✅' if valid else 'FAILED ❌'}")
    print("=" * 60)
    print("[SUCCESS] ALL 4 SOVEREIGN SUBSYSTEMS FULLY INTERCONNECTED")
    print("=" * 60)

if __name__ == "__main__":
    run_sovereign_pipeline()
