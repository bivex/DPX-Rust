"""Rust Bridge Pattern Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class BridgePatternRule(BasePatternRule):
    """Detects Bridge pattern in Rust (struct generic over abstraction trait)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.BRIDGE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            evidences: list[Evidence] = []
            # Generic struct with backend/driver field
            bridge_fields = [
                f for f in st.fields
                if f.name in ("backend", "driver", "platform", "transport", "engine", "impl_")
                and f.type_str in st.generics
            ]
            if bridge_fields:
                evidences.append(
                    Evidence(
                        description=f"Decouples abstraction in '{st.name}' from implementation backend '{bridge_fields[0].name}: {bridge_fields[0].type_str}'",
                        weight=0.65,
                        rule_code="BRIDGE_GENERIC_BACKEND",
                        location=st.location,
                    )
                )

            if evidences:
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="struct",
                    evidences=evidences,
                    location=st.location,
                )
                detections.append(det)

        return detections
