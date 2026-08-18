---
name: UI Style: Material You (MD3 Mobile)
source: UIUXProMax
version: 1.0.0
description: Android ecosystem apps, cross-platform productivity tools, MD3-based admin panels, data-heavy back-office UI with Material UI
tags: ["style", "ui"]
triggers: ["Material You (MD3 Mobile)"]
license: MIT
target_agent: design
category: ui_style
---

**No:** 76
**Style Category:** Material You (MD3 Mobile)
**Type:** Mobile
**Keywords:** material design 3, md3, tonal surfaces, pills, soft curves, android, md3 easing, state layers, haptic, fab, google
**Primary Colors:** Primary Violet #6750A4, Secondary Container #E8DEF8, Tertiary #7D5260
**Secondary Colors:** Surface #FFFBFE, On Surface #1C1B1F, Surface Container #F3EDF7, Outline #79747E
**Effects & Animation:** Tonal elevation (overlay colors instead of strong shadows), pill-shaped buttons and chips (borderRadius 999), emphasized easing Easing.bezier(0.2,0,0,1), state layers (pressed overlays 10–15% opacity), Reanimated-filled label float for inputs, HapticFeedback on FAB/toggles
**Best For:** Android ecosystem apps, cross-platform productivity tools, MD3-based admin panels, data-heavy back-office UI with Material UI
**Do Not Use For:** Ultra-minimal brutalist brands, terminal/hacker aesthetics, monochrome editorial apps
**Light Mode ✓:** ✓ Full
**Dark Mode ✓:** ✓ Full
**Performance:** ⚠ Good (requires gradients and overlays)
**Accessibility:** ✓ WCAG AA (with MD3 token checks)
**Mobile-Friendly:** ✓ Mobile-First
**Conversion-Focused:** ✓ High
**Framework Compatibility:** React Native 9/10, Expo 10/10, React Native Paper 9/10
**Era/Origin:** Material Design 3
**Complexity:** Medium
**AI Prompt Keywords:** Design a Material You (MD3) mobile app. Use #FFFBFE background, #6750A4 primary, #E8DEF8 secondary container, #F3EDF7 surface container. All interactive elements are pill-shaped (borderRadius: 999). Buttons use Pressable with scale: 0.95 on press and state-layer overlays (black 10% or primary 12%). Inputs use filled M3 style: background #E7E0EC with floating label animation on focus. Elevation is tonal (layering containers) plus light shadow/elevation on Android. Animations use emphasized easing (0.2,0,0,1) at 100–400ms. FABs are tertiary-colored rounded squares/circles with level 3 elevation.
**CSS/Technical Keywords:** borderRadius: 999 (buttons/chips), containerRadius: 16–28, backgroundColor: '#FFFBFE', colorPrimary: '#6750A4', colorSecondaryContainer: '#E8DEF8', colorSurfaceContainer: '#F3EDF7', outlineColor: '#79747E', Pressable state-layer overlay (opacity 0.1–0.15), Easing.bezier(0.2,0,0,1), HapticFeedback.impactMedium on FAB, floating label using Reanimated translateY/scale
**Implementation Checklist:** ☐ MD3 color tokens applied (background/surface/container), ☐ All CTAs are pill-shaped, ☐ State-layer overlays instead of opacity 0.5 hacks, ☐ Emphasized easing used for all animations, ☐ Floating label inputs implemented, ☐ FAB uses tertiary color with correct elevation, ☐ Safe areas respected for organic shapes, ☐ No pure white background, ☐ No harsh box-shadows (ambient only)
**Design System Variables:** --md3-bg: #FFFBFE, --md3-on-surface: #1C1B1F, --md3-primary: #6750A4, --md3-on-primary: #FFFFFF, --md3-secondary-container: #E8DEF8, --md3-on-secondary-container: #1D192B, --md3-tertiary: #7D5260, --md3-surface-container: #F3EDF7, --md3-outline: #79747E, --radius-pill: 999px, --easing-emphasized: cubic-bezier(0.2,0,0,1)
