from __future__ import annotations

from typing import Any, ClassVar

from src.orchestrator import NomaanOSOrchestrator


class SecurityFuzzer:
    """
    NomaanOS Automated Security Fuzzer & Payload Mutation Engine.
    Generates targeted shell escapes, path traversals, boundary overflows,
    and null-byte injections to verify sentinel fail-closed invariants.
    """

    BASE_ATTACK_SEEDS: ClassVar[list[str]] = [
        "rm -rf / --no-preserve-root",
        "; cat /etc/shadow",
        "$(reboot)",
        "`whoami`",
        "../../../../../../etc/passwd",
        "A" * 4096,
        "valid_cmd\x00_hidden_payload",
        "%s%p%x%n",
        "${IFS}cat${IFS}/etc/hosts",
    ]

    def __init__(self) -> None:
        self.os_core = NomaanOSOrchestrator()

    def generate_mutations(self) -> list[str]:
        mutations = list(self.BASE_ATTACK_SEEDS)
        for seed in self.BASE_ATTACK_SEEDS:
            mutations.append(f"EXEC: {seed}")
            mutations.append(f"{seed} # comment")
            mutations.append(f"sudo {seed}")
        return mutations

    def run_fuzz_test(self, max_payloads: int = 15) -> dict[str, Any]:
        payloads = self.generate_mutations()[:max_payloads]
        blocked_count = 0
        passed_count = 0
        results: list[dict[str, Any]] = []

        for p in payloads:
            res = self.os_core.process_request(p, ["echo", "test"])
            status = res.get("pipeline_status", "UNKNOWN")

            is_blocked = (
                "BLOCKED" in status or res.get("sentinel_verdict") == "REJECTED"
            )
            if is_blocked:
                blocked_count += 1
            else:
                passed_count += 1

            results.append(
                {"payload_sample": p[:32], "status": status, "blocked": is_blocked}
            )

        return {
            "status": "FUZZING_COMPLETED",
            "total_tested": len(payloads),
            "blocked_count": blocked_count,
            "passed_count": passed_count,
            "fail_closed_ratio": round(blocked_count / max(1, len(payloads)), 2),
            "results": results,
        }


if __name__ == "__main__":
    fuzzer = SecurityFuzzer()
    print("Fuzzer Output:", fuzzer.run_fuzz_test(5))
