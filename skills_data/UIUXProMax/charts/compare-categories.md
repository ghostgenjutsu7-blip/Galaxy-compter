---
name: Chart Pattern: Compare Categories
source: UIUXProMax
version: 1.0.0
description: Bar Chart (Horizontal or Vertical)
tags: ["chart", "data-viz"]
triggers: ["Compare Categories"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 2
**Data Type:** Compare Categories
**Keywords:** compare, categories, bar, comparison, ranking
**Best Chart Type:** Bar Chart (Horizontal or Vertical)
**Secondary Options:** Column Chart, Grouped Bar
**When to Use:** Comparing discrete categories by magnitude; ranking or ordering is the core insight; categories ≤ 15
**When NOT to Use:** Categories > 15 (use table or search); data has time dimension (use line); showing proportions (use waffle/stacked)
**Data Volume Threshold:** <20 categories: vertical bar; 20–50: horizontal bar; >50: paginated table
**Color Guidance:** Each bar: distinct color. Grouped: same hue family. Always sort descending by value
**Accessibility Grade:** AAA
**Accessibility Notes:** Value labels on each bar by default. Sort control for user reordering.
**A11y Fallback:** Value labels always visible; provide CSV export
**Library Recommendation:** Chart.js, Recharts, D3.js
**Interactive Level:** Hover + Sort
