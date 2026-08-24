"""Rust Adapter Pattern Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class AdapterPatternRule(BasePatternRule):
    """Detects Adapter Pattern implementations in Rust."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.ADAPTER

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        # 1. Structs with Adapter naming or wrapping inner struct
        for st in model.all_structs():
            evidences: list[Evidence] = []
            name_lower = st.name.lower()

            if name_lower.endswith("adapter") or "adapter" in name_lower:
                evidences.append(
                    Evidence(
                        description=f"Struct '{st.name}' follows Adapter naming convention",
                        weight=0.45,
                        rule_code="ADAPTER_NAMING",
                        location=st.location,
                    )
                )

            # Wraps an adaptee/inner object in fields
            inner_fields = [f for f in st.fields if f.name in ("inner", "adaptee", "backend", "driver", "source")]
            if inner_fields:
                evidences.append(
                    Evidence(
                        description=f"Wraps underlying adaptee/backend in field '{inner_fields[0].name}: {inner_fields[0].type_str}'",
                        weight=0.40,
                        rule_code="ADAPTER_WRAPS_INNER",
                        location=st.location,
                    )
                )

            # Implements a standard trait for the adapted struct
            impls = model.find_impls_for(st.name)
            trait_impls = [imp for imp in impls if imp.trait_name and imp.trait_name not in ("Debug", "Clone", "Default", "PartialEq", "Eq")]
            if trait_impls:
                evidences.append(
                    Evidence(
                        description=f"Adapts wrapped inner type to trait '{trait_impls[0].trait_name}'",
                        weight=0.40,
                        rule_code="ADAPTER_TARGET_TRAIT",
                        location=trait_impls[0].location or st.location,
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

        # 2. Implements From<T> / TryFrom<T> type conversion adapters
        for imp in model.all_impls():
            if imp.trait_name and (imp.trait_name.startswith("From<") or imp.trait_name.startswith("TryFrom<")):
                evidences = [
                    Evidence(
                        description=f"Implements '{imp.trait_name}' type adapter converting external type into '{imp.target_type}'",
                        weight=0.60,
                        rule_code="ADAPTER_FROM_IMPL",
                        location=imp.location,
                    )
                ]
                det = self._create_detection(
                    target_name=f"impl {imp.trait_name} for {imp.target_type}",
                    target_kind="adapter_impl",
                    evidences=evidences,
                    location=imp.location,
                )
                detections.append(det)

        return detections
