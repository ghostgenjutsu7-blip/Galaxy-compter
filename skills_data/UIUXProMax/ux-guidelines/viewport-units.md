---
name: UX Guideline: Viewport Units
source: UIUXProMax
version: 1.0.0
description: 100vh can be problematic on mobile browsers
tags: ["ux", "Web"]
triggers: ["Viewport Units", "Layout"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 20
**Category:** Layout
**Issue:** Viewport Units
**Platform:** Web
**Description:** 100vh can be problematic on mobile browsers
**Do:** Use dvh or account for mobile browser chrome
**Don't:** Use 100vh for full-screen mobile layouts
**Code Example Good:** min-h-dvh or min-h-screen
**Code Example Bad:** h-screen on mobile
**Severity:** Medium
