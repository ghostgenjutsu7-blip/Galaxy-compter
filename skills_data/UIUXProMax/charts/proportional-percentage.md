---
name: Chart Pattern: Proportional / Percentage
source: UIUXProMax
version: 1.0.0
description: Waffle Chart
tags: ["chart", "data-viz"]
triggers: ["Proportional / Percentage"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 19
**Data Type:** Proportional / Percentage
**Keywords:** waffle, percentage, proportion, progress, filled, grid
**Best Chart Type:** Waffle Chart
**Secondary Options:** Pictogram, Stacked Bar 100%
**When to Use:** Showing what fraction of a whole is filled; percentage progress in a visually engaging and accessible format
**When NOT to Use:** More than 5 categories (use stacked bar); exact values matter over visual proportion; very tight space
**Data Volume Threshold:** 10×10 grid standard (100 cells); for > 5 categories switch to stacked 100% bar
**Color Guidance:** 3–5 categories max. 2–3px gap between cells. Each category a distinct accessible color pair
**Accessibility Grade:** AA
**Accessibility Notes:** Better than pie for accessibility. Percentage text label always visible. Each cell has aria-label.
**A11y Fallback:** Percentage text always visible; grid cells labeled with aria-label value; provide legend
**Library Recommendation:** D3.js, React-Waffle, Custom CSS Grid
**Interactive Level:** Hover
