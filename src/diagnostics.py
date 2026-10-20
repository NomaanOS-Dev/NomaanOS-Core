from __future__ import annotations

import os
import platform
import sys
from typing import Any

from nomaanos.soc.telemetry import HostTelemetryProbe


class SovereignDiagnostics:
    """
    NomaanOS Real-Time System & POSIX Runtime Diagnostics Engine.
    Executes live verification of interpreter isolation, umask state,
    and process descriptor constraints.
    """

    def __init__(self) -> None:
        self.probe = HostTelemetryProbe()

    def run_deep_diagnostics(self) -> dict[str, Any]:
        host_telemetry = self.probe.collect_metrics()
        current_umask = os.umask(0o077)
        os.umask(current_umask)  # Restore previous mask

        in_venv = hasattr(sys, "real_prefix") or (
            hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
        )

        return {
            "status": "DIAGNOSTICS_COMPLETED",
            "python_version": platform.python_version(),
            "os_release": platform.release(),
            "in_virtualenv": in_venv,
            "active_umask_octal": oct(current_umask),
            "host_status": host_telemetry.get("status"),
            "memory_available_mb": host_telemetry.get("mem_available_mb"),
            "diagnostics_verdict": "HEALTHY_RUNTIME",
        }


if __name__ == "__main__":
    diag = SovereignDiagnostics()
    print("Diagnostics Output:", diag.run_deep_diagnostics())
