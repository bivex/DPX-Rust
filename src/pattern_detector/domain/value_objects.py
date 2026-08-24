"""Domain value objects for the Rust Pattern Detector."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class PatternCategory(str, Enum):
    """Broad classification of design patterns, Rust idioms, and engineering principles."""

    CREATIONAL = "creational"
    STRUCTURAL = "structural"
    BEHAVIORAL = "behavioral"
    ARCHITECTURAL = "architectural"
    IDIOM = "idiom"
    PRINCIPLE = "principle"
    SAFETY = "safety"


class PatternType(str, Enum):
    """Specific design pattern, Rust idiom, and engineering principle identifiers."""

    # Creational
    SINGLETON = "singleton"
    FACTORY_METHOD = "factory_method"
    ABSTRACT_FACTORY = "abstract_factory"
    BUILDER = "builder"
    PROTOTYPE = "prototype"

    # Structural
    ADAPTER = "adapter"
    DECORATOR = "decorator"
    FACADE = "facade"
    COMPOSITE = "composite"
    PROXY = "proxy"
    BRIDGE = "bridge"
    FLYWEIGHT = "flyweight"

    # Behavioral
    OBSERVER = "observer"
    STRATEGY = "strategy"
    COMMAND = "command"
    TEMPLATE_METHOD = "template_method"
    CHAIN_OF_RESPONSIBILITY = "chain_of_responsibility"
    STATE = "state"
    ITERATOR = "iterator"
    MEDIATOR = "mediator"
    MEMENTO = "memento"
    VISITOR = "visitor"
    INTERPRETER = "interpreter"

    # Rust-Specific Idioms & Architectural Patterns
    TYPESTATE = "typestate"
    NEWTYPE = "newtype"
    RAII_DROP = "raii_drop"
    ACTOR_MPSC = "actor_mpsc"
    MIDDLEWARE_PIPELINE = "middleware_pipeline"
    INTERIOR_MUTABILITY = "interior_mutability"
    CIRCULAR_DEPENDENCY = "circular_dependency"

    # SOLID & Engineering Principles
    SINGLE_RESPONSIBILITY = "single_responsibility"
    OPEN_CLOSED = "open_closed"
    LISKOV_SUBSTITUTION = "liskov_substitution"
    INTERFACE_SEGREGATION = "interface_segregation"
    DEPENDENCY_INVERSION = "dependency_inversion"
    COMPOSITION_OVER_INHERITANCE = "composition_over_inheritance"
    LAW_OF_DEMETER = "law_of_demeter"
    HIGH_COHESION_LOW_COUPLING = "high_cohesion_low_coupling"
    KISS = "kiss"
    DRY = "dry"

    # Safety & Unsoundness Auditing
    UNSAFE_BLOCK_GUARD = "unsafe_block_guard"


class ConfidenceLevel(str, Enum):
    """Categorical confidence rating for a pattern detection."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

    @classmethod
    def from_score(cls, score: float) -> ConfidenceLevel:
        if score >= 0.85:
            return cls.VERY_HIGH
        if score >= 0.70:
            return cls.HIGH
        if score >= 0.50:
            return cls.MEDIUM
        return cls.LOW


@dataclass(frozen=True)
class SourceLocation:
    """Represents a precise location in a Rust source code file."""

    file_path: str
    line: int = 1
    column: int = 1
    end_line: int | None = None
    end_column: int | None = None

    def __str__(self) -> str:
        return f"{self.file_path}:{self.line}:{self.column}"


@dataclass(frozen=True)
class Evidence:
    """A single piece of heuristic evidence supporting a pattern detection."""

    description: str
    weight: float
    rule_code: str
    location: SourceLocation | None = None

    def __post_init__(self) -> None:
        if not (0.0 <= self.weight <= 1.0):
            raise ValueError(f"Evidence weight must be between 0.0 and 1.0, got {self.weight}")


@dataclass(frozen=True)
class Confidence:
    """Aggregated confidence score computed from multiple pieces of evidence."""

    score: float
    level: ConfidenceLevel = field(init=False)

    def __post_init__(self) -> None:
        clamped = max(0.0, min(1.0, self.score))
        object.__setattr__(self, "score", clamped)
        object.__setattr__(self, "level", ConfidenceLevel.from_score(clamped))

    @classmethod
    def from_evidences(cls, evidences: list[Evidence]) -> Confidence:
        if not evidences:
            return cls(0.0)
        # Saturating accumulation: 1 - prod(1 - w_i)
        complement_product = 1.0
        for ev in evidences:
            complement_product *= (1.0 - ev.weight)
        return cls(1.0 - complement_product)

    @property
    def percentage_str(self) -> str:
        return f"{int(self.score * 100)}%"
