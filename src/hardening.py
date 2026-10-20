from __future__ import annotations

import os
from pathlib import Path
from typing import Any


class SystemHardening:
    """
    NomaanOS Kernel & Host Environment Hardening Inspector.
    Directly audits Linux kernel runtime flags (ASLR, Yama ptrace, restrictive umask)
    and verifies zero-privilege non-root execution policies.
    """

    def __init__(self) -> None:
        self.va_space_path = Path("/proc/sys/kernel/randomize_va_space")
        self.yama_path = Path("/proc/sys/kernel/yama/ptrace_scope")

    def audit_kernel_hardening(self) -> dict[str, Any]:
        aslr_active = False
        if self.va_space_path.exists():
            try:
                aslr_val = self.va_space_path.read_text().strip()
                aslr_active = aslr_val in ("1", "2")
            except OSError:
                pass

        yama_active = False
        if self.yama_path.exists():
            try:
                yama_val = self.yama_path.read_text().strip()
                yama_active = yama_val in ("1", "2", "3")
            except OSError:
                pass

        current_umask = os.umask(0o077)
        os.umask(current_umask)

        is_non_root = (os.geteuid() != 0) if hasattr(os, "geteuid") else True

        checks = {
            "aslr_enabled": aslr_active,
            "yama_ptrace_hardened": yama_active,
            "restrictive_umask": current_umask in (0o027, 0o077),
            "non_root_execution": is_non_root,
        }

        score = sum(1 for v in checks.values() if v)
        compliance_level = "L5_HARDENED" if score >= 2 else "PARTIALLY_HARDENED"

        return {
            "status": "HARDENING_AUDIT_COMPLETE",
            "compliance_level": compliance_level,
            "score": f"{score}/{len(checks)}",
            "checks": checks,
        }


if __name__ == "__main__":
    hardening = SystemHardening()
    print("Hardening Report:", hardening.audit_kernel_hardening())
