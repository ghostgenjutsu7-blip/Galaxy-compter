---
name: Chart Pattern: Hierarchical Proportional
source: UIUXProMax
version: 1.0.0
description: Sunburst Chart
tags: ["chart", "data-viz"]
triggers: ["Hierarchical Proportional"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 20
**Data Type:** Hierarchical Proportional
**Keywords:** sunburst, hierarchy, nested, proportion, radial, circle
**Best Chart Type:** Sunburst Chart
**Secondary Options:** Treemap, Icicle, Circle Packing
**When to Use:** Exploring nested proportions where both hierarchy and relative size matter (e.g., org spend breakdown)
**When NOT to Use:** More than 3 hierarchy levels (outer rings become unreadable); precision matters over overview; mobile
**Data Volume Threshold:** <100 nodes: SVG; 100–500: Canvas; >500: filter to top N before rendering
**Color Guidance:** Center to outer: darker to lighter hue. Each level 15–20% lighter. Contrasting border between sectors
**Accessibility Grade:** C
**Accessibility Notes:** Poor accessibility beyond 2 levels. Mandatory table alternative required for any production use.
**A11y Fallback:** Collapsible indented list with percentages; breadcrumb trail for current drill-down state
**Library Recommendation:** D3.js (d3-hierarchy), Recharts, ApexCharts
**Interactive Level:** Drilldown + Hover
