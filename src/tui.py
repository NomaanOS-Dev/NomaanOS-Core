from __future__ import annotations

import shutil
from typing import Any

from health_check import MasterHealthCheck
from nomaanos.ledger.engine import EvidenceLedger
from nomaanos.soc.telemetry import HostTelemetryProbe


class SovereignTUI:
    """
    NomaanOS Text-based User Interface (TUI) Dashboard.
    Renders structured ANSI console views of node operations, load indicators,
    and ledger block attestations without simulated delay loops.
    """

    def __init__(self, ledger_path: str = "config/audit_trail.jsonl") -> None:
        self.probe = HostTelemetryProbe()
        self.health = MasterHealthCheck()
        self.ledger = EvidenceLedger(storage_path=ledger_path)

    def draw_screen(self) -> dict[str, Any]:
        metrics = self.probe.collect_metrics()
        attestation = self.health.run_full_attestation()
        ledger_ok = self.ledger.verify_integrity()

        cols = shutil.get_terminal_size((80, 24)).columns
        header = "=== NOMAANOS SOVEREIGN CONSOLE INTERFACE ==="

        print(header.center(cols))
        print(
            f"[*] Node State       : {metrics.get('status')} (Linux {metrics.get('release')})"
        )
        print(f"[*] Memory Headroom  : {metrics.get('mem_available_mb')} MB Available")
        print(f"[*] Load 1m          : {metrics.get('load_1m')}")
        print(f"[*] Health Verdict   : {attestation.get('verdict')}")
        print(
            f"[*] Ledger Status    : {'SECURE' if ledger_ok else 'COMPROMISED'} ({len(self.ledger.chain)} blocks)"
        )
        print("=" * min(cols, 80))

        return {
            "status": "RENDERED",
            "metrics": metrics,
            "ledger_verified": ledger_ok,
            "blocks_count": len(self.ledger.chain),
        }


if __name__ == "__main__":
    tui = SovereignTUI()
    tui.draw_screen()
