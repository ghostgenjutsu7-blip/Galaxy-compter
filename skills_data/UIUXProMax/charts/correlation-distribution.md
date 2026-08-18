---
name: Chart Pattern: Correlation / Distribution
source: UIUXProMax
version: 1.0.0
description: Scatter Plot or Bubble Chart
tags: ["chart", "data-viz"]
triggers: ["Correlation / Distribution"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 4
**Data Type:** Correlation / Distribution
**Keywords:** correlation, distribution, scatter, relationship, pattern, cluster
**Best Chart Type:** Scatter Plot or Bubble Chart
**Secondary Options:** Heat Map, Matrix
**When to Use:** Exploring relationship between two continuous variables; identifying clusters or outliers in a dataset
**When NOT to Use:** Variables are categorical (use grouped bar); fewer than 20 points (patterns aren't meaningful); mobile-primary context
**Data Volume Threshold:** <500 pts: SVG; 500–5000: Canvas at 0.6–0.8 opacity; >5000: hexbin or aggregate first
**Color Guidance:** Color axis: gradient (blue → red). Bubble size: relative to 3rd variable. Opacity: 0.6–0.8 to show density
**Accessibility Grade:** B
**Accessibility Notes:** Provide data table alternative. Combine color + shape distinction for colorblind users.
**A11y Fallback:** Data table with correlation coefficient annotation; shape markers (circle/square/triangle) per group
**Library Recommendation:** D3.js, Plotly, Recharts
**Interactive Level:** Hover + Brush
