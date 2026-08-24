"""High-performance Native Rust AST & CST Parser Adapter implementing ParserPort."""

from __future__ import annotations

import os
import re
from pathlib import Path

from pattern_detector.domain.code_model import (
    CodeModel,
    EnumModel,
    EnumVariantModel,
    FieldModel,
    FunctionModel,
    ImplModel,
    ModuleModel,
    StructModel,
    TraitMethodModel,
    TraitModel,
)
from pattern_detector.domain.value_objects import SourceLocation
from pattern_detector.ports.outbound import ParserPort


class NativeRustParserAdapter(ParserPort):
    """High-performance, fault-tolerant native Rust AST parser (zero external deps)."""

    def parse_sources(self, sources: dict[str, str]) -> CodeModel:
        model = CodeModel()
        for file_path, source_text in sources.items():
            mod_model = self.parse_file(file_path, source_text)
            model.modules[mod_model.name] = mod_model
        return model

    def parse_file(self, file_path: str, source_text: str) -> ModuleModel:
        mod_name = self._derive_module_name(file_path)
        loc = SourceLocation(file_path=file_path, line=1, column=1)

        mod = ModuleModel(
            name=mod_name,
            file_path=file_path,
            raw_source=source_text,
            location=loc,
        )

        clean_text = self._strip_comments(source_text)

        # 1. Parse use statements and submodules
        mod.use_statements = self._parse_use_statements(clean_text)
        mod.submodules = self._parse_submodules(clean_text)

        # 2. Parse Traits
        mod.traits = self._parse_traits(clean_text, file_path)

        # 3. Parse Structs
        mod.structs = self._parse_structs(clean_text, file_path)

        # 4. Parse Enums
        mod.enums = self._parse_enums(clean_text, file_path)

        # 5. Parse Impl blocks
        mod.impls = self._parse_impls(clean_text, file_path)

        # 6. Parse standalone functions
        mod.functions = self._parse_standalone_functions(clean_text, file_path)

        # Attach inherent methods to structs/enums
        for imp in mod.impls:
            if not imp.trait_name:
                if imp.target_type in mod.structs:
                    mod.structs[imp.target_type].methods.update(imp.methods)
                elif imp.target_type in mod.enums:
                    mod.enums[imp.target_type].methods.update(imp.methods)
            else:
                if imp.target_type in mod.structs:
                    mod.structs[imp.target_type].traits_implemented.append(imp.trait_name)
                elif imp.target_type in mod.enums:
                    mod.enums[imp.target_type].traits_implemented.append(imp.trait_name)

        return mod

    # -------------------------------------------------------------------------
    # Parsing Helpers
    # -------------------------------------------------------------------------

    def _derive_module_name(self, file_path: str) -> str:
        stem = Path(file_path).stem
        if stem == "mod" or stem == "lib" or stem == "main":
            return Path(file_path).parent.name or stem
        return stem

    def _strip_comments(self, text: str) -> str:
        text = re.sub(r"//.*", "", text)
        text = re.sub(r"/\*[\s\S]*?\*/", "", text)
        return text

    def _parse_use_statements(self, text: str) -> list[str]:
        return [m.group(1).strip() for m in re.finditer(r"\buse\s+([^;]+);", text)]

    def _parse_submodules(self, text: str) -> list[str]:
        return [m.group(1).strip() for m in re.finditer(r"\bmod\s+([a-zA-Z0-9_]+)\s*;", text)]

    def _parse_structs(self, text: str, file_path: str) -> dict[str, StructModel]:
        structs = {}
        pattern = re.compile(
            r"((?:#\[derive\([^)]+\)\]\s*)*)(pub(?:\([^)]+\))?\s+)?struct\s+([a-zA-Z0-9_]+)(?:<([^>]+)>)?\s*(?:(\([^)]*\));|;|\{([^}]*)\})",
            re.MULTILINE,
        )
        for m in pattern.finditer(text):
            derives_raw = m.group(1) or ""
            vis = (m.group(2) or "private").strip()
            name = m.group(3)
            generics_raw = m.group(4) or ""
            tuple_fields_raw = m.group(5)
            block_fields_raw = m.group(6)

            line_no = text[:m.start()].count("\n") + 1
            loc = SourceLocation(file_path=file_path, line=line_no)

            derives = []
            if derives_raw:
                derives_matches = re.findall(r"#\[derive\(([^)]+)\)\]", derives_raw)
                for dm in derives_matches:
                    derives.extend([d.strip() for d in dm.split(",") if d.strip()])

            generics = [g.strip() for g in generics_raw.split(",") if g.strip()]

            fields = []
            is_tuple = False
            is_unit = False

            if tuple_fields_raw is not None:
                is_tuple = True
                # e.g. (pub u64, String)
                raw_tuple = tuple_fields_raw.strip("()")
                for idx, tf in enumerate(raw_tuple.split(",")):
                    tf_clean = tf.strip()
                    if tf_clean:
                        tf_parts = tf_clean.split()
                        tf_vis = "pub" if "pub" in tf_parts else "private"
                        tf_type = tf_parts[-1]
                        fields.append(FieldModel(name=f"_{idx}", type_str=tf_type, visibility=tf_vis, location=loc))
            elif block_fields_raw is not None:
                for line in block_fields_raw.splitlines():
                    line = line.strip().rstrip(",")
                    if not line or line.startswith("//"):
                        continue
                    field_m = re.match(r"(?:(pub(?:\([^)]+\))?)\s+)?([a-zA-Z0-9_]+)\s*:\s*(.+)", line)
                    if field_m:
                        f_vis = (field_m.group(1) or "private").strip()
                        f_name = field_m.group(2)
                        f_type = field_m.group(3).strip()
                        fields.append(FieldModel(name=f_name, type_str=f_type, visibility=f_vis, location=loc))
            else:
                is_unit = True

            st = StructModel(
                name=name,
                fields=fields,
                visibility=vis,
                derives=derives,
                generics=generics,
                is_tuple=is_tuple,
                is_unit=is_unit,
                location=loc,
            )
            structs[name] = st

        return structs

    def _parse_enums(self, text: str, file_path: str) -> dict[str, EnumModel]:
        enums = {}
        pattern = re.compile(
            r"((?:#\[derive\([^)]+\)\]\s*)*)(pub(?:\([^)]+\))?\s+)?enum\s+([a-zA-Z0-9_]+)(?:<([^>]+)>)?\s*\{([^}]*)\}",
            re.MULTILINE,
        )
        for m in pattern.finditer(text):
            derives_raw = m.group(1) or ""
            vis = (m.group(2) or "private").strip()
            name = m.group(3)
            generics_raw = m.group(4) or ""
            variants_raw = m.group(5)

            line_no = text[:m.start()].count("\n") + 1
            loc = SourceLocation(file_path=file_path, line=line_no)

            derives = []
            if derives_raw:
                derives_matches = re.findall(r"#\[derive\(([^)]+)\)\]", derives_raw)
                for dm in derives_matches:
                    derives.extend([d.strip() for d in dm.split(",") if d.strip()])

            generics = [g.strip() for g in generics_raw.split(",") if g.strip()]

            variants = []
            for v_str in variants_raw.split(","):
                v_str = v_str.strip()
                if not v_str:
                    continue
                v_match = re.match(r"([a-zA-Z0-9_]+)(?:\(([^)]*)\)|\{([^}]*)\})?", v_str)
                if v_match:
                    v_name = v_match.group(1)
                    v_tuple = v_match.group(2)
                    v_struct = v_match.group(3)
                    v_fields = []
                    is_t = False
                    is_s = False
                    if v_tuple is not None:
                        is_t = True
                        for tf in v_tuple.split(","):
                            if tf.strip():
                                v_fields.append(("", tf.strip()))
                    elif v_struct is not None:
                        is_s = True
                        for sf in v_struct.split(","):
                            if ":" in sf:
                                sfn, sft = sf.split(":", 1)
                                v_fields.append((sfn.strip(), sft.strip()))
                    variants.append(EnumVariantModel(name=v_name, fields=v_fields, is_tuple=is_t, is_struct=is_s, location=loc))

            enums[name] = EnumModel(
                name=name,
                variants=variants,
                visibility=vis,
                derives=derives,
                generics=generics,
                location=loc,
            )

        return enums

    def _parse_traits(self, text: str, file_path: str) -> dict[str, TraitModel]:
        traits = {}
        pattern = re.compile(
            r"(pub(?:\([^)]+\))?\s+)?(?:(unsafe)\s+)?trait\s+([a-zA-Z0-9_]+)(?:<([^>]+)>)?(?:\s*:\s*([^{]+))?\s*\{([^}]*)\}",
            re.MULTILINE,
        )
        for m in pattern.finditer(text):
            vis = (m.group(1) or "private").strip()
            is_unsafe = bool(m.group(2))
            name = m.group(3)
            generics_raw = m.group(4) or ""
            super_traits_raw = m.group(5) or ""
            body = m.group(6)

            line_no = text[:m.start()].count("\n") + 1
            loc = SourceLocation(file_path=file_path, line=line_no)

            super_traits = [st.strip() for st in super_traits_raw.split("+") if st.strip()]
            generics = [g.strip() for g in generics_raw.split(",") if g.strip()]

            methods = {}
            associated_types = []

            for line in body.splitlines():
                line = line.strip()
                if line.startswith("type "):
                    type_name = line.replace("type ", "").split(";")[0].split(":")[0].strip()
                    associated_types.append(type_name)

            method_pat = re.compile(
                r"(?:async\s+)?fn\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)(?:\s*->\s*([^{;]+))?\s*(\{;?)?",
            )
            for mm in method_pat.finditer(body):
                m_name = mm.group(1)
                params_raw = mm.group(2)
                ret_type = (mm.group(3) or "()").strip()
                has_default = "{" in (mm.group(4) or "")

                params = []
                receiver = None
                for p in params_raw.split(","):
                    p = p.strip()
                    if p in ("&self", "&mut self", "self", "mut self"):
                        receiver = p
                    elif ":" in p:
                        pn, pt = p.split(":", 1)
                        params.append((pn.strip(), pt.strip()))

                methods[m_name] = TraitMethodModel(
                    name=m_name,
                    params=params,
                    return_type=ret_type,
                    has_default_body=has_default,
                    receiver=receiver,
                    location=loc,
                )

            traits[name] = TraitModel(
                name=name,
                methods=methods,
                associated_types=associated_types,
                super_traits=super_traits,
                is_unsafe=is_unsafe,
                visibility=vis,
                generics=generics,
                location=loc,
            )

        return traits

    def _parse_impls(self, text: str, file_path: str) -> list[ImplModel]:
        impls = []
        pattern = re.compile(
            r"impl(?:<([^>]+)>)?\s+(?:([a-zA-Z0-9_:<>\s',&*]+?)\s+for\s+)?([a-zA-Z0-9_:<>\s',&*]+?)\s*\{",
            re.MULTILINE,
        )
        pos = 0
        while pos < len(text):
            m = pattern.search(text, pos)
            if not m:
                break
            generics_raw = m.group(1) or ""
            trait_name = (m.group(2) or "").strip() if m.group(2) else None
            target_type = m.group(3).strip()

            brace_start = m.end() - 1
            body, brace_end = self._extract_balanced_braces(text, brace_start)
            pos = brace_end + 1

            line_no = text[:m.start()].count("\n") + 1
            loc = SourceLocation(file_path=file_path, line=line_no)

            methods = self._parse_methods_in_block(body, file_path, line_no)

            impls.append(
                ImplModel(
                    target_type=target_type,
                    trait_name=trait_name,
                    generics=[g.strip() for g in generics_raw.split(",") if g.strip()],
                    methods=methods,
                    location=loc,
                )
            )

        return impls

    def _parse_methods_in_block(self, block: str, file_path: str, base_line: int) -> dict[str, FunctionModel]:
        methods = {}
        fn_pattern = re.compile(
            r"((?:pub(?:\([^)]+\))?\s+)?(?:async\s+)?(?:unsafe\s+)?(?:const\s+)?fn\s+([a-zA-Z0-9_]+)\s*(?:<[^>]+>)?\s*\(([^)]*)\)(?:\s*->\s*([^{]+))?)\s*\{",
        )
        pos = 0
        while pos < len(block):
            m = fn_pattern.search(block, pos)
            if not m:
                break
            fn_header = m.group(1)
            name = m.group(2)
            params_raw = m.group(3)
            ret_type = (m.group(4) or "()").strip()

            is_async = "async fn" in fn_header
            is_unsafe = "unsafe fn" in fn_header
            is_const = "const fn" in fn_header

            brace_start = m.end() - 1
            fn_body, brace_end = self._extract_balanced_braces(block, brace_start)
            pos = brace_end + 1

            line_no = base_line + block[:m.start()].count("\n")
            loc = SourceLocation(file_path=file_path, line=line_no)

            params = []
            receiver = None
            for p in params_raw.split(","):
                p = p.strip()
                if p in ("&self", "&mut self", "self", "mut self"):
                    receiver = p
                elif ":" in p:
                    pn, pt = p.split(":", 1)
                    params.append((pn.strip(), pt.strip()))

            complexity = 1 + len(re.findall(r"\b(if|match|while|for|loop|\&\&|\|\||\?)\b", fn_body))
            calls = re.findall(r"([a-zA-Z0-9_]+(?:::|(?:\.)[a-zA-Z0-9_]+)*)\s*\(", fn_body)

            methods[name] = FunctionModel(
                name=name,
                params=params,
                return_type=ret_type,
                is_async=is_async,
                is_unsafe=is_unsafe,
                is_const=is_const,
                is_method=True,
                receiver=receiver,
                body=fn_body,
                calls=calls,
                cyclomatic_complexity=complexity,
                location=loc,
            )

        return methods

    def _parse_standalone_functions(self, text: str, file_path: str) -> dict[str, FunctionModel]:
        # Parse top-level functions outside impl blocks
        functions = {}
        # Simple extraction
        fn_pattern = re.compile(
            r"((?:pub(?:\([^)]+\))?\s+)?(?:async\s+)?(?:unsafe\s+)?(?:const\s+)?fn\s+([a-zA-Z0-9_]+)\s*(?:<[^>]+>)?\s*\(([^)]*)\)(?:\s*->\s*([^{]+))?)\s*\{",
        )
        for m in fn_pattern.finditer(text):
            name = m.group(2)
            # Ensure not inside impl
            idx = m.start()
            prefix = text[:idx]
            open_braces = prefix.count("{") - prefix.count("}")
            if open_braces == 0:  # top level
                fn_header = m.group(1)
                params_raw = m.group(3)
                ret_type = (m.group(4) or "()").strip()
                line_no = text[:m.start()].count("\n") + 1
                loc = SourceLocation(file_path=file_path, line=line_no)

                body, _ = self._extract_balanced_braces(text, m.end() - 1)
                complexity = 1 + len(re.findall(r"\b(if|match|while|for|loop|\&\&|\|\||\?)\b", body))
                calls = re.findall(r"([a-zA-Z0-9_]+(?:::|(?:\.)[a-zA-Z0-9_]+)*)\s*\(", body)

                params = []
                for p in params_raw.split(","):
                    p = p.strip()
                    if ":" in p:
                        pn, pt = p.split(":", 1)
                        params.append((pn.strip(), pt.strip()))

                functions[name] = FunctionModel(
                    name=name,
                    params=params,
                    return_type=ret_type,
                    is_async="async fn" in fn_header,
                    is_unsafe="unsafe fn" in fn_header,
                    is_const="const fn" in fn_header,
                    is_method=False,
                    body=body,
                    calls=calls,
                    cyclomatic_complexity=complexity,
                    location=loc,
                )

        return functions

    def _extract_balanced_braces(self, text: str, start_index: int) -> tuple[str, int]:
        depth = 0
        in_string = False
        quote_char = ""
        escape = False

        for i in range(start_index, len(text)):
            c = text[i]
            if escape:
                escape = False
                continue
            if c == "\\" and in_string:
                escape = True
                continue
            if c in ('"', "'") and not in_string:
                in_string = True
                quote_char = c
            elif c == quote_char and in_string:
                in_string = False
            elif not in_string:
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        return text[start_index + 1 : i], i

        return text[start_index + 1 :], len(text) - 1
