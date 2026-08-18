---
name: UX Guideline: Image Optimization
source: UIUXProMax
version: 1.0.0
description: Large images slow page load
tags: ["ux", "All"]
triggers: ["Image Optimization", "Performance"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 46
**Category:** Performance
**Issue:** Image Optimization
**Platform:** All
**Description:** Large images slow page load
**Do:** Use appropriate size and format (WebP)
**Don't:** Unoptimized full-size images
**Code Example Good:** srcset with multiple sizes
**Code Example Bad:** 4000px image for 400px display
**Severity:** High
