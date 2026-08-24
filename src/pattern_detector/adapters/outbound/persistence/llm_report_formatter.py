"""LLM Report Formatter for generating AI Architectural Context Prompts."""

from __future__ import annotations

from pattern_detector.domain.detection import DetectionReport
from pattern_detector.ports.outbound import ReportFormatterPort


class LlmReportFormatter(ReportFormatterPort):
    """Formats DetectionReport as optimized context prompt for LLM architects."""

    def format(self, report: DetectionReport) -> str:
        return self.format_scan_report(report)

    def format_scan_report(self, report: DetectionReport) -> str:
        lines = [
            "<codebase_architecture_analysis>",
            f"<project_path>{report.project_path}</project_path>",
            f"<scanned_files>{report.scanned_files_count}</scanned_files>",
            f"<total_findings>{report.total_detections_count}</total_findings>",
            "<architectural_patterns>",
        ]
        for d in report.detections:
            loc = f" location=\"{d.primary_location}\"" if d.primary_location else ""
            lines.append(
                f"  <detection type=\"{d.pattern_type.value}\" category=\"{d.pattern_category.value}\" target=\"{d.target_name}\" confidence=\"{d.confidence.percentage_str}\"{loc}>"
            )
            for ev in d.evidences:
                lines.append(f"    <evidence rule=\"{ev.rule_code}\" weight=\"{ev.weight}\">{ev.description}</evidence>")
            lines.append("  </detection>")

        lines.extend([
            "</architectural_patterns>",
            "</codebase_architecture_analysis>",
        ])
        return "\n".join(lines)
