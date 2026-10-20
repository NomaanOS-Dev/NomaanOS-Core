from __future__ import annotations

import hashlib
import hmac
import time
from typing import Any

from neural_lock import NeuralLock
from nomaanos.ledger.engine import EvidenceLedger


class SovereignAttestationIssuer:
    """
    NomaanOS Sovereign Node Attestation Issuer.
    Issues cryptographically bound hardware context tokens and ledger head
    attestations to establish trust with external nodes.
    """

    def __init__(
        self,
        ledger_path: str = "config/audit_trail.jsonl",
        signing_key: bytes | None = None,
    ) -> None:
        self.neural_lock = NeuralLock()
        self.ledger = EvidenceLedger(storage_path=ledger_path)
        self.signing_key = signing_key or b"NOMAANOS_SOVEREIGN_NODE_KEY_DEFAULT"

    def issue_node_attestation(self, claim: str) -> dict[str, Any]:
        node_token = self.neural_lock.generate_attestation_token(claim)
        ledger_head = (
            self.ledger.chain[-1]["current_hash"] if self.ledger.chain else "0" * 64
        )

        timestamp = time.time()
        payload = f"{node_token['node_fingerprint']}:{claim}:{ledger_head}:{timestamp}"
        signature = hmac.new(
            self.signing_key, payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        return {
            "claim": claim,
            "node_fingerprint": node_token["node_fingerprint"],
            "ledger_head": ledger_head,
            "ledger_blocks": len(self.ledger.chain),
            "timestamp": timestamp,
            "attestation_signature": signature,
            "status": "ATTESTED",
        }

    def verify_attestation(self, attestation: dict[str, Any]) -> bool:
        required_fields = [
            "claim",
            "node_fingerprint",
            "ledger_head",
            "timestamp",
            "attestation_signature",
        ]
        if not all(field in attestation for field in required_fields):
            return False

        payload = (
            f"{attestation['node_fingerprint']}:{attestation['claim']}:"
            f"{attestation['ledger_head']}:{attestation['timestamp']}"
        )
        expected = hmac.new(
            self.signing_key, payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, attestation["attestation_signature"])


if __name__ == "__main__":
    issuer = SovereignAttestationIssuer()
    att = issuer.issue_node_attestation("NODE_PRIMARY_BOOT")
    print("Issued Attestation:", att)
    print("Verification:", issuer.verify_attestation(att))
