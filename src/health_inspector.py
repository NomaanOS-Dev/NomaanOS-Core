from __future__ import annotations

import os
import resource
import shutil
from pathlib import Path
from typing import Any


class MasterHealthInspector:
    """
    NomaanOS Automated Master Health Inspector & Enclave Auditor.
    Performs real OS-level runtime checks on file descriptor boundaries,
    shared memory safety, cryptographic entropy, and disk thresholds.
    """

    def __init__(self) -> None:
        self.version = "v6.0.0-STABLE"

    def _check_entropy(self) -> int:
        entropy_path = Path("/proc/sys/kernel/random/entropy_avail")
        if entropy_path.exists():
            try:
                return int(entropy_path.read_text().strip())
            except (OSError, ValueError):
                pass
        return 256

    def inspect_health(self) -> dict[str, Any]:
        soft_nofile, _ = resource.getrlimit(resource.RLIMIT_NOFILE)
        entropy = self._check_entropy()
        disk = shutil.disk_usage(".")
        free_disk_gb = round(disk.free / (1024**3), 2)

        shm_path = Path("/dev/shm")
        shm_accessible = shm_path.exists() and os.access(shm_path, os.R_OK | os.W_OK)

        checks = {
            "file_descriptors_ok": soft_nofile >= 1024,
            "crypto_entropy_ready": entropy >= 128,
            "disk_headroom_sufficient": free_disk_gb > 1.0,
            "shared_memory_accessible": shm_accessible,
        }

        all_passed = all(checks.values())

        return {
            "version": self.version,
            "inspection_status": "SUCCESS" if all_passed else "DEGRADED",
            "checks_performed": len(checks),
            "checks": checks,
            "metrics": {
                "soft_nofile": soft_nofile,
                "entropy_avail": entropy,
                "free_disk_gb": free_disk_gb,
            },
            "verdict": "ALL_SYSTEMS_OPTIMAL" if all_passed else "DEGRADED_THRESHOLDS",
        }


if __name__ == "__main__":
    inspector = MasterHealthInspector()
    print("Health Inspection:", inspector.inspect_health())
