"""Standalone, interactive Semantic UI (Fomantic-UI) HTML dashboard formatter for Rust Pattern Detector."""

from __future__ import annotations

import html
import os
from typing import Any

from pattern_detector.domain.detection import Detection, DetectionReport
from pattern_detector.domain.value_objects import (
    ConfidenceLevel,
    PatternCategory,
    PatternType,
)
from pattern_detector.ports.outbound import ReportFormatterPort

CATEGORY_STYLES = {
    PatternCategory.CREATIONAL: {
        "color": "teal",
        "icon": "cubes",
        "name": "Creational Patterns",
        "badge_bg": "rgba(45, 212, 191, 0.15)",
        "badge_border": "rgba(45, 212, 191, 0.4)",
        "badge_text": "#2dd4bf",
        "accent": "#2dd4bf",
        "label_color": "teal",
    },
    PatternCategory.STRUCTURAL: {
        "color": "blue",
        "icon": "sitemap",
        "name": "Structural Patterns",
        "badge_bg": "rgba(56, 189, 248, 0.15)",
        "badge_border": "rgba(56, 189, 248, 0.4)",
        "badge_text": "#38bdf8",
        "accent": "#38bdf8",
        "label_color": "blue",
    },
    PatternCategory.BEHAVIORAL: {
        "color": "violet",
        "icon": "random",
        "name": "Behavioral Patterns",
        "badge_bg": "rgba(167, 139, 250, 0.15)",
        "badge_border": "rgba(167, 139, 250, 0.4)",
        "badge_text": "#a78bfa",
        "accent": "#a78bfa",
        "label_color": "violet",
    },
    PatternCategory.IDIOM: {
        "color": "orange",
        "icon": "bolt",
        "name": "Rust Idioms & Typestates",
        "badge_bg": "rgba(251, 146, 60, 0.15)",
        "badge_border": "rgba(251, 146, 60, 0.4)",
        "badge_text": "#fb923c",
        "accent": "#fb923c",
        "label_color": "orange",
    },
    PatternCategory.ARCHITECTURAL: {
        "color": "purple",
        "icon": "project diagram",
        "name": "Architectural Patterns",
        "badge_bg": "rgba(192, 132, 252, 0.15)",
        "badge_border": "rgba(192, 132, 252, 0.4)",
        "badge_text": "#c084fc",
        "accent": "#c084fc",
        "label_color": "purple",
    },
    PatternCategory.PRINCIPLE: {
        "color": "pink",
        "icon": "shield alternate",
        "name": "Principles & SOLID",
        "badge_bg": "rgba(244, 114, 182, 0.15)",
        "badge_border": "rgba(244, 114, 182, 0.4)",
        "badge_text": "#f472b6",
        "accent": "#f472b6",
        "label_color": "pink",
    },
    PatternCategory.SAFETY: {
        "color": "red",
        "icon": "exclamation triangle",
        "name": "Unsafe & Memory Safety",
        "badge_bg": "rgba(248, 113, 113, 0.15)",
        "badge_border": "rgba(248, 113, 113, 0.4)",
        "badge_text": "#f87171",
        "accent": "#f87171",
        "label_color": "red",
    },
}

_HTML_DASHBOARD_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🦀 DPX-Rust: Architecture & Pattern Dashboard - {project_name}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/fomantic-ui/2.9.3/semantic.min.css">
    <style>
        :root {{
            --bg-main: #0b0f19;
            --bg-card: #131b2e;
            --border-color: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
        }}
        body {{
            background-color: var(--bg-main) !important;
            color: var(--text-primary) !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            padding: 30px 15px;
        }}
        .ui.container {{
            max-width: 1200px !important;
        }}
        .header-box {{
            background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
            border: 1px solid #312e81;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 25px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        }}
        .kpi-card {{
            background: var(--bg-card) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 10px !important;
            padding: 16px !important;
            text-align: center;
        }}
        .pattern-card {{
            background: var(--bg-card) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 10px !important;
            margin-bottom: 16px !important;
            padding: 20px !important;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .pattern-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.4);
            border-color: #3b82f6 !important;
        }}
        .evidence-box {{
            background: #090d16;
            border-radius: 6px;
            padding: 12px 16px;
            margin-top: 12px;
            border-left: 3px solid #38bdf8;
            font-size: 13px;
        }}
        .code-pill {{
            background: #1e293b;
            color: #38bdf8;
            padding: 3px 8px;
            border-radius: 4px;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="ui container">
        <!-- Header -->
        <div class="header-box">
            <div class="ui grid stackable middle aligned">
                <div class="ten wide column">
                    <h1 class="ui header inverted" style="margin: 0; font-size: 28px;">
                        🦀 DPX-Rust Pattern Scanner & Architecture Dashboard
                        <div class="sub header" style="color: #a5b4fc; margin-top: 6px;">
                            Static Analysis, Gang of Four Patterns, Rust Idioms & Safety Guard for <strong>{project_name}</strong>
                        </div>
                    </h1>
                </div>
                <div class="six wide column right aligned">
                    <button id="copyLlmBtn" class="ui purple button" onclick="copyArchMapForLlm()">
                        <i class="copy icon"></i> Copy Architecture Map for LLM
                    </button>
                    <textarea id="llmArchMapRaw" style="display:none;">{llm_arch_map_raw}</textarea>
                </div>
            </div>
        </div>

        <!-- KPI Metrics Grid -->
        <div class="ui grid stackable four column" style="margin-bottom: 20px;">
            <div class="column">
                <div class="kpi-card">
                    <div style="font-size: 28px; font-weight: 700; color: #38bdf8;">{total_detections}</div>
                    <div style="color: #94a3b8; font-size: 13px; margin-top: 4px;">Total Findings</div>
                </div>
            </div>
            <div class="column">
                <div class="kpi-card">
                    <div style="font-size: 28px; font-weight: 700; color: #f87171;">{total_violations}</div>
                    <div style="color: #94a3b8; font-size: 13px; margin-top: 4px;">Violations / Smells</div>
                </div>
            </div>
            <div class="column">
                <div class="kpi-card">
                    <div style="font-size: 28px; font-weight: 700; color: #fb923c;">{total_patterns}</div>
                    <div style="color: #94a3b8; font-size: 13px; margin-top: 4px;">Patterns & Idioms</div>
                </div>
            </div>
            <div class="column">
                <div class="kpi-card">
                    <div style="font-size: 28px; font-weight: 700; color: #a78bfa;">{scanned_files} files</div>
                    <div style="color: #94a3b8; font-size: 13px; margin-top: 4px;">Scan Time: {elapsed_seconds}s</div>
                </div>
            </div>
        </div>

        <!-- Category Filter Pills -->
        <div class="ui secondary pointing menu inverted" style="border-color: #1e293b; margin-bottom: 16px; overflow-x: auto;">
            <a class="item active cat-filter-btn" data-filter="all">
                <i class="layer group icon"></i> All Findings
            </a>
            {category_filters}
        </div>

        <!-- Action Status Sub-Tabs Bar -->
        <div class="ui inverted segment" style="background: #0f172a; border: 1px solid #1e293b; border-radius: 8px; margin-bottom: 16px; padding: 10px 16px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
            <div class="ui mini inverted basic buttons" id="statusFilterGroup">
                <button class="ui button active status-filter-btn" data-status="all">
                    <i class="eye icon"></i> All <span class="ui mini blue label" id="statusCountAll">{total_detections}</span>
                </button>
                <button class="ui button status-filter-btn" data-status="violation" style="color: #f87171 !important;">
                    <i class="exclamation triangle icon"></i> ⚠️ Violations <span class="ui mini red label" id="statusCountViolation">{total_violations}</span>
                </button>
                <button class="ui button status-filter-btn" data-status="adherence" style="color: #4ade80 !important;">
                    <i class="check circle icon"></i> ✅ Adherences <span class="ui mini green label" id="statusCountAdherence">{total_adherences}</span>
                </button>
                <button class="ui button status-filter-btn" data-status="pattern" style="color: #38bdf8 !important;">
                    <i class="cube icon"></i> 🔷 Patterns & Idioms <span class="ui mini teal label" id="statusCountPattern">{total_patterns}</span>
                </button>
            </div>
            <div>
                <button id="principlesToggleBtn" class="ui mini inverted basic button" onclick="togglePrinciplesVisibility()" style="border-color: #4f46e5; color: #a5b4fc; font-weight: 600;">
                    <i class="shield alternate icon" style="color: #818cf8;"></i> <span id="principlesToggleText">Hide SOLID & Principles</span>
                </button>
            </div>
        </div>

        <!-- Search Bar -->
        <div class="ui fluid icon inverted input" style="margin-bottom: 20px;">
            <input type="text" id="searchInput" placeholder="🔎 Instant search by pattern name, struct/trait, category, or rule (e.g. builder, typestate, drop, srp, raii)..." style="background: #0f172a; border: 1px solid #1e293b; color: #f8fafc; padding: 12px 16px;">
            <i class="search icon"></i>
        </div>

        <!-- Zero Violations Alert -->
        <div id="noViolationsAlert" class="ui positive icon message" style="display: none; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.35); color: #86efac; margin-bottom: 20px; border-radius: 8px;">
            <i class="check circle outline icon" style="color: #34d399;"></i>
            <div class="content">
                <div class="header" style="color: #34d399; font-size: 16px; font-weight: 700;">Zero Violations Found!</div>
                <p style="color: #cbd5e1; margin-top: 4px;">All evaluated code conforms cleanly to idiomatic Rust architecture and safety guidelines.</p>
            </div>
        </div>

        <!-- No Matching Results Message -->
        <div id="noResultsMessage" class="ui inverted segment" style="display: none; background: #0f172a; border: 1px solid #1e293b; text-align: center; padding: 30px; border-radius: 8px;">
            <i class="search icon" style="font-size: 24px; color: #64748b; margin-bottom: 10px;"></i>
            <div style="color: #94a3b8; font-size: 15px;">No findings match the selected category, action status, or search query.</div>
        </div>

        <!-- Pattern Cards Container -->
        <div id="cardsContainer">
            {cards_html}
        </div>
    </div>

    <script>
        const searchInput = document.getElementById('searchInput');
        const cards = document.querySelectorAll('.pattern-card');
        const categoryBtns = document.querySelectorAll('.cat-filter-btn');
        const statusBtns = document.querySelectorAll('.status-filter-btn');
        const noViolationsAlert = document.getElementById('noViolationsAlert');
        const noResultsMessage = document.getElementById('noResultsMessage');

        let selectedCategory = 'all';
        let selectedStatus = 'all';
        let hidePrinciples = false;

        function togglePrinciplesVisibility() {{
            hidePrinciples = !hidePrinciples;
            const btn = document.getElementById('principlesToggleBtn');
            const btnText = document.getElementById('principlesToggleText');
            if (hidePrinciples) {{
                btn.classList.remove('basic');
                btn.classList.add('purple');
                btnText.textContent = 'Show SOLID & Principles';
            }} else {{
                btn.classList.remove('purple');
                btn.classList.add('basic');
                btnText.textContent = 'Hide SOLID & Principles';
            }}
            updateStatusCounts();
            filterCards();
        }}

        function updateStatusCounts() {{
            let total = 0, violations = 0, adherences = 0, patterns = 0;
            cards.forEach(card => {{
                const category = card.dataset.category || '';
                const status = card.dataset.status || '';
                if (hidePrinciples && category === 'principle') {{
                    return;
                }}
                if (selectedCategory === 'all' || category === selectedCategory) {{
                    total++;
                    if (status === 'violation') violations++;
                    if (status === 'adherence') adherences++;
                    if (status === 'pattern') patterns++;
                }}
            }});
            document.getElementById('statusCountAll').textContent = total;
            document.getElementById('statusCountViolation').textContent = violations;
            document.getElementById('statusCountAdherence').textContent = adherences;
            document.getElementById('statusCountPattern').textContent = patterns;
        }}

        function filterCards() {{
            const query = searchInput.value.toLowerCase();
            let visibleCount = 0;

            cards.forEach(card => {{
                const text = card.textContent.toLowerCase();
                const pattern = card.dataset.pattern || '';
                const category = card.dataset.category || '';
                const target = card.dataset.target || '';
                const status = card.dataset.status || '';

                if (hidePrinciples && category === 'principle') {{
                    card.style.display = 'none';
                    return;
                }}

                const matchesCategory = (selectedCategory === 'all' || category === selectedCategory);
                const matchesStatus = (selectedStatus === 'all' || status === selectedStatus);
                const matchesSearch = (!query || text.includes(query) || pattern.includes(query) || category.includes(query) || target.includes(query));

                if (matchesCategory && matchesStatus && matchesSearch) {{
                    card.style.display = 'block';
                    visibleCount++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});

            if (selectedStatus === 'violation' && visibleCount === 0) {{
                noViolationsAlert.style.display = 'flex';
                noResultsMessage.style.display = 'none';
            }} else if (visibleCount === 0) {{
                noViolationsAlert.style.display = 'none';
                noResultsMessage.style.display = 'block';
            }} else {{
                noViolationsAlert.style.display = 'none';
                noResultsMessage.style.display = 'none';
            }}
        }}

        searchInput.addEventListener('input', filterCards);

        categoryBtns.forEach(btn => {{
            btn.addEventListener('click', () => {{
                categoryBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                selectedCategory = btn.dataset.filter;
                updateStatusCounts();
                filterCards();
            }});
        }});

        statusBtns.forEach(btn => {{
            btn.addEventListener('click', () => {{
                statusBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                selectedStatus = btn.dataset.status;
                filterCards();
            }});
        }});

        function copyArchMapForLlm() {{
            const rawText = document.getElementById('llmArchMapRaw').value;
            const btn = document.getElementById('copyLlmBtn');
            const originalHtml = btn.innerHTML;

            if (navigator.clipboard && navigator.clipboard.writeText) {{
                navigator.clipboard.writeText(rawText).then(() => {{
                    btn.innerHTML = '<i class="check icon"></i> Copied to Clipboard!';
                    setTimeout(() => {{ btn.innerHTML = originalHtml; }}, 2000);
                }});
            }}
        }}

        updateStatusCounts();
    </script>
</body>
</html>
"""


class HtmlReportFormatter(ReportFormatterPort):
    """Renders a standalone, responsive, interactive Semantic UI HTML dashboard for Rust DetectionReport."""

    def __init__(self, include_principles: bool = True) -> None:
        self.include_principles = include_principles

    def format(self, report: DetectionReport, include_principles: bool | None = None) -> str:
        inc_principles = self.include_principles if include_principles is None else include_principles

        if not inc_principles:
            detections = [d for d in report.detections if d.pattern_category != PatternCategory.PRINCIPLE]
        else:
            detections = report.detections

        project_name = html.escape(os.path.basename(os.path.abspath(report.project_path)) or "Rust Crate")
        counts = self._count_detection_statuses(detections)
        category_filters = "".join(self._render_category_filters(detections))
        cards_html = "".join(self._render_cards_list(detections))
        llm_arch_map = self._build_llm_architectural_map(report, counts, project_name, detections=detections)

        return _HTML_DASHBOARD_TEMPLATE.format(
            project_name=project_name,
            total_detections=len(detections),
            total_violations=counts["violation"],
            total_adherences=counts["adherence"],
            total_patterns=counts["pattern"],
            scanned_files=report.scanned_files_count,
            elapsed_seconds=f"{report.elapsed_seconds:.3f}",
            category_filters=category_filters,
            cards_html=cards_html,
            llm_arch_map_raw=html.escape(llm_arch_map),
        )

    def _classify_detection_status(self, det: Detection) -> str:
        if det.pattern_category == PatternCategory.SAFETY:
            return "violation"
        if det.pattern_category == PatternCategory.PRINCIPLE:
            if det.pattern_type in (PatternType.DEPENDENCY_INVERSION, PatternType.COMPOSITION_OVER_INHERITANCE):
                return "adherence"
            return "violation"
        if det.pattern_type == PatternType.CIRCULAR_DEPENDENCY:
            return "violation"
        return "pattern"

    def _count_detection_statuses(self, detections: list[Detection]) -> dict[str, int]:
        counts = {"violation": 0, "adherence": 0, "pattern": 0}
        for d in detections:
            status = self._classify_detection_status(d)
            counts[status] += 1
        return counts

    def _render_category_filters(self, detections: list[Detection]) -> list[str]:
        cat_counts: dict[str, int] = {}
        for d in detections:
            cat_val = d.pattern_category.value
            cat_counts[cat_val] = cat_counts.get(cat_val, 0) + 1

        filters = []
        for cat_enum, style in CATEGORY_STYLES.items():
            count = cat_counts.get(cat_enum.value, 0)
            if count > 0:
                filters.append(
                    f"""
                    <a class="item cat-filter-btn" data-filter="{cat_enum.value}">
                        <i class="{style['icon']} icon" style="color: {style['accent']};"></i>
                        {style['name']}
                        <div class="ui mini {style['label_color']} label">{count}</div>
                    </a>
                    """
                )
        return filters

    def _render_cards_list(self, detections: list[Detection]) -> list[str]:
        cards = []
        for idx, det in enumerate(detections, 1):
            status = self._classify_detection_status(det)
            cat_style = CATEGORY_STYLES.get(det.pattern_category, CATEGORY_STYLES[PatternCategory.STRUCTURAL])
            loc_str = html.escape(str(det.primary_location)) if det.primary_location else "N/A"

            evidences_html = []
            for ev in det.evidences:
                ev_loc = f" <span class='code-pill'>{html.escape(str(ev.location))}</span>" if ev.location else ""
                evidences_html.append(
                    f"""
                    <div style="margin-top: 4px;">
                        <span style="color: #38bdf8; font-weight: 600;">+{int(ev.weight * 100)}%</span>
                        <span class="code-pill">[{html.escape(ev.rule_code)}]</span>
                        {html.escape(ev.description)}{ev_loc}
                    </div>
                    """
                )

            cards.append(
                f"""
                <div class="pattern-card" data-category="{det.pattern_category.value}" data-pattern="{det.pattern_type.value}" data-status="{status}" data-target="{html.escape(det.target_name.lower())}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span class="ui mini {cat_style['label_color']} label">#{idx} {det.pattern_type.value.upper()}</span>
                            <strong style="font-size: 16px; margin-left: 8px; color: #f8fafc;">{html.escape(det.target_name)}</strong>
                            <span style="color: #94a3b8; font-size: 13px;">({det.target_kind})</span>
                        </div>
                        <div>
                            <span class="ui mini label" style="background: {cat_style['badge_bg']}; color: {cat_style['badge_text']}; border: 1px solid {cat_style['badge_border']};">
                                {det.confidence.percentage_str} [{det.level.value.upper()}]
                            </span>
                        </div>
                    </div>
                    <div style="margin-top: 10px; font-size: 13px; color: #cbd5e1;">
                        {html.escape(det.summary)}
                    </div>
                    <div style="margin-top: 6px; font-size: 12px; color: #64748b;">
                        <i class="map marker alternate icon"></i> {loc_str}
                    </div>
                    <div class="evidence-box">
                        <strong>Evidence Trail ({len(det.evidences)} heuristics):</strong>
                        {''.join(evidences_html)}
                    </div>
                </div>
                """
            )
        return cards

    def _build_llm_architectural_map(
        self,
        report: DetectionReport,
        counts: dict[str, int],
        project_name: str,
        detections: list[Detection] | None = None,
    ) -> str:
        dets = report.detections if detections is None else detections
        lines = [
            "# 🦀 DPX-Rust: Codebase Architecture Map & Refactoring Analysis",
            "",
            "## 📌 Project Overview",
            f"- **Target Project:** `{project_name}`",
            f"- **Files Scanned:** `{report.scanned_files_count}`",
            f"- **Total Architecture Findings:** `{len(dets)}`",
            f"- **⚠️ Violations / Smells:** `{counts.get('violation', 0)}`",
            f"- **🔷 Patterns & Idioms:** `{counts.get('pattern', 0)}`",
            f"- **✅ Clean Adherences:** `{counts.get('adherence', 0)}`",
            "",
            "---",
            "",
            "## 🎯 Task for AI / LLM Rust Architect",
            "> **Prompt Instructions:**",
            "> 1. **Analyze Modularity & Trait Abstractions:** Review struct/trait distributions, high-coupling components, and decoupling.",
            "> 2. **Review Safety Invariants & Smells:** Audit any unsafe blocks, KISS complexity, and cyclic dependencies.",
            "> 3. **Propose Idiomatic Rust Refactorings:** Suggest Builder, Typestate, or Tower Service architectures with concrete code signatures.",
            "> 4. **SOLID Improvements:** Explain how to resolve the identified smells cleanly.",
            "",
            "---",
            "",
        ]

        patterns_by_type: dict[str, list[Detection]] = {}
        violations_by_type: dict[str, list[Detection]] = {}
        adherences_by_type: dict[str, list[Detection]] = {}
        file_to_findings: dict[str, list[str]] = {}

        for d in dets:
            status = self._classify_detection_status(d)
            ptype = d.pattern_type.value.upper()
            if status == "pattern":
                patterns_by_type.setdefault(ptype, []).append(d)
            elif status == "violation":
                violations_by_type.setdefault(ptype, []).append(d)
            else:
                adherences_by_type.setdefault(ptype, []).append(d)

            loc_file = d.primary_location.file_path if d.primary_location and d.primary_location.file_path else "unknown"
            short_file = loc_file.replace("\\", "/").split("/")[-1]
            file_to_findings.setdefault(short_file, []).append(f"{ptype} ({status})")

        # 1. Design Patterns & Idioms
        lines.append(f"## 🔷 Active Design Patterns & Rust Idioms ({counts.get('pattern', 0)} instances)")
        if patterns_by_type:
            for ptype, items in sorted(patterns_by_type.items()):
                lines.append(f"### Pattern: `{ptype}` ({len(items)} instances)")
                for d in items:
                    loc = f"{d.primary_location.file_path}:{d.primary_location.line}" if d.primary_location else ""
                    loc_str = f" in `{loc}`" if loc else ""
                    lines.append(f"- **{d.target_name}** ({d.target_kind}, confidence {d.confidence.percentage_str}){loc_str}")
                    lines.append(f"  - *Summary:* {d.summary}")
            lines.append("")
        else:
            lines.append("*No design patterns identified.*\n")

        lines.append("---")
        lines.append("")

        # 2. Violations & Code Smells
        if violations_by_type:
            lines.append(f"## ⚠️ Architectural Violations & Code Smells ({counts.get('violation', 0)} instances)")
            for vtype, items in sorted(violations_by_type.items()):
                lines.append(f"### Violation: `{vtype}` ({len(items)} occurrences)")
                for d in items[:35]:
                    loc = f"{d.primary_location.file_path}:{d.primary_location.line}" if d.primary_location else ""
                    loc_str = f" in `{loc}`" if loc else ""
                    lines.append(f"- **{d.target_name}** ({d.confidence.percentage_str}){loc_str}")
                    lines.append(f"  - *Risk / Smell:* {d.summary}")
                    for ev in d.evidences[:2]:
                        lines.append(f"  - *Evidence:* `+{int(ev.weight * 100)}%` [{ev.rule_code}] {ev.description}")
                if len(items) > 35:
                    lines.append(f"  *(... and {len(items) - 35} more {vtype} occurrences)*")
            lines.append("")
            lines.append("---")
            lines.append("")

        # 3. Clean Adherences
        if adherences_by_type:
            lines.append(f"## ✅ Clean Architectural Adherences ({counts.get('adherence', 0)} instances)")
            for atype, items in sorted(adherences_by_type.items()):
                lines.append(f"### Principle: `{atype}` ({len(items)} instances)")
                for d in items[:30]:
                    loc = f"{d.primary_location.file_path}:{d.primary_location.line}" if d.primary_location else ""
                    loc_str = f" in `{loc}`" if loc else ""
                    lines.append(f"- **{d.target_name}** ({d.confidence.percentage_str}){loc_str} - {d.summary}")
            lines.append("")
            lines.append("---")
            lines.append("")

        # 4. Module & File Hotspots Distribution
        lines.append("## 🗺️ Module & File Hotspots Distribution")
        top_files = sorted(file_to_findings.items(), key=lambda x: len(x[1]), reverse=True)[:25]
        if top_files:
            for fname, f_items in top_files:
                p_count = sum(1 for x in f_items if "pattern" in x)
                v_count = sum(1 for x in f_items if "violation" in x)
                a_count = sum(1 for x in f_items if "adherence" in x)
                lines.append(f"- **`{fname}`**: {len(f_items)} findings ({v_count} violations, {p_count} patterns, {a_count} adherences)")
        lines.append("")

        return "\n".join(lines)
