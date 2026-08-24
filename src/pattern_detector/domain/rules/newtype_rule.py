"""Rust Newtype Pattern Rule (single-element tuple structs)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class NewtypePatternRule(BasePatternRule):
    """Detects Newtype Pattern in Rust (struct Id(u64);)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.NEWTYPE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            if st.is_tuple and len(st.fields) == 1:
                evidences = [
                    Evidence(
                        description=f"Single-element tuple struct '{st.name}({st.fields[0].type_str})' implements the idiomatic Rust Newtype pattern for strong type safety and orphan rule bypass",
                        weight=0.85,
                        rule_code="NEWTYPE_SINGLE_ELEMENT_TUPLE",
                        location=st.location,
                    )
                ]
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="newtype_struct",
                    evidences=evidences,
                    location=st.location,
                )
                detections.append(det)

        return detections
