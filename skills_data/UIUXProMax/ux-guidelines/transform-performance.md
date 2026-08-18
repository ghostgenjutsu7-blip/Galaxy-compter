---
name: UX Guideline: Transform Performance
source: UIUXProMax
version: 1.0.0
description: Some CSS properties trigger expensive repaints
tags: ["ux", "Web"]
triggers: ["Transform Performance", "Animation"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 13
**Category:** Animation
**Issue:** Transform Performance
**Platform:** Web
**Description:** Some CSS properties trigger expensive repaints
**Do:** Use transform and opacity for animations
**Don't:** Animate width/height/top/left properties
**Code Example Good:** transform: translateY()
**Code Example Bad:** top: 10px animation
**Severity:** Medium
