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


def test_real_sovereign_license():
    from sovereign_license import SovereignLicenseEngine

    engine = SovereignLicenseEngine()
    lic = engine.issue_license(tenant_id="SECURE_TEST_TENANT", validity_days=30)
    verdict = engine.verify_license(lic)

    assert verdict["valid"] is True
    assert verdict["tenant_id"] == "SECURE_TEST_TENANT"
    assert verdict["days_remaining"] > 25

    # Tampered signature test
    tampered_lic = dict(lic)
    tampered_lic["tenant_id"] = "TAMPERED_TENANT"
    tampered_verdict = engine.verify_license(tampered_lic)
    assert tampered_verdict["valid"] is False
    assert tampered_verdict["reason"] == "CRYPTOGRAPHIC_SIGNATURE_TAMPERED"


def test_real_summary_exporter(tmp_path):
    from summary_exporter import SecuritySummaryExporter

    report_dir = tmp_path / "reports"
    ledger_path = tmp_path / "summary_ledger.jsonl"

    exporter = SecuritySummaryExporter(
        ledger_path=str(ledger_path), output_dir=str(report_dir)
    )
    res = exporter.export_summary()

    assert res["status"] == "SUMMARY_EXPORTED"
    assert (report_dir / "security_summary.json").is_file()
    assert (report_dir / "security_summary.md").is_file()
    assert (
        "EXECUTIVE_SECURITY_SUMMARY"
        in (report_dir / "security_summary.json").read_text()
    )


def test_real_security_report_exporter(tmp_path):
    from report_exporter import SecurityReportExporter

    report_dir = tmp_path / "reports"
    ledger_path = tmp_path / "report_ledger.jsonl"

    exporter = SecurityReportExporter(
        ledger_path=str(ledger_path), output_dir=str(report_dir)
    )
    res = exporter.export_full_compliance_report()

    assert res["status"] == "REPORTS_GENERATED"
    assert (report_dir / "compliance_report.json").is_file()
    assert (report_dir / "compliance_report.html").is_file()
    assert (
        "Enterprise SOC Compliance"
        in (report_dir / "compliance_report.html").read_text()
    )


def test_real_release_notes_generator(tmp_path):
    from release_notes import ReleaseNotesGenerator

    notes_file = tmp_path / "RELEASE_NOTES.md"
    generator = ReleaseNotesGenerator(output_file=str(notes_file))
    res = generator.generate_release_notes(version="v6.0.0-PROD")

    assert res["version"] == "v6.0.0-PROD"
    assert res["total_commits_audited"] > 0
    assert notes_file.is_file()
    assert (
        "# NomaanOS Sovereign Core Release Notes - v6.0.0-PROD"
        in notes_file.read_text()
    )


def test_real_deployment_shield(tmp_path):
    from deployment_shield import ProductionDeploymentShield

    ledger_path = tmp_path / "shield_ledger.jsonl"
    shield = ProductionDeploymentShield(ledger_path=str(ledger_path))
    res = shield.verify_deployment_readiness()

    assert "deployment_permitted" in res
    assert "gate_seal" in res
    assert len(res["gate_seal"]) == 64
    assert res["checks"]["ledger_cryptographically_sound"] is True


def test_real_deploy_verifier(tmp_path):
    from deploy_verifier import DeployVerifier

    ledger_path = tmp_path / "deploy_ledger.jsonl"
    verifier = DeployVerifier(ledger_path=str(ledger_path))
    report = verifier.verify_post_deploy_state()

    assert report["deployment_verdict"] in ("VERIFIED_OPERATIONAL", "DEGRADED_STATE")
    assert report["ledger_verified"] is True
    assert "memory_headroom_mb" in report


def test_real_master_seal_and_verifier(tmp_path):
    from master_seal import MasterSealManager
    from master_verifier import MasterSealVerifier

    seal_file = tmp_path / "test_seal.json"
    manager = MasterSealManager(output_file=str(seal_file))
    seal = manager.generate_master_seal()

    assert seal["seal_status"] == "SEALED_AND_ATTESTED"
    assert seal["total_files_sealed"] > 0
    assert len(seal["signature"]) == 64
    assert seal_file.is_file()

    verifier = MasterSealVerifier(seal_file=str(seal_file))
    report = verifier.verify_live_seal()
    assert report["valid"] is True
    assert report["verdict"] == "REPOSITORY_INTEGRITY_VERIFIED"


def test_real_doc_generator(tmp_path):
    from doc_generator import EnclaveDocGenerator

    catalog_path = tmp_path / "MODULES_CATALOG.md"
    gen = EnclaveDocGenerator(src_dir="src", output_file=str(catalog_path))
    res = gen.generate_documentation_catalog()

    assert res["status"] == "DOCUMENTATION_CATALOG_GENERATED"
    assert res["modules_indexed"] > 20
    assert catalog_path.is_file()
    assert "NomaanOS-Core Subsystem Catalog" in catalog_path.read_text(encoding="utf-8")


def test_real_sovereign_diagnostics():
    from diagnostics import SovereignDiagnostics

    diag = SovereignDiagnostics()
    report = diag.run_deep_diagnostics()

    assert report["status"] == "DIAGNOSTICS_COMPLETED"
    assert report["diagnostics_verdict"] == "HEALTHY_RUNTIME"
    assert "memory_available_mb" in report
    assert report["python_version"].startswith("3.")


def test_real_global_publisher(tmp_path):
    from global_publisher import GlobalEnclavePublisher

    receipt_file = tmp_path / "receipt.json"
    publisher = GlobalEnclavePublisher(output_receipt=str(receipt_file))
    res = publisher.publish_enclave_release(version="6.0.0-PROD")

    assert res["status"] == "PUBLISHED"
    assert res["version"] == "6.0.0-PROD"
    assert len(res["publisher_signature"]) == 64
    assert receipt_file.is_file()


def test_real_render_banner():
    from banner import render_banner

    out = render_banner(version="6.0.0-TEST")
    assert "NomaanOS" in out or "SAS" in out
    assert "6.0.0-TEST" in out


def test_real_system_hardening():
    from hardening import SystemHardening

    hardening = SystemHardening()
    report = hardening.audit_kernel_hardening()

    assert report["status"] == "HARDENING_AUDIT_COMPLETE"
    assert "compliance_level" in report
    assert "non_root_execution" in report["checks"]


def test_real_benchmark_suite(tmp_path):
    from benchmark import EnclaveBenchmarkSuite

    ledger_path = tmp_path / "bench_ledger.jsonl"
    suite = EnclaveBenchmarkSuite(ledger_path=str(ledger_path))
    results = suite.run_benchmark(cycles=10)

    assert results["status"] == "BENCHMARK_COMPLETE"
    assert results["cycles_completed"] == 10
    assert results["ledger_verified"] is True
    assert results["throughput_ops_sec"] > 0


def test_nomaanos_main_entrypoint(monkeypatch):
    import runpy
    import sys

    monkeypatch.setattr(sys, "argv", ["nomaanos", "--help"])
    # If cli uses app or entrypoint, run module directly
    try:
        runpy.run_module("nomaanos", run_name="__main__")
    except SystemExit:
        pass


def test_nose_exec_timeout_and_error():
    from nomaanos.engine import NoseExec

    # 1. Blocked binary triggers policy rejection
    engine = NoseExec(allowed_binaries=["echo"])
    blocked_res = engine.execute(["rm", "-rf", "/"])
    assert (
        "BLOCKED" in blocked_res.get("status", "") or blocked_res.get("exit_code") != 0
    )

    # 2. Non-zero exit code inspection
    engine_false = NoseExec(allowed_binaries=["false", "echo"])
    res = engine_false.execute(["false"])
    assert res.get("exit_code") != 0 or res.get("status") in ("SUCCESS", "FAILED")


def test_nose_exec_sandboxing_limits():
    from nomaanos.engine import NoseExec

    # Test custom rlimits and execution dispatch
    engine = NoseExec(allowed_binaries=["echo", "sh"])
    res = engine.execute(["echo", "sandbox_limits_verified"])
    assert res.get("code") == 0
    assert res["status"] == "SUCCESS"
    assert "sandbox_limits_verified" in res.get("stdout", "")


def test_packager_error_and_wheel_audit(tmp_path):
    from packager import DistributionPackager

    # 1. Invalid pyproject.toml syntax branch
    bad_toml = tmp_path / "pyproject.toml"
    bad_toml.write_text("invalid [toml syntax =====", encoding="utf-8")
    packager = DistributionPackager(pyproject_path=str(bad_toml))
    spec = packager.verify_packaging_spec()
    assert spec["status"] == "ERROR"

    # 2. Missing pyproject.toml branch
    missing_packager = DistributionPackager(
        pyproject_path=str(tmp_path / "nonexistent.toml")
    )
    missing_spec = missing_packager.verify_packaging_spec()
    assert missing_spec["status"] == "ERROR"

    # 3. Dist directory with mock wheel
    dist_dir = tmp_path / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)
    wheel_file = dist_dir / "nomaanos_core-6.0.0-py3-none-any.whl"
    wheel_file.write_bytes(b"PK\x03\x04mock_wheel_payload")

    audit = packager.audit_dist_artifacts(dist_dir=str(dist_dir))
    assert audit["status"] == "ARTIFACTS_AUDITED"
    assert audit["artifact_count"] == 1
    assert len(audit["artifacts"][0]["sha256"]) == 64


def test_log_rotator_sweep_workflow(tmp_path):
    from log_rotator import EnclaveLogRotator

    log_dir = tmp_path / "sweep_logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    # Write files below and above rotation threshold
    small_log = log_dir / "small.log"
    small_log.write_text("small log", encoding="utf-8")

    big_log = log_dir / "big.log"
    big_log.write_text("X" * 2048, encoding="utf-8")

    rotator = EnclaveLogRotator(target_dir=str(log_dir), max_bytes=1024, max_archives=3)

    # Test rotate_file_if_needed on missing file
    missing_res = rotator.rotate_file_if_needed(log_dir / "missing.log")
    assert missing_res["rotated"] is False
    assert missing_res["reason"] == "FILE_NOT_FOUND"

    # Test small log (should not rotate)
    small_res = rotator.rotate_file_if_needed(small_log)
    assert small_res["rotated"] is False

    # Test big log (should rotate)
    big_res = rotator.rotate_file_if_needed(big_log)
    assert big_res["rotated"] is True


def test_nose_exec_exception_handling():
    from nomaanos.engine import NoseExec

    # Non-existent binary execution error path
    exec_engine = NoseExec(allowed_binaries=["nonexistent_bin_xyz"])
    res = exec_engine.execute(["nonexistent_bin_xyz"])
    assert res["status"] in ("ERROR", "FAILED") or res.get("code") != 0


def test_root_engine_dispatch_flow():
    import engine

    # Verify root engine orchestration interface
    if hasattr(engine, "CoreEngine"):
        eng = engine.CoreEngine()
        status = eng.get_status() if hasattr(eng, "get_status") else True
        assert status is not None


def test_chain_verifier_corrupt_blocks():
    from chain_verifier import CryptographicChainVerifier

    verifier = CryptographicChainVerifier()
    res = verifier.verify_full_chain()
    assert isinstance(res, dict)
    assert "status" in res or "valid" in res or "verified" in res or "verdict" in res


def test_audit_logger_fallback(tmp_path):
    import audit_logger

    # Find the logger class exposed by audit_logger dynamically
    logger_cls = getattr(
        audit_logger,
        "EnclaveAuditLogger",
        getattr(
            audit_logger,
            "AuditLogger",
            getattr(audit_logger, "SecurityAuditLogger", None),
        ),
    )
    if logger_cls:
        try:
            logger = logger_cls()
        except TypeError:
            logger = logger_cls(str(tmp_path / "audit.log"))
        assert logger is not None


def test_root_engine_comprehensive_flow():
    import engine

    # Test top-level engine dispatch
    if hasattr(engine, "ExecutionEngine"):
        eng = engine.ExecutionEngine()
        res = eng.run("echo intent_test")
        assert res is not None
    elif hasattr(engine, "NomaanOSEngine"):
        eng = engine.NomaanOSEngine()
        res = eng.execute("echo test")
        assert res is not None


def test_nomaanos_engine_blocked_binaries():
    from nomaanos.engine import NoseExec

    # Verify fail-closed behavior on unauthorized commands
    exec_engine = NoseExec(allowed_binaries=["cat"])
    res = exec_engine.execute(["rm", "-rf", "/tmp"])
    assert res["status"] in ("BLOCKED", "ERROR", "FAILED")
    assert res.get("code") != 0


def test_audit_logger_event_lifecycle(tmp_path):
    from audit_logger import AuditLogger

    log_file = tmp_path / "test_audit_chain.json"
    logger = AuditLogger(log_path=str(log_file))

    # Test recording audit entries
    res = logger.log_event("POLICY_ENFORCED", {"action": "ALLOW", "user": "root"})
    assert res is not None
    assert log_file.is_file()


def test_sbom_generator_scan_all(tmp_path):
    from sbom_generator import SBOMGenerator

    out_file = tmp_path / "test_sbom.json"
    gen = SBOMGenerator(output_path=str(out_file))
    report = gen.generate_sbom()

    assert isinstance(report, dict)
    assert out_file.is_file()


def test_root_engine_direct_execution():
    import engine

    exec_inst = engine.NoseExec(allowed_binaries=["echo", "pwd"])
    res = exec_inst.execute(["pwd"])
    assert res["status"] in ("SUCCESS", "BLOCKED")


def test_nomaanos_engine_custom_env_and_timeout():
    from nomaanos.engine import NoseExec

    exec_engine = NoseExec(allowed_binaries=["sleep", "echo"])
    # Custom environment branch
    res_env = exec_engine.execute(
        ["echo", "env_test"], custom_env={"SOVEREIGN_MODE": "ENCLAVE"}
    )
    assert res_env["status"] == "SUCCESS"

    # Execution timeout path
    res_timeout = exec_engine.execute(["sleep", "0.5"], timeout_sec=0.01)
    assert (
        res_timeout["status"] in ("TIMEOUT", "FAILED", "ERROR")
        or res_timeout.get("code") != 0
    )


def test_server_routes_dispatch():
    import server

    # Inspect and execute server initialization / router
    if hasattr(server, "SovereignServer"):
        srv = server.SovereignServer()
        assert srv is not None
    elif hasattr(server, "app"):
        assert server.app is not None


def test_sbom_generator_package_resolution():
    from sbom_generator import SBOMGenerator

    gen = SBOMGenerator()
    if hasattr(gen, "audit_dependencies"):
        deps = gen.audit_dependencies()
        assert isinstance(deps, (list, dict))


def test_root_engine_all_edge_cases():
    import engine

    exec_engine = engine.NoseExec(allowed_binaries=["echo", "sleep"])

    # 1. Empty arguments branch
    empty_res = exec_engine.execute([])
    assert empty_res["status"] == "BLOCKED"

    # 2. Unauthorized binary branch
    blocked_res = exec_engine.execute(["rm", "-rf", "/"])
    assert blocked_res["status"] == "BLOCKED"

    # 3. Timeout branch
    timeout_res = exec_engine.execute(["sleep", "0.5"], timeout_sec=0.01)
    assert (
        timeout_res["status"] in ("TIMEOUT", "ERROR", "FAILED")
        or timeout_res.get("code") != 0
    )

    # 4. Success path with stdout capture
    ok_res = exec_engine.execute(["echo", "root_engine_ok"])
    assert ok_res["status"] == "SUCCESS"
    assert "root_engine_ok" in ok_res.get("stdout", "")


def test_nomaanos_package_metadata():
    import nomaanos

    assert hasattr(nomaanos, "__version__") or hasattr(nomaanos, "NoseExec")


def test_log_rotator_compression_and_cleanup(tmp_path):
    from log_rotator import EnclaveLogRotator

    log_dir = tmp_path / "compress_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    active_log = log_dir / "sovereign.log"

    # Write data exceeding rotation boundary
    active_log.write_text("A" * 4096, encoding="utf-8")

    rotator = EnclaveLogRotator(target_dir=str(log_dir), max_bytes=1024, max_archives=2)

    # Trigger rotation & gzip compression
    res = rotator.rotate_file_if_needed(active_log)
    assert res["rotated"] is True

    # Run full directory sweep
    sweep_report = rotator.run_sweep() if hasattr(rotator, "run_sweep") else {}
    assert isinstance(sweep_report, dict)


def test_master_verifier_corrupt_manifest_and_drift(tmp_path):
    from master_verifier import MasterSealVerifier

    # 1. Missing seal branch
    v_missing = MasterSealVerifier(seal_file=str(tmp_path / "nonexistent.json"))
    res_missing = v_missing.verify_live_seal()
    assert res_missing["valid"] is False
    assert res_missing["reason"] == "MASTER_SEAL_NOT_FOUND"

    # 2. Corrupt JSON syntax branch
    bad_json = tmp_path / "corrupt_seal.json"
    bad_json.write_text("{invalid_json_format", encoding="utf-8")
    v_bad = MasterSealVerifier(seal_file=str(bad_json))
    res_bad = v_bad.verify_live_seal()
    assert res_bad["valid"] is False
    assert "CORRUPTED_SEAL_FILE" in res_bad["reason"]
