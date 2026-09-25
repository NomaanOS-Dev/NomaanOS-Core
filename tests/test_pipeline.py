import unittest
from src.orchestrator import NomaanOSOrchestrator

class TestNomaanOSPipeline(unittest.TestCase):
    def setUp(self):
        self.os_core = NomaanOSOrchestrator()

    def test_safe_execution_flow(self):
        result = self.os_core.process_request("List directory contents", ["ls"])
        self.assertEqual(result["pipeline_status"], "SUCCESS")
        self.assertIn("audit_block_hash", result)

    def test_malicious_intent_blocking(self):
        result = self.os_core.process_request("Delete system using rm -rf /", ["rm", "-rf", "/"])
        self.assertEqual(result["pipeline_status"], "BLOCKED_AT_INTENT_LAYER")
        self.assertEqual(result["details"]["action"], "HALT")
        self.assertIn("audit_block_hash", result)

if __name__ == "__main__":
    unittest.main()
