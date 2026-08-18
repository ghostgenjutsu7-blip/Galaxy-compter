"""core/agent/orchestrator.py — the Orchestrator (single mind).

§4, §25 Phase 3 ⑮. The only component that talks to the user directly. Owns
the goal lifecycle:
  1. Parse + clarify the goal
  2. Generate the GALAXY_META classification (LLM)
  3. Store classification on the Planet's session_context (the v0-bug fix)
  4. Research-First: L4 → L3 → assemble context
  5. Plan (Planning Agent) -> step list
  6. Execute steps, threading HandoffPackages, recording each to L2 immediately
     (durability checkpoint — a crash mid-goal doesn't lose everything)
  7. complete_task: gravity, promotion, L5 outcome (atomic end-of-goal analysis)
  8. Final summary

Every tool call from every agent passes through the Capability Gate — the gate
is enforced structurally because the Orchestrator is the only thing that hands
tools to agents. The Subconscious Loop yields entirely to any active goal.
"""
from __future__ import annotations

import asyncio
import json
import time
from typing import Any

from core.agent.base_agent import GalaxyMeta, HandoffPackage, new_id
from core.acceptance import evaluate_goal
from core.phase_contract import is_media_goal, media_phase_plan
from core.media_enforcer import ensure_media_execution
from core.core_agents import get_agent
from core.memory import GalaxyMemory, get_memory
from failure.checkpoint import checkpoint, load_checkpoint
from observability.timeline import record as timeline_record
from providers.client import LLMClient, get_llm_client
from providers.manager import get_provider_manager
from security.capability import get_gate
from storage.local import get_storage

CLASSIFY_SYSTEM = (
    "You are Galaxy's Orchestrator and capability strategist. Classify the user's "
    "goal using the GALAXY_META protocol. Return exactly one fenced "
    "```galaxy_meta JSON block with mode, classification {category, domain, intent, "
    "complexity}, plan_summary, needs_clarification, required_capabilities, "
    "acceptance_summary. Categories: code_generation, web_development, ui_ux_design, "
    "data_analysis, devops, document_processing, research, security, writing, "
    "api_integration, web_automation, media_production, video_editing, audio_video, "
    "tool_acquisition, general. Domains may include python, javascript, typescript, "
    "rust, go, java, cpp, video, audio, web, design, etc. Intents: write, fix, "
    "refactor, review, search, analyze, design, edit, discover, create_tool, deploy, "
    "verify. Complexity: low, medium, high. Choose media_production or video_editing "
    "for video/audio editing. Choose tool_acquisition when the goal explicitly asks "
    "to find, install, build, register, or learn a missing capability. Never silently "
    "downgrade a specialized goal to general/write."
)

CLASSIFY_REPAIR_SYSTEM = (
    "The prior classification was missing or malformed. Reclassify the goal now. "
    "Return only one fenced ```galaxy_meta JSON block. Preserve the user's actual "
    "domain, especially media/video/audio/tool-acquisition work. Include category, "
    "domain, intent, complexity, required_capabilities, and acceptance_summary."
)

_SPECIALIZED_KEYWORDS = {
    "media_production": ("video", "audio", "multimedia", "footage", "film", "subtitle", "voiceover", "voice-over", "ffmpeg"),
    "tool_acquisition": ("missing tool", "new tool", "find a tool", "install a tool", "create a tool", "build a tool", "register a tool", "connector", "mcp"),
    "ui_ux_design": ("landing page", "ui/ux", "user interface", "visual design", "design system"),
}


def _keyword_category(goal_text: str) -> str | None:
    lowered = goal_text.casefold()
    for category, words in _SPECIALIZED_KEYWORDS.items():
        if any(word in lowered for word in words):
            return category
    return None


def _requires_external_research(goal_text: str, meta: GalaxyMeta) -> bool:
    lowered = goal_text.casefold()
    research_markers = ("best way", "best tool", "latest", "search the web", "research", "find a tool", "missing tool", "connector", "mcp", "video", "audio", "ffmpeg")
    return meta.complexity == "high" or meta.category in {"media_production", "video_editing", "audio_video", "tool_acquisition"} or any(marker in lowered for marker in research_markers)



class Orchestrator:
    """The single mind. One instance per process."""

    def __init__(self, *, memory: GalaxyMemory | None = None,
                 llm_client: LLMClient | None = None) -> None:
        self.memory = memory or get_memory()
        self.llm = llm_client or get_llm_client()
        self._pm = get_provider_manager()
        self._st = get_storage()
        self._active_goal_ids: set[str] = set()
        self._goal_locks: dict[str, asyncio.Lock] = {}

    # ---- classification (GALAXY_META) ------------------------------------
    async def classify(self, goal_text: str) -> GalaxyMeta:
        """First LLM call for any goal. Returns the classification that gets
        stored on the Planet's session_context."""
        messages = [
            {"role": "system", "content": CLASSIFY_SYSTEM},
            {"role": "user", "content": goal_text},
        ]
        resp = await self.llm.complete(agent="orchestrator", messages=messages,
                                       max_tokens=4096)
        from core.memory.fingerprint import extract_meta_block
        meta = extract_meta_block(resp.text) or {}
        if not meta:
            repair = await self.llm.complete(
                agent="orchestrator",
                messages=[{"role": "system", "content": CLASSIFY_REPAIR_SYSTEM},
                          {"role": "user", "content": goal_text}],
                max_tokens=4096,
            )
            meta = extract_meta_block(repair.text) or {}
        cls = dict(meta.get("classification") or {})
        category = str(cls.get("category") or "general")
        inferred = _keyword_category(goal_text)
        if category == "general" and inferred:
            category = inferred
            cls["category_source"] = "keyword_safety_net"
        allowed = {"code_generation", "web_development", "ui_ux_design", "data_analysis",
                   "devops", "document_processing", "research", "security", "writing",
                   "api_integration", "web_automation", "media_production", "video_editing",
                   "audio_video", "tool_acquisition", "general"}
        if category not in allowed:
            category = inferred or "general"
            cls["unsupported_category"] = str(meta.get("classification", {}).get("category", ""))
        cls["category"] = category
        cls.setdefault("domain", "general")
        cls.setdefault("intent", "write")
        cls.setdefault("complexity", "medium")
        required = meta.get("required_capabilities") or cls.get("required_capabilities") or []
        acceptance = meta.get("acceptance_summary") or cls.get("acceptance_summary") or []
        if isinstance(required, str):
            required = [required]
        if isinstance(acceptance, str):
            acceptance = [acceptance]
        return GalaxyMeta(
            mode=str(meta.get("mode", "goal_confirmed")),
            category=category,
            domain=str(cls.get("domain", "general")),
            intent=str(cls.get("intent", "write")),
            complexity=str(cls.get("complexity", "medium")),
            plan_summary=str(meta.get("plan_summary", "")),
            needs_clarification=bool(meta.get("needs_clarification", False)),
            required_capabilities=[str(x) for x in required if x],
            acceptance_summary=[str(x) for x in acceptance if x],
            classification=cls,
        )

    # ---- the main goal lifecycle -----------------------------------------
    async def run_goal(self, goal_text: str, *,
                       language: str = "en",
                       on_step: Any = None,
                       on_handoff: Any = None,
                       capability_gate=None,
                       owner_session_id: str = "") -> dict[str, Any]:
        """Execute a goal with durable state transitions and real tool calls."""
        goal_id = new_id("goal-")
        now = time.time()
        with self._st.transaction() as conn:
            conn.execute(
                "INSERT INTO goals(id,text,status,created_at,owner_session_id) VALUES(?,?,?,?,?);",
                (goal_id, goal_text, "running", now, owner_session_id),
            )
        self._active_goal_ids.add(goal_id)
        self._goal_locks[goal_id] = asyncio.Lock()
        lock = self._goal_locks[goal_id]
        await lock.acquire()
        gate = capability_gate or get_gate()
        handoffs: list[dict[str, Any]] = []
        planet = None
        classification: dict[str, str] = {}
        try:
            meta = await self.classify(goal_text)
            classification = {"category": meta.category, "domain": meta.domain,
                              "intent": meta.intent, "complexity": meta.complexity,
                              "required_capabilities": json.dumps(meta.required_capabilities, ensure_ascii=False),
                              "acceptance_summary": json.dumps(meta.acceptance_summary, ensure_ascii=False),
                              **{k: str(v) for k, v in meta.classification.items()
                                 if k not in {"category", "domain", "intent", "complexity", "required_capabilities", "acceptance_summary"}}}
            planet = self.memory.l1.create_planet(
                goal_id=goal_id, goal_text=goal_text, classification=classification,
                language=language, owner_session_id=owner_session_id)
            timeline_record(goal_id, agent="orchestrator", event="classified", detail=json.dumps(classification))
            checkpoint(goal_id, state={"status": "classified", "goal_text": goal_text,
                                       "language": language, "owner_session_id": owner_session_id,
                                       "classification": classification, "planet_id": planet.id,
                                       "handoffs": [], "remaining_plan": []})
            if on_step:
                await self._maybe_call(on_step, {"phase": "classified", "meta": meta.model_dump()})

            plan = self._default_plan(meta, goal_text)
            try:
                from config import get_config
                project_root = str(get_config().get("project_root", "") or "")
            except Exception:
                project_root = ""
            context = {"phase_contract": plan, "project_root": project_root,
                       "l4_skills": [s.to_dict() for s in self.memory.search_l4(
                            goal_text, category=meta.category, domain=meta.domain, top_k=5)],
                       "l3_stars": [s.to_dict() for s in self.memory.search_l3(goal_text, top_k=5)],
                       "active_rules": self.memory.active_rules(), "handoff": None,
                       "classification": classification, "untrusted": []}
            checkpoint(goal_id, state={"status": "planned", "goal_text": goal_text,
                                       "language": language, "owner_session_id": owner_session_id,
                                       "classification": classification, "planet_id": planet.id,
                                       "handoffs": [], "remaining_plan": plan})
            if on_step:
                await self._maybe_call(on_step, {"phase": "planned", "plan": plan})

            handoff: HandoffPackage | None = None
            recovery_attempts: set[str] = set()
            for i, step in enumerate(plan):
                agent_name = step["agent"]
                timeline_record(goal_id, agent=agent_name, event="agent_start",
                                detail=step.get("instruction", ""))
                if on_step:
                    await self._maybe_call(on_step, {"phase": "agent_start", "agent": agent_name,
                                                     "step": i, "instruction": step.get("instruction", "")})
                step_context = dict(context)
                step_context["phase"] = step
                step_context["handoff"] = handoff.model_dump() if handoff else None
                if handoff:
                    step_context["research_result"] = handoff.context_for_memory.get("research_result")
                    step_context["capability_gap"] = handoff.context_for_memory.get("capability_gap")
                instruction = step.get("instruction", goal_text)
                step_context["l4_skills"] = [s.to_dict() for s in self.memory.search_l4(
                    instruction, category=meta.category, domain=meta.domain,
                    target_agent=agent_name, top_k=5)]
                step_context["l3_stars"] = [s.to_dict() for s in self.memory.search_l3(instruction, top_k=3)]
                pkg = await get_agent(agent_name).run(
                    memory=self.memory, llm_client=self.llm, goal_text=goal_text,
                    classification=classification, handoff=handoff, context=step_context,
                    capability_gate=gate, goal_id=goal_id)
                if (is_media_goal(meta.category, goal_text)
                        and str(step.get("phase_id")) == "ffprobe"
                        and step_context.get("project_root")):
                    enforcement = await ensure_media_execution(
                        goal_id=goal_id, project_root=step_context["project_root"],
                        agent="code", capability_gate=gate)
                    timeline_record(goal_id, agent="orchestrator", event="media_enforcer",
                                    detail=json.dumps(enforcement, ensure_ascii=False, default=str)[:4000])
                    if enforcement.get("ok"):
                        pkg.context_for_memory["media_enforcer"] = enforcement
                        pkg.task_success = True
                        pkg.decision_confidence = max(pkg.decision_confidence, 0.85)
                    else:
                        pkg.task_success = False
                        pkg.what_was_done = (pkg.what_was_done + " Media enforcer: "
                                             + str(enforcement.get("failure", "failed")))[:1000]
                handoff = pkg
                handoffs.append(pkg.model_dump())
                self._record_partial_handoff(goal_id, planet.id, pkg)
                phase_key = str(step.get("phase_id", agent_name))
                if not pkg.task_success and phase_key not in recovery_attempts:
                    recovery = self._recovery_steps(agent_name, goal_text, meta, step)
                    if recovery:
                        recovery_attempts.add(phase_key)
                        plan[i + 1:i + 1] = recovery
                        timeline_record(goal_id, agent="orchestrator", event="obstacle_detected",
                                        detail=json.dumps({"agent": agent_name, "phase": phase_key, "recovery": recovery}, ensure_ascii=False))
                timeline_record(goal_id, agent=agent_name, event="agent_complete",
                                detail=json.dumps({"success": pkg.task_success, "tools": pkg.tools_used}))
                if on_handoff:
                    await self._maybe_call(on_handoff, pkg.model_dump())
                checkpoint(goal_id, state={"status": "executing", "goal_text": goal_text,
                                           "language": language, "owner_session_id": owner_session_id,
                                           "classification": classification, "planet_id": planet.id,
                                           "handoffs": handoffs, "remaining_plan": plan[i + 1:]})
            acceptance = evaluate_goal(goal_text=goal_text, classification=classification,
                                       handoffs=handoffs)
            self._apply_acceptance(handoffs, acceptance, goal_id=goal_id)
            timeline_record(goal_id, agent="orchestrator", event="acceptance_checked",
                            detail=json.dumps(acceptance, ensure_ascii=False, default=str))
            asteroid = self.memory.complete_task(planet=planet, handoffs=handoffs,
                                                 classification=classification, language=language)
            summary = self._build_summary(goal_id, goal_text, asteroid, handoffs, meta, acceptance)
            with self._st.transaction() as conn:
                conn.execute("UPDATE goals SET status=?, completed_at=?, final_summary=? WHERE id=?;",
                             ("completed" if asteroid.task_success else "failed", time.time(),
                              json.dumps(summary), goal_id))
            checkpoint(goal_id, state={"status": "completed" if summary["success"] else "failed",
                                       "goal_text": goal_text, "language": language,
                                       "owner_session_id": owner_session_id,
                                       "classification": classification, "planet_id": planet.id,
                                       "handoffs": handoffs, "remaining_plan": [], "summary": summary})
            timeline_record(goal_id, agent="orchestrator", event="goal_complete",
                            detail=json.dumps({"success": summary["success"]}))
            return summary
        except asyncio.CancelledError:
            self._mark_goal_failed(goal_id, "cancelled")
            checkpoint(goal_id, state={"status": "cancelled", "goal_text": goal_text,
                                       "classification": classification, "handoffs": handoffs,
                                       "remaining_plan": []})
            raise
        except Exception as exc:
            self._mark_goal_failed(goal_id, str(exc))
            checkpoint(goal_id, state={"status": "failed", "goal_text": goal_text,
                                       "classification": classification, "handoffs": handoffs,
                                       "remaining_plan": [], "error": str(exc)})
            timeline_record(goal_id, agent="orchestrator", event="goal_failed", detail=str(exc))
            raise
        finally:
            if lock.locked():
                lock.release()
            self._active_goal_ids.discard(goal_id)
            self._goal_locks.pop(goal_id, None)

    def _mark_goal_failed(self, goal_id: str, error: str) -> None:
        with self._st.transaction() as conn:
            conn.execute("UPDATE goals SET status=?, completed_at=?, final_summary=? WHERE id=?;",
                         ("failed", time.time(), json.dumps({"error": error}), goal_id))

    async def resume_goal(self, goal_id: str, *, on_step: Any = None,
                          capability_gate=None) -> dict[str, Any]:
        """Resume remaining plan steps from a durable checkpoint."""
        cp = load_checkpoint(goal_id)
        if not cp or not cp.get("remaining_plan"):
            raise ValueError(f"no resumable checkpoint for {goal_id}")
        planet = self.memory.l1.get_planet_by_goal(goal_id)
        if planet is None:
            raise ValueError(f"planet for {goal_id} not found")
        classification = dict(cp.get("classification") or planet.session_context.get("classification", {}))
        goal_text = str(cp.get("goal_text") or planet.goal_text)
        language = str(cp.get("language") or planet.session_context.get("language", "en"))
        handoffs = list(cp.get("handoffs") or [])
        handoff = HandoffPackage(**handoffs[-1]) if handoffs else None
        plan = list(cp.get("remaining_plan") or [])
        gate = capability_gate or get_gate()
        self._active_goal_ids.add(goal_id)
        lock = self._goal_locks.setdefault(goal_id, asyncio.Lock())
        await lock.acquire()
        try:
            for i, step in enumerate(plan):
                agent_name = step["agent"]
                instruction = step.get("instruction", goal_text)
                context = {                           "l4_skills": [s.to_dict() for s in self.memory.search_l4(
                                instruction, category=classification.get("category", ""),
                                domain=classification.get("domain", ""), target_agent=agent_name,
                                top_k=5)],
                           "l3_stars": [s.to_dict() for s in self.memory.search_l3(instruction, top_k=3)],
                           "active_rules": self.memory.active_rules(), "handoff": handoff.model_dump() if handoff else None,
                           "classification": classification, "untrusted": []}
                if on_step:
                    await self._maybe_call(on_step, {"phase": "resume_agent_start", "agent": agent_name})
                pkg = await get_agent(agent_name).run(
                    memory=self.memory, llm_client=self.llm, goal_text=goal_text,
                    classification=classification, handoff=handoff, context=context,
                    capability_gate=gate, goal_id=goal_id)
                handoff = pkg
                handoffs.append(pkg.model_dump())
                self._record_partial_handoff(goal_id, planet.id, pkg)
                checkpoint(goal_id, state={"status": "resuming", "goal_text": goal_text,
                                           "language": language, "classification": classification,
                                           "planet_id": planet.id, "handoffs": handoffs,
                                           "remaining_plan": plan[i + 1:]})
            acceptance = evaluate_goal(goal_text=goal_text, classification=classification,
                                       handoffs=handoffs)
            self._apply_acceptance(handoffs, acceptance, goal_id=goal_id)
            meta = GalaxyMeta(category=classification.get("category", "general"),
                              domain=classification.get("domain", "general"),
                              intent=classification.get("intent", "write"),
                              complexity=classification.get("complexity", "medium"),
                              classification=classification)
            asteroid = self.memory.complete_task(planet=planet, handoffs=handoffs,
                                                 classification=classification, language=language)
            summary = self._build_summary(goal_id, goal_text, asteroid, handoffs, meta, acceptance)
            with self._st.transaction() as conn:
                conn.execute("UPDATE goals SET status=?, completed_at=?, final_summary=? WHERE id=?;",
                             ("completed" if asteroid.task_success else "failed", time.time(),
                              json.dumps(summary), goal_id))
            checkpoint(goal_id, state={"status": "completed" if summary["success"] else "failed",
                                       "goal_text": goal_text, "language": language,
                                       "classification": classification, "planet_id": planet.id,
                                       "handoffs": handoffs, "remaining_plan": [], "summary": summary})
            return summary
        finally:
            if lock.locked():
                lock.release()
            self._active_goal_ids.discard(goal_id)
            self._goal_locks.pop(goal_id, None)

    # ---- default plan -----------------------------------------------------
    def _default_plan(self, meta: GalaxyMeta, goal_text: str) -> list[dict[str, Any]]:
        """Map a classification to an ordered agent sequence. The Planning
        Agent can override this with a richer plan; this is the sensible
        default that engages >=3 agents for a real handoff chain."""
        cat = meta.category
        if is_media_goal(cat, goal_text):
            return media_phase_plan()
        plan: list[dict[str, Any]] = [{"agent": "planning",
            "instruction": f"Decompose this goal into steps: {goal_text}"}]
        if cat in ("media_production", "video_editing", "audio_video"):
            plan.append({"agent": "research", "instruction": "Research the best current video/audio editing approach and available tools before implementation"})
            plan.append({"agent": "api", "instruction": "Inspect and connect an appropriate external connector or MCP capability if the registered tools are insufficient"})
            plan.append({"agent": "code", "instruction": "Implement the media edit and produce verified output artifacts"})
            plan.append({"agent": "review", "instruction": "Verify the media output with probes, streams, duration, and acceptance criteria"})
        elif cat in ("tool_acquisition",):
            plan.append({"agent": "research", "instruction": "Search the web and trusted sources for the best tool or connector for this capability"})
            plan.append({"agent": "api", "instruction": "Discover, connect, and verify the selected connector or MCP capability"})
            plan.append({"agent": "code", "instruction": "Build a local tool only if no suitable existing capability is usable"})
            plan.append({"agent": "review", "instruction": "Verify registration, real invocation, safety boundary, and persistence"})
        elif cat in ("code_generation", "web_development"):
            if _requires_external_research(goal_text, meta):
                plan.append({"agent": "research", "instruction": "Research the best current implementation approach and available tools before coding"})
            plan.append({"agent": "code", "instruction": "Implement the change and produce a concrete verified artifact"})
            plan.append({"agent": "review", "instruction": "Review the implementation and verify required outputs"})
        elif cat in ("api_integration",):
            plan.append({"agent": "api", "instruction": "Build the API integration"})
            plan.append({"agent": "review", "instruction": "Review the integration"})
        elif cat in ("ui_ux_design",):
            plan.append({"agent": "design", "instruction": "Produce the design"})
            plan.append({"agent": "review", "instruction": "Review the design"})
        elif cat in ("data_analysis",):
            plan.append({"agent": "data", "instruction": "Analyze the data"})
            plan.append({"agent": "review", "instruction": "Review the analysis"})
        elif cat in ("research",):
            plan.append({"agent": "research", "instruction": "Research the topic"})
            plan.append({"agent": "write", "instruction": "Write up the findings"})
        elif cat in ("devops",):
            plan.append({"agent": "devops", "instruction": "Perform the infra task"})
            plan.append({"agent": "review", "instruction": "Verify the change"})
        elif cat in ("security",):
            plan.append({"agent": "security", "instruction": "Perform the security review"})
            plan.append({"agent": "review", "instruction": "Confirm findings"})
        elif cat in ("document_processing",):
            plan.append({"agent": "file", "instruction": "Process the document"})
            plan.append({"agent": "review", "instruction": "Verify the output"})
        elif cat in ("writing",):
            plan.append({"agent": "write", "instruction": "Write the document"})
            plan.append({"agent": "review", "instruction": "Review the writing"})
        elif cat in ("web_automation",):
            plan.append({"agent": "browser", "instruction": "Perform the automation"})
            plan.append({"agent": "review", "instruction": "Verify the result"})
        else:
            plan.append({"agent": "code", "instruction": "Handle the goal"})
            plan.append({"agent": "review", "instruction": "Review"})
        return plan

    @staticmethod
    def _recovery_steps(agent_name: str, goal_text: str, meta: GalaxyMeta,
                        step: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Map a real failure to one bounded obstacle-resolution rung."""
        step = step or {}
        if is_media_goal(meta.category, goal_text):
            phase_id = str(step.get("phase_id", agent_name))
            if agent_name == "review":
                return []
            # The contract is intentionally closed: no late Research/API loops.
            return [{**step,
                     "instruction": f"Retry only the failed media phase {phase_id} once using the prior handoff and existing tools. Do not restart discovery or add a new connector.",
                     "retry_of": phase_id,
                     "budget": min(int(step.get("budget", 2) or 2), 2)}]
        if agent_name == "review":
            return []
        if agent_name == "research":
            return [{"agent": "api", "instruction": "Use the research findings to inspect or connect a suitable registered/MCP capability"}]
        if agent_name == "api":
            return [{"agent": "code", "instruction": "Implement a local fallback only after connector discovery failed"}]
        if agent_name == "code":
            return [
                {"agent": "research", "instruction": "Investigate the obstacle and search for a better supported approach"},
                {"agent": "api", "instruction": "Try an existing connector or MCP capability for the blocked operation"},
                {"agent": "code", "instruction": "Retry implementation using the verified capability or build a bounded local tool"},
            ]
        return [{"agent": "research", "instruction": f"Investigate the obstacle in: {goal_text}"}]

    def _record_partial_handoff(self, goal_id: str, planet_id: str,
                                pkg: HandoffPackage) -> None:
        """Durability checkpoint (§4): write context_for_memory to L2 on every
        handoff, not just at the end. A crash mid-goal doesn't lose everything.
        This is purely durability — the final Gravity Score still happens once,
        atomically, after the whole Planet completes."""
        with self._st.transaction() as conn:
            conn.execute(
                "INSERT INTO handoffs(goal_id,step,from_agent,to_agent,package,ts) "
                "VALUES(?,?,?,?,?,?);",
                (goal_id, len(self._handoff_count(goal_id)) + 0, pkg.agent,
                 pkg.next_agent, pkg.model_dump_json(), time.time()),
            )

    def _handoff_count(self, goal_id: str) -> list[dict[str, Any]]:
        return self._st.query_all(
            "SELECT * FROM handoffs WHERE goal_id=? ORDER BY step;", (goal_id,))

    # ---- summary ----------------------------------------------------------
    @staticmethod
    def _apply_acceptance(handoffs: list[dict[str, Any]], acceptance: dict[str, Any], *, goal_id: str = "") -> None:
        """Make acceptance and lifecycle evidence authoritative over model prose."""
        if not handoffs:
            return
        final = handoffs[-1]
        ctx = final.setdefault("context_for_memory", {})
        ctx["acceptance_evidence"] = acceptance
        try:
            from observability.tool_lifecycle import lifecycle_snapshot
            ctx["tool_lifecycle_evidence"] = lifecycle_snapshot(goal_id)
        except Exception:
            ctx["tool_lifecycle_evidence"] = []
        if acceptance.get("success", False):
            # Acceptance is the source of truth for the goal outcome. Earlier
            # bounded retries may have failed on malformed arguments or a
            # transient whitelist issue while a later phase/enforcer proved all
            # required artifacts. Preserve that evidence but do not fail the
            # completed goal because of a recovered attempt.
            for handoff in handoffs:
                if not handoff.get("task_success", True):
                    recovered_ctx = handoff.setdefault("context_for_memory", {})
                    recovered_ctx["recovered_by_acceptance"] = True
                    handoff["task_success"] = True
                    handoff["decision_confidence"] = max(float(handoff.get("decision_confidence", 0.2)), 0.5)
            final.setdefault("context_for_memory", {})["acceptance_status"] = "proven"
        else:
            final["task_success"] = False
            final["decision_confidence"] = min(float(final.get("decision_confidence", 0.5)), 0.2)
            final["what_was_done"] = (str(final.get("what_was_done", "")) +
                                       " Acceptance failed: " + str(acceptance.get("failure", "unknown")))[:1000]

    def _build_summary(self, goal_id: str, goal_text: str, asteroid, handoffs,
                       meta: GalaxyMeta, acceptance: dict[str, Any] | None = None) -> dict[str, Any]:
        in_t, out_t = self.llm.session_tokens()
        artifacts: list[dict[str, Any]] = []
        for h in handoffs:
            artifacts.extend(h.get("artifacts_created") or [])
        return {
            "goal_id": goal_id,
            "goal_text": goal_text,
            "classification": meta.classification,
            "success": asteroid.task_success,
            "gravity_score": round(asteroid.gravity_score, 4),
            "gravity_bucket": _bucket(asteroid.gravity_score),
            "steps": [{"agent": h.get("agent"), "what": h.get("what_was_done", "")[:120],
                       "success": h.get("task_success", True),
                       "tools_used": h.get("tools_used", [])} for h in handoffs],
            "artifacts": artifacts,
            "promoted_to_l3": bool(asteroid.promoted_to),
            "asteroid_id": asteroid.id,
            "llm_calls": len(self.llm.call_log()),
            "input_tokens": in_t,
            "output_tokens": out_t,
            "elapsed_ms": sum(h.get("elapsed_ms", 0) for h in handoffs),
            "acceptance": acceptance or {"success": bool(asteroid.task_success)},
        }

    # ---- chat mode (no agents) -------------------------------------------
    async def chat(self, text: str, *, language: str = "en") -> str:
        """Pure conversation. No agents visible. Draws on L1–L5 silently."""
        l3 = self.memory.search_l3(text, top_k=3)
        l4 = self.memory.search_l4(text, top_k=3)
        sys_parts = ["You are Galaxy Computer. Respond conversationally in the user's language."]
        if l3:
            sys_parts.append("Relevant memories:\n" + "\n".join(f"- {s.topic}: {s.summary}" for s in l3))
        if l4:
            sys_parts.append("Relevant skills:\n" + "\n".join(f"- {s.name}" for s in l4))
        resp = await self.llm.complete(agent="orchestrator",
            messages=[{"role": "system", "content": "\n\n".join(sys_parts)},
                      {"role": "user", "content": text}],
            max_tokens=600)
        return resp.text

    # ---- helpers ----------------------------------------------------------
    async def _maybe_call(self, fn, arg) -> None:
        import inspect
        if inspect.iscoroutinefunction(fn):
            await fn(arg)
        else:
            fn(arg)

    def is_goal_active(self) -> bool:
        return bool(self._active_goal_ids)


def _bucket(g: float) -> str:
    if g < 0.30:
        return "nebula"
    if g < 0.60:
        return "asteroid"
    if g < 0.85:
        return "planet_to_l3"
    return "star_permanent"


_orchestrator: Orchestrator | None = None


def get_orchestrator() -> Orchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = Orchestrator()
    return _orchestrator


def reset_orchestrator_for_tests() -> Orchestrator:
    global _orchestrator
    _orchestrator = Orchestrator()
    return _orchestrator
