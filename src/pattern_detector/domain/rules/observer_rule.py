"""Rust Observer Pattern Rule (broadcast channels, event emitters, listeners)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class ObserverPatternRule(BasePatternRule):
    """Detects Observer Pattern in Rust."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.OBSERVER

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            evidences: list[Evidence] = []
            name_lower = st.name.lower()

            if "event" in name_lower or "observer" in name_lower or "hub" in name_lower or "bus" in name_lower:
                evidences.append(
                    Evidence(
                        description=f"Struct '{st.name}' follows Observer / Event Bus naming convention",
                        weight=0.35,
                        rule_code="OBSERVER_NAMING",
                        location=st.location,
                    )
                )

            # Check for broadcast sender or channel fields
            broadcast_fields = [
                f for f in st.fields
                if "broadcast::Sender" in f.type_str
                or "sync::broadcast" in f.type_str
                or "watch::Sender" in f.type_str
                or "crossbeam" in f.type_str
                or "Vec<Box<dyn " in f.type_str
                or "listeners" in f.name
                or "subscribers" in f.name
            ]
            if broadcast_fields:
                evidences.append(
                    Evidence(
                        description=f"Maintains multi-subscriber event broadcast channel/listener list '{broadcast_fields[0].name}: {broadcast_fields[0].type_str}'",
                        weight=0.60,
                        rule_code="OBSERVER_BROADCAST_CHANNEL",
                        location=st.location,
                    )
                )

            # Check methods for subscribe / emit / notify / publish
            impls = model.find_impls_for(st.name)
            all_methods = dict(st.methods)
            for imp in impls:
                all_methods.update(imp.methods)

            event_methods = [
                m for m_name, m in all_methods.items()
                if m_name in ("subscribe", "listen", "add_listener", "emit", "publish", "notify", "send_event")
            ]
            if event_methods:
                evidences.append(
                    Evidence(
                        description=f"Provides observer subscription/dispatch method(s) ({', '.join(m.name for m in event_methods[:3])})",
                        weight=0.45,
                        rule_code="OBSERVER_DISPATCH_METHODS",
                        location=event_methods[0].location or st.location,
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
