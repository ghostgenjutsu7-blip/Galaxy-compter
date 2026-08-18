---
name: UX Guideline: Stacking Context
source: UIUXProMax
version: 1.0.0
description: New stacking contexts reset z-index
tags: ["ux", "Web"]
triggers: ["Stacking Context", "Layout"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 18
**Category:** Layout
**Issue:** Stacking Context
**Platform:** Web
**Description:** New stacking contexts reset z-index
**Do:** Understand what creates new stacking context
**Don't:** Expect z-index to work across contexts
**Code Example Good:** Parent with z-index isolates children
**Code Example Bad:** z-index: 9999 not working
**Severity:** Medium
