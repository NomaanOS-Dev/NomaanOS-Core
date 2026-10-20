from __future__ import annotations

import shutil
from typing import Any

from health_check import MasterHealthCheck
from nomaanos.ledger.engine import EvidenceLedger
from nomaanos.soc.telemetry import HostTelemetryProbe


class MasterDashboardUI:
    """
    NomaanOS Real-Time Terminal Operational Dashboard.
    Renders live system status, memory allocation, load averages,
    and ledger block attestations without simulated sleep delays.
    """

    def __init__(self, ledger_path: str = "config/audit_trail.jsonl") -> None:
        self.probe = HostTelemetryProbe()
        self.health_check = MasterHealthCheck()
        self.ledger = EvidenceLedger(storage_path=ledger_path)

    def render_snapshot(self) -> dict[str, Any]:
        metrics = self.probe.collect_metrics()
        attestation = self.health_check.run_full_attestation()
        ledger_valid = self.ledger.verify_integrity()

        cols = shutil.get_terminal_size((80, 24)).columns
        separator = "=" * min(cols, 80)

        print(separator)
        print(" NOMAANOS LIVE SOVEREIGN DASHBOARD ".center(min(cols, 80), " "))
        print(separator)
        print(
            f"[*] Node State       : {metrics.get('status')} | Linux {metrics.get('release')}"
        )
        print(
            f"[*] Memory Headroom  : {metrics.get('mem_available_mb')} MB / {metrics.get('mem_total_mb')} MB"
        )
        print(
            f"[*] Load Average 1m  : {metrics.get('load_1m')} | Active Tasks: {metrics.get('active_processes')}"
        )
        print(f"[*] Subsystem Health : {attestation.get('verdict')}")
        print(
            f"[*] Ledger Audit     : {'VALID' if ledger_valid else 'CORRUPTED'} ({len(self.ledger.chain)} blocks)"
        )
        print(separator)

        return {
            "telemetry": metrics,
            "attestation": attestation,
            "ledger_blocks": len(self.ledger.chain),
            "ledger_valid": ledger_valid,
        }


if __name__ == "__main__":
    ui = MasterDashboardUI()
    ui.render_snapshot()
