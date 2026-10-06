import os
import platform
import time

class HostTelemetryProbe:
    def __init__(self):
        self.host_info = {
            "system": platform.system(),
            "machine": platform.machine(),
            "release": platform.release()
        }

    def collect_metrics(self):
        metrics = dict(self.host_info)
        metrics["timestamp"] = time.time()
        metrics["status"] = "HEALTHY"
        return metrics
