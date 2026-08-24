"""Rust Interpreter Pattern Rule (evaluate/eval on AST enums)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class InterpreterPatternRule(BasePatternRule):
    """Detects Interpreter Pattern in Rust."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.INTERPRETER

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for en in model.all_enums():
            impls = model.find_impls_for(en.name)
            all_methods = dict(en.methods)
            for imp in impls:
                all_methods.update(imp.methods)

            eval_methods = [
                m for m_name, m in all_methods.items()
                if m_name in ("eval", "evaluate", "interpret", "exec_node")
            ]
            if eval_methods and len(en.variants) >= 3:
                evidences = [
                    Evidence(
                        description=f"Enum '{en.name}' implements AST Interpreter expression evaluation method '{eval_methods[0].name}()' across {len(en.variants)} grammar variant(s)",
                        weight=0.75,
                        rule_code="INTERPRETER_EVALUATE_METHOD",
                        location=eval_methods[0].location or en.location,
                    )
                ]
                det = self._create_detection(
                    target_name=en.name,
                    target_kind="interpreter_ast_enum",
                    evidences=evidences,
                    location=en.location,
                )
                detections.append(det)

        return detections
