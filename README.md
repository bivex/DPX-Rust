# 🦀 DPX-Rust: Design Pattern Detector & Software Architecture Scanner for Rust

> **Hexagonal Architecture (Ports & Adapters) + Domain-Driven Design (DDD)** static analysis and software design pattern detection engine for **Rust (2015 - 2024 edition)**.

[![PyPI Version](https://img.shields.io/pypi/v/dpx-rust.svg?style=flat&color=blue)](https://pypi.org/project/dpx-rust/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=flat&logo=python)](https://www.python.org/)
[![Rust](https://img.shields.io/badge/Rust-2015%20--%202024%20edition-DEA584.svg?style=flat&logo=rust)](https://www.rust-lang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)](https://opensource.org/licenses/MIT)
[![Rules](https://img.shields.io/badge/Supported%20Rules-41%20Rules-orange.svg?style=flat)]()
[![SARIF](https://img.shields.io/badge/SARIF-v2.1.0%20OASIS-blue.svg?style=flat)]()

---

## 📦 Installation

```bash
# Using pip
pip install dpx-rust

# Using uv
uv tool install dpx-rust
```

---

## ✨ Key Capabilities

### 🔍 All 23 Gang of Four (GoF) Design Patterns in Idiomatic Rust:
* **Creational**: Builder (fluent typestate, `build()`, consuming builder), Factory Method (`fn new()`, `fn from_*()`), Abstract Factory, Prototype (`Clone`), Singleton (`OnceLock`, `LazyLock`, `lazy_static!`).
* **Structural**: Adapter (`From`/`Into` traits, inner struct wrapping), Decorator (`Box<dyn Trait>` wrapping, generic layer wrappers), Facade, Composite (recursive tree enums, `Vec<Box<dyn Node>>`), Proxy (`Deref`/`DerefMut` smart forwarders), Bridge, Flyweight (`Arc<T>` pools, string interning).
* **Behavioral**: Command (command enums with `execute()`, closures), Strategy (trait polymorphism `&dyn Trait` / static monomorphization `impl Trait`), Observer (`broadcast::Sender`, channels, callback registries), State (Enum state machines, transition methods), Template Method (traits with provided default methods), Chain of Responsibility (`tower::Service`, middleware chains), Iterator (`impl Iterator`), Mediator, Memento (snapshots), Visitor (AST visitor traits), Interpreter (`evaluate()` over AST enums).

### 🦀 7 Rust-Specific Idioms & Architectural Patterns:
* **Typestate Pattern**: Zero-cost compile-time state machines via `PhantomData<State>` with consuming `self` transitions.
* **Newtype Pattern**: Strong type safety and orphan rule bypass via single-element tuple structs (`struct UserId(pub u64);`).
* **RAII / Drop Guard**: Deterministic resource management via `impl Drop for Struct`.
* **Actor / MPSC Worker**: Background async worker loops consuming command queues (`tokio::sync::mpsc`).
* **Middleware Pipeline**: Layered request processing pipelines (`tower::Layer`, `axum::middleware`).
* **Interior Mutability**: Synchronization via `Arc<Mutex<T>>`, `RwLock<T>`, `RefCell<T>`, `Atomic*`.
* **Circular Module Dependency**: Cyclic dependency detection between Rust modules and sub-crates via Tarjan's SCC.

### 🛡️ 11 SOLID, Clean Code & Safety Rules:
* **SRP**: God Struct detection (≥15 methods or ≥12 fields mixing domains).
* **OCP**: Large match expression cascades that should be open to extension via trait polymorphism.
* **LSP**: Trait implementations calling `unimplemented!()`, `todo!()`, or unconditional `panic!()`.
* **ISP**: Fat Traits (≥8 methods) forcing unnecessary implementation obligations.
* **DIP**: Functions parameterizing on `impl Trait` / `dyn Trait` rather than concrete structs.
* **Composition Over Inheritance**: Struct composition over deep trait hierarchies.
* **Law of Demeter**: Deep train-wreck invocation chains (`a.b().c().d().e()`).
* **High Cohesion / Low Coupling**: Structs with high fan-out coupling.
* **KISS**: High cyclomatic complexity and long parameter lists.
* **DRY**: Duplicated function and match arm implementations.
* **Unsafe Block Guard**: Auditing and cataloging `unsafe { ... }` blocks and raw pointer dereferences.

### 🎨 Interactive HTML Dashboards:
* **Pattern Scanner Dashboard**: Semantic UI Dark Theme, KPI stats, category filter pills, Evidence Trail heuristic inspector, instant search, live `[ 🛡️ Hide SOLID & Principles ]` toggle, and **AI Architectural Map** with one-click copy for LLM analysis.

---

## 🚀 Usage & CLI Commands

```bash
# Basic scan (terminal output)
dpx scan /path/to/rust/crate

# Scan and export standalone interactive HTML dashboard
dpx scan /path/to/rust/crate -H reports/dashboard.html

# Scan GoF & Architecture patterns only (exclude SOLID/Clean code rules)
dpx scan /path/to/rust/crate -H reports/patterns_only.html --no-principles

# Filter by minimum confidence (low, medium, high, very_high)
dpx scan /path/to/rust/crate -c high

# Scan specific patterns only
dpx scan /path/to/rust/crate -p builder -p typestate -p raii_drop

# Generate SARIF v2.1.0 report for GitHub Security / Code Scanning
dpx scan /path/to/rust/crate -S report.sarif

# Generate AI Architectural Context Prompt (paste to Claude / ChatGPT / Gemini)
dpx scan /path/to/rust/crate --llm
```

---

## 🧪 Running Tests

```bash
uv run pytest -v
```

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more information.
