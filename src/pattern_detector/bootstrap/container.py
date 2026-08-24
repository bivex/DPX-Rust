"""Dependency Injection container wiring hexagonal ports and adapters for DPX-Rust."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_rust_parser_adapter import NativeRustParserAdapter
from pattern_detector.adapters.outbound.persistence.file_result_repositories import (
    HtmlResultRepository,
    JsonResultRepository,
    MarkdownResultRepository,
    SarifResultRepository,
)
from pattern_detector.adapters.outbound.persistence.file_source_provider import FileSourceProvider
from pattern_detector.application.services.detection_service import DetectionService
from pattern_detector.application.services.scanning_service import ScanningService
from pattern_detector.domain.rules import DEFAULT_RULES
from pattern_detector.ports.inbound import DetectorPort, ScannerPort
from pattern_detector.ports.outbound import (
    ParserPort,
    ResultRepositoryPort,
    SourceProviderPort,
)


class Container:
    """IoC container managing singleton services and adapters for DPX-Rust."""

    def __init__(self) -> None:
        self._source_provider: SourceProviderPort | None = None
        self._parser: ParserPort | None = None
        self._detector: DetectorPort | None = None
        self._scanner: ScannerPort | None = None

        self._json_repo: ResultRepositoryPort | None = None
        self._html_repo: ResultRepositoryPort | None = None
        self._markdown_repo: ResultRepositoryPort | None = None
        self._sarif_repo: ResultRepositoryPort | None = None

    @property
    def source_provider(self) -> SourceProviderPort:
        if self._source_provider is None:
            self._source_provider = FileSourceProvider()
        return self._source_provider

    @property
    def parser(self) -> ParserPort:
        if self._parser is None:
            self._parser = NativeRustParserAdapter()
        return self._parser

    @property
    def detector(self) -> DetectorPort:
        if self._detector is None:
            self._detector = DetectionService(rules=list(DEFAULT_RULES))
        return self._detector

    @property
    def json_repository(self) -> ResultRepositoryPort:
        if self._json_repo is None:
            self._json_repo = JsonResultRepository()
        return self._json_repo

    @property
    def html_repository(self) -> ResultRepositoryPort:
        if self._html_repo is None:
            self._html_repo = HtmlResultRepository()
        return self._html_repo

    @property
    def markdown_repository(self) -> ResultRepositoryPort:
        if self._markdown_repo is None:
            self._markdown_repo = MarkdownResultRepository()
        return self._markdown_repo

    @property
    def sarif_repository(self) -> ResultRepositoryPort:
        if self._sarif_repo is None:
            self._sarif_repo = SarifResultRepository()
        return self._sarif_repo

    def get_scanner(self) -> ScannerPort:
        if self._scanner is None:
            self._scanner = ScanningService(
                source_provider=self.source_provider,
                parser=self.parser,
                detector=self.detector,
                json_repository=self.json_repository,
                html_repository=self.html_repository,
                markdown_repository=self.markdown_repository,
                sarif_repository=self.sarif_repository,
            )
        return self._scanner


def create_container() -> Container:
    return Container()
