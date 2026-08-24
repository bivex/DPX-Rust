"""Rust Facade Pattern Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class FacadePatternRule(BasePatternRule):
    """Detects Facade Pattern in Rust."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.FACADE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            evidences: list[Evidence] = []
            name_lower = st.name.lower()

            if name_lower.endswith("facade") or name_lower.endswith("client") or name_lower.endswith("engine") or name_lower.endswith("manager"):
                evidences.append(
                    Evidence(
                        description=f"Struct '{st.name}' follows Facade / High-Level Client naming convention",
                        weight=0.40,
                        rule_code="FACADE_NAMING",
                        location=st.location,
                    )
                )

            # High-level aggregator of multiple subsystem fields
            if len(st.fields) >= 3 and not st.is_tuple:
                subsystem_fields = [f for f in st.fields if f.type_str[0].isupper()]
                if len(subsystem_fields) >= 2:
                    evidences.append(
                        Evidence(
                            description=f"Aggregates {len(subsystem_fields)} subsystem components ({', '.join(f.name for f in subsystem_fields[:3])})",
                            weight=0.40,
                            rule_code="FACADE_AGGREGATES_SUBSYSTEMS",
                            location=st.location,
                        )
                    )

            # Public delegating methods
            impls = model.find_impls_for(st.name)
            pub_methods = []
            for imp in impls:
                pub_methods.extend([m for m in imp.methods.values() if m.name not in ("new", "default")])

            if len(pub_methods) >= 3:
                evidences.append(
                    Evidence(
                        description=f"Exposes {len(pub_methods)} unified high-level operations delegating to internal subsystems",
                        weight=0.35,
                        rule_code="FACADE_UNIFIED_API",
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
