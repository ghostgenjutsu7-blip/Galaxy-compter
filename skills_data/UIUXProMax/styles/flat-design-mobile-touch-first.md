---
name: UI Style: Flat Design Mobile (Touch-First)
source: UIUXProMax
version: 1.0.0
description: Cross-platform apps (iOS+Android parity), information-dense dashboards, system UI, brand illustration, onboarding flows, marketing pages, icon design
tags: ["style", "ui"]
triggers: ["Flat Design Mobile (Touch-First)"]
license: MIT
target_agent: design
category: ui_style
---

**No:** 75
**Style Category:** Flat Design Mobile (Touch-First)
**Type:** Mobile
**Keywords:** flat, 2D, no shadow, color blocking, geometric, bold, poster, icon, touch-first, minimal, clean, tailored, cross-platform
**Primary Colors:** Blue #3B82F6, Emerald #10B981
**Secondary Colors:** Background #FFFFFF, Surface #F3F4F6, Text #111827, Amber #F59E0B, Border #E5E7EB
**Effects & Animation:** Immediate press feedback (scale 0.97, no delay), color section blocking (full-width contrasting View), zero elevation/shadow, solid icon containers (colored squares/circles), geometric low-opacity shape overlays, bottom tabs solid fill (no floating)
**Best For:** Cross-platform apps (iOS+Android parity), information-dense dashboards, system UI, brand illustration, onboarding flows, marketing pages, icon design
**Do Not Use For:** Ultra-premium contexts needing depth/shadow, dark-mode-first products, contexts where flat design reads as unfinished or sterile
**Light Mode ✓:** ✓ Full
**Dark Mode ✓:** ◐ Partial (Dark mode via color swap only)
**Performance:** ⚡ Excellent (no GPU effects)
**Accessibility:** ✓ WCAG AA (large bold type helps)
**Mobile-Friendly:** ✓ Mobile-First
**Conversion-Focused:** ✓ High
**Framework Compatibility:** React Native 10/10, Expo 10/10, NativeWind 10/10, Flutter 9/10, SwiftUI 9/10
**Era/Origin:** 2010s–2020s Flat Mobile
**Complexity:** Low
**AI Prompt Keywords:** Design a Flat Mobile app. NO shadows (shadowOpacity: 0, elevation: 0). Color creates all hierarchy. Sections: full-width View blocks alternating contrasting bg colors (Blue Hero → White Content → Gray Block). Buttons: solid #3B82F6, borderRadius 8, height 56. Cards: backgroundColor #FFFFFF (on gray bg) or #DBEAFE (blue tint) — no shadow. Text: fontWeight 800 letterSpacing -0.5 (heads), 600 (sub), 400 (body). Inputs: #F3F4F6 bg, focused: borderWidth 2 borderColor #3B82F6. Icons: Lucide strokeWidth 2.5 inside solid colored square/circle. Press feedback: scale 0.97 Pressable. Use position absolute low-opacity geometric shapes (circles, rotated squares) as background decoration.
**CSS/Technical Keywords:** shadowOpacity: 0, elevation: 0, borderRadius: 6/12/999, height: 48 minimum touch targets, spacing: 4/8/16/24/32/48 system, backgroundColor (section blocking), Pressable scale: pressed ? 0.97 : 1, fontWeight: '800' heads / '600' sub / '400' body, letterSpacing: -0.5 heads / 1 labels, textTransform: 'uppercase' labels, strokeWidth={2.5} icons, borderWidth: 3/4 for featured CTAs
**Implementation Checklist:** ☐ Zero elevation AND shadowOpacity on all elements, ☐ Color-blocking sections (not borders), ☐ All touch targets ≥ 48×48, ☐ No gradients on flat elements, ☐ Icons inside solid colored containers, ☐ Pressable scale feedback, ☐ Geometric shapes as bg decoration, ☐ Bold flat bottom tabs (no floating), ☐ Primary headlines much larger than body, ☐ 4pt spacing system throughout
**Design System Variables:** --bg: #FFFFFF, --surface: #F3F4F6, --fg: #111827, --primary: #3B82F6, --secondary: #10B981, --accent: #F59E0B, --border: #E5E7EB, --radius-sm: 6px, --radius-md: 12px, --radius-pill: 999px, --shadow: none, --elevation: 0, --touch-target: 48px, --spacing: 4 8 16 24 32 48
