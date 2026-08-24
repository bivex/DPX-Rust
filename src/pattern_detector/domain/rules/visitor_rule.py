"""Rust Visitor Pattern Rule (AST traversal traits with visit_* methods)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class VisitorPatternRule(BasePatternRule):
    """Detects Visitor Pattern in Rust."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.VISITOR

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for tr in model.all_traits():
            visit_methods = [m for m in tr.methods.values() if m.name.startswith("visit_")]
            if len(visit_methods) >= 2 or tr.name.lower().endswith("visitor"):
                evidences = [
                    Evidence(
                        description=f"Trait '{tr.name}' defines Visitor traversal interface with {len(visit_methods)} visit method(s) ({', '.join(m.name for m in visit_methods[:3])})",
                        weight=0.75,
                        rule_code="VISITOR_TRAIT_METHODS",
                        location=tr.location,
                    )
                ]
                det = self._create_detection(
                    target_name=tr.name,
                    target_kind="visitor_trait",
                    evidences=evidences,
                    location=tr.location,
                )
                detections.append(det)

        return detections
