"""Rust Interior Mutability Rule (Arc<Mutex<T>>, RwLock<T>, RefCell<T>, Atomic*)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class InteriorMutabilityRule(BasePatternRule):
    """Detects Interior Mutability synchronizations in Rust."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.INTERIOR_MUTABILITY

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            sync_fields = [
                f for f in st.fields
                if "Mutex<" in f.type_str or "RwLock<" in f.type_str or "RefCell<" in f.type_str or "Atomic" in f.type_str
            ]
            if sync_fields:
                evidences = [
                    Evidence(
                        description=f"Struct '{st.name}' uses Interior Mutability pattern via synchronized field(s): {', '.join(f'{f.name}: {f.type_str}' for f in sync_fields[:2])}",
                        weight=0.75,
                        rule_code="INTERIOR_MUTABILITY_SYNC_FIELDS",
                        location=st.location,
                    )
                ]
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="interior_mutability_struct",
                    evidences=evidences,
                    location=st.location,
                )
                detections.append(det)

        return detections
