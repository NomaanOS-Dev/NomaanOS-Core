from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nomaanos.ledger.engine import EvidenceLedger
from nomaanos.soc.telemetry import HostTelemetryProbe
from sbom_generator import SBOMGenerator


class SecurityReportExporter:
    """
    NomaanOS Automated Security & Compliance Report Exporter.
    Compiles live SBOM inventories, telemetry, and ledger audit chains
    into structured JSON and HTML compliance artifacts.
    """

    def __init__(
        self,
        ledger_path: str = "config/audit_trail.jsonl",
        output_dir: str = "docs/reports",
    ) -> None:
        self.probe = HostTelemetryProbe()
        self.sbom_gen = SBOMGenerator()
        self.ledger = EvidenceLedger(storage_path=ledger_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_full_compliance_report(self) -> dict[str, Any]:
        metrics = self.probe.collect_metrics()
        # Call generate_sbom() or fallback gracefully
        if hasattr(self.sbom_gen, "generate_sbom"):
            sbom = self.sbom_gen.generate_sbom()
        elif hasattr(self.sbom_gen, "generate_cyclonedx_sbom"):
            sbom = self.sbom_gen.generate_cyclonedx_sbom()
        else:
            sbom = {"components": []}

        ledger_valid = self.ledger.verify_integrity()

        report_data = {
            "title": "NomaanOS Enterprise SOC Compliance Audit",
            "host_status": metrics.get("status"),
            "kernel_version": metrics.get("release"),
            "memory_available_mb": metrics.get("mem_available_mb"),
            "sbom_packages_audited": len(
                sbom.get("components", []) if isinstance(sbom, dict) else []
            ),
            "ledger_verified": ledger_valid,
            "ledger_blocks": len(self.ledger.chain),
        }

        # Save JSON artifact
        json_file = self.output_dir / "compliance_report.json"
        json_file.write_text(json.dumps(report_data, indent=2), encoding="utf-8")

        # Save HTML artifact
        html_content = f"""<!DOCTYPE html>
<html>
<head><title>{report_data["title"]}</title></head>
<body>
  <h1>{report_data["title"]}</h1>
  <p><strong>Host:</strong> {report_data["host_status"]} ({report_data["kernel_version"]})</p>
  <p><strong>Packages:</strong> {report_data["sbom_packages_audited"]}</p>
  <p><strong>Ledger Verified:</strong> {report_data["ledger_verified"]}</p>
  <p><strong>Total Blocks:</strong> {report_data["ledger_blocks"]}</p>
</body>
</html>"""
        html_file = self.output_dir / "compliance_report.html"
        html_file.write_text(html_content, encoding="utf-8")

        return {
            "status": "REPORTS_GENERATED",
            "json_path": str(json_file),
            "html_path": str(html_file),
            "summary": report_data,
        }


if __name__ == "__main__":
    exporter = SecurityReportExporter()
    print("Export Status:", exporter.export_full_compliance_report())
