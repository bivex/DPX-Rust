"""Rust Singleton Pattern Rule (OnceLock, LazyLock, lazy_static!, OnceCell)."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType, SourceLocation


class SingletonPatternRule(BasePatternRule):
    """Detects Singleton pattern implementations in Rust."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.SINGLETON

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.modules.values():
            src = mod.raw_source
            if not src:
                continue

            # 1. Look for static OnceLock / LazyLock / OnceCell / lazy_static!
            static_matches = re.finditer(
                r"(?:pub\s+)?static\s+(?:ref\s+)?([A-Z0-9_]+)\s*:\s*(?:std::sync::)?(?:OnceLock|LazyLock|OnceCell|lazy_static|RwLock|Mutex)<([^>]+)>",
                src,
            )
            for m in static_matches:
                var_name = m.group(1)
                type_name = m.group(2).strip()
                line = src[:m.start()].count("\n") + 1
                loc = SourceLocation(file_path=mod.file_path, line=line)

                evidences: list[Evidence] = [
                    Evidence(
                        description=f"Static global singleton instance '{var_name}' synchronized via OnceLock/LazyLock/OnceCell for type '{type_name}'",
                        weight=0.75,
                        rule_code="SINGLETON_STATIC_ONCE",
                        location=loc,
                    )
                ]

                # Look for accessor function
                if f"get_{var_name.lower()}" in src or "instance" in src.lower():
                    evidences.append(
                        Evidence(
                            description=f"Provides global accessor/initialization entry point for singleton '{var_name}'",
                            weight=0.35,
                            rule_code="SINGLETON_ACCESSOR",
                            location=loc,
                        )
                    )

                det = self._create_detection(
                    target_name=var_name,
                    target_kind="static_singleton",
                    evidences=evidences,
                    location=loc,
                )
                detections.append(det)

        return detections
