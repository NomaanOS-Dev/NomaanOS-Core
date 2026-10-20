from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler
from typing import Any

from health_check import MasterHealthCheck
from nomaanos.ledger.engine import EvidenceLedger
from nomaanos.soc.telemetry import HostTelemetryProbe


class SovereignAPIHandler(BaseHTTPRequestHandler):
    """
    NomaanOS Sovereign HTTP API Request Handler.
    Serves live telemetry probes, ledger proofs, and subsystem attestation verdicts.
    """

    probe = HostTelemetryProbe()
    health = MasterHealthCheck()
    ledger = EvidenceLedger(storage_path="config/audit_trail.jsonl")

    def log_message(self, format: str, *args: Any) -> None:
        # Suppress stdout clutter during testing
        pass

    def do_GET(self) -> None:
        if self.path == "/health":
            self._send_json(200, self.health.run_full_attestation())
        elif self.path == "/telemetry":
            self._send_json(200, self.probe.collect_metrics())
        elif self.path == "/ledger/verify":
            valid = self.ledger.verify_integrity()
            self._send_json(200, {"valid": valid, "blocks": len(self.ledger.chain)})
        else:
            self._send_json(404, {"error": "ROUTE_NOT_FOUND", "path": self.path})

    def _send_json(self, status_code: int, data: dict[str, Any]) -> None:
        payload = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("X-Sovereign-Stack", "NomaanOS-Core/6.0")
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    from http.server import HTTPServer

    server = HTTPServer(("127.0.0.1", 8088), SovereignAPIHandler)
    print("Sovereign Node API listening on http://127.0.0.1:8088 ...")
    server.server_close()
