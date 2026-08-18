---
name: Chart Pattern: Performance vs Target (Compact)
source: UIUXProMax
version: 1.0.0
description: Bullet Chart
tags: ["chart", "data-viz"]
triggers: ["Performance vs Target (Compact)"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 18
**Data Type:** Performance vs Target (Compact)
**Keywords:** bullet, compact, kpi, dashboard, target, benchmark, range
**Best Chart Type:** Bullet Chart
**Secondary Options:** Gauge, Progress Bar
**When to Use:** Dashboard with multiple KPIs side by side; space-constrained contexts where a gauge is too large
**When NOT to Use:** Single KPI with emphasis (use gauge); data has no defined target range; fewer than 3 KPIs
**Data Volume Threshold:** Ideal for 3–10 bullet charts in a grid; scales to any count efficiently
**Color Guidance:** Qualitative ranges: #FFCDD2 / #FFF9C4 / #C8E6C9 (bad/ok/good). Performance bar: #1976D2. Target: black 3px marker
**Accessibility Grade:** AAA
**Accessibility Notes:** All values always visible as text. Color ranges are labeled with text thresholds not color alone.
**A11y Fallback:** Numerical values always visible (not hover-only); color ranges labeled with threshold text
**Library Recommendation:** D3.js, Plotly, Custom SVG
**Interactive Level:** Hover
