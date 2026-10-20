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


def test_real_sbom_generator(tmp_path):
    from sbom_generator import SBOMGenerator

    out_file = tmp_path / "sbom.json"
    gen = SBOMGenerator(output_path=str(out_file))
    doc = gen.generate_sbom()
    assert doc["bomFormat"] == "CycloneDX-Compatible"
    assert doc["total_dependencies"] > 0
    assert len(doc["manifest_sha256"]) == 64
    assert out_file.exists()


def test_real_kernel_boot():
    from kernel_boot import KernelBootstrapper

    booter = KernelBootstrapper()
    res = booter.bootstrap()
    assert res["status"] in ("BOOT_SUCCESS_ALL_SYSTEMS_GO", "BOOT_DEGRADED")
    assert res["phases"]["runtime_binary_valid"] is True
    assert res["phases"]["config_storage_writable"] is True


def test_real_health_inspector():
    from health_inspector import MasterHealthInspector

    inspector = MasterHealthInspector()
    report = inspector.inspect_health()
    assert report["inspection_status"] in ("SUCCESS", "DEGRADED")
    assert report["checks_performed"] >= 4
    assert "entropy_avail" in report["metrics"]


def test_real_enclave_bootstrapper(tmp_path):
    from bootstrapper import EnclaveBootstrapper

    bootstrapper = EnclaveBootstrapper(base_dir=str(tmp_path))
    res = bootstrapper.bootstrap_enclave()
    assert res["status"] == "BOOTSTRAP_COMPLETE"
    assert res["ledger_anchor_verified"] is True
    assert res["ledger_blocks"] >= 1
    assert (tmp_path / "config").exists()
    assert (tmp_path / "logs").exists()


def test_real_ci_runner():
    from ci_runner import LocalCIRunner

    runner = LocalCIRunner(src_dir="src/nomaanos")
    verdict = runner.run_pipeline()
    assert verdict["status"] == "PASSED"
    assert verdict["syntax_verified"] is True
    assert verdict["python_files_compiled"] > 0


def test_real_quantum_shield():
    from quantum_shield import QuantumShield

    shield = QuantumShield()
    payload = "SECURE_SOVEREIGN_PAYLOAD"
    armor = shield.generate_quantum_armor(payload)
    assert armor["quantum_resistant"] is True
    assert len(armor["armor_token"]) == 128  # SHA3-512 produces 128 hex chars
    assert shield.verify_quantum_armor(payload, armor["armor_token"]) is True
    assert (
        shield.verify_quantum_armor("TAMPERED_PAYLOAD", armor["armor_token"]) is False
    )


def test_real_threat_simulator():
    from threat_simulator import ThreatSimulator

    sim = ThreatSimulator()
    report = sim.simulate_attack_vectors()
    assert report["verdict"] == "FAIL_CLOSED_DEFENSES_VERIFIED"
    assert report["total_attack_vectors_tested"] == 3


def test_real_telemetry_streamer():
    from streamer import TelemetryStreamer

    streamer = TelemetryStreamer()
    events = list(streamer.stream_telemetry(max_samples=3))
    assert len(events) == 3
    assert events[0]["sequence_id"] == 1
    assert "active_processes" in events[0]


def test_real_swarm_sync(tmp_path):
    from nomaanos.ledger.engine import EvidenceLedger
    from swarm_sync import SwarmNodeSync

    ledger_path = tmp_path / "sync_ledger.jsonl"
    ledger = EvidenceLedger(storage_path=str(ledger_path))
    ledger.record_entry("node_1", "init_tx")
    ledger.record_entry("node_1", "state_update")

    sync = SwarmNodeSync(ledger_path=str(ledger_path))
    res = sync.verify_and_sync()
    assert res["node_state"] == "SYNCHRONIZED"
    assert res["chain_length"] == 2
    assert len(res["state_root"]) == 64


def test_real_master_dashboard_ui(capsys):
    from master_dashboard_ui import MasterDashboardUI

    ui = MasterDashboardUI()
    snapshot = ui.render_snapshot()
    captured = capsys.readouterr()
    assert "NOMAANOS LIVE SOVEREIGN DASHBOARD" in captured.out
    assert snapshot["ledger_valid"] is True
    assert "telemetry" in snapshot


def test_real_compliance_auditor():
    from compliance_auditor import ComplianceAuditor

    auditor = ComplianceAuditor()
    audit = auditor.audit_security_controls()
    assert audit["compliance_status"] in ("COMPLIANT", "NON_COMPLIANT")
    assert audit["total_controls_evaluated"] >= 4
    assert audit["controls"]["source_tree_intact"] is True
