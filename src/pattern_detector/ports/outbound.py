"""Outbound (driven) ports for external persistence, parsing, and source retrieval."""

from __future__ import annotations

from typing import Protocol

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import DetectionReport


class SourceProviderPort(Protocol):
    """Port for reading Rust source files from filesystem or memory."""

    def get_sources(self, target_path: str, extensions: list[str] | None = None) -> dict[str, str]:
        ...


class ParserPort(Protocol):
    """Port for parsing raw Rust source strings into domain CodeModel."""

    def parse_sources(self, sources: dict[str, str]) -> CodeModel:
        ...


class ReportFormatterPort(Protocol):
    """Port for formatting DetectionReport into string representations."""

    def format(self, report: DetectionReport) -> str:
        ...


class ResultRepositoryPort(Protocol):
    """Port for saving DetectionReports to disk or storage."""

    def save(self, report: DetectionReport, destination: str) -> None:
        ...
