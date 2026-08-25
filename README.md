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

## 🌐 The DPX Suite Family

Cross-language architectural static analysis across all modern programming languages:

| Repository | Language / Ecosystem | Primary Paradigms & Focus |
|---|---|---|
| **[`DPX-Gleam`](https://github.com/bivex/DPX-Gleam)** | **Gleam** (1.0 - 1.8+) | **Type-Safe OTP Actors, Algebraic Data Types, Railway Monads, GoF 23** |
| **[`DPX-Mojo`](https://github.com/bivex/DPX-Mojo)** | **Mojo** (24.x - 25.x+) | **SIMD Vectorization, Ownership, Memory Safety, GoF 23, AI Acceleration** |
| **[`DPX-Julia`](https://github.com/bivex/DPX-Julia)** | **Julia** (1.6 - 1.11+) | **Multiple Dispatch, Holy Traits, Metaprogramming, Tasks, GoF 23** |
| **[`DPX-Kotlin`](https://github.com/bivex/DPX-Kotlin)** | **Kotlin** (1.8 - 2.0+) | **Coroutines, Flow, Jetpack Compose, Multiplatform, GoF 23** |
| **[`DPX-Swift`](https://github.com/bivex/DPX-Swift)** | **Swift** (5.5 - 6.0+) | **Protocol-Oriented, Actor Concurrency, SwiftUI, ARC Safety** |
| **[`DPX-CSharp`](https://github.com/bivex/DPX-CSharp)** | **C#** (10 - 13 / .NET 8-9) | **Clean Architecture, CQRS MediatR, Channel Pipelines** |
| **[`DPX-TypeScript`](https://github.com/bivex/DPX-TypeScript)** | **TypeScript / JavaScript** | **Hexagonal DI, Decorator Meta, Reactive Streams, React/NestJS** |
| **[`DPX-Rust`](https://github.com/bivex/DPX-Rust)** | **Rust** (Edition 2021/2024) | **Zero-Cost Abstractions, RAII Lifetimes, Typestate Pattern** |
| **[`DPX-Go`](https://github.com/bivex/DPX-Go)** | **Go** (1.18 - 1.24+) | **Goroutine Channels, CSP Concurrency, Pipeline Streaming** |
| **[`DPX-Py`](https://github.com/bivex/DPX-Py)** | **Python** (3.8 - 3.13+) | **Multi-Paradigm Hexagonal, Data Flow Engine, AsyncIO** |
| **[`DPX-Php`](https://github.com/bivex/DPX-Php)** | **PHP** (8.1 - 8.4+) | **Attribute-driven DDD, Fiber Concurrency, Laravel/Symfony** |
| **[`DPX-Haskell`](https://github.com/bivex/DPX-Haskell)** | **Haskell** (GHC 9.2 - 9.12+) | **Category Theory, Monad Transformers, Free Monads, Optics** |
| **[`DPX-OCaml`](https://github.com/bivex/DPX-OCaml)** | **OCaml** (4.14 - 5.3+ Multicore) | **Functor Modules, Effect Handlers, GADTs, Railway Monads** |
| **[`DPX-Elixir`](https://github.com/bivex/DPX-Elixir)** | **Elixir** (OTP 25 - 27+) | **GenServer, DynamicSupervisor, Actor Fault Tolerance** |
| **[`DPX-Erlang`](https://github.com/bivex/DPX-Erlang)** | **Erlang/OTP** (24 - 27+) | **OTP Behaviors, Supervision Trees, Message Passing** |
| **[`DPX-C`](https://github.com/bivex/DPX-C)** | **C** (C99 - C23) | **Opaque Structs, VTables, MISRA/CERT Safety, Arena Allocators** |
| **[`DPX-Cpp`](https://github.com/bivex/DPX-Cpp)** | **C++** (C++14 - C++20) | **CRTP, Policy-Based Design, RAII Memory Safety, ANTLR4 AST** |
| **[`DPX-Java`](https://github.com/bivex/DPX-Java)** | **Java** (17 - 23+) | **Virtual Threads, Spring Boot / Jakarta EE, GoF Patterns** |
| **[`DPX`](https://github.com/bivex/DPX)** | **Clojure** / Meta Engine | **Pure Functional, Multimethods, Homoiconic Macro Architecture** |
---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more information.
