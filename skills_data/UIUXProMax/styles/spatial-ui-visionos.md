---
name: UI Style: Spatial UI (VisionOS)
source: UIUXProMax
version: 1.0.0
description: Spatial computing apps, VR/AR interfaces, immersive media, futuristic dashboards
tags: ["style", "ui"]
triggers: ["Spatial UI (VisionOS)"]
license: MIT
target_agent: design
category: ui_style
---

**No:** 55
**Style Category:** Spatial UI (VisionOS)
**Type:** General
**Keywords:** Glass, depth, immersion, spatial, translucent, gaze, gesture, apple, vision-pro
**Primary Colors:** Frosted Glass #FFFFFF (15-30% opacity), System White
**Secondary Colors:** Vibrant system colors for active states, deep shadows for depth
**Effects & Animation:** Parallax depth, dynamic lighting response, gaze-hover effects, smooth scale on focus
**Best For:** Spatial computing apps, VR/AR interfaces, immersive media, futuristic dashboards
**Do Not Use For:** Text-heavy documents, high-contrast requirements, non-3D capable devices
**Light Mode ✓:** ✓ Full
**Dark Mode ✓:** ✓ Full
**Performance:** ⚠ Moderate (blur cost)
**Accessibility:** ⚠ Contrast risks
**Mobile-Friendly:** ✓ High (if adapted)
**Conversion-Focused:** ✓ High
**Framework Compatibility:** SwiftUI, React (Three.js/Fiber)
**Era/Origin:** 2024 Spatial Era
**Complexity:** High
**AI Prompt Keywords:** Design a VisionOS-style spatial interface. Use: frosted glass panels, depth layers, translucent backgrounds (15-30% opacity), vibrant colors for active states, gaze-hover effects, floating windows, immersive feel.
**CSS/Technical Keywords:** backdrop-filter: blur(40px) saturate(180%), background: rgba(255,255,255,0.2), border-radius: 24px, box-shadow: 0 8px 32px rgba(0,0,0,0.1), transform: scale on focus, depth via shadows
**Implementation Checklist:** ☐ Glass effect visible, ☐ Depth layers clear, ☐ Hover states defined, ☐ Colors vibrant on active, ☐ Floating feel achieved, ☐ Contrast maintained
**Design System Variables:** --glass-bg: rgba(255,255,255,0.2), --glass-blur: 40px, --glass-saturate: 180%, --window-radius: 24px, --depth-shadow: 0 8px 32px rgba(0,0,0,0.1), --focus-scale: 1.02
