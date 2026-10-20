from __future__ import annotations

import time
from typing import Any

from nomaanos.engine import NoseExec
from nomaanos.ledger.engine import EvidenceLedger


class EnclaveStressTester:
    """
    NomaanOS High-Throughput Enclave Stress & Concurrency Tester.
    Exercises sandboxed command execution and cryptographic ledger persistence
    under rapid sequential load to compute latency percentiles and verify stability.
    """

    def __init__(self, ledger_path: str = "config/stress_ledger.jsonl") -> None:
        self.engine = NoseExec(allowed_binaries=["echo", "uname"])
        self.ledger = EvidenceLedger(storage_path=ledger_path)

    def execute_stress_run(self, iterations: int = 50) -> dict[str, Any]:
        execution_latencies_ms: list[float] = []
        ledger_latencies_ms: list[float] = []
        failures = 0

        for i in range(iterations):
            # 1. Sandboxed process dispatch latency
            t0 = time.perf_counter()
            exec_res = self.engine.execute(["echo", f"payload_iteration_{i}"])
            t1 = time.perf_counter()

            if exec_res.get("status") != "SUCCESS":
                failures += 1
            execution_latencies_ms.append(round((t1 - t0) * 1000, 3))

            # 2. Cryptographic append-only write latency
            t2 = time.perf_counter()
            self.ledger.record_entry(f"stress_worker_{i}", f"proof_payload_{i}")
            t3 = time.perf_counter()
            ledger_latencies_ms.append(round((t3 - t2) * 1000, 3))

        # Latency metrics
        execution_latencies_ms.sort()
        ledger_latencies_ms.sort()

        p50_exec = execution_latencies_ms[len(execution_latencies_ms) // 2]
        p95_exec = execution_latencies_ms[int(len(execution_latencies_ms) * 0.95)]
        avg_ledger = round(
            sum(ledger_latencies_ms) / max(1, len(ledger_latencies_ms)), 3
        )

        ledger_valid = self.ledger.verify_integrity()

        return {
            "status": "STRESS_TEST_PASSED"
            if (failures == 0 and ledger_valid)
            else "STRESS_TEST_FAILED",
            "iterations": iterations,
            "exec_failures": failures,
            "ledger_verified": ledger_valid,
            "p50_exec_latency_ms": p50_exec,
            "p95_exec_latency_ms": p95_exec,
            "avg_ledger_write_ms": avg_ledger,
        }


if __name__ == "__main__":
    tester = EnclaveStressTester()
    print("Stress Test Output:", tester.execute_stress_run(20))
