---
name: Chart Pattern: Flow / Process Data
source: UIUXProMax
version: 1.0.0
description: Sankey Diagram
tags: ["chart", "data-viz"]
triggers: ["Flow / Process Data"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 12
**Data Type:** Flow / Process Data
**Keywords:** flow, process, sankey, distribution, source, target, transfer
**Best Chart Type:** Sankey Diagram
**Secondary Options:** Alluvial, Chord Diagram
**When to Use:** Showing how quantities flow between nodes; multi-source multi-target distribution
**When NOT to Use:** Flow directions form loops (use network graph); fewer than 3 source-target pairs; mobile-primary context
**Data Volume Threshold:** <50 flows: SVG; ≥50: Canvas; >200 flows: aggregate minor flows into 'Other' node
**Color Guidance:** Gradient from source to target color. Flow opacity: 0.4–0.6. Node labels always visible
**Accessibility Grade:** C
**Accessibility Notes:** Structural flow charts cannot be conveyed by color alone. Provide flow table. Avoid on mobile.
**A11y Fallback:** Flow table (Source → Target → Value); keyboard-traversable node list with tab stops
**Library Recommendation:** D3.js (d3-sankey), Plotly
**Interactive Level:** Hover + Drilldown
