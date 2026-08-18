---
name: UX Guideline: Reduced Motion
source: UIUXProMax
version: 1.0.0
description: Respect user's motion preferences
tags: ["ux", "All"]
triggers: ["Reduced Motion", "Animation"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 9
**Category:** Animation
**Issue:** Reduced Motion
**Platform:** All
**Description:** Respect user's motion preferences
**Do:** Check prefers-reduced-motion media query
**Don't:** Ignore accessibility motion settings
**Code Example Good:** @media (prefers-reduced-motion: reduce)
**Code Example Bad:** No motion query check
**Severity:** High
