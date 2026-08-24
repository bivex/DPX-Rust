"""Rust Builder Pattern Rule (including Fluent Chaining and Typestate Builders)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class BuilderPatternRule(BasePatternRule):
    """Detects Builder pattern implementations in Rust."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.BUILDER

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for st in model.all_structs():
            evidences: list[Evidence] = []
            name_lower = st.name.lower()

            # 1. Naming Convention
            if name_lower.endswith("builder") or "builder" in name_lower:
                evidences.append(
                    Evidence(
                        description=f"Struct '{st.name}' follows the Builder naming convention",
                        weight=0.40,
                        rule_code="BUILDER_NAMING",
                        location=st.location,
                    )
                )

            # Check methods on this struct
            impls = model.find_impls_for(st.name)
            all_methods = dict(st.methods)
            for imp in impls:
                all_methods.update(imp.methods)

            # 2. Terminal Build Method
            build_methods = [
                m for m_name, m in all_methods.items()
                if m_name in ("build", "create", "finish", "compile", "spawn")
            ]
            if build_methods:
                bm = build_methods[0]
                evidences.append(
                    Evidence(
                        description=f"Provides terminal build method '{bm.name}()' constructing target instance",
                        weight=0.45,
                        rule_code="BUILDER_TERMINAL_METHOD",
                        location=bm.location or st.location,
                    )
                )

            # 3. Fluent chaining methods returning Self or consuming self
            chaining_methods = [
                m for m_name, m in all_methods.items()
                if (m.return_type in ("Self", st.name, f"&mut Self", f"&mut {st.name}") or m.takes_self_by_val)
                and m_name not in ("new", "default", "build", "create", "finish")
            ]
            if len(chaining_methods) >= 2:
                evidences.append(
                    Evidence(
                        description=f"Contains {len(chaining_methods)} fluent configuration method(s) returning Self or &mut Self ({', '.join(m.name for m in chaining_methods[:3])})",
                        weight=0.40,
                        rule_code="BUILDER_FLUENT_SETTERS",
                        location=chaining_methods[0].location or st.location,
                    )
                )

            # 4. Typestate or Option fields for progressive construction
            option_fields = [f for f in st.fields if "Option<" in f.type_str or "PhantomData" in f.type_str]
            if option_fields:
                evidences.append(
                    Evidence(
                        description=f"Stores optional/typestate fields for staged construction ({', '.join(f.name for f in option_fields[:3])})",
                        weight=0.30,
                        rule_code="BUILDER_OPTIONAL_FIELDS",
                        location=st.location,
                    )
                )

            if evidences:
                det = self._create_detection(
                    target_name=st.name,
                    target_kind="struct",
                    evidences=evidences,
                    location=st.location,
                )
                if det.confidence.score >= 0.50:
                    detections.append(det)

        return detections
