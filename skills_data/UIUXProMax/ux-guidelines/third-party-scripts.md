---
name: UX Guideline: Third Party Scripts
source: UIUXProMax
version: 1.0.0
description: External scripts can block rendering
tags: ["ux", "Web"]
triggers: ["Third Party Scripts", "Performance"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 51
**Category:** Performance
**Issue:** Third Party Scripts
**Platform:** Web
**Description:** External scripts can block rendering
**Do:** Load non-critical scripts async/defer
**Don't:** Synchronous third-party scripts
**Code Example Good:** async or defer attribute
**Code Example Bad:** <script src='...'> in head
**Severity:** Medium
