---
name: UX Guideline: Motion Sensitivity
source: UIUXProMax
version: 1.0.0
description: Parallax/Scroll-jacking causes nausea
tags: ["ux", "All"]
triggers: ["Motion Sensitivity", "Accessibility"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 99
**Category:** Accessibility
**Issue:** Motion Sensitivity
**Platform:** All
**Description:** Parallax/Scroll-jacking causes nausea
**Do:** Respect prefers-reduced-motion
**Don't:** Force scroll effects
**Code Example Good:** @media (prefers-reduced-motion)
**Code Example Bad:** ScrollTrigger.create()
**Severity:** High
