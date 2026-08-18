---
name: Chart Pattern: Trend Over Time
source: UIUXProMax
version: 1.0.0
description: Line Chart
tags: ["chart", "data-viz"]
triggers: ["Trend Over Time"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 1
**Data Type:** Trend Over Time
**Keywords:** trend, time-series, line, growth, timeline, progress
**Best Chart Type:** Line Chart
**Secondary Options:** Area Chart, Smooth Area
**When to Use:** Data has a time axis; user needs to observe rise/fall trends or rate of change over a continuous period
**When NOT to Use:** Fewer than 4 data points (use stat card); more than 6 series (visual noise); no time dimension exists
**Data Volume Threshold:** <1000 pts: SVG; ≥1000 pts: Canvas + downsampling; >10000: aggregate to intervals
**Color Guidance:** Primary: #0080FF. Multiple series: distinct colors + distinct line styles. Fill: 20% opacity
**Accessibility Grade:** AA
**Accessibility Notes:** Differentiate series by line style (solid/dashed/dotted) not color alone. Add pattern overlays for colorblind users.
**A11y Fallback:** Dashed/dotted lines per series; togglable data table with timestamps and values
**Library Recommendation:** Chart.js, Recharts, ApexCharts
**Interactive Level:** Hover + Zoom
