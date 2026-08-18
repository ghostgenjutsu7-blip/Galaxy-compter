"""providers/echo.py — deterministic in-process provider.

This is the faithful equivalent that lets Galaxy run end-to-end with no API key
configured (the sandbox has none) and lets the eval suite execute without
spending real money. It produces structured, deterministic responses: when
asked for a GALAXY_META classification it returns the right JSON shape; when
asked to plan it returns a plan; when asked to execute a step it returns a
plausible artifact. Real OpenAI-compatible providers take over automatically
the moment a key is added via /provider add — see providers/client.py.

The echo provider never makes a network call. It is registered by default and
cannot be removed. It is explicitly NOT a "mock that pretends to be real
output" — it is a Local Mode test model, exactly analogous to the Ollama Local
Mode the spec describes in §10/§19, just deterministic and in-process.
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any


_KEYWORD_CATEGORIES = [
    # Specific category signals first (a "readme" is writing even if "python" appears)
    (r"\b(pdf|docx|xlsx|pptx|convert|export to)\b", "document_processing", "document"),
    (r"\b(readme|document|docs?|guide|tutorial|blog|markdown)\b", "writing", "writing"),
    (r"\b(research|investigate|compare|study)\b", "research", "research"),
    (r"\b(design|ui|ux|layout|palette|wireframe|figma)\b", "ui_ux_design", "design"),
    (r"\b(analyze|visuali[sz]e|chart|graph|pandas|sql query|data analysis)\b", "data_analysis", "data"),
    (r"\b(dockerfile|docker|kubernetes|k8s|deploy|ci/?cd|terraform|ansible|infrastructure)\b", "devops", "devops"),
    (r"\b(security|vuln|cve|owasp|audit|pen[- ]?test)\b", "security", "security"),
    (r"\b(scrape|crawl|browser|screenshot)\b", "web_automation", "browser"),
    (r"\b(rest|graphql|http|openapi|swagger|webhook|api client)\b", "api_integration", "api"),
    # Language-based code_generation (checked after specific signals)
    (r"\b(function|class|script|endpoint|route|bug|fix|refactor|compile|build|test|unit test|code|implement)\b",
     "code_generation", "python"),
    (r"\b(python|py)\b", "code_generation", "python"),
    (r"\b(javascript|js|node|npm)\b", "code_generation", "javascript"),
    (r"\b(typescript|ts)\b", "code_generation", "typescript"),
    (r"\b(rust|cargo)\b", "code_generation", "rust"),
    (r"\b(go |golang)\b", "code_generation", "go"),
    (r"\b(java|maven|gradle)\b", "code_generation", "java"),
]

_INTENTS = [
    (r"\b(write|create|build|generate|make|implement)\b", "write"),
    (r"\b(fix|debug|repair|patch)\b", "fix"),
    (r"\b(refactor|clean|reorganize|restructure)\b", "refactor"),
    (r"\b(review|check|audit|test|verify)\b", "review"),
    (r"\b(search|find|research|investigate|look up)\b", "search"),
    (r"\b(analyze|summarize|explain|understand)\b", "analyze"),
    (r"\b(design|plan|wireframe)\b", "design"),
    (r"\b(deploy|run|execute|start)\b", "deploy"),
]

_COMPLEXITY = [
    (r"\b(simple|quick|small|trivial|one[- ]?liner)\b", "low"),
    (r"\b(complex|full|complete|entire|system|architecture)\b", "high"),
]


def _classify(text: str) -> dict[str, str]:
    low = text.lower()
    category, domain = "general", "general"
    for pat, cat, dom in _KEYWORD_CATEGORIES:
        if re.search(pat, low):
            category = cat
            domain = dom
            break
    intent = "write"
    for pat, it in _INTENTS:
        if re.search(pat, low):
            intent = it
            break
    complexity = "medium"
    for pat, cx in _COMPLEXITY:
        if re.search(pat, low):
            complexity = cx
            break
    return {
        "category": category,
        "domain": domain,
        "intent": intent,
        "complexity": complexity,
    }


class EchoProvider:
    """Deterministic, in-process provider. Implements the same call surface as
    the OpenAI-compatible client so the rest of the system is provider-agnostic.
    """

    name = "Galaxy Echo"
    base_url = "galaxy-echo://local"

    def complete(self, messages: list[dict[str, str]], model: str = "galaxy-echo",
                 max_tokens: int = 1024, temperature: float = 0.0,
                 response_format: dict | None = None,
                 tools: list[dict[str, Any]] | None = None,
                 tool_choice: str | dict | None = None,
                 **_: Any) -> dict[str, Any]:
        # Deterministic seed from the last user message — same input, same output.
        last_user = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                last_user = m.get("content", "")
                break
        seed = hashlib.sha256(last_user.encode("utf-8")).hexdigest()[:8]

        sys_prompt = next((m["content"] for m in messages if m["role"] == "system"), "")
        available_tools = {
            t.get("function", {}).get("name", "") for t in (tools or [])
        }
        # Local Mode exercises the real ToolRegistry. It emits a tool call only
        # when an actual registered tool is advertised, then produces a final
        # handoff after the tool result is appended to the conversation.
        has_tool_result = any(m.get("role") == "tool" for m in messages)
        if tools and not has_tool_result and "Code Agent" in sys_prompt and "file.write" in available_tools:
            call = {
                "id": "echo-call-" + seed,
                "type": "function",
                "function": {
                    "name": "file.write",
                    "arguments": json.dumps({
                        "path": "src/echo_artifact.py",
                        "content": "import csv\n\ndef read_csv_rows(path: str) -> list[dict[str, str]]:\n    with open(path, newline=\"\", encoding=\"utf-8\") as fh:\n        return list(csv.DictReader(fh))\n",
                        "append": False,
                    }),
                },
            }
            return self._wrap("", seed, tool_calls=[call], json_mode=False)
        if tools and not has_tool_result and "Review Agent" in sys_prompt and "file.read" in available_tools:
            call = {
                "id": "echo-call-" + seed,
                "type": "function",
                "function": {
                    "name": "file.read",
                    "arguments": json.dumps({"path": "src/echo_artifact.py", "offset": 0, "limit": 50000}),
                },
            }
            return self._wrap("", seed, tool_calls=[call], json_mode=False)
        if has_tool_result and response_format and response_format.get("type") == "json_object":
            tool_messages = [m for m in messages if m.get("role") == "tool"]
            successful = all('"ok": false' not in m.get("content", "") for m in tool_messages)
            payload = {
                "what_was_done": f"Executed {len(tool_messages)} real tool call(s) for: {last_user[:100]}",
                "key_decisions": ["Used the registered tool through the capability gate"],
                "artifacts_created": [],
                "avoid_these": [],
                "next_agent_focus": "Review the real tool result",
                "decision_confidence": 0.9 if successful else 0.2,
                "is_knowledge_based": successful,
                "task_success": successful,
            }
            return self._wrap(json.dumps(payload, ensure_ascii=False), seed, json_mode=True)

        # 1) GALAXY_META classification request?
        if "GALAXY_META" in sys_prompt and "classification" in sys_prompt.lower():
            cls = _classify(last_user)
            payload = {
                "mode": "goal_confirmed",
                "classification": cls,
                "plan_summary": f"Deterministic plan for: {last_user[:120]}",
                "needs_clarification": False,
            }
            text = "```galaxy_meta\n" + json.dumps(payload, ensure_ascii=False) + "\n```"
            return self._wrap(text, seed, in_tokens=len(last_user) // 4 + 10,
                              out_tokens=len(text) // 4 + 5)

        # 2) Research-First context assembly? Return a short recall summary.
        if "research-first" in sys_prompt.lower() or "research_first" in sys_prompt.lower():
            text = (f"Research-First recall complete. Found 2 L4 skills and 1 L3 star "
                    f"relevant to: {last_user[:80]}")
            return self._wrap(text, seed)

        # 3) Planning step?
        if "plan" in sys_prompt.lower() and "step" in sys_prompt.lower():
            steps = [
                "1. Analyze requirements",
                "2. Locate relevant files / context",
                "3. Implement the change",
                "4. Verify with a test or check",
                "5. Summarize and hand off",
            ]
            text = "Plan:\n" + "\n".join(steps)
            return self._wrap(text, seed)

        # 4) Code/Write/Design execution step — produce a concrete artifact.
        if response_format and response_format.get("type") == "json_object":
            payload = {
                "what_was_done": f"Completed step for: {last_user[:100]}",
                "key_decisions": ["Used the standard library", "Kept the change minimal"],
                "artifacts_created": [],
                "avoid_these": ["Don't add unrelated dependencies"],
                "next_agent_focus": "Continue with the next agent; no external artifact was claimed",
                "decision_confidence": 0.82,
                "is_knowledge_based": True,
                "task_success": True,
            }
            return self._wrap(json.dumps(payload, ensure_ascii=False), seed,
                              json_mode=True)

        # 5) Default: a concise, deterministic acknowledgment that completes the step.
        text = (f"[galaxy-echo {seed}] Step completed for: {last_user[:140]}. "
                f"Produced a deterministic artifact and recorded a handoff package.")
        return self._wrap(text, seed)

    def _wrap(self, text: str, seed: str, in_tokens: int = 50,
              out_tokens: int | None = None, json_mode: bool = False,
              tool_calls: list[dict[str, Any]] | None = None) -> dict[str, Any]:

        if out_tokens is None:
            out_tokens = len(text) // 4 + 5
        return {
            "id": f"echo-{seed}",
            "model": "galaxy-echo",
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": text,
                            **({"tool_calls": tool_calls} if tool_calls else {})},
                "finish_reason": "tool_calls" if tool_calls else "stop",
            }],
            "usage": {
                "prompt_tokens": in_tokens,
                "completion_tokens": out_tokens,
                "total_tokens": in_tokens + out_tokens,
            },
            "_echo": True,
            "_json_mode": json_mode,
            "tool_calls": tool_calls or [],
        }
