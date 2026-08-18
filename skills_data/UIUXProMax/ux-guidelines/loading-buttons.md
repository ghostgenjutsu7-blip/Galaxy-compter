---
name: UX Guideline: Loading Buttons
source: UIUXProMax
version: 1.0.0
description: Prevent double submission during async actions
tags: ["ux", "All"]
triggers: ["Loading Buttons", "Interaction"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 32
**Category:** Interaction
**Issue:** Loading Buttons
**Platform:** All
**Description:** Prevent double submission during async actions
**Do:** Disable button and show loading state
**Don't:** Allow multiple clicks during processing
**Code Example Good:** disabled={loading} spinner
**Code Example Bad:** Button clickable while loading
**Severity:** High
