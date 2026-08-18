---
name: Chart Pattern: Anomaly Detection
source: UIUXProMax
version: 1.0.0
description: Line Chart with Highlights
tags: ["chart", "data-viz"]
triggers: ["Anomaly Detection"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 10
**Data Type:** Anomaly Detection
**Keywords:** anomaly, outlier, spike, alert, detection, monitoring, deviation
**Best Chart Type:** Line Chart with Highlights
**Secondary Options:** Scatter with Alert
**When to Use:** Monitoring a time-series for outliers; alerting users to unexpected spikes or dips in operational data
**When NOT to Use:** Anomalies are predefined categories (use bar with highlight); real-time context without a pause control
**Data Volume Threshold:** Stream at ≤60fps with Canvas; batch: up to 10,000 pts; mark anomalies as a separate data layer
**Color Guidance:** Normal: #0080FF solid line. Anomaly marker: #FF0000 circle + filled. Alert band: #FFF3CD background zone
**Accessibility Grade:** AA
**Accessibility Notes:** Use shape marker (not color only) for anomaly points. Add text annotation per anomaly event.
**A11y Fallback:** Text alert annotation per anomaly; anomaly summary list panel alongside chart
**Library Recommendation:** D3.js, Plotly, ApexCharts
**Interactive Level:** Hover + Alert
