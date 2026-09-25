import hashlib
import json
import time
from pathlib import Path

class AuditLogger:
    """
    Cryptographic Audit Logger for NomaanOS Operations.
    Maintains tamper-evident logs for Sentinel Proxy actions.
    """
    def __init__(self, log_file: str = "config/audit_trail.json"):
        self.log_path = Path(log_file)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            self._write_genesis_block()

    def _write_genesis_block(self):
        genesis = {
            "index": 0,
            "event": "GENESIS_BLOCK",
            "timestamp": time.time(),
            "hash": "0" * 64
        }
        self.log_path.write_text(json.dumps([genesis], indent=2))

    def log_event(self, action: str, details: dict):
        logs = json.loads(self.log_path.read_text())
        prev_hash = logs[-1]["hash"]
        
        event_record = {
            "index": len(logs),
            "action": action,
            "details": details,
            "timestamp": time.time(),
            "previous_hash": prev_hash
        }
        
        # Compute SHA-256 block hash
        block_str = json.dumps(event_record, sort_keys=True).encode()
        event_record["hash"] = hashlib.sha256(block_str).hexdigest()
        
        logs.append(event_record)
        self.log_path.write_text(json.dumps(logs, indent=2))
        return event_record["hash"]

if __name__ == "__main__":
    logger = AuditLogger()
    print("Audit Logger initialized. Test Hash:", logger.log_event("TEST_ACTION", {"status": "SECURE"}))
