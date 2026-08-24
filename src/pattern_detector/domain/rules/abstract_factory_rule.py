"""Rust Abstract Factory Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class AbstractFactoryRule(BasePatternRule):
    """Detects Abstract Factory traits creating families of products in Rust."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.ABSTRACT_FACTORY

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for tr in model.all_traits():
            evidences: list[Evidence] = []
            name_lower = tr.name.lower()

            if name_lower.endswith("factory") or "abstractfactory" in name_lower:
                evidences.append(
                    Evidence(
                        description=f"Trait '{tr.name}' follows Abstract Factory naming convention",
                        weight=0.45,
                        rule_code="ABSTRACT_FACTORY_NAMING",
                        location=tr.location,
                    )
                )

            # Factory methods in trait returning Box<dyn Product> or associated types
            factory_methods = [
                m for m in tr.methods.values()
                if m.name.startswith("create_") or m.name.startswith("build_") or m.name.startswith("make_") or "Box<dyn" in m.return_type
            ]
            if factory_methods:
                evidences.append(
                    Evidence(
                        description=f"Declares {len(factory_methods)} product creation method(s) in trait ({', '.join(m.name for m in factory_methods[:3])})",
                        weight=0.50,
                        rule_code="ABSTRACT_FACTORY_METHODS",
                        location=tr.location,
                    )
                )

            # Associated product types
            if len(tr.associated_types) >= 1:
                evidences.append(
                    Evidence(
                        description=f"Defines family of abstract product associated types ({', '.join(tr.associated_types[:3])})",
                        weight=0.40,
                        rule_code="ABSTRACT_FACTORY_ASSOCIATED_TYPES",
                        location=tr.location,
                    )
                )

            implementors = model.find_trait_implementors(tr.name)
            if len(implementors) >= 1:
                evidences.append(
                    Evidence(
                        description=f"Implemented by concrete factory struct(s): {', '.join(implementors[:3])}",
                        weight=0.35,
                        rule_code="ABSTRACT_FACTORY_IMPLEMENTORS",
                        location=tr.location,
                    )
                )

            if evidences:
                det = self._create_detection(
                    target_name=tr.name,
                    target_kind="trait",
                    evidences=evidences,
                    location=tr.location,
                )
                if det.confidence.score >= 0.50:
                    detections.append(det)

        return detections
