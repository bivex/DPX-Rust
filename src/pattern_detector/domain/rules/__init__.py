"""Rule catalog registration for Rust pattern detector."""

from __future__ import annotations

from pattern_detector.domain.rules.abstract_factory_rule import AbstractFactoryRule
from pattern_detector.domain.rules.actor_mpsc_rule import ActorMpscRule
from pattern_detector.domain.rules.adapter_rule import AdapterPatternRule
from pattern_detector.domain.rules.base import BasePatternRule, PatternRule
from pattern_detector.domain.rules.bridge_rule import BridgePatternRule
from pattern_detector.domain.rules.builder_rule import BuilderPatternRule
from pattern_detector.domain.rules.chain_of_responsibility_rule import ChainOfResponsibilityRule
from pattern_detector.domain.rules.circular_dependency_rule import CircularDependencyRule
from pattern_detector.domain.rules.cohesion_coupling_rule import HighCohesionLowCouplingRule
from pattern_detector.domain.rules.command_rule import CommandPatternRule
from pattern_detector.domain.rules.composite_rule import CompositePatternRule
from pattern_detector.domain.rules.composition_over_inheritance_rule import CompositionOverInheritanceRule
from pattern_detector.domain.rules.decorator_rule import DecoratorPatternRule
from pattern_detector.domain.rules.dip_rule import DependencyInversionRule
from pattern_detector.domain.rules.dry_rule import DryRule
from pattern_detector.domain.rules.facade_rule import FacadePatternRule
from pattern_detector.domain.rules.factory_rule import FactoryMethodRule
from pattern_detector.domain.rules.flyweight_rule import FlyweightPatternRule
from pattern_detector.domain.rules.interior_mutability_rule import InteriorMutabilityRule
from pattern_detector.domain.rules.interpreter_rule import InterpreterPatternRule
from pattern_detector.domain.rules.isp_rule import InterfaceSegregationRule
from pattern_detector.domain.rules.iterator_rule import IteratorPatternRule
from pattern_detector.domain.rules.kiss_rule import KissRule
from pattern_detector.domain.rules.law_of_demeter_rule import LawOfDemeterRule
from pattern_detector.domain.rules.lsp_rule import LiskovSubstitutionRule
from pattern_detector.domain.rules.mediator_rule import MediatorPatternRule
from pattern_detector.domain.rules.memento_rule import MementoPatternRule
from pattern_detector.domain.rules.middleware_pipeline_rule import MiddlewarePipelineRule
from pattern_detector.domain.rules.newtype_rule import NewtypePatternRule
from pattern_detector.domain.rules.observer_rule import ObserverPatternRule
from pattern_detector.domain.rules.ocp_rule import OpenClosedPrincipleRule
from pattern_detector.domain.rules.prototype_rule import PrototypePatternRule
from pattern_detector.domain.rules.proxy_rule import ProxyPatternRule
from pattern_detector.domain.rules.raii_drop_rule import RaiiDropRule
from pattern_detector.domain.rules.singleton_rule import SingletonPatternRule
from pattern_detector.domain.rules.srp_rule import SingleResponsibilityRule
from pattern_detector.domain.rules.state_rule import StatePatternRule
from pattern_detector.domain.rules.strategy_rule import StrategyPatternRule
from pattern_detector.domain.rules.template_method_rule import TemplateMethodRule
from pattern_detector.domain.rules.typestate_rule import TypestatePatternRule
from pattern_detector.domain.rules.unsafe_guard_rule import UnsafeGuardRule
from pattern_detector.domain.rules.visitor_rule import VisitorPatternRule

DEFAULT_RULES: list[PatternRule] = [
    # Creational (5)
    BuilderPatternRule(),
    FactoryMethodRule(),
    AbstractFactoryRule(),
    PrototypePatternRule(),
    SingletonPatternRule(),

    # Structural (7)
    AdapterPatternRule(),
    DecoratorPatternRule(),
    FacadePatternRule(),
    CompositePatternRule(),
    ProxyPatternRule(),
    BridgePatternRule(),
    FlyweightPatternRule(),

    # Behavioral (11)
    ObserverPatternRule(),
    StrategyPatternRule(),
    CommandPatternRule(),
    TemplateMethodRule(),
    ChainOfResponsibilityRule(),
    StatePatternRule(),
    IteratorPatternRule(),
    MediatorPatternRule(),
    MementoPatternRule(),
    VisitorPatternRule(),
    InterpreterPatternRule(),

    # Rust Idioms & Architecture (7)
    TypestatePatternRule(),
    NewtypePatternRule(),
    RaiiDropRule(),
    ActorMpscRule(),
    MiddlewarePipelineRule(),
    InteriorMutabilityRule(),
    CircularDependencyRule(),

    # Principles & Safety (11)
    SingleResponsibilityRule(),
    OpenClosedPrincipleRule(),
    LiskovSubstitutionRule(),
    InterfaceSegregationRule(),
    DependencyInversionRule(),
    CompositionOverInheritanceRule(),
    LawOfDemeterRule(),
    HighCohesionLowCouplingRule(),
    KissRule(),
    DryRule(),
    UnsafeGuardRule(),
]

__all__ = [
    "BasePatternRule",
    "PatternRule",
    "DEFAULT_RULES",
    "BuilderPatternRule",
    "FactoryMethodRule",
    "AbstractFactoryRule",
    "PrototypePatternRule",
    "SingletonPatternRule",
    "AdapterPatternRule",
    "DecoratorPatternRule",
    "FacadePatternRule",
    "CompositePatternRule",
    "ProxyPatternRule",
    "BridgePatternRule",
    "FlyweightPatternRule",
    "ObserverPatternRule",
    "StrategyPatternRule",
    "CommandPatternRule",
    "TemplateMethodRule",
    "ChainOfResponsibilityRule",
    "StatePatternRule",
    "IteratorPatternRule",
    "MediatorPatternRule",
    "MementoPatternRule",
    "VisitorPatternRule",
    "InterpreterPatternRule",
    "TypestatePatternRule",
    "NewtypePatternRule",
    "RaiiDropRule",
    "ActorMpscRule",
    "MiddlewarePipelineRule",
    "InteriorMutabilityRule",
    "CircularDependencyRule",
    "SingleResponsibilityRule",
    "OpenClosedPrincipleRule",
    "LiskovSubstitutionRule",
    "InterfaceSegregationRule",
    "DependencyInversionRule",
    "CompositionOverInheritanceRule",
    "LawOfDemeterRule",
    "HighCohesionLowCouplingRule",
    "KissRule",
    "DryRule",
    "UnsafeGuardRule",
]
