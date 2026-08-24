"""Rust RAII / Drop Guard Pattern Rule (impl Drop for Struct)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class RaiiDropRule(BasePatternRule):
    """Detects RAII resource management via Drop trait implementations in Rust."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.RAII_DROP

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for imp in model.all_impls():
            if imp.trait_name and (imp.trait_name.strip() == "Drop" or imp.trait_name.strip().startswith("Drop<")):
                evidences = [
                    Evidence(
                        description=f"Implements 'Drop' trait for '{imp.target_type}', enforcing deterministic RAII cleanup of system resources",
                        weight=0.85,
                        rule_code="RAII_DROP_TRAIT_IMPL",
                        location=imp.location,
                    )
                ]
                det = self._create_detection(
                    target_name=f"impl Drop for {imp.target_type}",
                    target_kind="raii_drop_guard",
                    evidences=evidences,
                    location=imp.location,
                )
                detections.append(det)

        return detections
