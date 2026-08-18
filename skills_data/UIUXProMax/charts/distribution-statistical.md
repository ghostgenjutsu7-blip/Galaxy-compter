---
name: Chart Pattern: Distribution / Statistical
source: UIUXProMax
version: 1.0.0
description: Box Plot
tags: ["chart", "data-viz"]
triggers: ["Distribution / Statistical"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 17
**Data Type:** Distribution / Statistical
**Keywords:** distribution, statistical, spread, median, outlier, quartile, boxplot
**Best Chart Type:** Box Plot
**Secondary Options:** Violin Plot, Beeswarm
**When to Use:** Showing spread, median, and outliers of a dataset; comparing distributions across multiple groups
**When NOT to Use:** Fewer than 20 data points per group (distribution is not meaningful); audience unfamiliar with statistical charts
**Data Volume Threshold:** Any sample size; aggregated representation so rendering is ⚡ Excellent at any volume
**Color Guidance:** Box fill: #BBDEFB. Border: #1976D2. Median line: #D32F2F bold. Outlier dots: #F44336
**Accessibility Grade:** AA
**Accessibility Notes:** Include stats summary table. Annotate outlier count in chart subtitle.
**A11y Fallback:** Stats summary table (min / Q1 / median / Q3 / max / mean); outlier count annotation
**Library Recommendation:** Plotly, D3.js, Chart.js (plugin)
**Interactive Level:** Hover
