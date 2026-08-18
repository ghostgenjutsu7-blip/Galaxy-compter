---
name: UX Guideline: Back Button
source: UIUXProMax
version: 1.0.0
description: Users expect back to work predictably
tags: ["ux", "Mobile"]
triggers: ["Back Button", "Navigation"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 4
**Category:** Navigation
**Issue:** Back Button
**Platform:** Mobile
**Description:** Users expect back to work predictably
**Do:** Preserve navigation history properly
**Don't:** Break browser/app back button behavior
**Code Example Good:** history.pushState()
**Code Example Bad:** location.replace()
**Severity:** High
