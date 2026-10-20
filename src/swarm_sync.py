from __future__ import annotations

import hashlib
from typing import Any

from nomaanos.ledger.engine import EvidenceLedger


class SwarmNodeSync:
    """
    NomaanOS Node State Synchronization Engine.
    Generates node-level Merkle state roots across the audit ledger
    for zero-trust consensus and multi-node ledger verification.
    """

    def __init__(self, ledger_path: str = "config/audit_trail.jsonl") -> None:
        self.ledger = EvidenceLedger(storage_path=ledger_path)

    def compute_state_root(self) -> str:
        """Computes a unified root hash representing the entire node state."""
        if not self.ledger.chain:
            return "0" * 64

        concatenated_hashes = "".join(b["current_hash"] for b in self.ledger.chain)
        return hashlib.sha256(concatenated_hashes.encode("utf-8")).hexdigest()

    def verify_and_sync(self) -> dict[str, Any]:
        integrity_ok = self.ledger.verify_integrity()
        state_root = self.compute_state_root()

        return {
            "node_state": "SYNCHRONIZED" if integrity_ok else "DESYNCHRONIZED_TAMPERED",
            "chain_length": len(self.ledger.chain),
            "state_root": state_root,
            "integrity_verified": integrity_ok,
        }


if __name__ == "__main__":
    node = SwarmNodeSync()
    print("Swarm Sync State:", node.verify_and_sync())
