"""Pattern metadata, catalog definitions, and architectural descriptions for Rust."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from pattern_detector.domain.value_objects import PatternCategory, PatternType


@dataclass(frozen=True)
class PatternCatalogEntry:
    """Catalog entry describing a design pattern, idiom, or principle in Rust."""

    pattern_type: PatternType
    category: PatternCategory
    name: str
    description: str
    idiomatic_example: str


PATTERN_CATALOG: Mapping[PatternType, PatternCatalogEntry] = {
    # Creational
    PatternType.BUILDER: PatternCatalogEntry(
        pattern_type=PatternType.BUILDER,
        category=PatternCategory.CREATIONAL,
        name="Builder Pattern",
        description="Separates the construction of a complex struct from its representation, supporting fluent chaining and typestate validation before final .build().",
        idiomatic_example="struct ServerBuilder { ... } impl ServerBuilder { pub fn port(mut self, p: u16) -> Self { ... } pub fn build(self) -> Result<Server, Error> { ... } }",
    ),
    PatternType.FACTORY_METHOD: PatternCatalogEntry(
        pattern_type=PatternType.FACTORY_METHOD,
        category=PatternCategory.CREATIONAL,
        name="Factory Method",
        description="Provides constructor factory methods (such as fn new, fn create, fn from_*) encapsulating instantiation logic.",
        idiomatic_example="impl Connection { pub fn new(addr: &str) -> Self { ... } pub fn from_config(cfg: &Config) -> Result<Self, Error> { ... } }",
    ),
    PatternType.ABSTRACT_FACTORY: PatternCatalogEntry(
        pattern_type=PatternType.ABSTRACT_FACTORY,
        category=PatternCategory.CREATIONAL,
        name="Abstract Factory",
        description="Defines a trait with associated types or factory methods for creating families of related or dependent trait objects without specifying their concrete structs.",
        idiomatic_example="trait DatabaseFactory { type Conn: Connection; type Tx: Transaction; fn create_connection(&self) -> Self::Conn; }",
    ),
    PatternType.PROTOTYPE: PatternCatalogEntry(
        pattern_type=PatternType.PROTOTYPE,
        category=PatternCategory.CREATIONAL,
        name="Prototype Pattern",
        description="Specifies the kinds of objects to create using a prototypical instance, instantiated via the Clone trait.",
        idiomatic_example="#[derive(Clone)] struct Config { ... } let new_cfg = base_cfg.clone();",
    ),
    PatternType.SINGLETON: PatternCatalogEntry(
        pattern_type=PatternType.SINGLETON,
        category=PatternCategory.CREATIONAL,
        name="Singleton Pattern",
        description="Ensures a struct has only one global instance using std::sync::OnceLock, std::sync::LazyLock, or lazy_static!.",
        idiomatic_example="static INSTANCE: OnceLock<GlobalState> = OnceLock::new(); pub fn get_instance() -> &'static GlobalState { INSTANCE.get_or_init(GlobalState::new) }",
    ),

    # Structural
    PatternType.ADAPTER: PatternCatalogEntry(
        pattern_type=PatternType.ADAPTER,
        category=PatternCategory.STRUCTURAL,
        name="Adapter Pattern",
        description="Converts the interface of a struct into another interface clients expect via From/Into traits or wrapping.",
        idiomatic_example="impl From<LegacyPacket> for ModernPacket { fn from(p: LegacyPacket) -> Self { ... } }",
    ),
    PatternType.DECORATOR: PatternCatalogEntry(
        pattern_type=PatternType.DECORATOR,
        category=PatternCategory.STRUCTURAL,
        name="Decorator Pattern",
        description="Attaches additional responsibilities to an object dynamically by wrapping an inner struct implementing the same trait (or Box<dyn Trait>).",
        idiomatic_example="struct LoggingService<S> { inner: S } impl<S: Service> Service for LoggingService<S> { fn call(&self, req: Request) -> Response { ... self.inner.call(req) } }",
    ),
    PatternType.FACADE: PatternCatalogEntry(
        pattern_type=PatternType.FACADE,
        category=PatternCategory.STRUCTURAL,
        name="Facade Pattern",
        description="Provides a unified, simplified high-level struct API over a subsystem of modules and crates.",
        idiomatic_example="pub struct MediaEngine { decoder: Decoder, audio: AudioSubsystem, video: VideoSubsystem }",
    ),
    PatternType.COMPOSITE: PatternCatalogEntry(
        pattern_type=PatternType.COMPOSITE,
        category=PatternCategory.STRUCTURAL,
        name="Composite Pattern",
        description="Composes objects into tree structures to represent part-whole hierarchies (enums with recursive variants or Vec<Box<dyn Node>>).",
        idiomatic_example="enum AstNode { Leaf(Value), BinaryOp { left: Box<AstNode>, right: Box<AstNode> } }",
    ),
    PatternType.PROXY: PatternCatalogEntry(
        pattern_type=PatternType.PROXY,
        category=PatternCategory.STRUCTURAL,
        name="Proxy Pattern",
        description="Provides a surrogate or placeholder for another object to control access to it via Deref / DerefMut or custom forwarding.",
        idiomatic_example="struct LazyLoader<T> { cell: OnceLock<T>, init: fn() -> T } impl<T> Deref for LazyLoader<T> { ... }",
    ),
    PatternType.BRIDGE: PatternCatalogEntry(
        pattern_type=PatternType.BRIDGE,
        category=PatternCategory.STRUCTURAL,
        name="Bridge Pattern",
        description="Decouples an abstraction from its implementation so that the two can vary independently via generic trait bounds P: Platform.",
        idiomatic_example="struct Window<B: Backend> { backend: B }",
    ),
    PatternType.FLYWEIGHT: PatternCatalogEntry(
        pattern_type=PatternType.FLYWEIGHT,
        category=PatternCategory.STRUCTURAL,
        name="Flyweight Pattern",
        description="Uses sharing to support large numbers of fine-grained immutable objects efficiently (Arc<T>, string interning pools).",
        idiomatic_example="struct Interner { pool: HashMap<String, Arc<str>> }",
    ),

    # Behavioral
    PatternType.OBSERVER: PatternCatalogEntry(
        pattern_type=PatternType.OBSERVER,
        category=PatternCategory.BEHAVIORAL,
        name="Observer Pattern",
        description="Defines a one-to-many dependency between objects using tokio::sync::broadcast, crossbeam channels, or listener callbacks.",
        idiomatic_example="struct EventHub { tx: tokio::sync::broadcast::Sender<Event> }",
    ),
    PatternType.STRATEGY: PatternCatalogEntry(
        pattern_type=PatternType.STRATEGY,
        category=PatternCategory.BEHAVIORAL,
        name="Strategy Pattern",
        description="Defines a family of algorithms, encapsulates each one, and makes them interchangeable using trait objects (&dyn Strategy) or static generics <S: Strategy>.",
        idiomatic_example="pub trait CompressionStrategy { fn compress(&self, data: &[u8]) -> Vec<u8>; }",
    ),
    PatternType.COMMAND: PatternCatalogEntry(
        pattern_type=PatternType.COMMAND,
        category=PatternCategory.BEHAVIORAL,
        name="Command Pattern",
        description="Encapsulates a request as an object (enum or Box<dyn FnOnce()>), thereby letting users parameterize clients with different requests or queue execution.",
        idiomatic_example="enum AppCommand { CreateUser { id: u64, name: String }, DeleteUser(u64) }",
    ),
    PatternType.TEMPLATE_METHOD: PatternCatalogEntry(
        pattern_type=PatternType.TEMPLATE_METHOD,
        category=PatternCategory.BEHAVIORAL,
        name="Template Method",
        description="Defines the skeleton of an algorithm in a trait's default method implementation, deferring specific steps to required trait methods.",
        idiomatic_example="trait DataPipeline { fn extract(&self) -> RawData; fn transform(&self, r: RawData) -> Data; fn run(&self) { let r = self.extract(); self.transform(r); } }",
    ),
    PatternType.CHAIN_OF_RESPONSIBILITY: PatternCatalogEntry(
        pattern_type=PatternType.CHAIN_OF_RESPONSIBILITY,
        category=PatternCategory.BEHAVIORAL,
        name="Chain of Responsibility",
        description="Passes requests along a chain of handlers (tower::Service middleware or recursive handler structs).",
        idiomatic_example="impl<T: Handler> Handler for AuthHandler<T> { fn handle(&self, req: Request) -> Response { ... self.next.handle(req) } }",
    ),
    PatternType.STATE: PatternCatalogEntry(
        pattern_type=PatternType.STATE,
        category=PatternCategory.BEHAVIORAL,
        name="State Pattern",
        description="Allows an object to alter its behavior when its internal state changes using Rust enums or typestates.",
        idiomatic_example="enum ConnectionState { Disconnected, Connecting(SocketAddr), Connected(TcpStream) }",
    ),
    PatternType.ITERATOR: PatternCatalogEntry(
        pattern_type=PatternType.ITERATOR,
        category=PatternCategory.BEHAVIORAL,
        name="Iterator Pattern",
        description="Provides a way to access the elements of an aggregate object sequentially via impl Iterator<Item = T>.",
        idiomatic_example="impl Iterator for ChunkScanner { type Item = Chunk; fn next(&mut self) -> Option<Self::Item> { ... } }",
    ),
    PatternType.MEDIATOR: PatternCatalogEntry(
        pattern_type=PatternType.MEDIATOR,
        category=PatternCategory.BEHAVIORAL,
        name="Mediator Pattern",
        description="Defines an object that encapsulates how a set of objects interact, reducing direct coupling.",
        idiomatic_example="struct ChatRoomMediator { participants: HashMap<UserId, mpsc::Sender<Message>> }",
    ),
    PatternType.MEMENTO: PatternCatalogEntry(
        pattern_type=PatternType.MEMENTO,
        category=PatternCategory.BEHAVIORAL,
        name="Memento Pattern",
        description="Captures and externalizes an object's internal state so that it can be restored later without violating encapsulation.",
        idiomatic_example="impl Editor { pub fn save(&self) -> Snapshot { ... } pub fn restore(&mut self, s: Snapshot) { ... } }",
    ),
    PatternType.VISITOR: PatternCatalogEntry(
        pattern_type=PatternType.VISITOR,
        category=PatternCategory.BEHAVIORAL,
        name="Visitor Pattern",
        description="Represents an operation to be performed on the elements of an object structure (e.g. AST traversal trait).",
        idiomatic_example="pub trait AstVisitor { fn visit_stmt(&mut self, s: &Stmt); fn visit_expr(&mut self, e: &Expr); }",
    ),
    PatternType.INTERPRETER: PatternCatalogEntry(
        pattern_type=PatternType.INTERPRETER,
        category=PatternCategory.BEHAVIORAL,
        name="Interpreter Pattern",
        description="Given a language, defines a representation for its grammar along with an interpreter that uses the representation to evaluate sentences.",
        idiomatic_example="impl Expr { pub fn evaluate(&self, env: &Environment) -> Result<Value, EvalError> { match self { ... } } }",
    ),

    # Rust-Specific Idioms & Architecture
    PatternType.TYPESTATE: PatternCatalogEntry(
        pattern_type=PatternType.TYPESTATE,
        category=PatternCategory.IDIOM,
        name="Typestate Pattern",
        description="Uses the type system and PhantomData to enforce object state machines at compile-time, consuming self on state transitions.",
        idiomatic_example="struct HttpRequest<State> { _state: PhantomData<State> } impl HttpRequest<Unsent> { pub fn send(self) -> HttpRequest<Sent> { ... } }",
    ),
    PatternType.NEWTYPE: PatternCatalogEntry(
        pattern_type=PatternType.NEWTYPE,
        category=PatternCategory.IDIOM,
        name="Newtype Pattern",
        description="Encapsulates existing primitive or complex types into a single-field tuple struct for type safety, validation, and orphan rule workarounds.",
        idiomatic_example="pub struct UserId(pub u64); pub struct Kilometers(pub f64);",
    ),
    PatternType.RAII_DROP: PatternCatalogEntry(
        pattern_type=PatternType.RAII_DROP,
        category=PatternCategory.IDIOM,
        name="RAII / Drop Guard",
        description="Enforces deterministic resource cleanup (file descriptors, sockets, mutex locks, temp files) via Drop trait implementation.",
        idiomatic_example="pub struct LockGuard<'a> { lock: &'a Mutex } impl<'a> Drop for LockGuard<'a> { fn drop(&mut self) { ... } }",
    ),
    PatternType.ACTOR_MPSC: PatternCatalogEntry(
        pattern_type=PatternType.ACTOR_MPSC,
        category=PatternCategory.ARCHITECTURAL,
        name="Actor / MPSC Worker",
        description="Architectural pattern where isolated workers communicate exclusively via message-passing channels (tokio::sync::mpsc).",
        idiomatic_example="tokio::spawn(async move { while let Some(cmd) = rx.recv().await { match cmd { ... } } });",
    ),
    PatternType.MIDDLEWARE_PIPELINE: PatternCatalogEntry(
        pattern_type=PatternType.MIDDLEWARE_PIPELINE,
        category=PatternCategory.ARCHITECTURAL,
        name="Middleware Pipeline",
        description="Layered request/response architecture following Tower/Axum/Actix middleware patterns.",
        idiomatic_example="struct TowerService<L, S> { layer: L, inner: S }",
    ),
    PatternType.INTERIOR_MUTABILITY: PatternCatalogEntry(
        pattern_type=PatternType.INTERIOR_MUTABILITY,
        category=PatternCategory.IDIOM,
        name="Interior Mutability",
        description="Provides safe mutation of data behind shared immutable references using Arc<Mutex<T>>, RwLock<T>, or RefCell<T>.",
        idiomatic_example="pub struct SharedStore { data: Arc<RwLock<HashMap<String, String>>> }",
    ),
    PatternType.CIRCULAR_DEPENDENCY: PatternCatalogEntry(
        pattern_type=PatternType.CIRCULAR_DEPENDENCY,
        category=PatternCategory.ARCHITECTURAL,
        name="Circular Module Dependency",
        description="Detects cyclic cross-module use dependencies creating tight coupling between Rust modules and sub-crates.",
        idiomatic_example="mod a { use crate::b::B; } mod b { use crate::a::A; }",
    ),

    # Principles & Quality
    PatternType.SINGLE_RESPONSIBILITY: PatternCatalogEntry(
        pattern_type=PatternType.SINGLE_RESPONSIBILITY,
        category=PatternCategory.PRINCIPLE,
        name="Single Responsibility (SRP)",
        description="God Struct detection — structs with excessive fields or methods spanning multiple distinct domains.",
        idiomatic_example="Decompose monolithic structs into cohesive sub-structs.",
    ),
    PatternType.OPEN_CLOSED: PatternCatalogEntry(
        pattern_type=PatternType.OPEN_CLOSED,
        category=PatternCategory.PRINCIPLE,
        name="Open/Closed Principle (OCP)",
        description="Detects rigid concrete match cascades that should be open to extension via trait polymorphism.",
        idiomatic_example="Replace repetitive enum match dispatch with trait object dispatch.",
    ),
    PatternType.LISKOV_SUBSTITUTION: PatternCatalogEntry(
        pattern_type=PatternType.LISKOV_SUBSTITUTION,
        category=PatternCategory.PRINCIPLE,
        name="Liskov Substitution (LSP)",
        description="Detects trait implementations that abort or violate the contract via unimplemented!(), todo!(), or unconditional panic!().",
        idiomatic_example="Avoid unimplemented!() in trait impls; split traits into smaller ones.",
    ),
    PatternType.INTERFACE_SEGREGATION: PatternCatalogEntry(
        pattern_type=PatternType.INTERFACE_SEGREGATION,
        category=PatternCategory.PRINCIPLE,
        name="Interface Segregation (ISP)",
        description="Detects Fat Traits (≥8 methods) forcing implementors to define methods they don't need.",
        idiomatic_example="Break large traits into smaller, focused composable traits.",
    ),
    PatternType.DEPENDENCY_INVERSION: PatternCatalogEntry(
        pattern_type=PatternType.DEPENDENCY_INVERSION,
        category=PatternCategory.PRINCIPLE,
        name="Dependency Inversion (DIP)",
        description="High-level modules should depend on trait abstractions rather than concrete struct types directly.",
        idiomatic_example="fn process_order(repo: impl OrderRepository) instead of fn process_order(repo: SqlOrderRepo)",
    ),
    PatternType.COMPOSITION_OVER_INHERITANCE: PatternCatalogEntry(
        pattern_type=PatternType.COMPOSITION_OVER_INHERITANCE,
        category=PatternCategory.PRINCIPLE,
        name="Composition Over Deep Traits",
        description="Encourages struct composition and trait delegation rather than deeply nested super-trait hierarchies.",
        idiomatic_example="struct Robot { battery: Battery, arm: RoboticArm }",
    ),
    PatternType.LAW_OF_DEMETER: PatternCatalogEntry(
        pattern_type=PatternType.LAW_OF_DEMETER,
        category=PatternCategory.PRINCIPLE,
        name="Law of Demeter",
        description="Flags deep getter method call chains violating the principle of least knowledge.",
        idiomatic_example="Avoid a.b().c().d().e(); introduce helper methods on immediate dependencies.",
    ),
    PatternType.HIGH_COHESION_LOW_COUPLING: PatternCatalogEntry(
        pattern_type=PatternType.HIGH_COHESION_LOW_COUPLING,
        category=PatternCategory.PRINCIPLE,
        name="High Cohesion / Low Coupling",
        description="Flags structs with high fan-out (excessive dependencies) and scattered responsibilities.",
        idiomatic_example="Group related methods and minimize external struct references.",
    ),
    PatternType.KISS: PatternCatalogEntry(
        pattern_type=PatternType.KISS,
        category=PatternCategory.PRINCIPLE,
        name="Keep It Simple, Stupid (KISS)",
        description="Flags overly complex functions with high cyclomatic complexity and excessive parameter counts.",
        idiomatic_example="Decompose complex functions into smaller, easily testable subroutines.",
    ),
    PatternType.DRY: PatternCatalogEntry(
        pattern_type=PatternType.DRY,
        category=PatternCategory.PRINCIPLE,
        name="Don't Repeat Yourself (DRY)",
        description="Identifies duplicated method and match arm blocks across structs and functions.",
        idiomatic_example="Extract common logic into helper functions or macros.",
    ),

    # Safety
    PatternType.UNSAFE_BLOCK_GUARD: PatternCatalogEntry(
        pattern_type=PatternType.UNSAFE_BLOCK_GUARD,
        category=PatternCategory.SAFETY,
        name="Unsafe Block Guard",
        description="Audits and catalogs unsafe { ... } blocks, raw pointer dereferencing, and FFI bindings for memory safety review.",
        idiomatic_example="Enclose unsafe operations in safe, validated abstraction wrappers.",
    ),
}
