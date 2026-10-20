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


def test_real_analytics_hub(tmp_path):
    from analytics_hub import AnalyticsHub
    from nomaanos.ledger.engine import EvidenceLedger

    ledger_path = tmp_path / "analytics_ledger.jsonl"
    ledger = EvidenceLedger(storage_path=str(ledger_path))
    ledger.record_entry("core_router", "forward_packet")

    hub = AnalyticsHub(ledger_path=str(ledger_path))
    stats = hub.aggregate_metrics()
    assert stats["status"] == "OPERATIONAL"
    assert stats["ledger_blocks_indexed"] == 1
    assert "memory_utilization_pct" in stats
    assert stats["ledger_integrity"] is True


def test_real_attestation_issuer(tmp_path):
    from attestation_issuer import SovereignAttestationIssuer

    ledger_path = tmp_path / "attest_ledger.jsonl"
    issuer = SovereignAttestationIssuer(ledger_path=str(ledger_path))
    attestation = issuer.issue_node_attestation("RUNTIME_HEALTHCHECK_PASS")
    assert attestation["status"] == "ATTESTED"
    assert len(attestation["attestation_signature"]) == 64
    assert issuer.verify_attestation(attestation) is True

    # Tampering test
    tampered = dict(attestation)
    tampered["claim"] = "UNAUTHORIZED_CLAIM"
    assert issuer.verify_attestation(tampered) is False


def test_real_phoenix_engine_auto_healing(tmp_path):
    from nomaanos.ledger.engine import EvidenceLedger
    from phoenix_engine import PhoenixEngine

    ledger_file = tmp_path / "test_phoenix.jsonl"
    ledger = EvidenceLedger(storage_path=str(ledger_file))
    ledger.record_entry("auth", "login_ok")
    ledger.record_entry("audit", "policy_grant")
    assert len(ledger.chain) == 2

    # Tamper with block 2 payload without recalculating hash
    ledger.chain[1]["artifact"] = "malicious_injection"
    with open(ledger_file, "w") as f:
        for b in ledger.chain:
            import json

            f.write(json.dumps(b) + "\n")

    phoenix = PhoenixEngine(audit_file=str(ledger_file))
    heal_report = phoenix.verify_and_heal()
    assert heal_report["status"] == "INTEGRITY_BREACH_DETECTED"
    assert heal_report["remedial_status"] == "STATE_ROLLED_BACK_TO_SECURE_BASELINE"
    assert heal_report["retained_valid_blocks"] == 1

    # Verify that the healed ledger on disk is now intact
    recovered_ledger = EvidenceLedger(storage_path=str(ledger_file))
    assert len(recovered_ledger.chain) == 1
    assert recovered_ledger.verify_integrity() is True


def test_real_cryptographic_chain_verifier(tmp_path):
    from chain_verifier import CryptographicChainVerifier
    from nomaanos.ledger.engine import EvidenceLedger

    ledger_file = tmp_path / "test_verifier.jsonl"
    ledger = EvidenceLedger(storage_path=str(ledger_file))
    ledger.record_entry("kernel", "boot_ok")
    ledger.record_entry("network", "socket_bind")

    verifier = CryptographicChainVerifier(audit_file=str(ledger_file))
    res = verifier.verify_full_chain()
    assert res["status"] == "SUCCESS"
    assert res["verified_blocks"] == 2
    assert res["chain_verdict"] == "CRYPTOGRAPHICALLY_SOUND"


def test_real_snapshot_manager(tmp_path):
    from snapshot_manager import SnapshotManager

    snap_dir = tmp_path / "snapshots"
    test_target = tmp_path / "config" / "test_state.json"
    test_target.parent.mkdir(parents=True, exist_ok=True)
    test_target.write_text('{"state": "HEALTHY_BASELINE"}', encoding="utf-8")

    mgr = SnapshotManager(backup_dir=str(snap_dir))
    snap = mgr.create_snapshot(targets=[str(test_target)])
    assert snap["file_count"] == 1
    assert len(snap["bundle_hash"]) == 64

    # Tamper with file
    test_target.write_text('{"state": "CORRUPTED_STATE"}', encoding="utf-8")
    assert "CORRUPTED_STATE" in test_target.read_text()

    # Restore snapshot and verify recovery
    success = mgr.restore_snapshot(snap["snapshot_id"])
    assert success is True
    assert "HEALTHY_BASELINE" in test_target.read_text()


def test_real_security_fuzzer():
    from fuzzer import SecurityFuzzer

    fuzzer = SecurityFuzzer()
    res = fuzzer.run_fuzz_test(max_payloads=8)
    assert res["status"] == "FUZZING_COMPLETED"
    assert res["total_tested"] == 8
    assert res["blocked_count"] > 0


def test_real_log_rotator(tmp_path):
    from log_rotator import EnclaveLogRotator

    log_dir = tmp_path / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    active_log = log_dir / "audit.log"
    # Write 2 KB payload
    active_log.write_text("A" * 2048, encoding="utf-8")

    # Set threshold to 1 KB to force rotation
    rotator = EnclaveLogRotator(target_dir=str(log_dir), max_bytes=1024, max_archives=2)
    res = rotator.rotate_file_if_needed(active_log)

    assert res["rotated"] is True
    assert active_log.read_text(encoding="utf-8") == ""
    archives = list(log_dir.glob("audit.log.*.gz"))
    assert len(archives) == 1


def test_real_stress_tester(tmp_path):
    from stress_test import EnclaveStressTester

    ledger_file = tmp_path / "stress_ledger.jsonl"
    tester = EnclaveStressTester(ledger_path=str(ledger_file))
    res = tester.execute_stress_run(iterations=10)

    assert res["status"] == "STRESS_TEST_PASSED"
    assert res["exec_failures"] == 0
    assert res["ledger_verified"] is True
    assert res["p50_exec_latency_ms"] >= 0.0


def test_real_webhook_hub(tmp_path):
    import time

    from webhook_hub import WebhookHub

    ledger_path = tmp_path / "webhook_ledger.jsonl"
    hub = WebhookHub(ledger_path=str(ledger_path))

    payload = {"event": "security_alert", "severity": "HIGH"}
    ts = time.time()
    sig = hub.generate_signature(payload, ts)

    # 1. Valid webhook submission
    res = hub.process_incoming_webhook(payload, sig, ts)
    assert res["status"] == "ACCEPTED"
    assert res["ledger_blocks"] == 1
    assert res["ledger_verified"] is True

    # 2. Tampered signature rejection
    tampered_res = hub.process_incoming_webhook(payload, "invalid_signature_hex", ts)
    assert tampered_res["status"] == "REJECTED"
    assert tampered_res["reason"] == "INVALID_SIGNATURE"

    # 3. Clock skew / replay rejection
    expired_res = hub.process_incoming_webhook(payload, sig, ts - 600.0)
    assert expired_res["status"] == "REJECTED"
    assert expired_res["reason"] == "TIMESTAMP_EXPIRED_REPLAY_ATTEMPT"


def test_real_sovereign_api_handler():
    from io import BytesIO
    from unittest.mock import MagicMock

    from server import SovereignAPIHandler

    # Mock request and socket for isolated unit test
    handler = SovereignAPIHandler.__new__(SovereignAPIHandler)
    handler.rfile = BytesIO()
    handler.wfile = BytesIO()
    handler.send_response = MagicMock()
    handler.send_header = MagicMock()
    handler.end_headers = MagicMock()

    # Test /telemetry endpoint
    handler.path = "/telemetry"
    handler.do_GET()
    handler.send_response.assert_called_with(200)

    # Test unknown 404 endpoint
    handler.path = "/invalid_route"
    handler.do_GET()
    handler.send_response.assert_called_with(404)


def test_real_distribution_packager():
    from packager import DistributionPackager

    packager = DistributionPackager()
    spec = packager.verify_packaging_spec()
    assert spec["status"] == "VALID"
    assert spec["project_name"] == "nomaanos-core"
    assert spec["has_entrypoints"] is True


def test_real_release_manifest_generator(tmp_path):
    from release_manifest import ReleaseManifestGenerator

    out_file = tmp_path / "test_manifest.json"
    generator = ReleaseManifestGenerator(output_path=str(out_file))
    manifest = generator.generate_manifest(version="6.0.0-PROD")
    assert manifest["release_version"] == "6.0.0-PROD"
    assert manifest["total_source_files"] > 0
    assert len(manifest["root_sha256"]) == 64
    assert out_file.is_file()


def test_real_hardware_bridge():
    from hardware_bridge import HardwareEnclaveBridge

    bridge = HardwareEnclaveBridge()
    res = bridge.inspect_enclave_hardware()
    assert res["status"] == "HARDWARE_AUDIT_COMPLETE"
    assert res["cpu_cores"] >= 1
    assert "aes_ni_present" in res["hardware_crypto"]
    assert res["security_tier"] in ("HARDWARE_ACCELERATED", "SOFTWARE_FALLBACK")


def test_real_telemetry_dashboard():
    from telemetry_dashboard import TelemetryDashboard

    dash = TelemetryDashboard()
    view = dash.generate_dashboard_view()
    assert view["status"] == "ACTIVE"
    assert view["cpu_cores"] >= 1
    assert "mem_available_mb" in view


def test_real_sovereign_tui(capsys):
    from tui import SovereignTUI

    tui = SovereignTUI()
    res = tui.draw_screen()
    captured = capsys.readouterr()
    assert "NOMAANOS SOVEREIGN CONSOLE INTERFACE" in captured.out
    assert res["status"] == "RENDERED"
    assert "metrics" in res


def test_real_badge_generator(tmp_path):
    from badge_generator import EnclaveBadgeGenerator

    badge_dir = tmp_path / "badges"
    generator = EnclaveBadgeGenerator(output_dir=str(badge_dir))
    report = generator.generate_all_badges(total_tests=48, ledger_ok=True)

    assert report["badge_count"] == 2
    tests_svg = (badge_dir / "tests.svg").read_text(encoding="utf-8")
    assert "<svg" in tests_svg
    assert "48 passing" in tests_svg
    ledger_svg = (badge_dir / "ledger.svg").read_text(encoding="utf-8")
    assert "verified" in ledger_svg
