---
name: UX Guideline: Image Scaling
source: UIUXProMax
version: 1.0.0
description: Images should scale with container
tags: ["ux", "Web"]
triggers: ["Image Scaling", "Responsive"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 70
**Category:** Responsive
**Issue:** Image Scaling
**Platform:** Web
**Description:** Images should scale with container
**Do:** Use max-width: 100% on images
**Don't:** Fixed width images overflow
**Code Example Good:** max-w-full h-auto
**Code Example Bad:** width='800' fixed
**Severity:** Medium
