---
name: Chart Pattern: Process Mining
source: UIUXProMax
version: 1.0.0
description: Process Map / Graph
tags: ["chart", "data-viz"]
triggers: ["Process Mining"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 25
**Data Type:** Process Mining
**Keywords:** process, mining, variants, path, bottleneck, log, event
**Best Chart Type:** Process Map / Graph
**Secondary Options:** Directed Acyclic Graph (DAG), Petri Net
**When to Use:** Analyzing event logs to visualize actual process flows; identifying bottlenecks and deviations in ops/product funnels
**When NOT to Use:** No event log data available; audience expects a static flowchart (use diagram tool); node count > 100 without pre-filtering
**Data Volume Threshold:** <30 nodes: SVG; 30–100: Canvas; >100: apply variant filtering (top 80% of cases) before rendering
**Color Guidance:** Happy path: #10B981 thick line. Deviations: #F59E0B thin line. Bottleneck nodes: #EF4444 fill
**Accessibility Grade:** B
**Accessibility Notes:** Complex graphs are hard to navigate. Provide path summary text. Highlight top 3 bottlenecks as annotations.
**A11y Fallback:** Path summary table (variant → frequency → avg duration); top 3 bottlenecks as text annotation panel
**Library Recommendation:** React-Flow, Cytoscape.js, Recharts
**Interactive Level:** Drag + Node-Click
