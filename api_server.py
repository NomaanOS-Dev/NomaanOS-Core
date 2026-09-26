import json
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

# Module directory paths
BASE_DIR = os.path.expanduser("~/NomaanOS-Work")
sys.path.insert(0, os.path.join(BASE_DIR, "NomaanOS-ShieldSOC"))
sys.path.insert(0, os.path.join(BASE_DIR, "NomaanOS-GhostNode"))
sys.path.insert(0, os.path.join(BASE_DIR, "NomaanOS-EvidenceLedger"))

# Dynamic robust imports
try:
    from host_telemetry import get_genuine_telemetry
except ImportError:
    get_genuine_telemetry = lambda: {"status": "telemetry_module_offline"}

try:
    from ledger_persistent import PersistentEvidenceLedger
except ImportError:
    from ledger import EvidenceLedger as PersistentEvidenceLedger

class SASApiHandler(BaseHTTPRequestHandler):
    ledger = PersistentEvidenceLedger(os.path.join(BASE_DIR, "NomaanOS-EvidenceLedger", "audit_store.jsonl"))

    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("X-Security-Standard", "Sovereign-AI-Stack-v1")
        self.end_headers()

    def do_GET(self):
        if self.path == "/health":
            self._set_headers(200)
            res = {
                "status": "HEALTHY",
                "kernel": "Sovereign AI Stack (SAS) v6.0",
                "verified": True
            }
            self.wfile.write(json.dumps(res, indent=2).encode("utf-8"))

        elif self.path == "/telemetry":
            self._set_headers(200)
            data = get_genuine_telemetry()
            self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

        elif self.path == "/audit/verify":
            self._set_headers(200)
            valid = self.ledger.verify_chain()
            res = {
                "chain_length": len(self.ledger._chain),
                "tamper_proof_valid": valid
            }
            self.wfile.write(json.dumps(res, indent=2).encode("utf-8"))

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))

    def log_message(self, format, *args):
        sys.stderr.write(f"[SAS-API] {self.address_string()} - {args[0]} {args[1]}\n")

def run(port=8080):
    server = HTTPServer(("127.0.0.1", port), SASApiHandler)
    server.serve_forever()

if __name__ == "__main__":
    run()
