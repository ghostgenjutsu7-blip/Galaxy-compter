---
name: UX Guideline: Sticky Navigation
source: UIUXProMax
version: 1.0.0
description: Fixed nav should not obscure content
tags: ["ux", "Web"]
triggers: ["Sticky Navigation", "Navigation"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 2
**Category:** Navigation
**Issue:** Sticky Navigation
**Platform:** Web
**Description:** Fixed nav should not obscure content
**Do:** Add padding-top to body equal to nav height
**Don't:** Let nav overlap first section content
**Code Example Good:** pt-20 (if nav is h-20)
**Code Example Bad:** No padding compensation
**Severity:** Medium
