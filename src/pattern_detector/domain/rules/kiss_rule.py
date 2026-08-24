"""Rust Keep It Simple, Stupid (KISS) Rule (cyclomatic complexity & long parameter lists)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class KissRule(BasePatternRule):
    """Detects KISS violations in Rust (High Cyclomatic Complexity, Long Parameter Lists)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.KISS

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for fn in model.all_functions():
            evidences: list[Evidence] = []

            # 1. Cyclomatic Complexity
            if fn.cyclomatic_complexity >= 10:
                evidences.append(
                    Evidence(
                        description=f"KISS Violation (High Complexity): Function '{fn.name}' has cyclomatic complexity of {fn.cyclomatic_complexity} (control branch points)",
                        weight=0.75,
                        rule_code="KISS_HIGH_CYCLOMATIC_COMPLEXITY",
                        location=fn.location,
                    )
                )

            # 2. Long Parameter List (>= 5 params, excluding self)
            user_params = [p for p in fn.params if p[0] not in ("self", "&self", "&mut self")]
            if len(user_params) >= 5:
                evidences.append(
                    Evidence(
                        description=f"KISS Violation (Long Parameter List): Function '{fn.name}' takes {len(user_params)} parameters; consider a Config/Request struct or Builder",
                        weight=0.70,
                        rule_code="KISS_LONG_PARAMETER_LIST",
                        location=fn.location,
                    )
                )

            if evidences:
                det = self._create_detection(
                    target_name=fn.name,
                    target_kind="function",
                    evidences=evidences,
                    location=fn.location,
                )
                detections.append(det)

        return detections
