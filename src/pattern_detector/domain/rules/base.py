"""Base abstractions and protocol for Rust pattern detection rules."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.pattern import PATTERN_CATALOG
from pattern_detector.domain.value_objects import (
    Confidence,
    Evidence,
    PatternCategory,
    PatternType,
    SourceLocation,
)


@runtime_checkable
class PatternRule(Protocol):
    """Protocol that every Rust pattern detection rule must satisfy."""

    @property
    def pattern_type(self) -> PatternType:
        ...

    @property
    def pattern_category(self) -> PatternCategory:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def description(self) -> str:
        ...

    def detect(self, model: CodeModel) -> list[Detection]:
        ...


class BasePatternRule(ABC):
    """Base class for Rust pattern rules."""

    @property
    @abstractmethod
    def pattern_type(self) -> PatternType:
        ...

    @property
    def pattern_category(self) -> PatternCategory:
        entry = PATTERN_CATALOG.get(self.pattern_type)
        if entry:
            return entry.category
        return PatternCategory.STRUCTURAL

    @property
    def name(self) -> str:
        entry = PATTERN_CATALOG.get(self.pattern_type)
        if entry:
            return entry.name
        return self.pattern_type.value.replace("_", " ").title()

    @property
    def description(self) -> str:
        entry = PATTERN_CATALOG.get(self.pattern_type)
        if entry:
            return entry.description
        return ""

    @abstractmethod
    def detect(self, model: CodeModel) -> list[Detection]:
        ...

    def _create_detection(
        self,
        target_name: str,
        target_kind: str,
        evidences: list[Evidence],
        location: SourceLocation | None = None,
        related_locations: list[SourceLocation] | None = None,
        metadata: dict | None = None,
    ) -> Detection:
        return Detection(
            pattern_type=self.pattern_type,
            pattern_category=self.pattern_category,
            target_name=target_name,
            target_kind=target_kind,
            confidence=Confidence.from_evidences(evidences),
            primary_location=location,
            evidences=evidences,
            related_locations=related_locations or [],
            metadata=metadata or {},
        )
