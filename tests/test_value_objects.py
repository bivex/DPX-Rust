"""Tests for domain value objects in DPX-Rust."""

import pytest
from pattern_detector.domain.value_objects import (
    Confidence,
    ConfidenceLevel,
    Evidence,
    PatternCategory,
    PatternType,
    SourceLocation,
)


def test_source_location_formatting() -> None:
    loc = SourceLocation(file_path="src/main.rs", line=42, column=5)
    assert str(loc) == "src/main.rs:42:5"


def test_evidence_weight_validation() -> None:
    ev = Evidence(description="Builder setter", weight=0.45, rule_code="BUILDER_SETTER")
    assert ev.weight == 0.45

    with pytest.raises(ValueError):
        Evidence(description="Invalid", weight=1.5, rule_code="BAD")


def test_confidence_aggregation() -> None:
    ev1 = Evidence(description="E1", weight=0.5, rule_code="R1")
    ev2 = Evidence(description="E2", weight=0.5, rule_code="R2")
    conf = Confidence.from_evidences([ev1, ev2])

    assert conf.score == 0.75  # 1 - (1-0.5)*(1-0.5)
    assert conf.level == ConfidenceLevel.HIGH
    assert conf.percentage_str == "75%"


def test_pattern_types_and_categories() -> None:
    assert PatternCategory.CREATIONAL.value == "creational"
    assert PatternCategory.IDIOM.value == "idiom"
    assert PatternCategory.SAFETY.value == "safety"
    assert PatternType.TYPESTATE.value == "typestate"
    assert PatternType.RAII_DROP.value == "raii_drop"
    assert PatternType.NEWTYPE.value == "newtype"
