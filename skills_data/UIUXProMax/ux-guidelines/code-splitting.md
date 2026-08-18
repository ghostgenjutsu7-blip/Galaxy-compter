---
name: UX Guideline: Code Splitting
source: UIUXProMax
version: 1.0.0
description: Large bundles slow initial load
tags: ["ux", "Web"]
triggers: ["Code Splitting", "Performance"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 48
**Category:** Performance
**Issue:** Code Splitting
**Platform:** Web
**Description:** Large bundles slow initial load
**Do:** Split code by route/feature
**Don't:** Single large bundle
**Code Example Good:** dynamic import()
**Code Example Bad:** All code in main bundle
**Severity:** Medium
