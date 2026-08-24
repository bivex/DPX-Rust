"""Rust Strategy Pattern Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class StrategyPatternRule(BasePatternRule):
    """Detects Strategy pattern in Rust (traits with multiple concrete implementors or dynamic trait object parameters)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.STRATEGY

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for tr in model.all_traits():
            if tr.name in ("Debug", "Clone", "Default", "Send", "Sync", "Display", "Drop", "Iterator"):
                continue

            implementors = model.find_trait_implementors(tr.name)
            if len(implementors) >= 2:
                evidences = [
                    Evidence(
                        description=f"Trait '{tr.name}' acts as polymorphic Strategy interface implemented by {len(implementors)} interchangeable concrete algorithms ({', '.join(implementors[:3])})",
                        weight=0.65,
                        rule_code="STRATEGY_TRAIT_INTERFACE",
                        location=tr.location,
                    )
                ]
                if tr.name.lower().endswith("strategy") or "policy" in tr.name.lower() or "algorithm" in tr.name.lower():
                    evidences.append(
                        Evidence(
                            description=f"Follows Strategy/Policy naming convention '{tr.name}'",
                            weight=0.35,
                            rule_code="STRATEGY_NAMING",
                            location=tr.location,
                        )
                    )

                det = self._create_detection(
                    target_name=tr.name,
                    target_kind="strategy_trait",
                    evidences=evidences,
                    location=tr.location,
                )
                detections.append(det)

        return detections
