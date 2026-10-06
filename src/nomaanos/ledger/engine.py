import hashlib
import json
import time

class EvidenceLedger:
    def __init__(self, storage_path="ledger.jsonl"):
        self.storage_path = storage_path
        self.chain = []

    def compute_hash(self, block):
        serialized = json.dumps(block, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def record_entry(self, artifact_name, payload):
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

    def verify_integrity(self):
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]
            if curr["previous_hash"] != prev["current_hash"]:
                return False
        return True
