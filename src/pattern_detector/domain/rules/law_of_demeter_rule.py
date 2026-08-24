"""Rust Law of Demeter Rule (deep method chaining)."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class LawOfDemeterRule(BasePatternRule):
    """Detects Law of Demeter violations in Rust (deep train-wreck call chains)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.LAW_OF_DEMETER

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for fn in model.all_functions():
            # Exclude builder and iterator chains (e.g. .map().filter().collect())
            chains = re.findall(r"(?:[a-zA-Z0-9_]+\.){4,}[a-zA-Z0-9_]+\(", fn.body)
            filtered_chains = [
                c for c in chains
                if not any(k in c for k in ("iter()", "into_iter()", "map(", "filter(", "collect(", "unwrap(", "ok(", "build("))
            ]
            if filtered_chains:
                evidences = [
                    Evidence(
                        description=f"Law of Demeter Violation: Function '{fn.name}' has deep train-wreck invocation chain '{filtered_chains[0][:40]}...'",
                        weight=0.75,
                        rule_code="DEMETER_DEEP_CHAIN",
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
