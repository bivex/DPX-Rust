"""Markdown Report Formatter for Rust Pattern Detector."""

from __future__ import annotations

from pattern_detector.domain.detection import DetectionReport
from pattern_detector.ports.outbound import ReportFormatterPort


class MarkdownReportFormatter(ReportFormatterPort):
    """Formats DetectionReport as structured Markdown."""

    def format(self, report: DetectionReport) -> str:
        lines = [
            f"# 🦀 DPX-Rust: Software Design Pattern & Architecture Report",
            "",
            f"- **Target Path:** `{report.project_path}`",
            f"- **Files Scanned:** `{report.scanned_files_count}`",
            f"- **Total Patterns & Findings:** `{report.total_detections_count}`",
            f"- **Analysis Elapsed Time:** `{report.elapsed_seconds:.3f}s`",
            "",
            "## 📊 Breakdown by Category",
            "",
            "| Category | Count |",
            "|---|:---:|",
        ]
        for cat, count in report.summary_by_category.items():
            lines.append(f"| **{cat.upper()}** | {count} |")

        lines.extend([
            "",
            "## 📋 Detailed Pattern Findings",
            "",
        ])

        for idx, d in enumerate(report.detections, 1):
            loc_str = f"`{d.primary_location}`" if d.primary_location else "N/A"
            lines.extend([
                f"### #{idx} {d.pattern_type.value.upper()} on `{d.target_name}`",
                f"- **Category:** `{d.pattern_category.value}`",
                f"- **Confidence:** **{d.confidence.percentage_str}** [{d.level.value.upper()}]",
                f"- **Primary Location:** {loc_str}",
                f"- **Summary:** {d.summary}",
                "",
                "#### Evidence Trail:",
            ])
            for ev in d.evidences:
                ev_loc = f" -> `{ev.location}`" if ev.location else ""
                lines.append(f"- `+{int(ev.weight * 100)}%` **[{ev.rule_code}]** {ev.description}{ev_loc}")
            lines.append("")

        return "\n".join(lines)
