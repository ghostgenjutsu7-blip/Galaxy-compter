from __future__ import annotations

import pytest

from core.acceptance import evaluate_goal
from core.agent.base_agent import BaseAgent, GalaxyMeta, GALAXY_EXECUTION_PROTOCOL
from core.agent.orchestrator import Orchestrator
from core.phase_contract import media_phase_plan
from core.memory.fingerprint import extract_meta_block
from connectors.builtin import get_registry


def test_nested_galaxy_meta_is_not_truncated():
    payload = extract_meta_block(
        '```galaxy_meta {"mode":"goal_confirmed","classification":'
        '{"category":"video_editing","domain":"video","intent":"edit",'
        '"complexity":"high"}}```'
    )
    assert payload is not None
    assert payload["classification"]["category"] == "video_editing"


def test_media_plan_is_closed_and_ordered():
    orch = object.__new__(Orchestrator)
    plan = orch._default_plan(
        GalaxyMeta(category="video_editing", domain="video", intent="edit", complexity="high"),
        "edit video",
    )
    assert [step["phase_id"] for step in plan] == [
        "capability_check", "method_research", "input_probe", "scene_timestamps",
        "ffmpeg_edit", "subtitle_decision", "ffprobe", "final_review",
    ]
    assert "api" not in [step["agent"] for step in plan]
    assert all(int(step["budget"]) > 0 for step in plan)


def test_media_recovery_retries_only_failed_phase():
    orch = object.__new__(Orchestrator)
    step = media_phase_plan()[2]
    recovery = orch._recovery_steps("code", "edit video", GalaxyMeta(category="video_editing"), step)
    assert len(recovery) == 1
    assert recovery[0]["phase_id"] == "input_probe"
    assert recovery[0]["agent"] == "code"
    assert "research" not in recovery[0]["instruction"].lower()


def test_effective_prompt_contains_capability_and_acceptance_protocol():
    message = BaseAgent().build_messages({}, "perform a complex task", "execute")
    assert GALAXY_EXECUTION_PROTOCOL in message[0]["content"]
    assert "capability_catalog" in message[0]["content"]
    assert "acceptance criteria" in message[0]["content"]


def test_capability_catalog_is_registered():
    registry = get_registry()
    assert registry.get("capability_catalog") is not None


def test_media_acceptance_rejects_missing_output(tmp_path):
    result = evaluate_goal(
        goal_text="edit this video and produce final_edit.mp4",
        classification={"category": "video_editing"},
        handoffs=[], root=tmp_path,
    )
    assert result["success"] is False
    assert "verified edited media output" in result["failure"]


def test_media_acceptance_accepts_truthful_no_dialogue_decision(tmp_path):
    output = tmp_path / "output"
    output.mkdir()
    source = tmp_path / "source.mp4"
    import subprocess
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=320x180:d=1",
        "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-shortest", str(source)
    ], check=True, capture_output=True)
    (output / "EDIT_DECISIONS.md").write_text("No dialogue was intelligible; no-dialogue decision.", encoding="utf-8")
    source.rename(output / "suzume_final_edit.mp4")
    result = evaluate_goal(
        goal_text="edit this video with subtitles and produce final_edit.mp4",
        classification={"category": "video_editing"},
        handoffs=[], root=tmp_path,
    )
    assert result["success"] is True
