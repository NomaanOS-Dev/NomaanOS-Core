from __future__ import annotations

import hashlib
import hmac
import json
from pathlib import Path
from typing import Any


class MasterSealVerifier:
    """
    NomaanOS Institutional Master Seal Independent Verifier.
    Performs zero-trust verification of signed master seals against live disk state.
    """

    def __init__(
        self,
        seal_file: str = "config/master_seal.json",
        signing_key: bytes = b"NOMAANOS_MASTER_INSTITUTIONAL_SEAL_KEY",
    ) -> None:
        self.seal_path = Path(seal_file)
        self.signing_key = signing_key

    def verify_live_seal(self) -> dict[str, Any]:
        if not self.seal_path.is_file():
            return {"valid": False, "reason": "MASTER_SEAL_NOT_FOUND"}

        try:
            data = json.loads(self.seal_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            return {"valid": False, "reason": f"CORRUPTED_SEAL_FILE: {e}"}

        # 1. Verify HMAC signature on seal payload
        payload = f"SEAL_V6:{data['combined_source_hash']}:{data['timestamp']}"
        expected_sig = hmac.new(
            self.signing_key, payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(expected_sig, data.get("signature", "")):
            return {"valid": False, "reason": "CRYPTOGRAPHIC_SIGNATURE_INVALID"}

        # 2. Recompute live source hashes
        src_path = Path("src")
        live_hashes: list[str] = []
        if src_path.is_dir():
            for py_file in sorted(src_path.rglob("*.py")):
                live_hashes.append(hashlib.sha256(py_file.read_bytes()).hexdigest())

        live_combined_hash = hashlib.sha256(
            "".join(live_hashes).encode("utf-8")
        ).hexdigest()
        if live_combined_hash != data.get("combined_source_hash"):
            return {
                "valid": False,
                "reason": "SOURCE_CODE_DRIFT_DETECTED",
                "expected_hash": data.get("combined_source_hash"),
                "found_hash": live_combined_hash,
            }

        return {
            "valid": True,
            "verdict": "REPOSITORY_INTEGRITY_VERIFIED",
            "files_audited": len(live_hashes),
        }


if __name__ == "__main__":
    verifier = MasterSealVerifier()
    print("Master Seal Verification:", verifier.verify_live_seal())
