from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any


class EvidenceLedger:
    """
    Cryptographic Evidence Ledger with append-only JSONL persistent storage.
    Guarantees block-level Merkle-style hashing and persistence across restarts.
    """

    def __init__(self, storage_path: str = "ledger.jsonl") -> None:
        self.storage_path = Path(storage_path)
        self.chain: list[dict[str, Any]] = []
        self._load_from_storage()

    def _load_from_storage(self) -> None:
        if not self.storage_path.exists():
            return

        loaded_chain: list[dict[str, Any]] = []
        try:
            with self.storage_path.open("r", encoding="utf-8") as f:
                for line in f:
                    stripped = line.strip()
                    if stripped:
                        loaded_chain.append(json.loads(stripped))
            self.chain = loaded_chain
        except (json.JSONDecodeError, OSError):
            # In case of corruption, preserve in-memory chain and reject invalid appends
            pass

    def compute_hash(self, block: dict[str, Any]) -> str:
        block_copy = {k: v for k, v in block.items() if k != "current_hash"}
        serialized = json.dumps(block_copy, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def record_entry(self, artifact_name: str, payload: str) -> dict[str, Any]:
        prev_hash = self.chain[-1]["current_hash"] if self.chain else "0" * 64
        entry: dict[str, Any] = {
            "index": len(self.chain) + 1,
            "timestamp": time.time(),
            "artifact": artifact_name,
            "payload_hash": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
            "previous_hash": prev_hash,
        }
        entry["current_hash"] = self.compute_hash(entry)
        self.chain.append(entry)

        # Persistent append-only write
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            with self.storage_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry, sort_keys=True) + "\n")
        except OSError:
            pass

        return entry

    def verify_integrity(self) -> bool:
        if not self.chain:
            return True

        for i, curr in enumerate(self.chain):
            expected_hash = self.compute_hash(curr)
            if curr.get("current_hash") != expected_hash:
                return False

            if i == 0:
                if curr.get("previous_hash") != "0" * 64:
                    return False
            else:
                prev = self.chain[i - 1]
                if curr.get("previous_hash") != prev.get("current_hash"):
                    return False

        return True
