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

---

## 🌐 The DPX Multi-Language Static Analysis Family (33 Languages)

| # | Language | Repository | Ecosystem & Focus |
|:---:|---|---|---|
| 1 | **Ada** | [`bivex/DPX-Ada`](https://github.com/bivex/DPX-Ada) | Ada 2012/2022, SPARK Contracts, Ravenscar Tasking, DO-178C Safety |
| 2 | **Clojure** | [`bivex/DPX`](https://github.com/bivex/DPX) | Lisp S-Expressions, Protocols, Multimethods |
| 3 | **C** | [`bivex/DPX-C`](https://github.com/bivex/DPX-C) | Memory Safety, Struct VTables, Idiomatic C11/C23 |
| 4 | **Cairo** | [`bivex/DPX-Cairo`](https://github.com/bivex/DPX-Cairo) | Starknet Smart Contracts, ZK-Rollup Invariants |
| 5 | **C++** | [`bivex/DPX-Cpp`](https://github.com/bivex/DPX-Cpp) | RAII, CRTP, Concepts, Modern C++20/23 |
| 6 | **C#** | [`bivex/DPX-CSharp`](https://github.com/bivex/DPX-CSharp) | .NET 9, Roslyn AST, Linq, Records |
| 7 | **Dart** | [`bivex/DPX-Dart`](https://github.com/bivex/DPX-Dart) | Dart 3.x, Flutter, BLoC, Riverpod, Isolates |
| 8 | **Elixir** | [`bivex/DPX-Elixir`](https://github.com/bivex/DPX-Elixir) | BEAM OTP, GenServer, Supervisors |
| 9 | **Erlang** | [`bivex/DPX-Erlang`](https://github.com/bivex/DPX-Erlang) | Fault Tolerance, Actor Model, OTP Behaviors |
| 10 | **Gleam** | [`bivex/DPX-Gleam`](https://github.com/bivex/DPX-Gleam) | Type-Safe BEAM, Actor Concurrency |
| 11 | **Go** | [`bivex/DPX-Go`](https://github.com/bivex/DPX-Go) | Goroutines, Channels, Composition, Interfaces |
| 12 | **Haskell** | [`bivex/DPX-Haskell`](https://github.com/bivex/DPX-Haskell) | Pure Functional, Monads, Typeclasses, Arrows |
| 13 | **Huff** | [`bivex/DPX-Huff`](https://github.com/bivex/DPX-Huff) | Low-Level EVM Bytecode & Opcodes |
| 14 | **Idris 2** | [`bivex/DPX-Idris2`](https://github.com/bivex/DPX-Idris2) | Dependent Types, QTT Linear Protocols, Totality, Proofs |
| 15 | **Java** | [`bivex/DPX-Java`](https://github.com/bivex/DPX-Java) | Spring Boot, Enterprise Java, JVM Invariants |
| 16 | **Julia** | [`bivex/DPX-Julia`](https://github.com/bivex/DPX-Julia) | Multiple Dispatch, Scientific Computing |
| 17 | **Kotlin** | [`bivex/DPX-Kotlin`](https://github.com/bivex/DPX-Kotlin) | Coroutines, Multiplatform, Functional DSLs |
| 18 | **Lua** | [`bivex/DPX-Lua`](https://github.com/bivex/DPX-Lua) | Metatables, Coroutines, LuaJIT, Neovim |
| 19 | **Mojo** | [`bivex/DPX-Mojo`](https://github.com/bivex/DPX-Mojo) | SIMD Hardware, Memory Lifetimes, AI Systems |
| 20 | **Move** | [`bivex/DPX-Move`](https://github.com/bivex/DPX-Move) | Aptos & Sui Resource Safety, Linear Types |
| 21 | **OCaml** | [`bivex/DPX-OCaml`](https://github.com/bivex/DPX-OCaml) | Algebraic Data Types, Functors, Polymorphism |
| 22 | **PHP** | [`bivex/DPX-Php`](https://github.com/bivex/DPX-Php) | Modern PHP 8.4, Attributes, Traits, Laravel |
| 23 | **Prolog** | [`bivex/DPX-Prolog`](https://github.com/bivex/DPX-Prolog) | ISO Prolog, SWI-Prolog, DCG, CLP(FD/R/Q), CHR, Meta-Interpreters |
| 24 | **Puppet** | [`bivex/DPX-Puppet`](https://github.com/bivex/DPX-Puppet) | Puppet DSL, Roles/Profiles, IaC Security, Hiera |
| 25 | **Python** | [`bivex/DPX-Py`](https://github.com/bivex/DPX-Py) | Metaprogramming, Protocols, Hexagonal DDD |
| 26 | **Ruby** | [`bivex/DPX-Ruby`](https://github.com/bivex/DPX-Ruby) | Ruby 3.x, Rails, Metaprogramming, Dry-RB, Security |
| 27 | **Rust** | [`bivex/DPX-Rust`](https://github.com/bivex/DPX-Rust) | Zero-Cost Abstractions, Borrow Checker, Traits |
| 28 | **Solidity** | [`bivex/DPX-Solidity`](https://github.com/bivex/DPX-Solidity) | DeFi Security, Reentrancy, EVM Yul/Assembly |
| 29 | **SQL** | [`bivex/DPX-SQL`](https://github.com/bivex/DPX-SQL) | PostgreSQL, MySQL, SQLite, T-SQL, PL/SQL |
| 30 | **Swift** | [`bivex/DPX-Swift`](https://github.com/bivex/DPX-Swift) | Protocol-Oriented Programming, Actors |
| 31 | **TypeScript** | [`bivex/DPX-TypeScript`](https://github.com/bivex/DPX-TypeScript) | Generics, Conditional Types, Clean Architecture |
| 32 | **Yul** | [`bivex/DPX-Yul`](https://github.com/bivex/DPX-Yul) | EVM Intermediate Representation Optimization |
| 33 | **Zig** | [`bivex/DPX-Zig`](https://github.com/bivex/DPX-Zig) | Comptime, Manual Memory Allocators, C ABI |

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
