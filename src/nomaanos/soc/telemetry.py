from __future__ import annotations

import os
import platform
import time
from pathlib import Path
from typing import Any


class HostTelemetryProbe:
    """
    Real-time SOC Host Telemetry Probe.
    Inspects live kernel metrics, load averages, memory utilization,
    and process count directly from POSIX/Linux subsystems.
    """

    def __init__(self) -> None:
        self.host_info: dict[str, str] = {
            "system": platform.system(),
            "machine": platform.machine(),
            "release": platform.release(),
        }

    def _get_mem_stats(self) -> tuple[int, int]:
        """Returns (available_mb, total_mb)."""
        mem_avail = 0
        mem_total = 0
        meminfo = Path("/proc/meminfo")
        if meminfo.exists():
            try:
                with meminfo.open() as f:
                    for line in f:
                        if line.startswith("MemTotal:"):
                            mem_total = int(line.split()[1]) // 1024
                        elif line.startswith("MemAvailable:"):
                            mem_avail = int(line.split()[1]) // 1024
            except OSError:
                pass
        return mem_avail, mem_total

    def _get_process_count(self) -> int:
        """Counts current running processes via /proc numerical entries."""
        proc_path = Path("/proc")
        if proc_path.exists():
            try:
                return sum(1 for p in proc_path.iterdir() if p.name.isdigit())
            except OSError:
                pass
        return 0

    def collect_metrics(self) -> dict[str, Any]:
        metrics: dict[str, Any] = dict(self.host_info)
        metrics["timestamp"] = time.time()

        mem_avail, mem_total = self._get_mem_stats()
        metrics["mem_available_mb"] = mem_avail
        metrics["mem_total_mb"] = mem_total
        metrics["active_processes"] = self._get_process_count()

        if hasattr(os, "getloadavg"):
            load1, load5, _ = os.getloadavg()
            metrics["load_1m"] = round(load1, 2)
            metrics["load_5m"] = round(load5, 2)
        else:
            metrics["load_1m"] = 0.0
            metrics["load_5m"] = 0.0

        # Health is computed based on real pressure thresholds
        mem_critical = mem_total > 0 and (mem_avail / mem_total) < 0.05
        load_critical = metrics.get("load_1m", 0.0) > (os.cpu_count() or 1) * 4.0

        if mem_critical or load_critical:
            metrics["status"] = "DEGRADED"
        else:
            metrics["status"] = "HEALTHY"

        return metrics

    def sample_telemetry(self) -> dict[str, Any]:
        return self.collect_metrics()
