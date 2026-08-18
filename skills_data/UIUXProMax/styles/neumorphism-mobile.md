---
name: UI Style: Neumorphism (Mobile)
source: UIUXProMax
version: 1.0.0
description: Minimal hardware controls, smart home apps, aesthetic utility tools, health monitors, brand showcase pages
tags: ["style", "ui"]
triggers: ["Neumorphism (Mobile)"]
license: MIT
target_agent: design
category: ui_style
---

**No:** 85
**Style Category:** Neumorphism (Mobile)
**Type:** Mobile
**Keywords:** neumorphism, soft ui, dual shadow, extruded, inset, clay surface, monochromatic, cool grey, haptic, ceramic, physical, depth
**Primary Colors:** Accent Violet #6C63FF, Clay Base #E0E5EC
**Secondary Colors:** Text Dark #3D4852, Text Muted #6B7280, Shadow Light rgba(255,255,255,0.6), Shadow Dark rgba(163,177,198,0.7), Inset Background #D1D9E6
**Effects & Animation:** Full-screen #E0E5EC base, dual-layer shadow via nested View (light top-left + dark bottom-right), extruded convex resting state, inset concave pressed/input state, Reanimated scale 0.97 on press, shadow opacity interpolates 1→0.4 on press, Haptics Light on every interaction, 8pt grid, no blur shadows (no shadowRadius blend), nested depth (extruded card contains inset icon slot)
**Best For:** Minimal hardware controls, smart home apps, aesthetic utility tools, health monitors, brand showcase pages
**Do Not Use For:** High-density data, bright multi-color apps, apps needing strong visual hierarchy via color, dark-mode-only products
**Light Mode ✓:** ✓ Light-only
**Dark Mode ✓:** ✗ Dark (breaks material metaphor)
**Performance:** ✓ Lightweight
**Accessibility:** ⚠ Moderate (low-contrast risk)
**Mobile-Friendly:** ✓ Mobile-First
**Conversion-Focused:** ✗ Low-Conversion
**Framework Compatibility:** React Native 10/10, react-native-shadow-2 9/10, Reanimated 9/10
**Era/Origin:** Tools/Lifestyle
**Complexity:** Medium
**AI Prompt Keywords:** Design a Neumorphism (Soft UI) mobile app. Entire background is a single color #E0E5EC (Cool Clay). No other background colors. Dual shadows: outer dark shadowColor rgba(163,177,198,0.7) offset(6,6) radius 10 + outer light #FFFFFF offset(-6,-6) radius 10 using nested View or react-native-shadow-2. Extruded (convex) for resting buttons and cards. Inset (concave) for inputs and pressed states. Buttons: height 56, borderRadius 16, scale 0.97 on press with shadow opacity→0.4, Haptics.impactAsync Light. Cards: padding 24, borderRadius 32, nested inner icon container uses inset style. Inputs: height 50, borderRadius 16, backgroundColor #E0E5EC (NOT white), inset depth effect, focus borderColor #6C63FF width 1.5. Typography: Plus Jakarta Sans Bold or System. Heading 24–32pt, body 16pt, caption 12pt, letterSpacing -0.5 for headings. Animation: 250ms Bezier(0.4,0,0.2,1). No black shadows, no pure white backgrounds.
**CSS/Technical Keywords:** backgroundColor: '#E0E5EC', textPrimary: '#3D4852', textMuted: '#6B7280', accent: '#6C63FF', shadowLight: 'rgba(255,255,255,0.6)', shadowDark: 'rgba(163,177,198,0.7)', insetBg: '#D1D9E6', radiusCard: 32, radiusButton: 16, radiusPill: 999, shadowOffset: 6, shadowRadius: 10
**Implementation Checklist:** ☐ Single #E0E5EC base applied across all screens, ☐ Dual shadow (light+dark) implemented via nested View, ☐ Extruded resting state on cards/buttons, ☐ Inset concave state on inputs, ☐ Scale 0.97 press + shadow opacity interpolation, ☐ Haptics Light on all presses, ☐ No black shadows or white backgrounds, ☐ Nested depth pattern (extruded→inset), ☐ Accent #6C63FF on active/focus only, ☐ 8pt grid spacing
**Design System Variables:** --bg: #E0E5EC, --text: #3D4852, --muted: #6B7280, --accent: #6C63FF, --shadow-light: rgba(255,255,255,0.6), --shadow-dark: rgba(163,177,198,0.7), --inset-bg: #D1D9E6, --radius-card: 32px, --radius-button: 16px, --font: Plus Jakarta Sans or System
