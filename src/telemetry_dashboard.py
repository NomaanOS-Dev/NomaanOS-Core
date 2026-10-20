from __future__ import annotations

from typing import Any

from hardware_bridge import HardwareEnclaveBridge
from nomaanos.soc.telemetry import HostTelemetryProbe


class TelemetryDashboard:
    """
    NomaanOS Real-Time SOC Telemetry & Hardware Console Dashboard.
    Combines live /proc kernel metrics and hardware capability audits.
    """

    def __init__(self) -> None:
        self.probe = HostTelemetryProbe()
        self.hw_bridge = HardwareEnclaveBridge()

    def generate_dashboard_view(self) -> dict[str, Any]:
        host_metrics = self.probe.collect_metrics()
        hw_metrics = self.hw_bridge.inspect_enclave_hardware()

        return {
            "status": "ACTIVE",
            "host_state": host_metrics.get("status"),
            "load_1m": host_metrics.get("load_1m"),
            "mem_available_mb": host_metrics.get("mem_available_mb"),
            "cpu_cores": hw_metrics.get("cpu_cores"),
            "security_tier": hw_metrics.get("security_tier"),
            "hardware_crypto": hw_metrics.get("hardware_crypto"),
        }


if __name__ == "__main__":
    dashboard = TelemetryDashboard()
    print("Console Telemetry View:", dashboard.generate_dashboard_view())
