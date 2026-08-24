"""Rust Middleware Pipeline Rule (Tower / Axum / Actix Service & Layer architecture)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class MiddlewarePipelineRule(BasePatternRule):
    """Detects Middleware Pipeline architecture in Rust (Tower Layers/Services)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.MIDDLEWARE_PIPELINE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            evidences: list[Evidence] = []
            name_lower = st.name.lower()

            if "middleware" in name_lower or name_lower.endswith("layer") or name_lower.endswith("service"):
                evidences.append(
                    Evidence(
                        description=f"Struct '{st.name}' follows Tower / Middleware naming convention",
                        weight=0.40,
                        rule_code="MIDDLEWARE_PIPELINE_NAMING",
                        location=st.location,
                    )
                )

            impls = model.find_impls_for(st.name)
            service_impls = [
                imp for imp in impls
                if imp.trait_name and ("Service" in imp.trait_name or "Layer" in imp.trait_name or "Middleware" in imp.trait_name)
            ]
            if service_impls:
                evidences.append(
                    Evidence(
                        description=f"Implements layered middleware pipeline trait '{service_impls[0].trait_name}'",
                        weight=0.60,
                        rule_code="MIDDLEWARE_PIPELINE_TRAIT_IMPL",
                        location=service_impls[0].location or st.location,
                    )
                )

            if evidences:
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="middleware_struct",
                    evidences=evidences,
                    location=st.location,
                )
                if det.confidence.score >= 0.50:
                    detections.append(det)

        return detections
