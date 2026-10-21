from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any


class ReleaseNotesGenerator:
    """
    NomaanOS Dynamic Release Notes & Changelog Generator.
    Extracts recent git commit logs, parses conventional commit conventions,
    and publishes structured Markdown release manifests.
    """

    def __init__(self, output_file: str = "docs/RELEASE_NOTES.md") -> None:
        self.output_path = Path(output_file)

    def extract_recent_commits(self, count: int = 20) -> list[str]:
        try:
            res = subprocess.run(
                ["git", "log", f"-n{count}", "--oneline"],
                capture_output=True,
                text=True,
                check=False,
                timeout=5.0,
            )
            return [line.strip() for line in res.stdout.splitlines() if line.strip()]
        except (subprocess.SubprocessError, OSError):
            return ["HEAD Initial sovereign commit"]

    def generate_release_notes(self, version: str = "v6.0.0") -> dict[str, Any]:
        commits = self.extract_recent_commits(25)

        features: list[str] = []
        fixes: list[str] = []
        other: list[str] = []

        for c in commits:
            msg = c.split(" ", 1)[1] if " " in c else c
            if msg.startswith("feat"):
                features.append(msg)
            elif msg.startswith("fix"):
                fixes.append(msg)
            else:
                other.append(msg)

        content = f"""# NomaanOS Sovereign Core Release Notes - {version}

## Features & Hardening
{chr(10).join(f"- {f}" for f in features) if features else "- No new features in this cut."}

## Bug Fixes & Stability
{chr(10).join(f"- {f}" for f in fixes) if fixes else "- No specific bug fixes."}

## Infrastructure & Maintenance
{chr(10).join(f"- {o}" for o in other[:5]) if other else "- Up to date."}
"""

        try:
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            self.output_path.write_text(content, encoding="utf-8")
        except OSError:
            pass

        return {
            "version": version,
            "total_commits_audited": len(commits),
            "features_count": len(features),
            "fixes_count": len(fixes),
            "output_path": str(self.output_path),
        }


if __name__ == "__main__":
    generator = ReleaseNotesGenerator()
    print("Release Notes:", generator.generate_release_notes())
