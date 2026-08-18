---
name: Chart Pattern: Geographic Data
source: UIUXProMax
version: 1.0.0
description: Choropleth Map or Bubble Map
tags: ["chart", "data-viz"]
triggers: ["Geographic Data"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 6
**Data Type:** Geographic Data
**Keywords:** geographic, map, location, region, geo, spatial, choropleth
**Best Chart Type:** Choropleth Map or Bubble Map
**Secondary Options:** Geographic Heat Map
**When to Use:** Data has a regional/location dimension; spatial distribution is the core insight for the user
**When NOT to Use:** Regions have very different sizes making visual comparison misleading (use bar); mobile-primary context
**Data Volume Threshold:** <1000 regions: SVG; ≥1000: Canvas/WebGL (Deck.gl); global maps: tile-based rendering
**Color Guidance:** Single color gradient per region group. Categorized colors for discrete types. Legend with clear scale breaks
**Accessibility Grade:** B
**Accessibility Notes:** Include text labels for major regions. Provide keyboard navigation between regions.
**A11y Fallback:** Region text labels; sortable data table by region name and value; keyboard-navigable regions
**Library Recommendation:** D3.js, Mapbox, Leaflet
**Interactive Level:** Pan + Zoom + Drill
