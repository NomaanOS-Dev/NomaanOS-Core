from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Any

from nomaanos.ledger.engine import EvidenceLedger


class WebhookHub:
    """
    NomaanOS Zero-Trust Webhook Ingestion Engine.
    Verifies cryptographic signatures on inbound webhook events and commits
    authenticated payloads directly to the append-only ledger.
    """

    def __init__(
        self,
        shared_secret: bytes = b"NOMAANOS_WEBHOOK_SECRET_DEFAULT",
        ledger_path: str = "config/audit_trail.jsonl",
    ) -> None:
        self.secret = shared_secret
        self.ledger = EvidenceLedger(storage_path=ledger_path)

    def generate_signature(self, payload: dict[str, Any], timestamp: float) -> str:
        serialized = json.dumps(payload, sort_keys=True)
        message = f"{timestamp}:{serialized}".encode()
        return hmac.new(self.secret, message, hashlib.sha256).hexdigest()

    def process_incoming_webhook(
        self,
        payload: dict[str, Any],
        signature: str,
        timestamp: float,
        max_clock_skew_sec: float = 300.0,
    ) -> dict[str, Any]:
        # 1. Anti-replay clock skew check
        current_time = time.time()
        if abs(current_time - timestamp) > max_clock_skew_sec:
            return {"status": "REJECTED", "reason": "TIMESTAMP_EXPIRED_REPLAY_ATTEMPT"}

        # 2. Cryptographic signature check
        expected_sig = self.generate_signature(payload, timestamp)
        if not hmac.compare_digest(expected_sig, signature):
            return {"status": "REJECTED", "reason": "INVALID_SIGNATURE"}

        # 3. Commit authenticated payload to ledger
        event_type = payload.get("event", "generic_webhook")
        self.ledger.record_entry("webhook_hub", f"{event_type}:{signature[:16]}")

        return {
            "status": "ACCEPTED",
            "event": event_type,
            "ledger_verified": self.ledger.verify_integrity(),
            "ledger_blocks": len(self.ledger.chain),
        }


if __name__ == "__main__":
    hub = WebhookHub()
    ts = time.time()
    data = {"event": "node_joined", "node_id": "enclave_alpha"}
    sig = hub.generate_signature(data, ts)
    print("Webhook Process:", hub.process_incoming_webhook(data, sig, ts))
