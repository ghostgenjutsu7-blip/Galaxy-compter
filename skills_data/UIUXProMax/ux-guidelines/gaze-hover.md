---
name: UX Guideline: Gaze Hover
source: UIUXProMax
version: 1.0.0
description: Elements should respond to eye tracking before pinch
tags: ["ux", "VisionOS"]
triggers: ["Gaze Hover", "Spatial UI"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 94
**Category:** Spatial UI
**Issue:** Gaze Hover
**Platform:** VisionOS
**Description:** Elements should respond to eye tracking before pinch
**Do:** Scale/highlight element on look
**Don't:** Static element until pinch
**Code Example Good:** hoverEffect()
**Code Example Bad:** onTap only
**Severity:** High
