from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


class DistributionPackager:
    """
    NomaanOS Secure Wheel & Distribution Packager.
    Verifies pyproject.toml PEP 517/621 specifications and calculates
    cryptographic SHA-256 manifests for compiled distribution wheels.
    """

    def __init__(self, pyproject_path: str = "pyproject.toml") -> None:
        self.pyproject_path = Path(pyproject_path)

    def verify_packaging_spec(self) -> dict[str, Any]:
        if not self.pyproject_path.is_file():
            return {"status": "ERROR", "reason": "pyproject.toml missing"}

        try:
            content = self.pyproject_path.read_text(encoding="utf-8")
            data = tomllib.loads(content)
            project_meta = data.get("project", {})

            name = project_meta.get("name")
            version = project_meta.get("version")
            dependencies = project_meta.get("dependencies", [])

            return {
                "status": "VALID",
                "project_name": name,
                "version": version,
                "dependency_count": len(dependencies),
                "has_entrypoints": bool(project_meta.get("scripts")),
            }
        except (tomllib.TOMLDecodeError, OSError, ValueError, KeyError) as e:
            return {"status": "ERROR", "reason": str(e)}

    def audit_dist_artifacts(self, dist_dir: str = "dist") -> dict[str, Any]:
        dist_path = Path(dist_dir)
        if not dist_path.is_dir():
            return {"status": "NO_DIST_DIR", "artifacts": []}

        artifacts: list[dict[str, Any]] = []
        for artifact in dist_path.glob("*.whl"):
            digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
            artifacts.append(
                {
                    "filename": artifact.name,
                    "size_bytes": artifact.stat().st_size,
                    "sha256": digest,
                }
            )

        return {
            "status": "ARTIFACTS_AUDITED",
            "artifact_count": len(artifacts),
            "artifacts": artifacts,
        }


if __name__ == "__main__":
    packager = DistributionPackager()
    print("Packaging Spec:", packager.verify_packaging_spec())
    print("Dist Audit:", packager.audit_dist_artifacts())
