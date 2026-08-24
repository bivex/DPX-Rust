"""Rust Actor / MPSC Worker Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType, SourceLocation


class ActorMpscRule(BasePatternRule):
    """Detects Actor / MPSC worker loops in Rust."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.ACTOR_MPSC

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.modules.values():
            src = mod.raw_source
            if not src:
                continue

            # Look for channel creation + loop/recv in background task
            if ("mpsc::channel" in src or "tokio::sync::mpsc" in src or "crossbeam_channel" in src) and ("rx.recv()" in src or "receiver.recv()" in src or "rx.await" in src):
                line = src.find("mpsc::channel")
                line_no = src[:line].count("\n") + 1 if line != -1 else 1
                loc = SourceLocation(file_path=mod.file_path, line=line_no)

                evidences = [
                    Evidence(
                        description=f"Module '{mod.name}' implements Actor Pattern / Message Passing via MPSC channel worker loop",
                        weight=0.75,
                        rule_code="ACTOR_MPSC_WORKER_LOOP",
                        location=loc,
                    )
                ]
                det = self._create_detection(
                    target_name=f"{mod.name}::actor_worker",
                    target_kind="actor_worker",
                    evidences=evidences,
                    location=loc,
                )
                detections.append(det)

        return detections
