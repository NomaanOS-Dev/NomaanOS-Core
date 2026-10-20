from __future__ import annotations

import os
from pathlib import Path
from typing import Any


class HardwareEnclaveBridge:
    """
    NomaanOS Hardware Enclave & Hardware Crypto Interface.
    Directly inspects Linux sysfs and /proc/cpuinfo for hardware-accelerated
    cryptographic extensions (AES-NI, SHA-NI) and DMI chassis identifiers.
    """

    def __init__(self) -> None:
        self.dmi_path = Path("/sys/class/dmi/id")
        self.cpuinfo_path = Path("/proc/cpuinfo")

    def _probe_cpu_flags(self) -> set[str]:
        flags: set[str] = set()
        if not self.cpuinfo_path.exists():
            return flags

        try:
            for line in self.cpuinfo_path.read_text(encoding="utf-8").splitlines():
                if line.startswith(("flags", "Features")):
                    parts = line.split(":", 1)
                    if len(parts) == 2:
                        flags.update(parts[1].strip().split())
                    break
        except OSError:
            pass
        return flags

    def inspect_enclave_hardware(self) -> dict[str, Any]:
        cpu_flags = self._probe_cpu_flags()
        aes_ni = "aes" in cpu_flags or "aes-ni" in cpu_flags
        sha_extensions = bool({"sha_ni", "sha1", "sha2"} & cpu_flags)

        product_name = "KVM/Generic VM"
        vendor = "Linux Platform"

        prod_file = self.dmi_path / "product_name"
        vendor_file = self.dmi_path / "sys_vendor"

        if prod_file.exists():
            try:
                product_name = prod_file.read_text(encoding="utf-8").strip()
            except OSError:
                pass

        if vendor_file.exists():
            try:
                vendor = vendor_file.read_text(encoding="utf-8").strip()
            except OSError:
                pass

        return {
            "status": "HARDWARE_AUDIT_COMPLETE",
            "cpu_cores": os.cpu_count() or 1,
            "vendor": vendor,
            "product_name": product_name,
            "hardware_crypto": {
                "aes_ni_present": aes_ni,
                "sha_ni_present": sha_extensions,
            },
            "security_tier": "HARDWARE_ACCELERATED"
            if (aes_ni or sha_extensions)
            else "SOFTWARE_FALLBACK",
        }


if __name__ == "__main__":
    bridge = HardwareEnclaveBridge()
    print("Hardware Enclave Status:", bridge.inspect_enclave_hardware())
