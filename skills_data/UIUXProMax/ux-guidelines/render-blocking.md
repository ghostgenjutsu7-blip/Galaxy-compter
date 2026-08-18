---
name: UX Guideline: Render Blocking
source: UIUXProMax
version: 1.0.0
description: CSS/JS can block first paint
tags: ["ux", "Web"]
triggers: ["Render Blocking", "Performance"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 53
**Category:** Performance
**Issue:** Render Blocking
**Platform:** Web
**Description:** CSS/JS can block first paint
**Do:** Inline critical CSS defer non-critical
**Don't:** Large blocking CSS files
**Code Example Good:** Critical CSS inline
**Code Example Bad:** All CSS in head
**Severity:** Medium
