import unittest
import hashlib
import hmac

class TestSecurityPrimitives(unittest.TestCase):
    def setUp(self):
        self.secret = b"nomaanos_enclave_key_test"
        self.payload = b"audit_event_kernel_boot"

    def test_hmac_integrity_verification(self):
        sig = hmac.new(self.secret, self.payload, hashlib.sha256).hexdigest()
        tampered_sig = hmac.new(b"wrong_key", self.payload, hashlib.sha256).hexdigest()
        self.assertNotEqual(sig, tampered_sig, "Tampered signature should never match authentic signature")

    def test_tamper_detection_in_log(self):
        orig_hash = hashlib.sha256(self.payload).hexdigest()
        tampered_payload = b"audit_event_kernel_boot_modified"
        tampered_hash = hashlib.sha256(tampered_payload).hexdigest()
        self.assertNotEqual(orig_hash, tampered_hash, "Hash mismatch must trigger anomaly alert")

if __name__ == "__main__":
    unittest.main()
