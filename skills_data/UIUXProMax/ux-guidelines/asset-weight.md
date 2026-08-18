---
name: UX Guideline: Asset Weight
source: UIUXProMax
version: 1.0.0
description: Heavy 3D/Image assets increase carbon footprint
tags: ["ux", "Web"]
triggers: ["Asset Weight", "Sustainability"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 97
**Category:** Sustainability
**Issue:** Asset Weight
**Platform:** Web
**Description:** Heavy 3D/Image assets increase carbon footprint
**Do:** Compress and lazy load 3D models
**Don't:** Load 50MB textures
**Code Example Good:** Draco compression
**Code Example Bad:** Raw .obj files
**Severity:** Medium
