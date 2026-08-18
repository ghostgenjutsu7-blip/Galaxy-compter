---
name: Chart Pattern: Heatmap / Intensity
source: UIUXProMax
version: 1.0.0
description: Heat Map or Choropleth
tags: ["chart", "data-viz"]
triggers: ["Heatmap / Intensity"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 5
**Data Type:** Heatmap / Intensity
**Keywords:** heatmap, heat-map, intensity, density, matrix, calendar
**Best Chart Type:** Heat Map or Choropleth
**Secondary Options:** Grid Heat Map, Bubble Heat
**When to Use:** Showing intensity/density across a 2D grid; time-based patterns (e.g., activity by hour × day)
**When NOT to Use:** Fewer than 20 cells (use bar); user needs to read exact values; colorblind users without pattern fallback
**Data Volume Threshold:** Up to 10,000 cells efficiently; beyond that aggregate; calendar heatmap: 365 cells max per SVG
**Color Guidance:** Gradient: Cool (blue) to Hot (red). Divergent scale for ±data. Always include numeric color legend
**Accessibility Grade:** B
**Accessibility Notes:** Pattern overlay for colorblind users. Numerical value on hover. Legend must include scale ticks.
**A11y Fallback:** Numerical overlay on hover; downloadable grid table with row/column labels
**Library Recommendation:** D3.js, Plotly, ApexCharts
**Interactive Level:** Hover + Zoom
