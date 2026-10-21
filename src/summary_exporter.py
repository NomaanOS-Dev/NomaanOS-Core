from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from health_check import MasterHealthCheck
from nomaanos.ledger.engine import EvidenceLedger
from nomaanos.soc.telemetry import HostTelemetryProbe


class SecuritySummaryExporter:
    """
    NomaanOS Executive Security & Health Summary Exporter.
    Compiles real-time ledger attestations, telemetry baselines, and health verdicts
    into structured JSON and executive Markdown audit reports.
    """

    def __init__(
        self,
        ledger_path: str = "config/audit_trail.jsonl",
        output_dir: str = "docs/reports",
    ) -> None:
        self.probe = HostTelemetryProbe()
        self.health = MasterHealthCheck()
        self.ledger = EvidenceLedger(storage_path=ledger_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_summary(self) -> dict[str, Any]:
        metrics = self.probe.collect_metrics()
        attestation = self.health.run_full_attestation()
        ledger_ok = self.ledger.verify_integrity()

        summary_data = {
            "report_type": "EXECUTIVE_SECURITY_SUMMARY",
            "host_status": metrics.get("status"),
            "kernel_release": metrics.get("release"),
            "memory_available_mb": metrics.get("mem_available_mb"),
            "subsystem_verdict": attestation.get("verdict"),
            "ledger_verified": ledger_ok,
            "total_ledger_blocks": len(self.ledger.chain),
        }

        # Export JSON
        json_path = self.output_dir / "security_summary.json"
        json_path.write_text(json.dumps(summary_data, indent=2), encoding="utf-8")

        # Export Markdown
        md_content = f"""# NomaanOS Executive Security Summary

- **Subsystem Health:** `{summary_data["subsystem_verdict"]}`
- **Ledger Status:** `{"VERIFIED_INTEACT" if ledger_ok else "COMPROMISED"}`
- **Total Ledger Blocks:** `{summary_data["total_ledger_blocks"]}`
- **Host State:** `{summary_data["host_status"]}` ({summary_data["kernel_release"]})
- **Available Memory:** `{summary_data["memory_available_mb"]} MB`
"""
        md_path = self.output_dir / "security_summary.md"
        md_path.write_text(md_content, encoding="utf-8")

        return {
            "status": "SUMMARY_EXPORTED",
            "json_report": str(json_path),
            "markdown_report": str(md_path),
            "summary": summary_data,
        }


if __name__ == "__main__":
    exporter = SecuritySummaryExporter()
    print("Summary Export:", exporter.export_summary())
