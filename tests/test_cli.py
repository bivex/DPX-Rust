"""Tests for Typer CLI commands in DPX-Rust."""

from pathlib import Path
from typer.testing import CliRunner
from pattern_detector.adapters.inbound.cli.main import app

runner = CliRunner()


def test_cli_rules_command() -> None:
    result = runner.invoke(app, ["rules"])
    assert result.exit_code == 0
    assert "Supported Patterns & Rules in DPX-Rust" in result.stdout
    assert "Builder" in result.stdout
    assert "Typestate" in result.stdout
    assert "RAII" in result.stdout or "Raii" in result.stdout


def test_cli_info_command() -> None:
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert "DPX-Rust" in result.stdout
    assert "Rust" in result.stdout


def test_cli_scan_command() -> None:
    sample_path = str(Path(__file__).parent.parent / "examples" / "rust_samples" / "creational_and_idioms.rs")
    result = runner.invoke(app, ["scan", sample_path])
    assert result.exit_code == 0
    assert "DPX-Rust" in result.stdout
    assert "BUILDER" in result.stdout
    assert "NEWTYPE" in result.stdout
