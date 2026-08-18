---
name: UX Guideline: Screen Reader
source: UIUXProMax
version: 1.0.0
description: Content should make sense when read aloud
tags: ["ux", "All"]
triggers: ["Screen Reader", "Accessibility"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 42
**Category:** Accessibility
**Issue:** Screen Reader
**Platform:** All
**Description:** Content should make sense when read aloud
**Do:** Use semantic HTML and ARIA properly
**Don't:** Div soup with no semantics
**Code Example Good:** <nav> <main> <article>
**Code Example Bad:** <div> for everything
**Severity:** Medium
