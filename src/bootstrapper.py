from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from nomaanos.ledger.engine import EvidenceLedger


class EnclaveBootstrapper:
    """
    NomaanOS Enclave Bootstrapper.
    Ensures safe operational directory hierarchy, strict file masks,
    and initializes the tamper-evident ledger anchor.
    """

    def __init__(self, base_dir: str = ".") -> None:
        self.base_path = Path(base_dir)

    def bootstrap_enclave(self) -> dict[str, Any]:
        required_dirs = ["config", "logs"]
        dir_statuses: dict[str, bool] = {}

        for dir_name in required_dirs:
            target = self.base_path / dir_name
            try:
                target.mkdir(parents=True, exist_ok=True)
                os.chmod(target, 0o700)
                dir_statuses[dir_name] = os.access(target, os.R_OK | os.W_OK)
            except OSError:
                dir_statuses[dir_name] = False

        # Ledger initialization probe
        ledger_path = self.base_path / "config" / "audit_trail.jsonl"
        ledger = EvidenceLedger(storage_path=str(ledger_path))
        if not ledger.chain:
            ledger.record_entry("bootstrap", "enclave_initialization_anchor")
        ledger_ready = ledger.verify_integrity()

        all_ready = all(dir_statuses.values()) and ledger_ready

        return {
            "status": "BOOTSTRAP_COMPLETE" if all_ready else "BOOTSTRAP_FAILED",
            "directories": dir_statuses,
            "ledger_anchor_verified": ledger_ready,
            "ledger_blocks": len(ledger.chain),
        }


if __name__ == "__main__":
    bootstrapper = EnclaveBootstrapper()
    print("Enclave Bootstrap:", bootstrapper.bootstrap_enclave())
