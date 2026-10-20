from __future__ import annotations

import hashlib
import hmac
import time
from typing import Any

from neural_lock import NeuralLock


class SovereignLicenseEngine:
    """
    NomaanOS Sovereign Node License & Cryptographic Entitlement Engine.
    Validates cryptographically signed node leases, enforces anti-tamper expiry,
    and binds entitlements to local machine hardware fingerprints.
    """

    def __init__(self, master_secret: bytes = b"NOMAANOS_SOVEREIGN_KEY_SEED") -> None:
        self.secret = master_secret
        self.lock = NeuralLock()

    def _get_fingerprint(self) -> str:
        token = self.lock.generate_attestation_token("LICENSE_VERIFICATION")
        return token.get("node_fingerprint", "LOCAL_NODE_PRIMARY")

    def issue_license(
        self,
        tenant_id: str,
        validity_days: int = 365,
    ) -> dict[str, Any]:
        node_fp = self._get_fingerprint()
        issued_at = time.time()
        expires_at = issued_at + (validity_days * 86400)

        payload = f"{tenant_id}:{node_fp}:{issued_at}:{expires_at}"
        signature = hmac.new(
            self.secret, payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        return {
            "tenant_id": tenant_id,
            "node_fingerprint": node_fp,
            "issued_at": issued_at,
            "expires_at": expires_at,
            "signature": signature,
            "entitlement": "ENTERPRISE_L5_ENCLAVE",
        }

    def verify_license(self, license_data: dict[str, Any]) -> dict[str, Any]:
        required = [
            "tenant_id",
            "node_fingerprint",
            "issued_at",
            "expires_at",
            "signature",
        ]
        if not all(k in license_data for k in required):
            return {"valid": False, "reason": "MISSING_SCHEMA_FIELDS"}

        current_time = time.time()
        if current_time > license_data["expires_at"]:
            return {"valid": False, "reason": "LICENSE_EXPIRED"}

        current_fp = self._get_fingerprint()
        if license_data["node_fingerprint"] != current_fp:
            return {"valid": False, "reason": "HARDWARE_FINGERPRINT_MISMATCH"}

        payload = (
            f"{license_data['tenant_id']}:{license_data['node_fingerprint']}:"
            f"{license_data['issued_at']}:{license_data['expires_at']}"
        )
        expected_sig = hmac.new(
            self.secret, payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(expected_sig, license_data["signature"]):
            return {"valid": False, "reason": "CRYPTOGRAPHIC_SIGNATURE_TAMPERED"}

        return {
            "valid": True,
            "tenant_id": license_data["tenant_id"],
            "entitlement": license_data.get("entitlement", "STANDARD"),
            "days_remaining": round(
                (license_data["expires_at"] - current_time) / 86400, 1
            ),
        }


if __name__ == "__main__":
    engine = SovereignLicenseEngine()
    lic = engine.issue_license("IHFC-IITD-LAB")
    print("Issued License:", lic)
    print("Verification:", engine.verify_license(lic))
