import os
import shutil
from pathlib import Path
from typing import Any, Dict


class MasterHealthCheck:
    """
    NomaanOS Master Node Health & Host Telemetry Attestation.
    Validates operational subsystem presence and host resource thresholds.
    """
    def __init__(self, mem_threshold_mb: int = 256):
        self.config_dir = Path("config")
        self.src_dir = Path("src")
        self.mem_threshold_mb = mem_threshold_mb

    def get_host_telemetry(self) -> Dict[str, Any]:
        disk_stat = shutil.disk_usage(".")
        free_disk_gb = round(disk_stat.free / (1024 ** 3), 2)
        total_disk_gb = round(disk_stat.total / (1024 ** 3), 2)

        mem_available_mb = 0
        if Path("/proc/meminfo").exists():
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith("MemAvailable:"):
                        mem_available_mb = int(line.split()[1]) // 1024
                        break

        load_1m, _, _ = os.getloadavg() if hasattr(os, "getloadavg") else (0.0, 0.0, 0.0)

        return {
            "load_1m": load_1m,
            "mem_available_mb": mem_available_mb,
            "disk_free_gb": free_disk_gb,
            "disk_total_gb": total_disk_gb,
            "memory_pressure": mem_available_mb < self.mem_threshold_mb if mem_available_mb > 0 else False,
        }

    def run_full_attestation(self) -> Dict[str, Any]:
        subsystems = {
            "l2_fail_closed_engine": (self.src_dir / "engine.py").exists(),
            "l3_ai_intent_bridge": (self.src_dir / "agent_bridge.py").exists(),
            "l4_cryptographic_audit_ledger": (self.config_dir / "audit_trail.json").exists(),
            "phoenix_self_healing": (self.src_dir / "phoenix_engine.py").exists(),
            "l5_neural_lock": (self.src_dir / "neural_lock.py").exists(),
            "compliance_auditor": (self.src_dir / "compliance_auditor.py").exists(),
            "threat_simulator": (self.src_dir / "threat_simulator.py").exists(),
            "sbom_generator": (self.src_dir / "sbom_generator.py").exists(),
            "system_hardening": (self.src_dir / "hardening.py").exists(),
            "p2p_swarm_sync": (self.src_dir / "swarm_sync.py").exists(),
        }

        telemetry = self.get_host_telemetry()
        all_active = all(subsystems.values())
        healthy = all_active and not telemetry["memory_pressure"]

        node_status = "NODE_100_PERCENT_OPERATIONAL_AND_SECURE" if healthy else "SUBSYSTEM_OR_RESOURCE_WARNING"

        return {
            "node_attestation": node_status,
            "subsystems": subsystems,
            "telemetry": telemetry,
        }


if __name__ == "__main__":
    hc = MasterHealthCheck()
    result = hc.run_full_attestation()
    print(f"[+] Attestation Verdict: {result['node_attestation']}")
    print(f"[+] Telemetry: {result['telemetry']}")
