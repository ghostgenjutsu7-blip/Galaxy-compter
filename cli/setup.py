"""cli/setup.py — onboarding wizard (§9).

3-step minimum path: language detection → first API key → ready.
Optional follow-ups: provider bundle (Free Mode), Subconscious Loop, skill
preferences. Never blocks reaching step 3.
"""
from __future__ import annotations

import time
from typing import Any

from config import get_config
from schema.migrations import ensure_latest


async def run_setup(io) -> str:
    cfg = get_config()
    cfg.ensure_dirs()
    ensure_latest()

    io.print("=" * 60)
    io.print("Welcome to Galaxy Computer — the mind that remembers everything.")
    io.print("=" * 60)

    # Step 1: language
    io.print("\n[1/3] Language")
    io.print("Galaxy responds in your language. Detected: English.")
    lang = io.input("Confirm language (en/ar/fr, or blank for en)> ").strip() or "en"
    cfg.set("language", lang)

    # Step 2: first API key (optional — Galaxy Echo works without one)
    io.print("\n[2/3] API Key (optional)")
    io.print("Galaxy ships with a built-in deterministic model (Galaxy Echo) so you can")
    io.print("use it right now without any key. To use real LLMs (OpenAI, Anthropic, etc.),")
    io.print("add a provider now or later via /provider add.")
    add_key = io.input("Add a provider now? (y/N)> ").strip().lower()
    if add_key == "y":
        await _add_provider_flow(io)
    else:
        io.print("Skipping — Galaxy Echo is active. Add providers anytime via /provider add.")

    # Step 3: ready
    io.print("\n[3/3] Galaxy is ready!")
    name = io.input("Your name (optional)> ").strip()
    profession = io.input("Your profession (optional)> ").strip()
    if name or profession:
        from core.memory.orbits import get_orbits
        o = get_orbits()
        g = o.get_galactic()
        g.name = name or g.name
        g.profession = profession or g.profession
        g.preferred_language = lang
        o.save_galactic(g)

    # Optional follow-ups
    io.print("\n── Optional (all skippable) ──")
    fm = io.input("Enable Free Mode? Wires up NVIDIA NIM + Kilo Gateway + Groq + OpenRouter. (y/N)> ").strip().lower()
    if fm == "y":
        await _free_mode(io)
    sl = io.input("Enable the Subconscious Loop? Background learning, ~50MB RAM, every 30min. (y/N)> ").strip().lower()
    cfg.set("subconscious_enabled", sl == "y")

    # load skills
    io.print("\nLoading pre-loaded skills (ECC, UI UX Pro Max, Open Design, Anthropic)...")
    from skills.loader import load_all_skills
    counts = load_all_skills()
    io.print(f"  Loaded {counts['ingested']} skills ({counts['trusted']} trusted).")

    cfg.set("setup_complete", True)
    cfg.set("setup_at", time.time())

    io.print("\n" + "=" * 60)
    io.print("Setup complete. Type a goal or question, or /help for commands.")
    io.print("Try: /goal write a python function to read a csv")
    io.print("=" * 60)
    return "Setup complete."


async def _add_provider_flow(io) -> None:
    from providers.manager import get_provider_manager, KNOWN_PROVIDERS
    from security.secrets_fallback import encrypt_secret
    pm = get_provider_manager()
    io.print("Known providers: " + ", ".join(list(KNOWN_PROVIDERS.keys())[:8]))
    name = io.input("Provider name> ").strip()
    if not name:
        return
    base_url = KNOWN_PROVIDERS.get(name, "")
    if not base_url:
        base_url = io.input("Base URL> ").strip()
    pm.add_provider(name, base_url)
    key = io.input("API key (paste)> ").strip()
    alias = io.input("Alias (e.g. 'personal')> ").strip() or "default"
    tier = io.input("Tier (paid/free) [paid]> ").strip() or "paid"
    enc = encrypt_secret(key) if key else ""
    pm.add_key(name, alias, enc, tier=tier, status="high")
    # suggest a default model assignment
    model = io.input(f"Default model name for {name} (e.g. gpt-4o, claude-sonnet-4)> ").strip()
    if model:
        pm.set_agent_model("orchestrator", name, model)
        pm.set_agent_model("code", name, model)
    io.print(f"Provider {name} added.")


async def _free_mode(io) -> None:
    """Wire up the free-tier providers (§19). Galaxy Echo remains the fallback."""
    from providers.manager import get_provider_manager, KNOWN_PROVIDERS, FREE_PROVIDERS
    from security.secrets_fallback import encrypt_secret
    pm = get_provider_manager()
    for name in ["NVIDIA NIM", "Kilo Gateway", "Groq", "OpenRouter"]:
        base = KNOWN_PROVIDERS.get(name, "")
        if base:
            pm.add_provider(name, base)
            key = io.input(f"Paste {name} key (or blank to skip)> ").strip()
            if key:
                pm.add_key(name, "free", encrypt_secret(key), tier="free", status="high")
    io.print("Free Mode configured. Galaxy rotates among free keys before falling back to Echo.")
