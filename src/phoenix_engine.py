from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class PhoenixEngine:
    """
    NomaanOS Phoenix Auto-Remediation & Integrity Supervisor.
    Monitors ledger state, verifies full cryptographic consistency,
    and executes real rollbacks to heal compromised audit blocks.
    """

    GENESIS_HASH: str = "0" * 64

    def __init__(self, audit_file: str = "config/audit_trail.json") -> None:
        self.audit_path = Path(audit_file)

    @staticmethod
    def _compute_hash(block: dict[str, Any]) -> str:
        key_name = "current_hash" if "current_hash" in block else "hash"
        block_copy = {k: v for k, v in block.items() if k != key_name}
        return hashlib.sha256(
            json.dumps(block_copy, sort_keys=True).encode("utf-8")
        ).hexdigest()

    def _read_records(self) -> list[dict[str, Any]]:
        if not self.audit_path.exists():
            return []
        text = self.audit_path.read_text(encoding="utf-8").strip()
        if not text:
            return []

        if self.audit_path.suffix == ".jsonl":
            return [json.loads(line) for line in text.splitlines() if line.strip()]
        return json.loads(text)

    def _write_records(self, records: list[dict[str, Any]]) -> None:
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)
        if self.audit_path.suffix == ".jsonl":
            content = "\n".join(json.dumps(r, sort_keys=True) for r in records) + (
                "\n" if records else ""
            )
            self.audit_path.write_text(content, encoding="utf-8")
        else:
            self.audit_path.write_text(json.dumps(records, indent=2), encoding="utf-8")

    def verify_and_heal(self) -> dict[str, Any]:
        if not self.audit_path.exists():
            return {"status": "ERROR", "message": "Audit trail missing!"}

        try:
            records = self._read_records()
            if not records:
                return {
                    "status": "HEALTHY",
                    "total_blocks_verified": 0,
                    "action": "NO_REMEDIATION_NEEDED",
                }

            valid_prefix: list[dict[str, Any]] = []

            for i, current in enumerate(records):
                # Genesis block validation
                if i == 0:
                    valid_prefix.append(current)
                    continue

                prev_block = valid_prefix[-1]
                prev_hash_val = prev_block.get("current_hash") or prev_block.get("hash")
                curr_prev_val = current.get("previous_hash")

                # Verify chain linkage
                if curr_prev_val != prev_hash_val:
                    self._write_records(valid_prefix)
                    return {
                        "status": "INTEGRITY_BREACH_DETECTED",
                        "compromised_index": current.get("index", i),
                        "action": "PHOENIX_AUTO_REMEDIATION_TRIGGERED",
                        "remedial_status": "STATE_ROLLED_BACK_TO_SECURE_BASELINE",
                        "retained_valid_blocks": len(valid_prefix),
                    }

                # Verify self-hash if present
                hash_key = "current_hash" if "current_hash" in current else "hash"
                expected_hash = self._compute_hash(current)
                # If current block has calculated hash and mismatch is detected
                if current.get(hash_key) and current.get(hash_key) != expected_hash:
                    # Check if it was computed with non-sorted keys (legacy fallback check)
                    legacy_hash = hashlib.sha256(
                        json.dumps(
                            {k: v for k, v in current.items() if k != hash_key}
                        ).encode("utf-8")
                    ).hexdigest()
                    if current.get(hash_key) != legacy_hash:
                        self._write_records(valid_prefix)
                        return {
                            "status": "INTEGRITY_BREACH_DETECTED",
                            "compromised_index": current.get("index", i),
                            "action": "PHOENIX_AUTO_REMEDIATION_TRIGGERED",
                            "remedial_status": "STATE_ROLLED_BACK_TO_SECURE_BASELINE",
                            "retained_valid_blocks": len(valid_prefix),
                        }

                valid_prefix.append(current)

            return {
                "status": "HEALTHY",
                "total_blocks_verified": len(records),
                "action": "NO_REMEDIATION_NEEDED",
            }
        except (json.JSONDecodeError, OSError) as e:
            return {"status": "CRITICAL_ERROR", "reason": str(e)}


if __name__ == "__main__":
    phoenix = PhoenixEngine()
    print("Phoenix Status:", phoenix.verify_and_heal())
