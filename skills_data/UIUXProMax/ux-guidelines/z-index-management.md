---
name: UX Guideline: Z-Index Management
source: UIUXProMax
version: 1.0.0
description: Stacking context conflicts cause hidden elements
tags: ["ux", "Web"]
triggers: ["Z-Index Management", "Layout"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 15
**Category:** Layout
**Issue:** Z-Index Management
**Platform:** Web
**Description:** Stacking context conflicts cause hidden elements
**Do:** Define z-index scale system (10 20 30 50)
**Don't:** Use arbitrary large z-index values
**Code Example Good:** z-10 z-20 z-50
**Code Example Bad:** z-[9999]
**Severity:** High
