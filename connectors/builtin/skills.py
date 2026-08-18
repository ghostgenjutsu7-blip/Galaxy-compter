"""First-class skill retrieval and activation tools for every agent."""
from __future__ import annotations

from typing import Any

from core.agent.base_agent import Tool


def _json_skill(skill: Any, include_body: bool = False) -> dict[str, Any]:
    data = skill.to_dict()
    if not include_body:
        data["body"] = str(data.get("body", ""))[:800]
    return data


def register(reg) -> None:
    def skill_search(query: str = "", category: str = "", domain: str = "",
                     target_agent: str = "", solar_system: str = "", orbit: str = "",
                     top_k: int = 5, **_: Any) -> dict[str, Any]:
        from skills.loader import ensure_skills_bootstrapped
        ensure_skills_bootstrapped()
        from core.memory import get_memory
        hits = get_memory().search_l4(query, category=category, domain=domain,
                                      target_agent=target_agent, solar_system=solar_system,
                                      orbit=orbit, top_k=max(1, min(int(top_k), 20)))
        return {"ok": True, "count": len(hits), "skills": [_json_skill(skill) for skill in hits]}

    def skill_read(skill_id: str = "", skill_name: str = "", **_: Any) -> dict[str, Any]:
        from skills.loader import ensure_skills_bootstrapped
        ensure_skills_bootstrapped()
        from core.memory import get_memory
        skill = get_memory().l4.get(skill_id) if skill_id else get_memory().l4.find_by_name(skill_name)
        if not skill:
            return {"ok": False, "error": "skill not found", "skill_id": skill_id, "skill_name": skill_name}
        return {"ok": True, "skill": _json_skill(skill, include_body=True)}

    def skill_activate(skill_id: str = "", skill_name: str = "", agent: str = "",
                       goal_id: str = "", outcome: str = "success", **_: Any) -> dict[str, Any]:
        from skills.loader import ensure_skills_bootstrapped
        ensure_skills_bootstrapped()
        from core.memory import get_memory
        skill = get_memory().l4.get(skill_id) if skill_id else get_memory().l4.find_by_name(skill_name)
        if not skill:
            return {"ok": False, "error": "skill not found", "skill_id": skill_id, "skill_name": skill_name}
        normalized = "failure" if str(outcome).casefold() == "failure" else "success"
        get_memory().l4.record_activation(skill.id, agent=agent, goal_id=goal_id, outcome=normalized)
        return {"ok": True, "skill_id": skill.id, "name": skill.name, "agent": agent,
                "goal_id": goal_id, "outcome": normalized, "use_count": skill.use_count + 1}

    for tool in (
        Tool("skill.search", "memory.read", "Search trusted L4 skills by query, taxonomy, and agent ownership.", skill_search, "auto", ["galaxy:skills"]),
        Tool("skill.read", "memory.read", "Read the full body and metadata of a trusted L4 skill.", skill_read, "auto", ["galaxy:skills"]),
        Tool("skill.activate", "memory.read", "Record successful or failed use of a trusted L4 skill.", skill_activate, "auto", ["galaxy:skills"]),
    ):
        reg.register(tool)
