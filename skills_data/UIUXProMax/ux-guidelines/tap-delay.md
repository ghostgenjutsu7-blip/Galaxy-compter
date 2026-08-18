---
name: UX Guideline: Tap Delay
source: UIUXProMax
version: 1.0.0
description: 300ms tap delay feels laggy
tags: ["ux", "Mobile"]
triggers: ["Tap Delay", "Touch"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 25
**Category:** Touch
**Issue:** Tap Delay
**Platform:** Mobile
**Description:** 300ms tap delay feels laggy
**Do:** Use touch-action CSS or fastclick
**Don't:** Default mobile tap handling
**Code Example Good:** touch-action: manipulation
**Code Example Bad:** No touch optimization
**Severity:** Medium
