"""Rust Decorator Pattern Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class DecoratorPatternRule(BasePatternRule):
    """Detects Decorator pattern in Rust (generic struct wrapping T: Trait and implementing Trait)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.DECORATOR

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            impls = model.find_impls_for(st.name)
            name_lower = st.name.lower()

            for imp in impls:
                if not imp.trait_name or imp.trait_name in ("Debug", "Clone", "Default", "Send", "Sync"):
                    continue

                evidences: list[Evidence] = []
                trait_name = imp.trait_name.split("<")[0].strip()

                # Check if struct has an inner field of generic type or Box<dyn Trait>
                inner_fields = [
                    f for f in st.fields
                    if f.name in ("inner", "wrapped", "service", "handler", "delegate", "layer")
                    or "Box<dyn" in f.type_str
                    or f.type_str in st.generics
                ]

                if inner_fields:
                    evidences.append(
                        Evidence(
                            description=f"Wraps inner component '{inner_fields[0].name}: {inner_fields[0].type_str}'",
                            weight=0.45,
                            rule_code="DECORATOR_INNER_COMPONENT",
                            location=st.location,
                        )
                    )

                if name_lower.endswith("decorator") or name_lower.endswith("wrapper") or name_lower.endswith("layer") or "logging" in name_lower or "tracing" in name_lower:
                    evidences.append(
                        Evidence(
                            description=f"Follows Decorator/Wrapper naming convention '{st.name}'",
                            weight=0.35,
                            rule_code="DECORATOR_NAMING",
                            location=st.location,
                        )
                    )

                # Implements the same trait as wrapped component
                evidences.append(
                    Evidence(
                        description=f"Implements wrapped interface trait '{imp.trait_name}' to transparently extend behavior",
                        weight=0.45,
                        rule_code="DECORATOR_SAME_TRAIT_IMPL",
                        location=imp.location or st.location,
                    )
                )

                if evidences:
                    det = self._create_detection(
                        target_name=st.name,
                        target_kind="decorator_struct",
                        evidences=evidences,
                        location=st.location,
                    )
                    if det.confidence.score >= 0.50:
                        detections.append(det)

        return detections
