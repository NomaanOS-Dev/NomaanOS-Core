from __future__ import annotations

from typing import Any, Iterator

from nomaanos.soc.telemetry import HostTelemetryProbe


class TelemetryStreamer:
    """
    NomaanOS Live SOC Telemetry Streamer.
    Streams real kernel and host telemetry samples for real-time dashboards
    and audit ingestion without artificial delay loops.
    """

    def __init__(self) -> None:
        self.probe = HostTelemetryProbe()

    def stream_telemetry(self, max_samples: int = 5) -> Iterator[dict[str, Any]]:
        for i in range(max_samples):
            sample = self.probe.collect_metrics()
            sample["sequence_id"] = i + 1
            yield sample


if __name__ == "__main__":
    streamer = TelemetryStreamer()
    for telemetry_event in streamer.stream_telemetry(max_samples=2):
        print("Live Event:", telemetry_event)
