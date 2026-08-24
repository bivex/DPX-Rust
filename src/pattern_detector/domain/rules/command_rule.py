"""Rust Command Pattern Rule (Command enums, executable closures, Box<dyn Fn()>)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class CommandPatternRule(BasePatternRule):
    """Detects Command Pattern in Rust."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.COMMAND

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        # 1. Command Enums with execute / undo methods
        for en in model.all_enums():
            evidences: list[Evidence] = []
            name_lower = en.name.lower()

            if name_lower.endswith("command") or name_lower.endswith("action") or name_lower.endswith("msg"):
                evidences.append(
                    Evidence(
                        description=f"Enum '{en.name}' follows Command/Action naming convention",
                        weight=0.45,
                        rule_code="COMMAND_ENUM_NAMING",
                        location=en.location,
                    )
                )

            impls = model.find_impls_for(en.name)
            all_methods = dict(en.methods)
            for imp in impls:
                all_methods.update(imp.methods)

            exec_methods = [
                m for m_name, m in all_methods.items()
                if m_name in ("execute", "run", "handle", "apply", "undo", "rollback")
            ]
            if exec_methods:
                evidences.append(
                    Evidence(
                        description=f"Implements command execution/dispatch method(s) ({', '.join(m.name for m in exec_methods[:3])})",
                        weight=0.50,
                        rule_code="COMMAND_EXECUTE_METHOD",
                        location=exec_methods[0].location or en.location,
                    )
                )

            if len(en.variants) >= 2 and (name_lower.endswith("command") or exec_methods):
                evidences.append(
                    Evidence(
                        description=f"Encapsulates {len(en.variants)} discrete executable actions as enum variants ({', '.join(en.variant_names[:3])})",
                        weight=0.35,
                        rule_code="COMMAND_VARIANTS",
                        location=en.location,
                    )
                )

            if evidences:
                det = self._create_detection(
                    target_name=en.name,
                    target_kind="command_enum",
                    evidences=evidences,
                    location=en.location,
                )
                if det.confidence.score >= 0.50:
                    detections.append(det)

        return detections
