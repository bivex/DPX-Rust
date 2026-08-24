"""JSON Report Formatter for Rust Pattern Detector."""

from __future__ import annotations

import json
from typing import Any

from pattern_detector.domain.detection import DetectionReport
from pattern_detector.ports.outbound import ReportFormatterPort


class JsonReportFormatter(ReportFormatterPort):
    """Formats DetectionReport as pretty-printed JSON."""

    def format(self, report: DetectionReport) -> str:
        data: dict[str, Any] = {
            "project_path": report.project_path,
            "scanned_files_count": report.scanned_files_count,
            "total_detections_count": report.total_detections_count,
            "elapsed_seconds": round(report.elapsed_seconds, 4),
            "summary_by_category": report.summary_by_category,
            "summary_by_confidence_level": report.summary_by_confidence_level,
            "detections": [
                {
                    "pattern_type": d.pattern_type.value,
                    "pattern_category": d.pattern_category.value,
                    "target_name": d.target_name,
                    "target_kind": d.target_kind,
                    "confidence": {
                        "score": round(d.confidence.score, 4),
                        "level": d.level.value,
                        "percentage": d.confidence.percentage_str,
                    },
                    "primary_location": str(d.primary_location) if d.primary_location else None,
                    "evidences": [
                        {
                            "description": e.description,
                            "weight": e.weight,
                            "rule_code": e.rule_code,
                            "location": str(e.location) if e.location else None,
                        }
                        for e in d.evidences
                    ],
                    "metadata": d.metadata,
                }
                for d in report.detections
            ],
        }
        return json.dumps(data, indent=2, ensure_ascii=False)
