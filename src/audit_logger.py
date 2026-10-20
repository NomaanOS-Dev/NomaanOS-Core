from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any


class AuditLogger:
    """
    NomaanOS Immutable Cryptographic Audit Logger.
    Logs structured event records linked cryptographically to the preceding block.
    """

    GENESIS_HASH: str = "0" * 64

    def __init__(self, log_path: str = "config/audit_trail.json") -> None:
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_genesis()

    def _ensure_genesis(self) -> None:
        if (
            not self.log_path.exists()
            or not self.log_path.read_text(encoding="utf-8").strip()
        ):
            genesis_record = [
                {
                    "index": 0,
                    "event": "GENESIS_BLOCK",
                    "timestamp": 1700000000.0,
                    "hash": self.GENESIS_HASH,
                }
            ]
            self.log_path.write_text(
                json.dumps(genesis_record, indent=2), encoding="utf-8"
            )
        else:
            try:
                logs = json.loads(self.log_path.read_text(encoding="utf-8"))
                if not logs:
                    self._ensure_genesis()
            except (json.JSONDecodeError, OSError):
                pass

    @staticmethod
    def compute_record_hash(record: dict[str, Any]) -> str:
        record_copy = {k: v for k, v in record.items() if k != "hash"}
        return hashlib.sha256(
            json.dumps(record_copy, sort_keys=True).encode("utf-8")
        ).hexdigest()

    def log_event(self, action: str, details: dict[str, Any]) -> str:
        try:
            logs: list[dict[str, Any]] = json.loads(
                self.log_path.read_text(encoding="utf-8")
            )
        except (json.JSONDecodeError, OSError):
            logs = []

        if not logs:
            prev_hash = self.GENESIS_HASH
            next_idx = 1
        else:
            prev_hash = (
                logs[-1].get("hash")
                or logs[-1].get("current_hash")
                or self.GENESIS_HASH
            )
            next_idx = len(logs)

        record: dict[str, Any] = {
            "index": next_idx,
            "action": action,
            "details": details,
            "timestamp": time.time(),
            "previous_hash": prev_hash,
        }
        record["hash"] = self.compute_record_hash(record)
        logs.append(record)

        self.log_path.write_text(json.dumps(logs, indent=2), encoding="utf-8")
        return record["hash"]


if __name__ == "__main__":
    logger = AuditLogger()
    print("Logged event hash:", logger.log_event("DIAGNOSTIC_PROBE", {"status": "OK"}))
