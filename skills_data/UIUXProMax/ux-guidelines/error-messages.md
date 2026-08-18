---
name: UX Guideline: Error Messages
source: UIUXProMax
version: 1.0.0
description: Error messages must be announced
tags: ["ux", "All"]
triggers: ["Error Messages", "Accessibility"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 44
**Category:** Accessibility
**Issue:** Error Messages
**Platform:** All
**Description:** Error messages must be announced
**Do:** Use aria-live or role=alert for errors
**Don't:** Visual-only error indication
**Code Example Good:** role='alert'
**Code Example Bad:** Red border only
**Severity:** High
