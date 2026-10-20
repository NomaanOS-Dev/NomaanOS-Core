from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any


class SnapshotManager:
    """
    NomaanOS Cryptographic Snapshot & State Backup Manager.
    Archives enclave configs, audit logs, and system manifests with
    block-level hash verification and rollback restoration capabilities.
    """

    def __init__(self, backup_dir: str = "config/snapshots") -> None:
        self.backup_path = Path(backup_dir)
        self.backup_path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _hash_file(file_path: Path) -> str:
        if not file_path.is_file():
            return ""
        return hashlib.sha256(file_path.read_bytes()).hexdigest()

    def create_snapshot(self, targets: list[str] | None = None) -> dict[str, Any]:
        timestamp = time.time()
        snap_id = f"SNAP-{int(timestamp)}"
        snapshot_file = self.backup_path / f"snapshot_{int(timestamp)}.json"

        target_paths = [
            Path(p)
            for p in (
                targets
                or [
                    "config/audit_trail.json",
                    "config/audit_trail.jsonl",
                    "config/sbom.json",
                ]
            )
        ]

        bundled_files: dict[str, dict[str, Any]] = {}
        for path in target_paths:
            if path.is_file():
                content = path.read_text(encoding="utf-8")
                bundled_files[str(path)] = {
                    "sha256": self._hash_file(path),
                    "size_bytes": path.stat().st_size,
                    "content": content,
                }

        manifest = {
            "snapshot_id": snap_id,
            "timestamp": timestamp,
            "file_count": len(bundled_files),
            "files": bundled_files,
        }

        # Calculate root bundle hash over all serialized state
        manifest_raw = json.dumps(manifest, sort_keys=True).encode("utf-8")
        manifest["bundle_hash"] = hashlib.sha256(manifest_raw).hexdigest()

        snapshot_file.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        return manifest

    def restore_snapshot(self, snapshot_id: str) -> bool:
        target_file = None
        for snap_file in self.backup_path.glob("snapshot_*.json"):
            try:
                data = json.loads(snap_file.read_text(encoding="utf-8"))
                if data.get("snapshot_id") == snapshot_id:
                    target_file = snap_file
                    break
            except (json.JSONDecodeError, OSError):
                continue

        if not target_file:
            return False

        try:
            bundle = json.loads(target_file.read_text(encoding="utf-8"))
            files = bundle.get("files", {})

            for file_path_str, file_meta in files.items():
                dest = Path(file_path_str)
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(file_meta["content"], encoding="utf-8")

                if self._hash_file(dest) != file_meta["sha256"]:
                    return False

            return True
        except (json.JSONDecodeError, OSError):
            return False


if __name__ == "__main__":
    manager = SnapshotManager()
    snap = manager.create_snapshot()
    print("Snapshot Created:", snap["snapshot_id"], "Hash:", snap["bundle_hash"])
