"""Rust Factory Method Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class FactoryMethodRule(BasePatternRule):
    """Detects Factory Method implementations in Rust (fn new, fn create, fn from_*)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.FACTORY_METHOD

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            impls = model.find_impls_for(st.name)
            all_methods = dict(st.methods)
            for imp in impls:
                if not imp.trait_name:  # inherent impl
                    all_methods.update(imp.methods)

            for m_name, fn in all_methods.items():
                evidences: list[Evidence] = []
                # Factory methods in Rust are associated functions (no self) returning Self or Result<Self, E>
                if fn.is_associated_fn and (
                    fn.return_type in ("Self", st.name, f"Result<Self, ", f"Result<{st.name}, ")
                    or fn.return_type.startswith("Self")
                    or fn.return_type.startswith(st.name)
                ):
                    if m_name in ("new", "default", "create", "make"):
                        evidences.append(
                            Evidence(
                                description=f"Provides standard factory constructor '{st.name}::{m_name}()' returning {fn.return_type}",
                                weight=0.55,
                                rule_code="FACTORY_METHOD_CONSTRUCTOR",
                                location=fn.location or st.location,
                            )
                        )
                    elif m_name.startswith("from_") or m_name.startswith("with_") or m_name.startswith("open_"):
                        evidences.append(
                            Evidence(
                                description=f"Provides specialized domain factory method '{st.name}::{m_name}()' constructing {fn.return_type}",
                                weight=0.60,
                                rule_code="FACTORY_METHOD_NAMED_CONSTRUCTOR",
                                location=fn.location or st.location,
                            )
                        )

                    if len(fn.params) >= 1:
                        evidences.append(
                            Evidence(
                                description=f"Encapsulates parameterized construction across {len(fn.params)} input parameter(s)",
                                weight=0.30,
                                rule_code="FACTORY_METHOD_PARAMETERIZED",
                                location=fn.location or st.location,
                            )
                        )

                    if evidences:
                        det = self._create_detection(
                            target_name=f"{st.name}::{m_name}",
                            target_kind="factory_method",
                            evidences=evidences,
                            location=fn.location or st.location,
                        )
                        if det.confidence.score >= 0.50:
                            detections.append(det)

        return detections
