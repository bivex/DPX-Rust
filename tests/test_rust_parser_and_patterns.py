"""Tests for Native Rust Parser and Pattern Detection Rules."""

from pathlib import Path
from pattern_detector.bootstrap.container import create_container
from pattern_detector.domain.value_objects import PatternCategory, PatternType
from pattern_detector.ports.inbound import ScanOptions


def test_native_rust_parser_extracts_structures() -> None:
    container = create_container()
    parser = container.parser

    code = """
    pub struct ServerBuilder {
        host: Option<String>,
        port: Option<u16>,
    }

    impl ServerBuilder {
        pub fn new() -> Self { Self { host: None, port: None } }
        pub fn host(mut self, h: String) -> Self { self.host = Some(h); self }
        pub fn build(self) -> Result<String, ()> { Ok("server".into()) }
    }
    """
    mod = parser.parse_file("src/server.rs", code)

    assert "ServerBuilder" in mod.structs
    st = mod.structs["ServerBuilder"]
    assert len(st.fields) == 2
    assert "new" in st.methods
    assert "build" in st.methods
    assert "host" in st.methods


def test_full_scan_on_rust_examples() -> None:
    container = create_container()
    scanner = container.get_scanner()

    examples_dir = str(Path(__file__).parent.parent / "examples" / "rust_samples")
    report = scanner.scan_path(examples_dir)

    assert report.scanned_files_count == 3
    assert report.total_detections_count > 10

    detected_types = {d.pattern_type for d in report.detections}

    # Verify key Rust patterns were detected
    assert PatternType.BUILDER in detected_types
    assert PatternType.NEWTYPE in detected_types
    assert PatternType.TYPESTATE in detected_types
    assert PatternType.RAII_DROP in detected_types
    assert PatternType.FACTORY_METHOD in detected_types
    assert PatternType.STRATEGY in detected_types
    assert PatternType.OBSERVER in detected_types
    assert PatternType.COMMAND in detected_types
    assert PatternType.TEMPLATE_METHOD in detected_types
    assert PatternType.ITERATOR in detected_types
    assert PatternType.SINGLE_RESPONSIBILITY in detected_types
    assert PatternType.LISKOV_SUBSTITUTION in detected_types
    assert PatternType.KISS in detected_types
    assert PatternType.UNSAFE_BLOCK_GUARD in detected_types


def test_no_principles_option_filters_solid() -> None:
    container = create_container()
    scanner = container.get_scanner()

    examples_dir = str(Path(__file__).parent.parent / "examples" / "rust_samples")
    opts = ScanOptions(include_principles=False)
    report = scanner.scan_path(examples_dir, options=opts)

    for d in report.detections:
        assert d.pattern_category != PatternCategory.PRINCIPLE


def test_all_38_rules_registered_and_executable() -> None:
    from pattern_detector.domain.rules import DEFAULT_RULES
    from pattern_detector.domain.code_model import CodeModel

    assert len(DEFAULT_RULES) == 41
    empty_model = CodeModel()

    for rule in DEFAULT_RULES:
        dets = rule.detect(empty_model)
        assert isinstance(dets, list)


def test_circular_dependency_detection() -> None:
    container = create_container()
    parser = container.parser
    scanner = container.get_scanner()

    sources = {
        "src/a.rs": "use crate::b::B; pub struct A;",
        "src/b.rs": "use crate::c::C; pub struct B;",
        "src/c.rs": "use crate::a::A; pub struct C;",
    }
    report = scanner.scan_sources(sources)
    circ_dets = [d for d in report.detections if d.pattern_type == PatternType.CIRCULAR_DEPENDENCY]
    assert len(circ_dets) >= 1
    assert "a ➔ b ➔ c ➔ a" in circ_dets[0].summary or "a" in circ_dets[0].target_name


def test_interior_mutability_and_actor_detection() -> None:
    container = create_container()
    scanner = container.get_scanner()

    code = """
    use std::sync::{Arc, Mutex};
    use tokio::sync::mpsc;

    pub struct SharedState {
        pub count: Arc<Mutex<u64>>,
    }

    pub async fn run_actor() {
        let (tx, mut rx) = mpsc::channel::<String>(32);
        tokio::spawn(async move {
            while let Some(msg) = rx.recv().await {
                println!("Received: {}", msg);
            }
        });
    }
    """
    report = scanner.scan_sources({"src/actor.rs": code})
    detected = {d.pattern_type for d in report.detections}
    assert PatternType.INTERIOR_MUTABILITY in detected
    assert PatternType.ACTOR_MPSC in detected

