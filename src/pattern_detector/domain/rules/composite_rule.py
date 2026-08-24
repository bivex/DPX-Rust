"""Rust Composite Pattern Rule (recursive enum trees or struct child collections)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class CompositePatternRule(BasePatternRule):
    """Detects Composite Pattern in Rust (AST trees, hierarchical nodes)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.COMPOSITE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        # 1. Enums with recursive variants (Box<Self>, Vec<Self>)
        for en in model.all_enums():
            evidences: list[Evidence] = []
            recursive_variants = [
                v for v in en.variants
                if any("Self" in f[1] or en.name in f[1] for f in v.fields)
            ]
            if recursive_variants:
                evidences.append(
                    Evidence(
                        description=f"Enum '{en.name}' contains recursive composite branches ({', '.join(v.name for v in recursive_variants[:3])})",
                        weight=0.70,
                        rule_code="COMPOSITE_RECURSIVE_ENUM",
                        location=en.location,
                    )
                )

            if evidences:
                det = self._create_detection(
                    target_name=en.name,
                    target_kind="composite_enum",
                    evidences=evidences,
                    location=en.location,
                )
                detections.append(det)

        # 2. Structs with children collections (Vec<Box<dyn Component>> or Vec<Self>)
        for st in model.all_structs():
            evidences = []
            child_fields = [
                f for f in st.fields
                if f.name in ("children", "nodes", "sub_items", "elements", "branches")
                or f.type_str in (f"Vec<{st.name}>", f"Vec<Box<{st.name}>>", "Vec<Box<dyn ")
            ]
            if child_fields:
                evidences.append(
                    Evidence(
                        description=f"Struct '{st.name}' contains composite hierarchical child collection '{child_fields[0].name}: {child_fields[0].type_str}'",
                        weight=0.65,
                        rule_code="COMPOSITE_STRUCT_CHILDREN",
                        location=st.location,
                    )
                )

            if evidences:
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="composite_struct",
                    evidences=evidences,
                    location=st.location,
                )
                detections.append(det)

        return detections
