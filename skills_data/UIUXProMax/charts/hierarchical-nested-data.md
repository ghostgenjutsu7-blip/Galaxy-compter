---
name: Chart Pattern: Hierarchical / Nested Data
source: UIUXProMax
version: 1.0.0
description: Treemap
tags: ["chart", "data-viz"]
triggers: ["Hierarchical / Nested Data"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 11
**Data Type:** Hierarchical / Nested Data
**Keywords:** hierarchy, nested, treemap, parent, children, breakdown, drill
**Best Chart Type:** Treemap
**Secondary Options:** Sunburst, Nested Donut, Icicle
**When to Use:** Showing size relationships within a hierarchy; overview of proportional structure (e.g., budget breakdown)
**When NOT to Use:** Hierarchy depth > 3 levels (too complex to read); user needs to compare sibling values precisely
**Data Volume Threshold:** <200 nodes: SVG; 200–1000: Canvas; >1000: paginate or pre-filter before rendering
**Color Guidance:** Parent nodes: distinct hues. Children: lighter shades of same hue. White separator borders: 2–3px
**Accessibility Grade:** C
**Accessibility Notes:** Poor baseline accessibility. Always provide table alternative as primary view. Label all large areas.
**A11y Fallback:** Collapsible tree table as primary view; treemap as supplementary visual only
**Library Recommendation:** D3.js, Recharts, ApexCharts
**Interactive Level:** Hover + Drilldown
