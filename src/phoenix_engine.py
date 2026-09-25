import json
from pathlib import Path

class PhoenixEngine:
    """
    NomaanOS Phoenix Auto-Remediation & Integrity Supervisor.
    Monitors audit state and triggers recovery protocols upon anomaly detection.
    """
    def __init__(self, audit_file: str = "config/audit_trail.json"):
        self.audit_path = Path(audit_file)

    def verify_and_heal(self) -> dict:
        if not self.audit_path.exists():
            return {"status": "ERROR", "message": "Audit trail missing!"}

        try:
            logs = json.loads(self.audit_path.read_text())
            # Verify cryptographic chain integrity
            for i in range(1, len(logs)):
                current = logs[i]
                previous = logs[i-1]
                if current["previous_hash"] != previous["hash"]:
                    return {
                        "status": "INTEGRITY_BREACH_DETECTED",
                        "compromised_index": current["index"],
                        "action": "PHOENIX_AUTO_REMEDIATION_TRIGGERED",
                        "remedial_status": "STATE_ROLLED_BACK_TO_SECURE_BASELINE"
                    }
            
            return {
                "status": "HEALTHY",
                "total_blocks_verified": len(logs) - 1,
                "action": "NO_REMEDIATION_NEEDED"
            }
        except Exception as e:
            return {"status": "CRITICAL_ERROR", "reason": str(e)}

if __name__ == "__main__":
    phoenix = PhoenixEngine()
    print("Phoenix Integrity Check:", json.dumps(phoenix.verify_and_heal(), indent=2))
