from __future__ import annotations

import hashlib
import hmac
import json
import time
from pathlib import Path
from typing import Any

from packager import DistributionPackager
from release_manifest import ReleaseManifestGenerator


class GlobalEnclavePublisher:
    """
    NomaanOS Secure Global Distribution & Swarm Publishing Engine.
    Validates distribution wheels, packaging manifests, and issues
    cryptographically signed publication release receipts.
    """

    def __init__(
        self,
        signing_key: bytes = b"NOMAANOS_GLOBAL_PUBLISHER_KEY",
        output_receipt: str = "config/publish_receipt.json",
    ) -> None:
        self.signing_key = signing_key
        self.output_path = Path(output_receipt)
        self.packager = DistributionPackager()
        self.manifest_gen = ReleaseManifestGenerator()

    def publish_enclave_release(self, version: str = "6.0.0") -> dict[str, Any]:
        spec_audit = self.packager.verify_packaging_spec()
        manifest = self.manifest_gen.generate_manifest(version=version)

        is_valid = spec_audit.get("status") == "VALID" and "root_sha256" in manifest
        timestamp = time.time()

        payload = f"PUBLISH:{version}:{manifest.get('root_sha256')}:{timestamp}"
        receipt_signature = hmac.new(
            self.signing_key, payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        receipt = {
            "status": "PUBLISHED" if is_valid else "PUBLICATION_FAILED",
            "version": version,
            "root_sha256": manifest.get("root_sha256"),
            "timestamp": timestamp,
            "publisher_signature": receipt_signature,
            "institutional_tier": "SOVEREIGN_ENTERPRISE_L5",
        }

        try:
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            self.output_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
        except OSError:
            pass

        return receipt


if __name__ == "__main__":
    publisher = GlobalEnclavePublisher()
    print("Publisher Receipt:", publisher.publish_enclave_release())
