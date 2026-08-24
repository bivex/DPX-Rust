"""Rust Iterator Pattern Rule (impl Iterator for Struct)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class IteratorPatternRule(BasePatternRule):
    """Detects Iterator Pattern implementation in Rust."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.ITERATOR

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for imp in model.all_impls():
            if imp.trait_name and (imp.trait_name.strip() == "Iterator" or imp.trait_name.startswith("Iterator<")):
                evidences = [
                    Evidence(
                        description=f"Implements standard 'Iterator' trait providing sequential element traversal for '{imp.target_type}'",
                        weight=0.85,
                        rule_code="ITERATOR_TRAIT_IMPL",
                        location=imp.location,
                    )
                ]
                det = self._create_detection(
                    target_name=f"impl Iterator for {imp.target_type}",
                    target_kind="iterator_impl",
                    evidences=evidences,
                    location=imp.location,
                )
                detections.append(det)

        return detections
