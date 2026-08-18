---
name: Chart Pattern: 3D Spatial Data
source: UIUXProMax
version: 1.0.0
description: 3D Scatter / Surface Plot
tags: ["chart", "data-viz"]
triggers: ["3D Spatial Data"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 22
**Data Type:** 3D Spatial Data
**Keywords:** 3d, spatial, immersive, terrain, molecular, volumetric, point-cloud
**Best Chart Type:** 3D Scatter / Surface Plot
**Secondary Options:** Volumetric Rendering, Point Cloud
**When to Use:** Scientific/engineering context where Z-axis carries essential info not expressible in 2D
**When NOT to Use:** 2D projection conveys the same insight; mobile context; accessibility-required environments; standard business dashboards
**Data Volume Threshold:** WebGL required. Deck.gl: up to 1M points. Three.js: LOD required beyond 50,000 pts
**Color Guidance:** Depth cues: lighting and shading. Z-axis: color gradient (cool → warm). Transparent overlapping: opacity 0.4
**Accessibility Grade:** D
**Accessibility Notes:** 3D spatial charts are fundamentally inaccessible. Must not be used as primary chart type in any product UI.
**A11y Fallback:** Mandatory 2D projection view + data table; do not use as primary chart type in product UI
**Library Recommendation:** Three.js, Deck.gl, Plotly 3D
**Interactive Level:** Rotate + Zoom + VR
