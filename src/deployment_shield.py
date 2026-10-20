from __future__ import annotations

import hashlib
import hmac
import time
from pathlib import Path
from typing import Any

from nomaanos.ledger.engine import EvidenceLedger


class ProductionDeploymentShield:
    """
    NomaanOS Zero-Trust Production Deployment Gate & Shield.
    Validates immutable ledger integrity and release manifest presence
    prior to permitting service initialization or remote artifact publishing.
    """

    def __init__(
        self,
        ledger_path: str = "config/audit_trail.jsonl",
        signing_key: bytes = b"NOMAANOS_DEPLOYMENT_GATE_KEY",
    ) -> None:
        self.ledger = EvidenceLedger(storage_path=ledger_path)
        self.signing_key = signing_key

    def verify_deployment_readiness(self) -> dict[str, Any]:
        ledger_ok = self.ledger.verify_integrity()
        manifest_path = Path("config/release_manifest.json")
        pyproject_path = Path("pyproject.toml")

        checks: dict[str, bool] = {
            "ledger_cryptographically_sound": ledger_ok,
            "release_manifest_present": manifest_path.is_file()
            and manifest_path.stat().st_size > 0,
            "pyproject_spec_present": pyproject_path.is_file(),
        }

        ready = all(checks.values())
        timestamp = time.time()
        seal_payload = f"{ready}:{timestamp}:{len(self.ledger.chain)}"
        seal_signature = hmac.new(
            self.signing_key, seal_payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        return {
            "deployment_permitted": ready,
            "verdict": "DEPLOYMENT_AUTHORIZED" if ready else "DEPLOYMENT_BLOCKED",
            "timestamp": timestamp,
            "checks": checks,
            "gate_seal": seal_signature,
        }


if __name__ == "__main__":
    shield = ProductionDeploymentShield()
    print("Deployment Gate Status:", shield.verify_deployment_readiness())
