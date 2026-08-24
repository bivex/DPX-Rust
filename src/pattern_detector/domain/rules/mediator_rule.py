"""Rust Mediator Pattern Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class MediatorPatternRule(BasePatternRule):
    """Detects Mediator Pattern in Rust."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.MEDIATOR

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            evidences: list[Evidence] = []
            name_lower = st.name.lower()

            if name_lower.endswith("mediator") or name_lower.endswith("coordinator") or name_lower.endswith("dispatcher"):
                evidences.append(
                    Evidence(
                        description=f"Struct '{st.name}' follows Mediator / Coordinator naming convention",
                        weight=0.45,
                        rule_code="MEDIATOR_NAMING",
                        location=st.location,
                    )
                )

            participant_fields = [
                f for f in st.fields
                if "HashMap<" in f.type_str and ("Sender<" in f.type_str or "mpsc" in f.type_str or "Box<dyn" in f.type_str)
            ]
            if participant_fields:
                evidences.append(
                    Evidence(
                        description=f"Maintains decoupled participant dispatch registry '{participant_fields[0].name}: {participant_fields[0].type_str}'",
                        weight=0.55,
                        rule_code="MEDIATOR_PARTICIPANT_REGISTRY",
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
