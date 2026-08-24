"""Rust Chain of Responsibility Rule (middleware handler chains, tower::Service)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class ChainOfResponsibilityRule(BasePatternRule):
    """Detects Chain of Responsibility in Rust."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.CHAIN_OF_RESPONSIBILITY

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            evidences: list[Evidence] = []
            name_lower = st.name.lower()

            if name_lower.endswith("handler") or name_lower.endswith("middleware") or "chain" in name_lower:
                evidences.append(
                    Evidence(
                        description=f"Struct '{st.name}' follows Chain of Responsibility / Middleware naming convention",
                        weight=0.35,
                        rule_code="CHAIN_OF_RESPONSIBILITY_NAMING",
                        location=st.location,
                    )
                )

            # Next handler reference in fields
            next_fields = [
                f for f in st.fields
                if f.name in ("next", "next_handler", "inner", "layer", "service")
            ]
            if next_fields:
                evidences.append(
                    Evidence(
                        description=f"Maintains forward successor chain reference '{next_fields[0].name}: {next_fields[0].type_str}'",
                        weight=0.55,
                        rule_code="CHAIN_OF_RESPONSIBILITY_NEXT_FIELD",
                        location=st.location,
                    )
                )

            # Handler call / process method
            impls = model.find_impls_for(st.name)
            all_methods = dict(st.methods)
            for imp in impls:
                all_methods.update(imp.methods)

            handle_methods = [
                m for m_name, m in all_methods.items()
                if m_name in ("handle", "process", "call", "poll_ready")
            ]
            if handle_methods:
                evidences.append(
                    Evidence(
                        description=f"Provides chain processing entry point '{handle_methods[0].name}()'",
                        weight=0.35,
                        rule_code="CHAIN_OF_RESPONSIBILITY_HANDLE_METHOD",
                        location=handle_methods[0].location or st.location,
                    )
                )

            if evidences:
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="chain_handler_struct",
                    evidences=evidences,
                    location=st.location,
                )
                if det.confidence.score >= 0.50:
                    detections.append(det)

        return detections
