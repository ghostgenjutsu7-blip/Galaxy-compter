---
name: Chart Pattern: Cumulative Changes
source: UIUXProMax
version: 1.0.0
description: Waterfall Chart
tags: ["chart", "data-viz"]
triggers: ["Cumulative Changes"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 13
**Data Type:** Cumulative Changes
**Keywords:** waterfall, cumulative, variance, incremental, bridge, delta
**Best Chart Type:** Waterfall Chart
**Secondary Options:** Stacked Bar, Cascade
**When to Use:** Showing how individual positive/negative components add up to a final total (e.g., P&L, budget variance)
**When NOT to Use:** Changes are not additive; more than 12 bars (readability breaks); audience expects a simple total
**Data Volume Threshold:** 4–12 bars optimal; beyond 12 aggregate minor items into a single 'Other' bar
**Color Guidance:** Increases: #4CAF50. Decreases: #F44336. Start total: #2196F3. End total: #0D47A1. Running total line: dashed
**Accessibility Grade:** AA
**Accessibility Notes:** Color + directional arrow icon per bar (not color alone). Labels on every bar.
**A11y Fallback:** Table with running total column; directional arrow icons per row
**Library Recommendation:** ApexCharts, Highcharts, Plotly
**Interactive Level:** Hover
