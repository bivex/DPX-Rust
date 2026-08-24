"""Rust Template Method Rule (traits with provided default methods calling required methods)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class TemplateMethodRule(BasePatternRule):
    """Detects Template Method pattern in Rust."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.TEMPLATE_METHOD

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for tr in model.all_traits():
            # A template method trait in Rust has at least one required method (no body) and at least one provided default method (has body)
            required_methods = [m for m in tr.methods.values() if not m.has_default_body]
            default_methods = [m for m in tr.methods.values() if m.has_default_body]

            if required_methods and default_methods:
                evidences = [
                    Evidence(
                        description=f"Trait '{tr.name}' defines template skeleton default method(s) ({', '.join(m.name for m in default_methods[:2])}) with customizable required step(s) ({', '.join(m.name for m in required_methods[:2])})",
                        weight=0.70,
                        rule_code="TEMPLATE_METHOD_DEFAULT_TRAIT_BODY",
                        location=tr.location,
                    )
                ]
                det = self._create_detection(
                    target_name=tr.name,
                    target_kind="template_trait",
                    evidences=evidences,
                    location=tr.location,
                )
                detections.append(det)

        return detections
