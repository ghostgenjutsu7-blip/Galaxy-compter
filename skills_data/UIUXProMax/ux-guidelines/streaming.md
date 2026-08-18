---
name: UX Guideline: Streaming
source: UIUXProMax
version: 1.0.0
description: Waiting for full text is slow
tags: ["ux", "All"]
triggers: ["Streaming", "AI Interaction"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 93
**Category:** AI Interaction
**Issue:** Streaming
**Platform:** All
**Description:** Waiting for full text is slow
**Do:** Stream text response token by token
**Don't:** Show loading spinner for 10s+
**Code Example Good:** Typewriter effect
**Code Example Bad:** Spinner until 100% complete
**Severity:** Medium
