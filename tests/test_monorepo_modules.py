import unittest
from src.nomaanos.ledger.engine import EvidenceLedger
from src.nomaanos.soc.telemetry import HostTelemetryProbe

class TestMonorepoCore(unittest.TestCase):
    def test_ledger_append_and_verify(self):
        ledger = EvidenceLedger()
        ledger.record_entry("test_artifact", "sample_payload_data")
        self.assertTrue(ledger.verify_integrity())

    def test_telemetry_metrics(self):
        probe = HostTelemetryProbe()
        res = probe.collect_metrics()
        self.assertEqual(res["status"], "HEALTHY")

if __name__ == "__main__":
    unittest.main()
