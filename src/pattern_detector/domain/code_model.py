"""Domain Code Model for Rust Static Architecture and Pattern Analysis."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Any, Sequence

from pattern_detector.domain.value_objects import SourceLocation


@dataclass
class FieldModel:
    """Represents a struct field in Rust."""

    name: str
    type_str: str
    visibility: str = "private"
    location: SourceLocation | None = None


@dataclass
class FunctionModel:
    """Represents a standalone function or method in Rust."""

    name: str
    params: list[tuple[str, str]] = field(default_factory=list)  # [(param_name, param_type), ...]
    return_type: str = "()"
    is_async: bool = False
    is_unsafe: bool = False
    is_const: bool = False
    is_method: bool = False
    receiver: str | None = None  # "&self", "&mut self", "self", "mut self", or None (associated function)
    body: str = ""
    calls: list[str] = field(default_factory=list)
    doc: str = ""
    cyclomatic_complexity: int = 1
    control_flow_count: int = 0
    location: SourceLocation | None = None

    @property
    def is_associated_fn(self) -> bool:
        return self.is_method and self.receiver is None

    @property
    def takes_self_by_val(self) -> bool:
        return self.receiver in ("self", "mut self")


@dataclass
class StructModel:
    """Represents a Rust struct definition."""

    name: str
    fields: list[FieldModel] = field(default_factory=list)
    visibility: str = "private"
    derives: list[str] = field(default_factory=list)
    generics: list[str] = field(default_factory=list)
    lifetimes: list[str] = field(default_factory=list)
    is_tuple: bool = False
    is_unit: bool = False
    methods: dict[str, FunctionModel] = field(default_factory=dict)
    traits_implemented: list[str] = field(default_factory=list)
    doc: str = ""
    location: SourceLocation | None = None

    @property
    def field_names(self) -> list[str]:
        return [f.name for f in self.fields]

    @property
    def field_types(self) -> list[str]:
        return [f.type_str for f in self.fields]


@dataclass
class EnumVariantModel:
    """Represents a single variant of a Rust enum."""

    name: str
    fields: list[tuple[str, str]] = field(default_factory=list)  # [(name, type)] or [("", type)]
    is_tuple: bool = False
    is_struct: bool = False
    location: SourceLocation | None = None


@dataclass
class EnumModel:
    """Represents a Rust enum definition."""

    name: str
    variants: list[EnumVariantModel] = field(default_factory=list)
    visibility: str = "private"
    derives: list[str] = field(default_factory=list)
    generics: list[str] = field(default_factory=list)
    methods: dict[str, FunctionModel] = field(default_factory=dict)
    traits_implemented: list[str] = field(default_factory=list)
    doc: str = ""
    location: SourceLocation | None = None

    @property
    def variant_names(self) -> list[str]:
        return [v.name for v in self.variants]


@dataclass
class TraitMethodModel:
    """Represents a method declared in a Rust trait."""

    name: str
    params: list[tuple[str, str]] = field(default_factory=list)
    return_type: str = "()"
    has_default_body: bool = False
    is_async: bool = False
    receiver: str | None = None
    location: SourceLocation | None = None


@dataclass
class TraitModel:
    """Represents a Rust trait definition."""

    name: str
    methods: dict[str, TraitMethodModel] = field(default_factory=dict)
    associated_types: list[str] = field(default_factory=list)
    super_traits: list[str] = field(default_factory=list)
    is_unsafe: bool = False
    visibility: str = "private"
    generics: list[str] = field(default_factory=list)
    doc: str = ""
    location: SourceLocation | None = None


@dataclass
class ImplModel:
    """Represents an impl block in Rust (`impl Struct` or `impl Trait for Struct`)."""

    target_type: str
    trait_name: str | None = None  # None for inherent impl
    generics: list[str] = field(default_factory=list)
    methods: dict[str, FunctionModel] = field(default_factory=dict)
    location: SourceLocation | None = None


@dataclass
class ModuleModel:
    """Represents a Rust module or source file (`mod foo;` or `foo.rs`)."""

    name: str
    file_path: str
    structs: dict[str, StructModel] = field(default_factory=dict)
    enums: dict[str, EnumModel] = field(default_factory=dict)
    traits: dict[str, TraitModel] = field(default_factory=dict)
    impls: list[ImplModel] = field(default_factory=list)
    functions: dict[str, FunctionModel] = field(default_factory=dict)
    use_statements: list[str] = field(default_factory=list)
    submodules: list[str] = field(default_factory=list)
    unsafe_blocks_count: int = 0
    raw_source: str = ""
    location: SourceLocation | None = None


@dataclass
class CodeModel:
    """Aggregated semantic domain model of an entire Rust codebase or crate."""

    modules: dict[str, ModuleModel] = field(default_factory=dict)
    project_path: str = ""

    # -------------------------------------------------------------------------
    # Accessors and Aggregations
    # -------------------------------------------------------------------------

    def all_structs(self) -> list[StructModel]:
        res = []
        for mod in self.modules.values():
            res.extend(mod.structs.values())
        return res

    def all_enums(self) -> list[EnumModel]:
        res = []
        for mod in self.modules.values():
            res.extend(mod.enums.values())
        return res

    def all_traits(self) -> list[TraitModel]:
        res = []
        for mod in self.modules.values():
            res.extend(mod.traits.values())
        return res

    def all_impls(self) -> list[ImplModel]:
        res = []
        for mod in self.modules.values():
            res.extend(mod.impls)
        return res

    def all_functions(self) -> list[FunctionModel]:
        seen: set[int] = set()
        res: list[FunctionModel] = []

        def _add(fn: FunctionModel) -> None:
            obj_id = id(fn)
            if obj_id not in seen:
                seen.add(obj_id)
                res.append(fn)

        for mod in self.modules.values():
            for fn in mod.functions.values():
                _add(fn)
            for st in mod.structs.values():
                for m in st.methods.values():
                    _add(m)
            for en in mod.enums.values():
                for m in en.methods.values():
                    _add(m)
            for imp in mod.impls:
                for m in imp.methods.values():
                    _add(m)
        return res

    def find_struct(self, name: str) -> StructModel | None:
        for st in self.all_structs():
            if st.name == name or st.name.endswith(f"::{name}"):
                return st
        return None

    def find_enum(self, name: str) -> EnumModel | None:
        for en in self.all_enums():
            if en.name == name or en.name.endswith(f"::{name}"):
                return en
        return None

    def find_trait(self, name: str) -> TraitModel | None:
        for tr in self.all_traits():
            if tr.name == name or tr.name.endswith(f"::{name}"):
                return tr
        return None

    def find_impls_for(self, type_name: str) -> list[ImplModel]:
        clean = type_name.split("<")[0].strip()
        res = []
        for imp in self.all_impls():
            imp_clean = imp.target_type.split("<")[0].strip()
            if imp_clean == clean or imp_clean.endswith(f"::{clean}"):
                res.append(imp)
        return res

    def find_trait_implementors(self, trait_name: str) -> list[str]:
        clean = trait_name.split("<")[0].strip()
        implementors = []
        for imp in self.all_impls():
            if imp.trait_name:
                imp_tr = imp.trait_name.split("<")[0].strip()
                if imp_tr == clean or imp_tr.endswith(f"::{clean}"):
                    implementors.append(imp.target_type)
        return implementors

    # -------------------------------------------------------------------------
    # Dependency Graph & Circular Dependency Detection
    # -------------------------------------------------------------------------

    def build_module_dependency_graph(self) -> dict[str, set[str]]:
        """Builds directed adjacency graph of module dependencies."""
        graph: dict[str, set[str]] = {m_name: set() for m_name in self.modules}
        all_mod_names = set(self.modules.keys())

        # Precompute symbol to module index
        symbol_to_mod: dict[str, str] = {}
        for m_name, mod in self.modules.items():
            for st_name in mod.structs:
                symbol_to_mod[f"{m_name}::{st_name}"] = m_name
            for en_name in mod.enums:
                symbol_to_mod[f"{m_name}::{en_name}"] = m_name
            for tr_name in mod.traits:
                symbol_to_mod[f"{m_name}::{tr_name}"] = m_name

        for m_name, mod in self.modules.items():
            for use_stmt in mod.use_statements:
                clean_use = use_stmt.replace("crate::", "").replace("super::", "").strip(";")
                if clean_use in all_mod_names and clean_use != m_name:
                    graph[m_name].add(clean_use)
                elif clean_use in symbol_to_mod:
                    target_mod = symbol_to_mod[clean_use]
                    if target_mod != m_name:
                        graph[m_name].add(target_mod)
                elif "::" in clean_use:
                    parent_mod = "::".join(clean_use.split("::")[:-1])
                    if parent_mod in all_mod_names and parent_mod != m_name:
                        graph[m_name].add(parent_mod)

        return graph

    def find_circular_dependencies(self, max_depth: int = 8, max_cycles: int = 50) -> list[list[str]]:
        """Detects cyclic dependencies between Rust modules."""
        graph = self.build_module_dependency_graph()
        cycles: list[list[str]] = []
        visited: set[str] = set()

        def _dfs(current: str, path: list[str], path_set: set[str]) -> None:
            if len(cycles) >= max_cycles:
                return
            path.append(current)
            path_set.add(current)

            for neighbor in sorted(graph.get(current, set())):
                if neighbor == path[0] and len(path) > 1:
                    canonical = tuple(path)
                    rotations = [canonical[i:] + canonical[:i] for i in range(len(canonical))]
                    min_rot = list(min(rotations))
                    if min_rot not in cycles:
                        cycles.append(min_rot)
                elif neighbor not in path_set and neighbor not in visited and len(path) < max_depth:
                    _dfs(neighbor, path, path_set)

            path.pop()
            path_set.remove(current)

        for node in sorted(graph.keys()):
            _dfs(node, [], set())
            visited.add(node)

        return cycles
