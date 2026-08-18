---
name: UX Guideline: ARIA Labels
source: UIUXProMax
version: 1.0.0
description: Interactive elements need accessible names
tags: ["ux", "All"]
triggers: ["ARIA Labels", "Accessibility"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 40
**Category:** Accessibility
**Issue:** ARIA Labels
**Platform:** All
**Description:** Interactive elements need accessible names
**Do:** Add aria-label for icon-only buttons
**Don't:** Icon buttons without labels
**Code Example Good:** aria-label='Close menu'
**Code Example Bad:** <button><Icon/></button>
**Severity:** High
