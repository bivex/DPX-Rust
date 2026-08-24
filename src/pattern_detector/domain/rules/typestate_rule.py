"""Rust Typestate Pattern Rule (PhantomData<State> compile-time state machines)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class TypestatePatternRule(BasePatternRule):
    """Detects Typestate Pattern in Rust using PhantomData markers and consuming self transitions."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.TYPESTATE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            evidences: list[Evidence] = []

            # 1. Has PhantomData field representing compile-time state
            phantom_fields = [
                f for f in st.fields
                if "PhantomData<" in f.type_str or "_state" in f.name or "marker" in f.name
            ]
            if phantom_fields:
                evidences.append(
                    Evidence(
                        description=f"Uses zero-cost marker field '{phantom_fields[0].name}: {phantom_fields[0].type_str}' to track compile-time typestate",
                        weight=0.60,
                        rule_code="TYPESTATE_PHANTOM_MARKER",
                        location=st.location,
                    )
                )

            # 2. Methods consuming `self` (by-value) and returning new struct state
            impls = model.find_impls_for(st.name)
            all_methods = dict(st.methods)
            for imp in impls:
                all_methods.update(imp.methods)

            transition_methods = [
                m for m in all_methods.values()
                if m.takes_self_by_val and m.name not in ("build", "into_inner", "drop")
            ]
            if transition_methods:
                evidences.append(
                    Evidence(
                        description=f"Contains {len(transition_methods)} by-value consuming state transition method(s) ({', '.join(m.name for m in transition_methods[:3])})",
                        weight=0.45,
                        rule_code="TYPESTATE_CONSUMING_TRANSITION",
                        location=transition_methods[0].location or st.location,
                    )
                )

            if phantom_fields and transition_methods:
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="typestate_struct",
                    evidences=evidences,
                    location=st.location,
                )
                detections.append(det)

        return detections
