"""Rust High Cohesion / Low Coupling Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class HighCohesionLowCouplingRule(BasePatternRule):
    """Detects High Fan-Out (High Coupling) in Rust structs."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.HIGH_COHESION_LOW_COUPLING

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            custom_types = set()
            for f in st.fields:
                t = f.type_str.split("<")[0].strip("&mut ").strip("&").strip()
                if t and t[0].isupper() and t not in ("String", "Option", "Vec", "Result", "Box", "Arc", "Rc"):
                    custom_types.add(t)

            if len(custom_types) >= 8:
                evidences = [
                    Evidence(
                        description=f"High Coupling (High Fan-Out): Struct '{st.name}' couples directly with {len(custom_types)} distinct types ({', '.join(sorted(list(custom_types))[:4])}...)",
                        weight=0.80,
                        rule_code="COUPLING_HIGH_FAN_OUT",
                        location=st.location,
                    )
                ]
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="high_coupling_struct",
                    evidences=evidences,
                    location=st.location,
                )
                detections.append(det)

        return detections
