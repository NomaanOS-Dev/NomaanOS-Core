from __future__ import annotations

import hashlib
import json
import time
from typing import Any


class EvidenceLedger:
    def __init__(self, storage_path: str = "ledger.jsonl"):
        self.storage_path = storage_path
        self.chain: list[dict[str, Any]] = []

    def compute_hash(self, block: dict[str, Any]) -> str:
        block_copy = {k: v for k, v in block.items() if k != "current_hash"}
        serialized = json.dumps(block_copy, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def record_entry(self, artifact_name: str, payload: str) -> dict[str, Any]:
        prev_hash = self.chain[-1]["current_hash"] if self.chain else "0" * 64
        entry = {
            "index": len(self.chain) + 1,
            "timestamp": time.time(),
            "artifact": artifact_name,
            "payload_hash": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
            "previous_hash": prev_hash,
        }
        entry["current_hash"] = self.compute_hash(entry)
        self.chain.append(entry)
        return entry

    def verify_integrity(self) -> bool:
        if not self.chain:
            return True

        for i, curr in enumerate(self.chain):
            # Check recalculation of current block's hash
            expected_hash = self.compute_hash(curr)
            if curr.get("current_hash") != expected_hash:
                return False

            # Check chain link to previous block
            if i == 0:
                if curr.get("previous_hash") != "0" * 64:
                    return False
            else:
                prev = self.chain[i - 1]
                if curr.get("previous_hash") != prev.get("current_hash"):
                    return False

        return True
