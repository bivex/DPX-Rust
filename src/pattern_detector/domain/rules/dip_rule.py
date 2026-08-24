"""Rust Dependency Inversion Principle (DIP) Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class DependencyInversionRule(BasePatternRule):
    """Detects DIP in Rust (functions parameterizing on impl Trait / dyn Trait)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.DEPENDENCY_INVERSION

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for fn in model.all_functions():
            trait_params = [
                (p_name, p_type) for p_name, p_type in fn.params
                if "impl " in p_type or "dyn " in p_type or "Box<dyn" in p_type or "&dyn" in p_type
            ]
            if trait_params:
                evidences = [
                    Evidence(
                        description=f"DIP Adherence: Function '{fn.name}' depends on abstraction interface(s) ({', '.join(f'{p[0]}: {p[1]}' for p in trait_params[:2])}) rather than concrete struct types",
                        weight=0.75,
                        rule_code="DIP_TRAIT_ABSTRACTION_PARAMETER",
                        location=fn.location,
                    )
                ]
                det = self._create_detection(
                    target_name=fn.name,
                    target_kind="function",
                    evidences=evidences,
                    location=fn.location,
                )
                detections.append(det)

        return detections
