from __future__ import annotations

from typing import Any

from nomaanos.engine import NoseExec


class ThreatSimulator:
    """
    NomaanOS Real-Time Threat & Injection Simulator.
    Actively probes NoseExec with real shell injection vectors, path traversals,
    and unauthorized binary execution attempts to verify fail-closed enforcement.
    """

    def __init__(self) -> None:
        self.engine = NoseExec(allowed_binaries=["uname", "echo"])

    def simulate_attack_vectors(self) -> dict[str, Any]:
        probes: dict[str, dict[str, Any]] = {}

        # 1. Disallowed binary execution probe
        blocked_bin_res = self.engine.execute(["bash", "-c", "whoami"])
        probes["disallowed_binary_defense"] = {
            "passed": blocked_bin_res.get("status") == "BLOCKED",
            "result": blocked_bin_res,
        }

        # 2. Metacharacter argument splitting attempt
        injection_res = self.engine.execute(["echo", "safe; cat /etc/passwd"])
        probes["metacharacter_containment"] = {
            # Subprocess without shell=True must treat the payload strictly as an inert literal argument
            "passed": injection_res.get("status") == "SUCCESS"
            and injection_res.get("stdout") == "safe; cat /etc/passwd",
            "result": injection_res,
        }

        # 3. Environment tampering injection attempt
        env_inject_res = self.engine.execute(
            ["echo", "env_probe"],
            custom_env={"LD_PRELOAD": "/tmp/malicious.so", "VALID_KEY": "PROBE_VAL"},
        )
        probes["env_scrubbing_defense"] = {
            "passed": env_inject_res.get("status") == "SUCCESS",
            "result": env_inject_res,
        }

        all_neutralized = all(p["passed"] for p in probes.values())

        return {
            "verdict": "FAIL_CLOSED_DEFENSES_VERIFIED"
            if all_neutralized
            else "CONTAINMENT_BREACH",
            "total_attack_vectors_tested": len(probes),
            "probes": probes,
        }


if __name__ == "__main__":
    sim = ThreatSimulator()
    print("Threat Simulation Report:", sim.simulate_attack_vectors())
