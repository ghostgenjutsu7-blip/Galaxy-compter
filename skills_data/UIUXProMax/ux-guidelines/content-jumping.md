---
name: UX Guideline: Content Jumping
source: UIUXProMax
version: 1.0.0
description: Layout shift when content loads is jarring
tags: ["ux", "Web"]
triggers: ["Content Jumping", "Layout"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 19
**Category:** Layout
**Issue:** Content Jumping
**Platform:** Web
**Description:** Layout shift when content loads is jarring
**Do:** Reserve space for async content
**Don't:** Let images/content push layout around
**Code Example Good:** aspect-ratio or fixed height
**Code Example Bad:** No dimensions on images
**Severity:** High
