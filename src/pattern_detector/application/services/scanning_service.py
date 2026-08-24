"""Application scanning service orchestrating source retrieval, parsing, and rule execution."""

from __future__ import annotations

import time

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection, DetectionReport
from pattern_detector.domain.value_objects import ConfidenceLevel, PatternCategory
from pattern_detector.ports.inbound import DetectorPort, ScannerPort, ScanOptions
from pattern_detector.ports.outbound import (
    ParserPort,
    ResultRepositoryPort,
    SourceProviderPort,
)


class ScanningService(ScannerPort):
    """End-to-end scanning orchestrator."""

    def __init__(
        self,
        source_provider: SourceProviderPort,
        parser: ParserPort,
        detector: DetectorPort,
        json_repository: ResultRepositoryPort | None = None,
        html_repository: ResultRepositoryPort | None = None,
        markdown_repository: ResultRepositoryPort | None = None,
        sarif_repository: ResultRepositoryPort | None = None,
    ) -> None:
        self._source_provider = source_provider
        self._parser = parser
        self._detector = detector
        self._json_repository = json_repository
        self._html_repository = html_repository
        self._markdown_repository = markdown_repository
        self._sarif_repository = sarif_repository

    def scan_path(self, path: str, options: ScanOptions | None = None) -> DetectionReport:
        options = options or ScanOptions()
        t0 = time.perf_counter()

        sources = self._source_provider.get_sources(path, extensions=[".rs"])
        code_model = self._parser.parse_sources(sources)
        code_model.project_path = path

        detections = self._detector.detect_patterns(code_model, options=options)
        filtered = self._filter_detections(detections, options)

        elapsed = time.perf_counter() - t0
        report = DetectionReport(
            project_path=path,
            scanned_files_count=len(sources),
            detections=filtered,
            elapsed_seconds=elapsed,
        )

        self._export_reports(report, options)
        return report

    def scan_sources(self, sources: dict[str, str], options: ScanOptions | None = None) -> DetectionReport:
        options = options or ScanOptions()
        t0 = time.perf_counter()

        code_model = self._parser.parse_sources(sources)
        detections = self._detector.detect_patterns(code_model, options=options)
        filtered = self._filter_detections(detections, options)

        elapsed = time.perf_counter() - t0
        report = DetectionReport(
            project_path="<memory>",
            scanned_files_count=len(sources),
            detections=filtered,
            elapsed_seconds=elapsed,
        )

        self._export_reports(report, options)
        return report

    def _filter_detections(self, detections: list[Detection], options: ScanOptions) -> list[Detection]:
        level_order = [
            ConfidenceLevel.LOW,
            ConfidenceLevel.MEDIUM,
            ConfidenceLevel.HIGH,
            ConfidenceLevel.VERY_HIGH,
        ]
        min_idx = level_order.index(options.min_confidence)

        filtered = []
        for d in detections:
            if level_order.index(d.level) < min_idx:
                continue
            if options.categories and d.pattern_category not in options.categories:
                continue
            if not options.include_principles and d.pattern_category == PatternCategory.PRINCIPLE:
                continue
            filtered.append(d)

        return filtered

    def _export_reports(self, report: DetectionReport, options: ScanOptions) -> None:
        if options.output_json_path and self._json_repository:
            self._json_repository.save(report, options.output_json_path)
        if options.output_html_path and self._html_repository:
            self._html_repository.save(report, options.output_html_path)
        if options.output_markdown_path and self._markdown_repository:
            self._markdown_repository.save(report, options.output_markdown_path)
        if options.output_sarif_path and self._sarif_repository:
            self._sarif_repository.save(report, options.output_sarif_path)
