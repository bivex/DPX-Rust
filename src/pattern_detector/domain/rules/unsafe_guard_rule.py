"""Rust Unsafe Block & Memory Safety Guard Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType, SourceLocation


class UnsafeGuardRule(BasePatternRule):
    """Audits and catalogs unsafe { ... } blocks, raw pointer dereferencing, and unsafe fns."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.UNSAFE_BLOCK_GUARD

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.modules.values():
            src = mod.raw_source
            if not src:
                continue

            unsafe_blocks = list(re.finditer(r"\bunsafe\s*\{", src))
            unsafe_fns = list(re.finditer(r"\bunsafe\s+(?:async\s+)?fn\s+([a-zA-Z0-9_]+)", src))

            total_unsafe = len(unsafe_blocks) + len(unsafe_fns)
            if total_unsafe >= 1:
                first_pos = unsafe_blocks[0].start() if unsafe_blocks else unsafe_fns[0].start()
                line = src[:first_pos].count("\n") + 1
                loc = SourceLocation(file_path=mod.file_path, line=line)

                evidences = [
                    Evidence(
                        description=f"Safety Audit: Module '{mod.name}' contains {len(unsafe_blocks)} unsafe block(s) and {len(unsafe_fns)} unsafe function(s); ensure safety invariants are documented with // SAFETY:",
                        weight=0.70 if total_unsafe < 5 else 0.85,
                        rule_code="UNSAFE_BLOCK_AUDIT",
                        location=loc,
                    )
                ]

                det = self._create_detection(
                    target_name=f"{mod.name}::unsafe_blocks",
                    target_kind="unsafe_audit",
                    evidences=evidences,
                    location=loc,
                    metadata={"unsafe_blocks_count": len(unsafe_blocks), "unsafe_fns_count": len(unsafe_fns)},
                )
                detections.append(det)

        return detections
