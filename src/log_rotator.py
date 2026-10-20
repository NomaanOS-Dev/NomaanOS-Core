from __future__ import annotations

import gzip
import shutil
import time
from pathlib import Path
from typing import Any


class EnclaveLogRotator:
    """
    NomaanOS Production Log Rotator.
    Monitors audit and execution log files, compresses aged entries via gzip,
    enforces maximum file size caps, and maintains archive bounds.
    """

    def __init__(
        self,
        target_dir: str = "logs",
        max_bytes: int = 10 * 1024 * 1024,
        max_archives: int = 5,
    ) -> None:
        self.target_dir = Path(target_dir)
        self.target_dir.mkdir(parents=True, exist_ok=True)
        self.max_bytes = max_bytes
        self.max_archives = max_archives

    def rotate_file_if_needed(self, file_path: Path) -> dict[str, Any]:
        if not file_path.is_file():
            return {
                "file": str(file_path),
                "rotated": False,
                "reason": "FILE_NOT_FOUND",
            }

        size = file_path.stat().st_size
        if size < self.max_bytes:
            return {"file": str(file_path), "rotated": False, "size_bytes": size}

        timestamp = int(time.time())
        archive_name = f"{file_path.name}.{timestamp}.gz"
        archive_dest = self.target_dir / archive_name

        try:
            with file_path.open("rb") as f_in, gzip.open(archive_dest, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

            # Truncate original file after successful archive
            file_path.write_text("", encoding="utf-8")
            self._prune_old_archives(file_path.name)

            return {
                "file": str(file_path),
                "rotated": True,
                "archived_as": str(archive_dest),
                "original_bytes": size,
            }
        except OSError as e:
            return {"file": str(file_path), "rotated": False, "error": str(e)}

    def _prune_old_archives(self, base_name: str) -> None:
        matching = sorted(
            self.target_dir.glob(f"{base_name}.*.gz"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        for old in matching[self.max_archives :]:
            try:
                old.unlink()
            except OSError:
                pass

    def run_sweep(self) -> dict[str, Any]:
        results: list[dict[str, Any]] = []
        for f in self.target_dir.iterdir():
            if f.is_file() and not f.name.endswith(".gz"):
                results.append(self.rotate_file_if_needed(f))

        return {
            "status": "SWEEP_COMPLETE",
            "evaluated": len(results),
            "rotated_count": sum(1 for r in results if r.get("rotated")),
            "details": results,
        }


if __name__ == "__main__":
    rotator = EnclaveLogRotator()
    print("Log Rotator Sweep:", rotator.run_sweep())
