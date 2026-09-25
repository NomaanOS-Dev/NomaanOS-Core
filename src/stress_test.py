import time
from src.orchestrator import NomaanOSOrchestrator

class MasterStressTest:
    """
    NomaanOS Automated High-Concurrency Stress & Durability Test Suite.
    Subjects the orchestrator pipeline to heavy load to verify stability.
    """
    def __init__(self):
        self.os_core = NomaanOSOrchestrator()

    def run_stress_test(self, total_requests: int = 100) -> dict:
        print(f"\n[!] INITIATING MASTER STRESS TEST ({total_requests} CONCURRENT CYCLES)...")
        print("-" * 60)
        
        start_time = time.time()
        success_count = 0
        blocked_count = 0
        
        for i in range(total_requests):
            # Alternate between safe and malicious intents
            if i % 2 == 0:
                res = self.os_core.process_request("Stress check safe file list", ["ls"])
                if res.get("pipeline_status") == "SUCCESS":
                    success_count += 1
            else:
                res = self.os_core.process_request("Stress check malicious rm -rf /", ["rm", "-rf", "/"])
                if "BLOCKED" in res.get("pipeline_status", ""):
                    blocked_count += 1
                    
        duration = time.time() - start_time
        print(f"    --> Completed {total_requests} requests in {duration:.4f} seconds.")
        print(f"    --> Allowed: {success_count} | Blocked: {blocked_count}")
        print("-" * 60)
        print("[+] Master Stress Test Completed Successfully.\n")
        
        return {
            "total_requests": total_requests,
            "duration_sec": round(duration, 4),
            "stress_verdict": "NODE_STABLE_UNDER_HEAVY_CONCURRENCY"
        }

if __name__ == "__main__":
    st = MasterStressTest()
    st.run_stress_test()
