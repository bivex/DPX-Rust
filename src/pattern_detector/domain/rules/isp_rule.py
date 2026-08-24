"""Rust Interface Segregation Principle (ISP) Rule (Fat Traits)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class InterfaceSegregationRule(BasePatternRule):
    """Detects Fat Traits (ISP violation) in Rust."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.INTERFACE_SEGREGATION

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for tr in model.all_traits():
            method_count = len(tr.methods)
            if method_count >= 8:
                evidences = [
                    Evidence(
                        description=f"ISP Violation (Fat Trait): Trait '{tr.name}' declares {method_count} methods; consider splitting into smaller, role-focused traits",
                        weight=0.80,
                        rule_code="ISP_FAT_TRAIT",
                        location=tr.location,
                    )
                ]
                det = self._create_detection(
                    target_name=tr.name,
                    target_kind="fat_trait",
                    evidences=evidences,
                    location=tr.location,
                )
                detections.append(det)

        return detections
