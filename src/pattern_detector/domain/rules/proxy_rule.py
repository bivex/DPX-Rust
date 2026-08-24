"""Rust Proxy Pattern Rule (impl Deref / DerefMut, Smart Pointers, Lazy Forwarders)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class ProxyPatternRule(BasePatternRule):
    """Detects Proxy pattern in Rust via Deref/DerefMut and wrapper proxies."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.PROXY

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            evidences: list[Evidence] = []
            name_lower = st.name.lower()

            if name_lower.endswith("proxy") or name_lower.endswith("guard") or "lazy" in name_lower:
                evidences.append(
                    Evidence(
                        description=f"Struct '{st.name}' follows Proxy / Smart Guard naming convention",
                        weight=0.40,
                        rule_code="PROXY_NAMING",
                        location=st.location,
                    )
                )

            impls = model.find_impls_for(st.name)
            deref_impls = [imp for imp in impls if imp.trait_name and imp.trait_name.startswith("Deref")]
            if deref_impls:
                evidences.append(
                    Evidence(
                        description=f"Implements 'Deref' trait to act as transparent smart proxy / pointer wrapper for target",
                        weight=0.55,
                        rule_code="PROXY_DEREF_IMPL",
                        location=deref_impls[0].location or st.location,
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
