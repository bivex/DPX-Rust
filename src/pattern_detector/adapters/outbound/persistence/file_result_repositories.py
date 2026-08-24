"""File Result Repositories for persisting reports to disk."""

from __future__ import annotations

from pathlib import Path

from pattern_detector.adapters.outbound.persistence.html_report_formatter import HtmlReportFormatter
from pattern_detector.adapters.outbound.persistence.json_report_formatter import JsonReportFormatter
from pattern_detector.adapters.outbound.persistence.markdown_report_formatter import MarkdownReportFormatter
from pattern_detector.adapters.outbound.persistence.sarif_report_formatter import SarifReportFormatter
from pattern_detector.domain.detection import DetectionReport
from pattern_detector.ports.outbound import ResultRepositoryPort


class JsonResultRepository(ResultRepositoryPort):
    def __init__(self, formatter: JsonReportFormatter | None = None) -> None:
        self._formatter = formatter or JsonReportFormatter()

    def save(self, report: DetectionReport, destination: str) -> None:
        content = self._formatter.format(report)
        dest_path = Path(destination).resolve()
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_text(content, encoding="utf-8")


class HtmlResultRepository(ResultRepositoryPort):
    def __init__(self, formatter: HtmlReportFormatter | None = None) -> None:
        self._formatter = formatter or HtmlReportFormatter()

    def save(self, report: DetectionReport, destination: str) -> None:
        content = self._formatter.format(report)
        dest_path = Path(destination).resolve()
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_text(content, encoding="utf-8")


class MarkdownResultRepository(ResultRepositoryPort):
    def __init__(self, formatter: MarkdownReportFormatter | None = None) -> None:
        self._formatter = formatter or MarkdownReportFormatter()

    def save(self, report: DetectionReport, destination: str) -> None:
        content = self._formatter.format(report)
        dest_path = Path(destination).resolve()
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_text(content, encoding="utf-8")


class SarifResultRepository(ResultRepositoryPort):
    def __init__(self, formatter: SarifReportFormatter | None = None) -> None:
        self._formatter = formatter or SarifReportFormatter()

    def save(self, report: DetectionReport, destination: str) -> None:
        content = self._formatter.format(report)
        dest_path = Path(destination).resolve()
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_text(content, encoding="utf-8")
