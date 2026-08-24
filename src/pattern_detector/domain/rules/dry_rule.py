"""Rust Don't Repeat Yourself (DRY) Rule."""

from __future__ import annotations

import hashlib
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class DryRule(BasePatternRule):
    """Detects duplicate function and method implementations in Rust."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.DRY

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        body_hashes: dict[str, list[tuple[str, any]]] = {}

        for fn in model.all_functions():
            clean_body = "".join(fn.body.split())
            if len(clean_body) >= 60 and fn.name not in ("new", "default", "clone", "drop"):
                h = hashlib.md5(clean_body.encode("utf-8")).hexdigest()
                body_hashes.setdefault(h, []).append((fn.name, fn))

        for h, duplicates in body_hashes.items():
            if len(duplicates) >= 2:
                primary_name, primary_fn = duplicates[0]
                other_names = [d[0] for d in duplicates[1:]]
                evidences = [
                    Evidence(
                        description=f"DRY Violation: Identical implementation logic duplicated across {len(duplicates)} functions ({primary_name}, {', '.join(other_names[:3])})",
                        weight=0.80,
                        rule_code="DRY_CODE_DUPLICATION",
                        location=primary_fn.location,
                    )
                ]
                det = self._create_detection(
                    target_name=primary_name,
                    target_kind="dry_duplicated_code",
                    evidences=evidences,
                    location=primary_fn.location,
                    related_locations=[d[1].location for d in duplicates[1:] if d[1].location],
                )
                detections.append(det)

        return detections
