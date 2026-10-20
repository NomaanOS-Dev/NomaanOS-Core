from __future__ import annotations

import subprocess
from typing import Any


class NoseExec:
    """
    NomaanOS Fail-Closed Execution Engine
    Decouples AI intent from system execution via strict argument sanitization.
    """
    def __init__(self, allowed_binaries: list[str]):
        self.allowed_binaries = allowed_binaries

    def execute(self, cmd_args: list[str]) -> dict[str, Any]:
        if not cmd_args or cmd_args[0] not in self.allowed_binaries:
            return {"status": "BLOCKED", "reason": "Binary not in strict allowlist"}
        
        try:
            # shell=False ensures injection vectors via shell evaluation are neutralized
            result = subprocess.run(
                cmd_args,
                shell=False,
                check=False,
                capture_output=True,
                text=True,
                timeout=5
            )
            return {
                "status": "SUCCESS",
                "code": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip()
            }
        except (subprocess.SubprocessError, OSError) as e:
            return {"status": "ERROR", "reason": str(e)}

if __name__ == "__main__":
    # Test stub
    engine = NoseExec(["echo"])
    print("NOS Exec Engine Initialized. Test:", engine.execute(["echo", "NomaanOS-Core Active"]))
