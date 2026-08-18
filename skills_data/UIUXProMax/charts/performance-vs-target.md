---
name: Chart Pattern: Performance vs Target
source: UIUXProMax
version: 1.0.0
description: Gauge Chart or Bullet Chart
tags: ["chart", "data-viz"]
triggers: ["Performance vs Target"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 8
**Data Type:** Performance vs Target
**Keywords:** performance, target, kpi, gauge, goal, threshold, progress
**Best Chart Type:** Gauge Chart or Bullet Chart
**Secondary Options:** Dial, Thermometer
**When to Use:** Single KPI measured against a defined target or threshold; dashboard summary context
**When NOT to Use:** No target or benchmark exists; comparing multiple KPIs at once (use bullet chart grid)
**Data Volume Threshold:** Single metric per gauge; for 3+ KPIs use bullet chart grid layout
**Color Guidance:** Performance: Red → Yellow → Green gradient. Target: marker line. Threshold zones clearly differentiated
**Accessibility Grade:** AA
**Accessibility Notes:** Always show numerical value + % of target as text beside chart. Never rely on color position alone.
**A11y Fallback:** Numerical value + % of target shown as visible text; ARIA live region for real-time updates
**Library Recommendation:** D3.js, ApexCharts, Custom SVG
**Interactive Level:** Hover
