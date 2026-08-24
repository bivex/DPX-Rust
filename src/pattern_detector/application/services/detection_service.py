"""Application service for running pattern detection rules against a CodeModel."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules import DEFAULT_RULES
from pattern_detector.domain.rules.base import PatternRule
from pattern_detector.domain.value_objects import PatternCategory
from pattern_detector.ports.inbound import DetectorPort, ScanOptions


class DetectionService(DetectorPort):
    """Coordinates the execution of all registered pattern detection rules."""

    def __init__(self, rules: list[PatternRule] | None = None) -> None:
        self._rules = rules if rules is not None else list(DEFAULT_RULES)

    def detect_patterns(self, model: CodeModel, options: ScanOptions | None = None) -> list[Detection]:
        options = options or ScanOptions()
        active_rules = self._filter_rules(self._rules, options)

        all_detections: list[Detection] = []
        for rule in active_rules:
            try:
                detections = rule.detect(model)
                all_detections.extend(detections)
            except Exception as e:
                if options.verbose:
                    print(f"Warning: Rule {rule.name} failed: {e}")

        return all_detections

    def _filter_rules(self, rules: list[PatternRule], options: ScanOptions) -> list[PatternRule]:
        active = rules

        if options.enabled_patterns:
            enabled_set = {p.lower().replace("-", "_") for p in options.enabled_patterns}
            active = [r for r in active if r.pattern_type.value.lower() in enabled_set]

        if options.categories:
            cat_set = set(options.categories)
            active = [r for r in active if r.pattern_category in cat_set]

        if not options.include_principles:
            active = [r for r in active if r.pattern_category != PatternCategory.PRINCIPLE]

        return active
