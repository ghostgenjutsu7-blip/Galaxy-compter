---
name: Chart Pattern: Root Cause Analysis
source: UIUXProMax
version: 1.0.0
description: Decomposition Tree
tags: ["chart", "data-viz"]
triggers: ["Root Cause Analysis"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 21
**Data Type:** Root Cause Analysis
**Keywords:** root cause, decomposition, tree, hierarchy, drill-down, ai-split, attribution
**Best Chart Type:** Decomposition Tree
**Secondary Options:** Decision Tree, Flow Chart
**When to Use:** Decomposing a metric into contributing factors; AI-assisted analysis or BI drill-down scenarios
**When NOT to Use:** No clear parent-child causal relationship; audience expects a summary rather than exploration
**Data Volume Threshold:** Up to 5 levels deep; limit visible nodes to 20 per level for readability; lazy-load deeper levels
**Color Guidance:** Positive impact nodes: #2563EB. Negative impact nodes: #EF4444. Neutral connectors: #94A3B8
**Accessibility Grade:** AA
**Accessibility Notes:** Keyboard-navigable expand/collapse. Screen reader announces node value and % contribution.
**A11y Fallback:** Keyboard expand/collapse tree; screen reader announces node label + value + % impact
**Library Recommendation:** Power BI (native), React-Flow, Custom D3.js
**Interactive Level:** Drill + Expand
