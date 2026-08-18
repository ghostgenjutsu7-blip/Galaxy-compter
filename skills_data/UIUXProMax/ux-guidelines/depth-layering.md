---
name: UX Guideline: Depth Layering
source: UIUXProMax
version: 1.0.0
description: UI needs Z-depth to separate content from environment
tags: ["ux", "VisionOS"]
triggers: ["Depth Layering", "Spatial UI"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 95
**Category:** Spatial UI
**Issue:** Depth Layering
**Platform:** VisionOS
**Description:** UI needs Z-depth to separate content from environment
**Do:** Use glass material and z-offset
**Don't:** Flat opaque panels blocking view
**Code Example Good:** .glassBackgroundEffect()
**Code Example Bad:** bg-white
**Severity:** Medium
