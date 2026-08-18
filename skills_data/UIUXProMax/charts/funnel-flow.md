---
name: Chart Pattern: Funnel / Flow
source: UIUXProMax
version: 1.0.0
description: Funnel Chart or Sankey
tags: ["chart", "data-viz"]
triggers: ["Funnel / Flow"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 7
**Data Type:** Funnel / Flow
**Keywords:** funnel, flow, conversion, drop-off, pipeline, stages
**Best Chart Type:** Funnel Chart or Sankey
**Secondary Options:** Waterfall (for flows)
**When to Use:** Sequential multi-stage process; showing conversion or drop-off rates between defined stages
**When NOT to Use:** Stages aren't sequential; values don't decrease monotonically (use bar); fewer than 3 stages
**Data Volume Threshold:** 3–8 stages optimal; beyond 8 stages group minor steps into 'Other'
**Color Guidance:** Stages: single color gradient (start → end). Show conversion % between each stage. Highlight biggest drop
**Accessibility Grade:** AA
**Accessibility Notes:** Explicit conversion % as text per stage. Stage labels always visible. Linear list view as fallback.
**A11y Fallback:** Provide linear list view with stage name + count + drop-off %; keyboard traversal
**Library Recommendation:** D3.js, Recharts, Custom SVG
**Interactive Level:** Hover + Drill
