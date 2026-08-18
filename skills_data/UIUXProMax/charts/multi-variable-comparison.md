---
name: Chart Pattern: Multi-Variable Comparison
source: UIUXProMax
version: 1.0.0
description: Radar / Spider Chart
tags: ["chart", "data-viz"]
triggers: ["Multi-Variable Comparison"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 14
**Data Type:** Multi-Variable Comparison
**Keywords:** radar, spider, multi-variable, attributes, dimensions, comparison
**Best Chart Type:** Radar / Spider Chart
**Secondary Options:** Parallel Coordinates, Grouped Bar
**When to Use:** Comparing multiple entities across the same fixed set of attributes (e.g., product feature comparison)
**When NOT to Use:** Axes > 8 (unreadable); values need precise comparison (use grouped bar); audience unfamiliar with radar charts
**Data Volume Threshold:** 2–3 datasets maximum per chart; 5–8 axes; beyond 8 axes switch to parallel coordinates
**Color Guidance:** Single dataset: #0080FF at 20% fill. Multiple: distinct hues with 30% fill. Border: full opacity
**Accessibility Grade:** B
**Accessibility Notes:** Limit axes to 5–8. Always provide grouped bar chart alternative for precise reading.
**A11y Fallback:** Grouped bar chart as mandatory alternative; include raw data table
**Library Recommendation:** Chart.js, Recharts, ApexCharts
**Interactive Level:** Hover + Toggle
