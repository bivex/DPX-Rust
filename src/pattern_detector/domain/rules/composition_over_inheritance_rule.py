"""Rust Composition Over Deep Trait Hierarchies Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class CompositionOverInheritanceRule(BasePatternRule):
    """Detects idiomatic struct composition in Rust."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.COMPOSITION_OVER_INHERITANCE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            composed_struct_fields = [
                f for f in st.fields
                if f.type_str[0].isupper() and f.type_str not in ("String", "Option", "Vec", "HashMap", "Result", "Arc", "Box", "Mutex", "RwLock")
            ]
            if len(composed_struct_fields) >= 2:
                evidences = [
                    Evidence(
                        description=f"Struct '{st.name}' follows Composition over Trait hierarchies by aggregating {len(composed_struct_fields)} component structs ({', '.join(f.name for f in composed_struct_fields[:3])})",
                        weight=0.70,
                        rule_code="COMPOSITION_STRUCT_AGGREGATION",
                        location=st.location,
                    )
                ]
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="struct",
                    evidences=evidences,
                    location=st.location,
                )
                detections.append(det)

        return detections
