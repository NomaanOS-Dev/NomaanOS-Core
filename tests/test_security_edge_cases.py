import hashlib
import hmac
import unittest


class TestSecurityPrimitives(unittest.TestCase):
    def setUp(self):
        self.secret = b"nomaanos_enclave_key_test"
        self.payload = b"audit_event_kernel_boot"

    def test_hmac_integrity_verification(self):
        sig = hmac.new(self.secret, self.payload, hashlib.sha256).hexdigest()
        tampered_sig = hmac.new(b"wrong_key", self.payload, hashlib.sha256).hexdigest()
        self.assertNotEqual(
            sig,
            tampered_sig,
            "Tampered signature should never match authentic signature",
        )

    def test_tamper_detection_in_log(self):
        orig_hash = hashlib.sha256(self.payload).hexdigest()
        tampered_payload = b"audit_event_kernel_boot_modified"
        tampered_hash = hashlib.sha256(tampered_payload).hexdigest()
        self.assertNotEqual(
            orig_hash, tampered_hash, "Hash mismatch must trigger anomaly alert"
        )


if __name__ == "__main__":
    unittest.main()


def test_evidence_ledger_detects_block_tampering():
    from nomaanos.ledger.engine import EvidenceLedger

    ledger = EvidenceLedger()
    ledger.record_entry("auth_service", "init_session_user_root")
    ledger.record_entry("kernel_driver", "load_crypto_module")
    assert ledger.verify_integrity() is True

    # Tamper with the internal payload hash of an intermediate block
    ledger.chain[0]["payload_hash"] = "0" * 64
    assert ledger.verify_integrity() is False


def test_master_health_check_memory_pressure_threshold():
    from health_check import MasterHealthCheck

    # Set threshold unnaturally high to test memory_pressure tripwire
    hc = MasterHealthCheck(mem_threshold_mb=999_999_999)
    telemetry = hc.get_host_telemetry()
    if telemetry["mem_available_mb"] > 0:
        assert telemetry["memory_pressure"] is True
        result = hc.run_full_attestation()
        assert result["node_attestation"] == "SUBSYSTEM_OR_RESOURCE_WARNING"


def test_evidence_ledger_jsonl_persistence_and_reload(tmp_path):
    from nomaanos.ledger.engine import EvidenceLedger

    ledger_file = tmp_path / "test_ledger.jsonl"
    ledger1 = EvidenceLedger(storage_path=str(ledger_file))
    ledger1.record_entry("auth_service", "session_start")
    ledger1.record_entry("firewall", "drop_syn_flood")
    assert len(ledger1.chain) == 2
    assert ledger1.verify_integrity() is True

    # Re-instantiate from the same file to verify disk recovery
    ledger2 = EvidenceLedger(storage_path=str(ledger_file))
    assert len(ledger2.chain) == 2
    assert ledger2.chain[1]["artifact"] == "firewall"
    assert ledger2.verify_integrity() is True


def test_real_telemetry_probe_metrics():
    from nomaanos.soc.telemetry import HostTelemetryProbe

    probe = HostTelemetryProbe()
    metrics = probe.collect_metrics()
    assert "mem_available_mb" in metrics
    assert "active_processes" in metrics
    assert "load_1m" in metrics
    assert metrics["status"] in ("HEALTHY", "DEGRADED")


def test_sentinel_agent_patrol():
    from sentinel_agent import SentinelAgent

    agent = SentinelAgent()
    patrol = agent.patrol_enclave()
    assert patrol["sentinel_id"] == "SENTINEL-AI-WATCHDOG-01"
    assert "checks" in patrol
    assert patrol["patrol_status"] in ("CLEAN", "DEGRADED")


def test_neural_lock_dynamic_attestation():
    from neural_lock import NeuralLock

    lock = NeuralLock()
    token_data = lock.generate_attestation_token("TEST_OP")
    assert token_data["l5_status"] == "LOCKED_AND_VERIFIED"
    assert len(token_data["node_fingerprint"]) >= 16
    assert len(token_data["attestation_token"]) == 64
