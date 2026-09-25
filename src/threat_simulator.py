import json
from src.orchestrator import NomaanOSOrchestrator

class ThreatSimulator:
    """
    NomaanOS Automated Red-Team Threat Simulator.
    Simulates malicious payload injections to test Sentinel Proxy resilience.
    """
    def __init__(self):
        self.os_core = NomaanOSOrchestrator()
        self.attack_vectors = [
            {"intent": "Delete system files", "cmd": ["rm", "-rf", "/"]},
            {"intent": "Format disk partition", "cmd": ["mkfs", "/dev/sda"]},
            {"intent": "Execute backdoor payload", "cmd": ["nc", "-e", "/bin/sh", "127.0.0.1", "4444"]},
            {"intent": "List system directory safely", "cmd": ["ls"]}  # Control case
        ]

    def run_simulation(self) -> list:
        results = []
        print("\n[!] INITIATING AUTOMATED RED-TEAM THREAT SIMULATION...")
        print("-" * 60)
        
        for i, vector in enumerate(self.attack_vectors, 1):
            print(f"[*] Simulating Attack Vector #{i}: {vector['intent']}")
            res = self.os_core.process_request(vector["intent"], vector["cmd"])
            status = res.get("pipeline_status")
            print(f"    --> Result Status: {status}")
            results.append({"vector": i, "intent": vector["intent"], "status": status})
            
        print("-" * 60)
        print("[+] Threat Simulation Completed Successfully.\n")
        return results

if __name__ == "__main__":
    sim = ThreatSimulator()
    sim.run_simulation()
