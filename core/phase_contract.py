"""Deterministic phase contracts for long-running adaptive goals."""
from __future__ import annotations

from typing import Any

MEDIA_CATEGORIES = {"media_production", "video_editing", "audio_video"}


def is_media_goal(category: str, goal_text: str) -> bool:
    lowered = goal_text.casefold()
    return category in MEDIA_CATEGORIES or any(
        marker in lowered for marker in ("video", "footage", "film", "audio", "ffmpeg", "subtitle", "voiceover")
    )


def media_phase_plan() -> list[dict[str, Any]]:
    """The bounded media pipeline required by the acceptance contract."""
    return [
        {
            "agent": "planning", "phase_id": "capability_check", "phase_kind": "capability",
            "budget": 2, "required_tools": ["capability_catalog"],
            "acceptance": ["catalog inspected", "capability sufficiency/gap recorded", "quality bar defined"],
            "instruction": "Inspect capability_catalog once, decide whether registered tools are sufficient, record any capability_gap, and define the acceptance contract. Do not perform implementation or repeat discovery.",
        },
        {
            "agent": "research", "phase_id": "method_research", "phase_kind": "research",
            "budget": 3, "required_tools": ["web_search", "web_fetch", "web_research"],
            "acceptance": ["current best method researched", "alternatives compared", "selected method and verification steps returned"],
            "instruction": "Research the best current safe method and compare FFmpeg, subtitle/transcription, and suitable open-source tools. Return one selected execution recipe with concrete commands/steps. Do not repeat research after this phase succeeds.",
        },
        {
            "agent": "code", "phase_id": "input_probe", "phase_kind": "execution",
            "budget": 3, "required_tools": ["file.list", "shell.exec"],
            "acceptance": ["input exists", "ffprobe streams/duration/resolution/audio captured", "probe evidence saved"],
            "instruction": "Execute the input probe now. Inspect the supplied media with real file and ffprobe tools and save a machine-readable probe artifact. Do not merely describe commands.",
        },
        {
            "agent": "code", "phase_id": "scene_timestamps", "phase_kind": "execution",
            "budget": 4, "required_tools": ["shell.exec", "file.write"],
            "acceptance": ["actual scene/timestamp evidence saved", "three edit windows selected from the real input"],
            "instruction": "Use the input probe and real media inspection to choose timestamps for at least three intentional edits. Save scene/timestamp decisions; do not invent timestamps without evidence.",
        },
        {
            "agent": "code", "phase_id": "ffmpeg_edit", "phase_kind": "execution",
            "budget": 5, "required_tools": ["shell.exec"],
            "acceptance": ["FFmpeg command actually ran", "final MP4 exists", "video and expected audio streams are present"],
            "instruction": "Run the selected FFmpeg edit now using the saved timestamps. Produce output/suzume_final_edit.mp4 and verify its non-zero size. Do not return success before a real output file exists.",
        },
        {
            "agent": "code", "phase_id": "subtitle_decision", "phase_kind": "execution",
            "budget": 3, "required_tools": ["file.write", "shell.exec"],
            "acceptance": ["SRT exists or truthful no-dialogue decision exists", "decision artifact explains evidence and limits"],
            "instruction": "Decide subtitles from the actual audio/content. Create output/suzume_subtitles.srt only for real dialogue, or create a truthful empty-dialogue decision note. Save output/EDIT_DECISIONS.md.",
        },
        {
            "agent": "review", "phase_id": "ffprobe", "phase_kind": "verification",
            "budget": 3, "required_tools": ["shell.exec", "file.read"],
            "acceptance": ["ffprobe validates final MP4", "duration/video/audio checks recorded"],
            "instruction": "Run ffprobe and read the final artifacts. Record objective media verification evidence. Reject missing, empty, or invalid outputs.",
        },
        {
            "agent": "review", "phase_id": "final_review", "phase_kind": "verification",
            "budget": 3, "required_tools": ["file.read", "shell.exec", "capability_catalog"],
            "acceptance": ["all phases evidenced", "tool lifecycle truthful", "quality/limitations reported", "task_success only with proof"],
            "instruction": "Perform the final acceptance review across every phase and artifact. Confirm only with evidence; otherwise task_success=false and name the exact missing phase.",
        },
    ]


def phase_for_step(step: dict[str, Any]) -> str:
    return str(step.get("phase_id", step.get("agent", "unknown")))


def should_insert_connector_phase(handoff: dict[str, Any]) -> bool:
    context = handoff.get("context_for_memory") or {}
    gap = context.get("capability_gap")
    if isinstance(gap, list):
        return bool(gap)
    if isinstance(gap, dict):
        return bool(gap.get("missing") or gap.get("required"))
    return bool(gap)
