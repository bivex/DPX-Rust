"""Rust Flyweight Pattern Rule (Arc/Rc interners and shared pools)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class FlyweightPatternRule(BasePatternRule):
    """Detects Flyweight pattern in Rust."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.FLYWEIGHT

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            evidences: list[Evidence] = []
            name_lower = st.name.lower()

            if "interner" in name_lower or "flyweight" in name_lower or "pool" in name_lower:
                evidences.append(
                    Evidence(
                        description=f"Struct '{st.name}' follows Flyweight / Symbol Interner naming convention",
                        weight=0.45,
                        rule_code="FLYWEIGHT_NAMING",
                        location=st.location,
                    )
                )

            interning_fields = [
                f for f in st.fields
                if "HashMap<" in f.type_str and ("Arc<" in f.type_str or "Rc<" in f.type_str or "Symbol" in f.type_str)
            ]
            if interning_fields:
                evidences.append(
                    Evidence(
                        description=f"Maintains shared immutable instance cache pool '{interning_fields[0].name}: {interning_fields[0].type_str}'",
                        weight=0.55,
                        rule_code="FLYWEIGHT_CACHE_POOL",
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
                if det.confidence.score >= 0.50:
                    detections.append(det)

        return detections
