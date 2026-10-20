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
    GENESIS_KEYS: frozenset[str] = frozenset({"index", "event", "timestamp", "hash"})
    STANDARD_KEYS: frozenset[str] = frozenset({"index", "action", "details", "timestamp", "previous_hash", "hash"})

    def __init__(self, audit_file: str = "config/audit_trail.json") -> None:
        self.audit_path = Path(audit_file)

    @staticmethod
    def compute_block_hash(block: dict[str, Any]) -> str:
        block_copy = {k: v for k, v in block.items() if k != "hash"}
        return hashlib.sha256(json.dumps(block_copy, sort_keys=True).encode()).hexdigest()

    def verify_full_chain(self) -> dict[str, Any]:
        if not self.audit_path.exists():
            return {"status": "ERROR", "reason": "Audit trail ledger missing."}

        try:
            logs: list[dict[str, Any]] = json.loads(self.audit_path.read_text())
        except (json.JSONDecodeError, OSError) as e:
            return {"status": "ERROR", "reason": f"Corrupt ledger file: {e}"}

        if not logs:
            return {"status": "SUCCESS", "verified_blocks": 0, "chain_verdict": "EMPTY_CHAIN"}

        # 1. Genesis Block Validation
        genesis = logs[0]
        if not self.GENESIS_KEYS.issubset(genesis.keys()):
            return {"status": "SCHEMA_VIOLATION_AT_BLOCK", "block_index": 0}

        if genesis.get("hash") != self.GENESIS_HASH:
            return {"status": "INVALID_GENESIS_HASH", "block_index": 0}

        # 2. Sequential Chain Validation
        valid_blocks = 1
        leaf_hashes: list[str] = [genesis["hash"]]

        for i in range(1, len(logs)):
            current = logs[i]
            previous = logs[i - 1]

            if not self.STANDARD_KEYS.issubset(current.keys()):
                return {"status": "SCHEMA_VIOLATION_AT_BLOCK", "block_index": current.get("index", i)}

            if current.get("previous_hash") != previous.get("hash"):
                return {"status": "CHAIN_BROKEN_AT_BLOCK", "block_index": current.get("index", i)}

            if current.get("hash") != self.compute_block_hash(current):
                return {"status": "HASH_MISMATCH_DETECTED", "block_index": current.get("index", i)}

            leaf_hashes.append(current["hash"])
            valid_blocks += 1

        # 3. Merkle Aggregation
        merkle_root = hashlib.sha256("".join(leaf_hashes).encode()).hexdigest()

        return {
            "status": "SUCCESS",
            "verified_blocks": valid_blocks,
            "merkle_root": merkle_root,
            "chain_verdict": "LEDGER_CRYPTOGRAPHIC_CHAIN_100_PERCENT_VALID",
        }


if __name__ == "__main__":
    cv = CryptographicChainVerifier()
    res = cv.verify_full_chain()
    print("Chain Verification Result:", res)
