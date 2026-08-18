---
name: Chart Pattern: Time-Series Forecast
source: UIUXProMax
version: 1.0.0
description: Line with Confidence Band
tags: ["chart", "data-viz"]
triggers: ["Time-Series Forecast"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 9
**Data Type:** Time-Series Forecast
**Keywords:** forecast, prediction, confidence, band, projection, estimate
**Best Chart Type:** Line with Confidence Band
**Secondary Options:** Ribbon Chart
**When to Use:** Historical data + model predictions; communicating uncertainty range to non-technical stakeholders
**When NOT to Use:** No historical baseline; prediction confidence is too low to be useful; audience is not data-literate
**Data Volume Threshold:** Keep historical window to 30–90 days for readability; forecast horizon ≤ 30% of visible x-axis range
**Color Guidance:** Actual: solid line #0080FF. Forecast: dashed #FF9500. Confidence band: 15% opacity fill same hue
**Accessibility Grade:** AA
**Accessibility Notes:** Toggle between actual-only and forecast views. Legend must distinguish lines beyond color (solid vs dashed).
**A11y Fallback:** Toggle actual/forecast independently; legend labels must include line-style description
**Library Recommendation:** Chart.js, ApexCharts, Plotly
**Interactive Level:** Hover + Toggle
