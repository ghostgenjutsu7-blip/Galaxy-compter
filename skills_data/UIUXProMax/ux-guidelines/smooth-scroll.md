---
name: UX Guideline: Smooth Scroll
source: UIUXProMax
version: 1.0.0
description: Anchor links should scroll smoothly to target section
tags: ["ux", "Web"]
triggers: ["Smooth Scroll", "Navigation"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 1
**Category:** Navigation
**Issue:** Smooth Scroll
**Platform:** Web
**Description:** Anchor links should scroll smoothly to target section
**Do:** Use scroll-behavior: smooth on html element
**Don't:** Jump directly without transition
**Code Example Good:** html { scroll-behavior: smooth; }
**Code Example Bad:** <a href='#section'> without CSS
**Severity:** High
