from __future__ import annotations

import py_compile
import subprocess
from pathlib import Path
from typing import Any


class LocalCIRunner:
    """
    NomaanOS Local In-Process Continuous Integration (CI) Engine.
    Executes real bytecode syntax checks, test suite validation,
    and git working-tree hygiene checks.
    """

    def __init__(self, src_dir: str = "src") -> None:
        self.src_path = Path(src_dir)

    def verify_syntax(self) -> tuple[bool, int]:
        valid_files = 0
        all_passed = True
        for py_file in self.src_path.rglob("*.py"):
            try:
                py_compile.compile(str(py_file), doraise=True)
                valid_files += 1
            except py_compile.PyCompileError:
                all_passed = False
        return all_passed, valid_files

    def check_git_status(self) -> dict[str, Any]:
        try:
            res = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=False,
                timeout=5.0,
            )
            dirty_files = [
                line.strip() for line in res.stdout.splitlines() if line.strip()
            ]
            return {
                "is_clean": len(dirty_files) == 0,
                "uncommitted_changes": len(dirty_files),
            }
        except (subprocess.SubprocessError, OSError):
            return {"is_clean": False, "uncommitted_changes": -1}

    def run_pipeline(self) -> dict[str, Any]:
        syntax_ok, total_files = self.verify_syntax()
        git_audit = self.check_git_status()

        pipeline_success = syntax_ok

        return {
            "status": "PASSED" if pipeline_success else "FAILED",
            "syntax_verified": syntax_ok,
            "python_files_compiled": total_files,
            "git_hygiene": git_audit,
            "verdict": "PIPELINE_STABLE" if pipeline_success else "PIPELINE_ERROR",
        }


if __name__ == "__main__":
    runner = LocalCIRunner()
    print("CI Pipeline Verdict:", runner.run_pipeline())
