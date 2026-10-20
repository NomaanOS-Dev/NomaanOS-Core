from __future__ import annotations

from nomaanos.cli import main_cli


def test_cli_help(capsys):
    exit_code = main_cli(["--help"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Usage: nomaanos" in captured.out


def test_cli_status(capsys):
    exit_code = main_cli(["status"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Sovereign SOC Host Telemetry" in captured.out
    assert "Subsystem Health Attestation" in captured.out


def test_cli_verify(capsys):
    exit_code = main_cli(["verify"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Audit Ledger Chain Verification: VALID" in captured.out


def test_cli_test_exec(capsys):
    exit_code = main_cli(["test-exec"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Kernel Attestation: SUCCESS" in captured.out
    assert "stdout: Linux" in captured.out


def test_cli_unknown_command(capsys):
    exit_code = main_cli(["invalid-subcommand"])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Unknown command: invalid-subcommand" in captured.out
