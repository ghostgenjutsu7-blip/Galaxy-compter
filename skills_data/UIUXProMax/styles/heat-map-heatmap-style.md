---
name: UI Style: Heat Map & Heatmap Style
source: UIUXProMax
version: 1.0.0
description: Geographical analysis, performance matrices, correlation analysis, user behavior heatmaps, temperature/intensity data
tags: ["style", "ui"]
triggers: ["Heat Map & Heatmap Style"]
license: MIT
target_agent: design
category: ui_style
---

**No:** 29
**Style Category:** Heat Map & Heatmap Style
**Type:** BI/Analytics
**Keywords:** Color-coded grid/matrix, data intensity visualization, geographical heat maps, correlation matrices, cell-based representation, gradient coloring
**Primary Colors:** Gradient scale: Cool (blue #0080FF) to hot (red #FF0000), neutral middle (white/yellow)
**Secondary Colors:** Support gradients: Light (cool blue) to dark (warm red), divergent for positive/negative data, monochromatic options
**Effects & Animation:** Color gradient transitions on data change, cell highlighting on hover, tooltip reveal on click, smooth color animation
**Best For:** Geographical analysis, performance matrices, correlation analysis, user behavior heatmaps, temperature/intensity data
**Do Not Use For:** Linear data representation, categorical comparisons (use bar charts), small datasets
**Light Mode ✓:** ✓ Full
**Dark Mode ✓:** ✓ Full (with adjustments)
**Performance:** ⚡ Excellent
**Accessibility:** ⚠ Colorblind considerations
**Mobile-Friendly:** ◐ Medium
**Conversion-Focused:** ✗ Not applicable
**Framework Compatibility:** Recharts 9/10, Chart.js 9/10, D3.js 10/10
**Era/Origin:** 2020s Modern
**Complexity:** Medium
**AI Prompt Keywords:** Design a heatmap visualization. Use: color gradient scale (cool to hot), cell-based grid, intensity legend, hover tooltips, geographic or matrix layout, divergent color scheme for +/- values, accessible color alternatives.
**CSS/Technical Keywords:** display: grid, background: linear-gradient for legend, cell hover states, tooltip positioning, color scale (blue→white→red), SVG for geographic, canvas for large datasets
**Implementation Checklist:** ☐ Color scale clear, ☐ Legend visible, ☐ Tooltips informative, ☐ Colorblind alternatives, ☐ Zoom/pan for geo, ☐ Performance for large data
**Design System Variables:** --heatmap-cool: #0080FF, --heatmap-neutral: #FFFFFF, --heatmap-hot: #FF0000, --cell-size: 24px, --legend-width: 200px, --tooltip-bg: rgba(0,0,0,0.9)
