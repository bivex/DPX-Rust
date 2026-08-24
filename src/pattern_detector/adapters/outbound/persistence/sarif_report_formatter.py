"""OASIS SARIF v2.1.0 Report Formatter for GitHub Code Scanning & CI/CD."""

from __future__ import annotations

import json
from typing import Any

from pattern_detector.domain.detection import DetectionReport
from pattern_detector.ports.outbound import ReportFormatterPort


class SarifReportFormatter(ReportFormatterPort):
    """Formats DetectionReport as standardized OASIS SARIF v2.1.0."""

    def format(self, report: DetectionReport) -> str:
        rules_map: dict[str, dict[str, Any]] = {}
        results: list[dict[str, Any]] = []

        for d in report.detections:
            rule_id = f"DPX-RUST-{d.pattern_type.value.upper()}"
            if rule_id not in rules_map:
                rules_map[rule_id] = {
                    "id": rule_id,
                    "name": d.pattern_type.value,
                    "shortDescription": {"text": f"Rust Pattern: {d.pattern_type.value.replace('_', ' ').title()}"},
                    "fullDescription": {"text": d.summary},
                    "properties": {"category": d.pattern_category.value},
                }

            result_item: dict[str, Any] = {
                "ruleId": rule_id,
                "level": "error" if d.pattern_category.value in ("principle", "safety") else "note",
                "message": {"text": d.summary},
            }

            if d.primary_location:
                result_item["locations"] = [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": d.primary_location.file_path},
                            "region": {
                                "startLine": max(1, d.primary_location.line),
                                "startColumn": max(1, d.primary_location.column),
                            },
                        }
                    }
                ]

            results.append(result_item)

        sarif: dict[str, Any] = {
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "version": "2.1.0",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "DPX-Rust",
                            "semanticVersion": "0.1.0",
                            "rules": list(rules_map.values()),
                        }
                    },
                    "results": results,
                }
            ],
        }

        return json.dumps(sarif, indent=2, ensure_ascii=False)
