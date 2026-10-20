from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

from nomaanos.soc.telemetry import HostTelemetryProbe


class SentinelAgent:
    """
    NomaanOS Autonomous AI Sentinel Watchdog.
    Performs live kernel parameter audits, telemetry health verification,
    and process privilege boundary inspections.
    """

    def __init__(self, agent_id: str = "SENTINEL-AI-WATCHDOG-01") -> None:
        self.agent_id = agent_id
        self.probe = HostTelemetryProbe()

    def _check_ptrace_scope(self) -> dict[str, Any]:
        ptrace_path = Path("/proc/sys/kernel/yama/ptrace_scope")
        if ptrace_path.exists():
            try:
                scope = int(ptrace_path.read_text().strip())
                # scope >= 1 restricts unprivileged process tracing
                return {
                    "name": "Ptrace Scope Enforcement",
                    "passed": scope >= 1,
                    "value": scope,
                }
            except (OSError, ValueError):
                pass
        return {"name": "Ptrace Scope Enforcement", "passed": True, "value": "N/A"}

    def _check_python_binary_perms(self) -> dict[str, Any]:
        exe_path = Path(sys.executable)
        is_secure = (
            not os.access(exe_path, os.W_OK)
            or os.getuid() == 0
            or os.getuid() == exe_path.stat().st_uid
        )
        return {
            "name": "Interpreter Binary Integrity",
            "passed": is_secure,
            "path": str(exe_path),
        }

    def patrol_enclave(self) -> dict[str, Any]:
        metrics = self.probe.collect_metrics()
        ptrace_check = self._check_ptrace_scope()
        binary_check = self._check_python_binary_perms()

        checks_results = {
            "telemetry_health": metrics.get("status") == "HEALTHY",
            "memory_available": metrics.get("mem_available_mb", 0) > 128,
            "ptrace_hardened": ptrace_check["passed"],
            "interpreter_integrity": binary_check["passed"],
        }

        all_clean = all(checks_results.values())
        verdict = "ENCLAVE_BEHAVIOR_NORMAL" if all_clean else "ANOMALY_DETECTED"

        return {
            "sentinel_id": self.agent_id,
            "patrol_status": "CLEAN" if all_clean else "DEGRADED",
            "verdict": verdict,
            "checks": checks_results,
            "live_telemetry": {
                "active_processes": metrics.get("active_processes"),
                "load_1m": metrics.get("load_1m"),
            },
        }


if __name__ == "__main__":
    sentinel = SentinelAgent()
    print("Sentinel Patrol:", sentinel.patrol_enclave())
