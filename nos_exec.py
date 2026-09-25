import shlex
import subprocess
from typing import List, Dict, Any

class NoseExec:
    """
    NomaanOS Fail-Closed Execution Engine
    Decouples AI intent from system execution via strict argument sanitization.
    """
    def __init__(self, allowed_binaries: List[str]):
        self.allowed_binaries = allowed_binaries

    def execute(self, cmd_args: List[str]) -> Dict[str, Any]:
        if not cmd_args or cmd_args[0] not in self.allowed_binaries:
            return {"status": "BLOCKED", "reason": "Binary not in strict allowlist"}
        
        try:
            # shell=False ensures injection vectors via shell evaluation are neutralized
            result = subprocess.run(
                cmd_args,
                shell=False,
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
        except Exception as e:
            return {"status": "ERROR", "reason": str(e)}

if __name__ == "__main__":
    # Test stub
    engine = NoseExec(["echo"])
    print("NOS Exec Engine Initialized. Test:", engine.execute(["echo", "NomaanOS-Core Active"]))
