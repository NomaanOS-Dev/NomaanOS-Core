import unittest
import time
from src.orchestrator import NomaanOSOrchestrator
from src.phoenix_engine import PhoenixEngine

class TestNomaanOSBenchmark(unittest.TestCase):
    def setUp(self):
        self.os_core = NomaanOSOrchestrator()
        self.phoenix = PhoenixEngine()

    def test_pipeline_throughput_benchmark(self):
        start_time = time.time()
        iterations = 50
        for _ in range(iterations):
            self.os_core.process_request("Benchmark secure check", ["ls"])
        duration = time.time() - start_time
        print(f"\n[BENCHMARK] Processed {iterations} pipeline intents in {duration:.4f} seconds.")
        self.assertLess(duration, 2.0, "Pipeline throughput benchmark failed (too slow)")

    def test_phoenix_integrity_benchmark(self):
        start_time = time.time()
        res = self.phoenix.verify_and_heal()
        duration = time.time() - start_time
        self.assertEqual(res["status"], "HEALTHY")
        print(f"[BENCHMARK] Phoenix ledger cryptographic verification completed in {duration:.4f} seconds.")

if __name__ == "__main__":
    unittest.main()
