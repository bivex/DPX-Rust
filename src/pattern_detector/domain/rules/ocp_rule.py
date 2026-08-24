"""Rust Open/Closed Principle (OCP) Rule (excessive match cascades)."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType, SourceLocation


class OpenClosedPrincipleRule(BasePatternRule):
    """Detects OCP violations in Rust (large match cascades on types)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.OPEN_CLOSED

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for fn in model.all_functions():
            # Check for large match expressions (>= 6 arms)
            match_arms = len(re.findall(r"=>\s*\{?", fn.body))
            if "match " in fn.body and match_arms >= 6:
                evidences = [
                    Evidence(
                        description=f"OCP Violation: Function '{fn.name}' has large match expression with {match_arms} branches; consider trait polymorphism for extensibility",
                        weight=0.75,
                        rule_code="OCP_LARGE_MATCH_CASCADE",
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
