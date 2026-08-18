---
name: Chart Pattern: Part-to-Whole
source: UIUXProMax
version: 1.0.0
description: Pie Chart or Donut
tags: ["chart", "data-viz"]
triggers: ["Part-to-Whole"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 3
**Data Type:** Part-to-Whole
**Keywords:** part-to-whole, pie, donut, percentage, proportion, share
**Best Chart Type:** Pie Chart or Donut
**Secondary Options:** Stacked Bar, Waffle Chart
**When to Use:** ≤5 categories; one dominant segment vs rest; emphasis on visual proportion over exact values
**When NOT to Use:** Categories > 5; slice differences < 5% (visually indistinguishable); user needs precise values; accessibility-first context
**Data Volume Threshold:** Max 6 slices; beyond that switch to stacked bar 100%
**Color Guidance:** 5–6 max colors. Contrasting palette. Largest slice at 12 o'clock. Always label slices with %
**Accessibility Grade:** C
**Accessibility Notes:** Pie charts fail WCAG for colorblind users. Slices rely on color alone. Avoid as primary chart in a11y contexts.
**A11y Fallback:** Must provide stacked bar alternative + percentage data table as mandatory fallback
**Library Recommendation:** Chart.js, Recharts, D3.js
**Interactive Level:** Hover + Drill
