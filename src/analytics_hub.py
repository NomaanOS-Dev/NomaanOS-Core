from __future__ import annotations

from typing import Any

from nomaanos.ledger.engine import EvidenceLedger
from nomaanos.soc.telemetry import HostTelemetryProbe


class AnalyticsHub:
    """
    NomaanOS Telemetry & Ledger Analytics Engine.
    Aggregates real-time host telemetry and cryptographic ledger statistics
    into actionable security operations center (SOC) metrics.
    """

    def __init__(self, ledger_path: str = "config/audit_trail.jsonl") -> None:
        self.probe = HostTelemetryProbe()
        self.ledger = EvidenceLedger(storage_path=ledger_path)

    def aggregate_metrics(self) -> dict[str, Any]:
        telemetry = self.probe.collect_metrics()
        chain = self.ledger.chain

        total_blocks = len(chain)
        artifacts_count: dict[str, int] = {}
        for block in chain:
            art = block.get("artifact", "unknown")
            artifacts_count[art] = artifacts_count.get(art, 0) + 1

        mem_total = telemetry.get("mem_total_mb", 1)
        mem_avail = telemetry.get("mem_available_mb", 0)
        mem_used_pct = (
            round(((mem_total - mem_avail) / mem_total) * 100, 2) if mem_total else 0.0
        )

        return {
            "status": "OPERATIONAL",
            "memory_utilization_pct": mem_used_pct,
            "load_1m": telemetry.get("load_1m", 0.0),
            "active_tasks": telemetry.get("active_processes", 0),
            "ledger_blocks_indexed": total_blocks,
            "ledger_integrity": self.ledger.verify_integrity(),
            "artifact_distribution": artifacts_count,
        }


if __name__ == "__main__":
    hub = AnalyticsHub()
    print("Analytics Snapshot:", hub.aggregate_metrics())
