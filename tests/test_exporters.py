"""Tests for Exporters (HTML, Markdown, SARIF, JSON, LLM) in DPX-Rust."""

import json
import tempfile
from pathlib import Path

from pattern_detector.adapters.outbound.persistence.file_result_repositories import (
    HtmlResultRepository,
    JsonResultRepository,
    MarkdownResultRepository,
    SarifResultRepository,
)
from pattern_detector.adapters.outbound.persistence.html_report_formatter import HtmlReportFormatter
from pattern_detector.adapters.outbound.persistence.llm_report_formatter import LlmReportFormatter
from pattern_detector.adapters.outbound.persistence.markdown_report_formatter import MarkdownReportFormatter
from pattern_detector.adapters.outbound.persistence.sarif_report_formatter import SarifReportFormatter
from pattern_detector.domain.detection import Detection, DetectionReport
from pattern_detector.domain.value_objects import (
    Confidence,
    Evidence,
    PatternCategory,
    PatternType,
    SourceLocation,
)


def _create_sample_report() -> DetectionReport:
    loc = SourceLocation(file_path="src/builder.rs", line=10)
    ev = Evidence(description="Builder pattern detected", weight=0.85, rule_code="BUILDER_NAMING", location=loc)
    det = Detection(
        pattern_type=PatternType.BUILDER,
        pattern_category=PatternCategory.CREATIONAL,
        target_name="ServerBuilder",
        target_kind="struct",
        confidence=Confidence.from_evidences([ev]),
        primary_location=loc,
        evidences=[ev],
    )
    return DetectionReport(
        project_path="src",
        scanned_files_count=1,
        detections=[det],
        elapsed_seconds=0.015,
    )


def test_html_report_formatter() -> None:
    formatter = HtmlReportFormatter()
    report = _create_sample_report()
    rendered = formatter.format(report)

    assert "<!DOCTYPE html>" in rendered
    assert "DPX-Rust" in rendered
    assert "ServerBuilder" in rendered
    assert "BUILDER_NAMING" in rendered
    assert "togglePrinciplesVisibility" in rendered


def test_sarif_report_formatter() -> None:
    formatter = SarifReportFormatter()
    report = _create_sample_report()
    rendered = formatter.format(report)

    data = json.loads(rendered)
    assert data["version"] == "2.1.0"
    assert data["runs"][0]["tool"]["driver"]["name"] == "DPX-Rust"


def test_markdown_and_json_repositories() -> None:
    report = _create_sample_report()
    with tempfile.TemporaryDirectory() as tmpdir:
        json_path = str(Path(tmpdir) / "report.json")
        md_path = str(Path(tmpdir) / "report.md")

        JsonResultRepository().save(report, json_path)
        MarkdownResultRepository().save(report, md_path)

        assert Path(json_path).exists()
        assert Path(md_path).exists()
        assert "ServerBuilder" in Path(json_path).read_text(encoding="utf-8")
        assert "# 🦀" in Path(md_path).read_text(encoding="utf-8")


def test_llm_report_formatter() -> None:
    formatter = LlmReportFormatter()
    report = _create_sample_report()
    rendered = formatter.format(report)

    assert "<codebase_architecture_analysis>" in rendered
    assert "ServerBuilder" in rendered
