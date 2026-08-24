"""Rust Liskov Substitution Principle (LSP) Rule (unimplemented!() / todo!() in trait impls)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class LiskovSubstitutionRule(BasePatternRule):
    """Detects LSP violations in Rust (trait impls aborting or unimplemented)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.LISKOV_SUBSTITUTION

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for imp in model.all_impls():
            if not imp.trait_name:
                continue

            for m_name, fn in imp.methods.items():
                if "unimplemented!" in fn.body or "todo!" in fn.body or "panic!(\"not supported" in fn.body:
                    evidences = [
                        Evidence(
                            description=f"LSP Violation: Trait method '{imp.trait_name}::{m_name}' in impl for '{imp.target_type}' panics or calls unimplemented!() / todo!(), violating trait contract",
                            weight=0.85,
                            rule_code="LSP_UNIMPLEMENTED_TRAIT_METHOD",
                            location=fn.location or imp.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=f"{imp.target_type}::{m_name}",
                        target_kind="trait_impl_method",
                        evidences=evidences,
                        location=fn.location or imp.location,
                    )
                    detections.append(det)

        return detections
