"""Rust State Pattern Rule (Enum state machine dispatch and transitions)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class StatePatternRule(BasePatternRule):
    """Detects State Pattern (Enum state machine) in Rust."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.STATE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for en in model.all_enums():
            evidences: list[Evidence] = []
            name_lower = en.name.lower()

            if name_lower.endswith("state") or name_lower.endswith("status") or "fsm" in name_lower:
                evidences.append(
                    Evidence(
                        description=f"Enum '{en.name}' follows State / Finite State Machine naming convention",
                        weight=0.45,
                        rule_code="STATE_NAMING",
                        location=en.location,
                    )
                )

            # Check for transition methods (transition_to, next_state, step, handle)
            impls = model.find_impls_for(en.name)
            all_methods = dict(en.methods)
            for imp in impls:
                all_methods.update(imp.methods)

            transition_methods = [
                m for m_name, m in all_methods.items()
                if m_name in ("transition", "next", "step", "handle_event", "update")
                or (m.takes_self_by_val and m.return_type in ("Self", en.name))
            ]
            if transition_methods:
                evidences.append(
                    Evidence(
                        description=f"Provides state transition method '{transition_methods[0].name}()'",
                        weight=0.45,
                        rule_code="STATE_TRANSITION_METHOD",
                        location=transition_methods[0].location or en.location,
                    )
                )

            if len(en.variants) >= 3 and (name_lower.endswith("state") or transition_methods):
                evidences.append(
                    Evidence(
                        description=f"Represents {len(en.variants)} discrete state machine modes as enum variants ({', '.join(en.variant_names[:3])})",
                        weight=0.35,
                        rule_code="STATE_VARIANTS",
                        location=en.location,
                    )
                )

            if evidences:
                det = self._create_detection(
                    target_name=en.name,
                    target_kind="state_enum",
                    evidences=evidences,
                    location=en.location,
                )
                if det.confidence.score >= 0.50:
                    detections.append(det)

        return detections
