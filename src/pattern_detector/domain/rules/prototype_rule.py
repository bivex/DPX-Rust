"""Rust Prototype Pattern Rule (Clone trait implementation and derive)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class PrototypePatternRule(BasePatternRule):
    """Detects Prototype pattern (Clone trait) in Rust."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.PROTOTYPE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            evidences: list[Evidence] = []

            # 1. Custom impl Clone for Struct
            clone_impls = [
                imp for imp in model.find_impls_for(st.name)
                if imp.trait_name and imp.trait_name.strip() == "Clone"
            ]
            if clone_impls:
                evidences.append(
                    Evidence(
                        description=f"Explicitly implements 'Clone' trait with custom cloning/prototyping logic for '{st.name}'",
                        weight=0.60,
                        rule_code="PROTOTYPE_CUSTOM_CLONE",
                        location=clone_impls[0].location or st.location,
                    )
                )

            # 2. Derive Clone with with_* modifier methods (functional prototyping)
            if "Clone" in st.derives:
                with_methods = [
                    m for m_name, m in st.methods.items()
                    if m_name.startswith("with_") and (m.return_type in ("Self", st.name) or m.takes_self_by_val)
                ]
                if with_methods:
                    evidences.append(
                        Evidence(
                            description=f"Derives 'Clone' and provides functional prototype mutation methods ({', '.join(m.name for m in with_methods[:3])})",
                            weight=0.55,
                            rule_code="PROTOTYPE_FUNCTIONAL_WITH",
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
