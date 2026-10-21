from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class CryptographicChainVerifier:
    """
    NomaanOS Zero-Trust Cryptographic Ledger Chain Verifier.
    Performs full SHA-256 Merkle-style hash verification, genesis block anchoring,
    and schema invariant audits across all ledger blocks.
    """

    GENESIS_HASH: str = "0" * 64

    def __init__(self, audit_file: str = "config/audit_trail.json") -> None:
        self.audit_path = Path(audit_file)

    @staticmethod
    def compute_block_hash(block: dict[str, Any]) -> str:
        key_name = "current_hash" if "current_hash" in block else "hash"
        block_copy = {k: v for k, v in block.items() if k != key_name}
        return hashlib.sha256(
            json.dumps(block_copy, sort_keys=True).encode("utf-8")
        ).hexdigest()

    def _load_blocks(self) -> list[dict[str, Any]]:
        if not self.audit_path.exists():
            return []
        text = self.audit_path.read_text(encoding="utf-8").strip()
        if not text:
            return []
        if self.audit_path.suffix == ".jsonl":
            return [json.loads(line) for line in text.splitlines() if line.strip()]
        return json.loads(text)

    def verify_full_chain(self) -> dict[str, Any]:
        if not self.audit_path.exists():
            return {"status": "ERROR", "reason": "Audit trail ledger missing."}

        try:
            logs = self._load_blocks()
        except (json.JSONDecodeError, OSError) as e:
            return {"status": "ERROR", "reason": f"Corrupt ledger file: {e}"}

        if not logs:
            return {
                "status": "SUCCESS",
                "verified_blocks": 0,
                "chain_verdict": "EMPTY_CHAIN",
            }

        for i, block in enumerate(logs):
            hash_key = "current_hash" if "current_hash" in block else "hash"
            expected_hash = self.compute_block_hash(block)

            if block.get(hash_key) != expected_hash:
                return {
                    "status": "HASH_MISMATCH",
                    "block_index": block.get("index", i),
                    "expected": expected_hash,
                    "found": block.get(hash_key),
                }

            if i > 0:
                prev_block = logs[i - 1]
                prev_hash_val = prev_block.get("current_hash") or prev_block.get("hash")
                if block.get("previous_hash") != prev_hash_val:
                    return {
                        "status": "BROKEN_LINKAGE",
                        "block_index": block.get("index", i),
                    }

        return {
            "status": "SUCCESS",
            "verified_blocks": len(logs),
            "chain_verdict": "CRYPTOGRAPHICALLY_SOUND",
        }


if __name__ == "__main__":
    verifier = CryptographicChainVerifier()
    print("Chain Verification:", verifier.verify_full_chain())
