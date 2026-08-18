---
name: UX Guideline: Caching
source: UIUXProMax
version: 1.0.0
description: Repeat visits should be fast
tags: ["ux", "Web"]
triggers: ["Caching", "Performance"]
license: MIT
target_agent: design
category: ux_guideline
---

**No:** 49
**Category:** Performance
**Issue:** Caching
**Platform:** Web
**Description:** Repeat visits should be fast
**Do:** Set appropriate cache headers
**Don't:** No caching strategy
**Code Example Good:** Cache-Control headers
**Code Example Bad:** Every request hits server
**Severity:** Medium
