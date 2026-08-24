"""Inbound (driver) ports for the Rust pattern detector application layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection, DetectionReport
from pattern_detector.domain.value_objects import ConfidenceLevel, PatternCategory


@dataclass
class ScanOptions:
    """Configuration options for a codebase scan execution."""

    min_confidence: ConfidenceLevel = ConfidenceLevel.LOW
    categories: list[PatternCategory] = field(default_factory=list)
    enabled_patterns: list[str] = field(default_factory=list)
    output_json_path: str | None = None
    output_html_path: str | None = None
    output_markdown_path: str | None = None
    output_sarif_path: str | None = None
    include_principles: bool = True
    verbose: bool = False


class ScannerPort(Protocol):
    """Primary inbound port for scanning codebases and returning DetectionReports."""

    def scan_path(self, path: str, options: ScanOptions | None = None) -> DetectionReport:
        ...

    def scan_sources(self, sources: dict[str, str], options: ScanOptions | None = None) -> DetectionReport:
        ...


class DetectorPort(Protocol):
    """Inbound port for executing pattern detection rules on an existing CodeModel."""

    def detect_patterns(self, model: CodeModel, options: ScanOptions | None = None) -> list[Detection]:
        ...
