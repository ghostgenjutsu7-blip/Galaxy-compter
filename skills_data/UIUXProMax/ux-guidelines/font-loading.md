---
name: UX Guideline: Font Loading
source: UIUXProMax
version: 1.0.0
description: Fonts should load without layout shift
tags: ["ux", "Web"]
triggers: ["Font Loading", "Typography"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 75
**Category:** Typography
**Issue:** Font Loading
**Platform:** Web
**Description:** Fonts should load without layout shift
**Do:** Reserve space with fallback font
**Don't:** Layout shift when fonts load
**Code Example Good:** font-display: swap + similar fallback
**Code Example Bad:** No fallback font
**Severity:** Medium
