import json
import time
import hashlib
from pathlib import Path

class SovereignLicenseManager:
    """
    NomaanOS Master Sovereign License & Institutional Attestation Manager.
    Binds institutional cryptographic watermarks to the core architecture.
    """
    def __init__(self):
        self.scholar = "Nomaan Khan (IHFC-IITD Scholar)"
        self.license_type = "SOVEREIGN-ENTERPRISE-AIR-GAPPED-LICENSE"

    def issue_license(self) -> dict:
        print(f"\n[!] ISSUING MASTER SOVEREIGN INSTITUTIONAL LICENSE...")
        print("-" * 60)
        
        timestamp = int(time.time())
        raw_token = f"{self.scholar}:{self.license_type}:{timestamp}"
        watermark_hash = hashlib.sha256(raw_token.encode()).hexdigest().upper()
        
        license_data = {
            "institution": "IHFC-IITD Sovereign Research",
            "scholar": self.scholar,
            "license_tier": self.license_type,
            "watermark": f"NOMAANOS-LIC-{watermark_hash[:32]}",
            "status": "ACTIVE_AND_BINDING",
            "timestamp": timestamp
        }
        
        license_file = Path("config/reports/sovereign_license_attestation.json")
        license_file.parent.mkdir(parents=True, exist_ok=True)
        license_file.write_text(json.dumps(license_data, indent=2))
        
        print(f"    --> Scholar    : {self.scholar}")
        print(f"    --> Watermark  : {license_data['watermark']}")
        print(f"    --> Status     : {license_data['status']}")
        print("-" * 60)
        print("[+] Sovereign Institutional License Issued Successfully.\n")
        
        return license_data

if __name__ == "__main__":
    lm = SovereignLicenseManager()
    lm.issue_license()
