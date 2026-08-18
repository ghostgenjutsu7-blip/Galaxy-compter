---
name: UI Style: Dimensional Layering
source: UIUXProMax
version: 1.0.0
description: Dashboards, card layouts, modals, navigation, product showcases, SaaS interfaces
tags: ["style", "ui"]
triggers: ["Dimensional Layering"]
license: MIT
target_agent: design
category: ui_style
---

**No:** 46
**Style Category:** Dimensional Layering
**Type:** General
**Keywords:** Depth, overlapping, z-index, layers, 3D, shadows, elevation, floating, cards, spatial hierarchy
**Primary Colors:** Neutral base (#FFFFFF, #F5F5F5, #E0E0E0) + brand accent for elevated elements
**Secondary Colors:** Shadow variations (sm/md/lg/xl), elevation colors, highlight colors for top layers
**Effects & Animation:** z-index stacking, box-shadow elevation (4 levels), transform: translateZ(), backdrop-filter, parallax
**Best For:** Dashboards, card layouts, modals, navigation, product showcases, SaaS interfaces
**Do Not Use For:** Print-style layouts, simple blogs, low-end devices, flat design requirements
**Light Mode ✓:** ✓ Full
**Dark Mode ✓:** ✓ Full
**Performance:** ⚠ Good
**Accessibility:** ⚠ Moderate (SR issues)
**Mobile-Friendly:** ✓ Good
**Conversion-Focused:** ✓ High
**Framework Compatibility:** Tailwind 10/10, MUI 10/10, Chakra 10/10
**Era/Origin:** 2020s Modern
**Complexity:** Medium
**AI Prompt Keywords:** Design with dimensional layering. Use: z-index depth (multiple layers), overlapping cards, elevation shadows (4 levels), floating elements, parallax depth, backdrop blur for hierarchy, spatial UI feel.
**CSS/Technical Keywords:** z-index: 1-4 levels, box-shadow: elevation scale (sm/md/lg/xl), transform: translateZ(), backdrop-filter: blur(), position: relative for stacking, parallax on scroll
**Implementation Checklist:** ☐ Layers clearly defined, ☐ Shadows show depth, ☐ Overlaps intentional, ☐ Hierarchy clear, ☐ Performance optimized, ☐ Mobile depth maintained
**Design System Variables:** --elevation-1: 0 1px 3px rgba(0,0,0,0.1), --elevation-2: 0 4px 6px rgba(0,0,0,0.1), --elevation-3: 0 10px 20px rgba(0,0,0,0.1), --elevation-4: 0 20px 40px rgba(0,0,0,0.15), --blur-amount: 8px
