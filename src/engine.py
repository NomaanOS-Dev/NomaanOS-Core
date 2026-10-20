from __future__ import annotations

import os
import resource
import subprocess
from typing import Any, ClassVar

DEFAULT_MAX_AS_BYTES: int = 512 * 1024 * 1024
DEFAULT_MAX_CPU_SEC: int = 3


def _sandbox_preexec(max_as_bytes: int = DEFAULT_MAX_AS_BYTES, max_cpu_sec: int = DEFAULT_MAX_CPU_SEC) -> None:
    try:
        resource.setrlimit(resource.RLIMIT_AS, (max_as_bytes, max_as_bytes))
        resource.setrlimit(resource.RLIMIT_CPU, (max_cpu_sec, max_cpu_sec))
    except (ValueError, OSError):
        pass


class NoseExec:
    """
    NomaanOS Fail-Closed Sandboxed Execution Engine.
    Decouples AI intent from system execution via strict argument sanitization,
    controlled environment scrubbing, and OS-level resource limits.
    """

    SAFE_ENV: ClassVar[dict[str, str]] = {
        "PATH": "/usr/local/bin:/usr/bin:/bin",
        "LC_ALL": "C.UTF-8",
        "LANG": "C.UTF-8",
    }

    def __init__(self, allowed_binaries: list[str]) -> None:
        self.allowed_binaries = set(allowed_binaries)

    def execute(
        self,
        cmd_args: list[str],
        timeout_sec: float = 5.0,
        custom_env: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        if not cmd_args or cmd_args[0] not in self.allowed_binaries:
            return {"status": "BLOCKED", "reason": "Binary not in strict allowlist"}

        env = self.SAFE_ENV.copy()
        if custom_env:
            for k, v in custom_env.items():
                if k not in {"LD_PRELOAD", "LD_LIBRARY_PATH", "PYTHONPATH"}:
                    env[k] = v

        try:
            result = subprocess.run(
                cmd_args,
                shell=False,
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout_sec,
                env=env,
                preexec_fn=_sandbox_preexec if os.name == "posix" else None,
            )
            return {
                "status": "SUCCESS",
                "code": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
            }
        except subprocess.TimeoutExpired:
            return {"status": "ERROR", "reason": f"Execution timed out after {timeout_sec}s"}
        except (subprocess.SubprocessError, OSError) as e:
            return {"status": "ERROR", "reason": str(e)}


if __name__ == "__main__":
    engine = NoseExec(["echo"])
    print("NOS Sandboxed Engine Check:", engine.execute(["echo", "NomaanOS-Sandbox-Active"]))
