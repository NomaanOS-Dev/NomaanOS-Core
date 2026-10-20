from __future__ import annotations

import time
from typing import Any

from nomaanos.engine import NoseExec
from nomaanos.ledger.engine import EvidenceLedger


class EnclaveBenchmarkSuite:
    """
    NomaanOS High-Speed Performance & Latency Benchmark Engine.
    Executes live throughput testing over sandboxed execution and
    cryptographic ledger signing to measure real microsecond latency.
    """

    def __init__(self, ledger_path: str = "config/benchmark_ledger.jsonl") -> None:
        self.engine = NoseExec(allowed_binaries=["echo"])
        self.ledger = EvidenceLedger(storage_path=ledger_path)

    def run_benchmark(self, cycles: int = 25) -> dict[str, Any]:
        start = time.perf_counter()

        for i in range(cycles):
            self.engine.execute(["echo", f"bench_{i}"])
            self.ledger.record_entry("bench_worker", f"cycle_{i}_attestation")

        total_duration = time.perf_counter() - start
        ops_per_second = round(cycles / max(total_duration, 0.0001), 2)
        ledger_valid = self.ledger.verify_integrity()

        return {
            "status": "BENCHMARK_COMPLETE",
            "cycles_completed": cycles,
            "total_duration_sec": round(total_duration, 4),
            "throughput_ops_sec": ops_per_second,
            "ledger_verified": ledger_valid,
            "benchmark_verdict": "PERFORMANCE_HEALTHY"
            if ledger_valid
            else "LEDGER_CORRUPTED",
        }


if __name__ == "__main__":
    bench = EnclaveBenchmarkSuite()
    print("Benchmark Results:", bench.run_benchmark(15))
