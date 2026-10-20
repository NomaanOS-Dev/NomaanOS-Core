from __future__ import annotations

from typing import Any

from health_check import MasterHealthCheck
from nomaanos.ledger.engine import EvidenceLedger
from nomaanos.soc.telemetry import HostTelemetryProbe


class DeployVerifier:
    """
    NomaanOS Post-Deployment Verification & System Gatekeeper.
    Performs runtime health attestation, ledger continuity inspection,
    and host resource validation immediately following node startup.
    """

    def __init__(self, ledger_path: str = "config/audit_trail.jsonl") -> None:
        self.probe = HostTelemetryProbe()
        self.health = MasterHealthCheck()
        self.ledger = EvidenceLedger(storage_path=ledger_path)

    def verify_post_deploy_state(self) -> dict[str, Any]:
        telemetry = self.probe.collect_metrics()
        attestation = self.health.run_full_attestation()
        ledger_valid = self.ledger.verify_integrity()

        status_healthy = telemetry.get("status") in (
            "OK",
            "NOMINAL",
            "ACTIVE",
            "HEALTHY",
        )
        all_passed = (
            status_healthy and ledger_valid and attestation.get("verdict") == "HEALTHY"
        )

        return {
            "deployment_verdict": "VERIFIED_OPERATIONAL"
            if all_passed
            else "DEGRADED_STATE",
            "ledger_verified": ledger_valid,
            "subsystem_health": attestation.get("verdict"),
            "host_status": telemetry.get("status"),
            "memory_headroom_mb": telemetry.get("mem_available_mb"),
            "active_tasks": telemetry.get("active_processes"),
        }


if __name__ == "__main__":
    verifier = DeployVerifier()
    print("Post-Deploy Verification:", verifier.verify_post_deploy_state())
