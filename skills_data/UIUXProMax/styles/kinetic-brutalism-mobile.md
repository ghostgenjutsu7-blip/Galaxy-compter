---
name: UI Style: Kinetic Brutalism (Mobile)
source: UIUXProMax
version: 1.0.0
description: Immersive storytelling apps, brand flagship mobile, music/culture platforms, sports apps, underground zines, limited-edition product drops, performance dashboards
tags: ["style", "ui"]
triggers: ["Kinetic Brutalism (Mobile)"]
license: MIT
target_agent: design
category: ui_style
---

**No:** 74
**Style Category:** Kinetic Brutalism (Mobile)
**Type:** Mobile
**Keywords:** kinetic, brutalism, motion, marquee, acid yellow, uppercase, oversized, aggressive typography, street, zine, high contrast, scroll-driven, haptic, reanimated
**Primary Colors:** Acid Yellow #DFE104, Rich Black #09090B
**Secondary Colors:** Off-white #FAFAFA, Dark Gray #27272A, Zinc #A1A1AA, Border Zinc #3F3F46
**Effects & Animation:** Infinite marquee (Reanimated, Linear easing, 5s loop, hard clip), hero parallax (scale 1.0→1.3 + fade), sticky section header push, card flood inversion on press (bg→#DFE104, text→#000000), haptic Medium on every press, scroll-triggered interpolate transforms, 0px radius, 2px borders, 100ms color transitions
**Best For:** Immersive storytelling apps, brand flagship mobile, music/culture platforms, sports apps, underground zines, limited-edition product drops, performance dashboards
**Do Not Use For:** Calm informational apps, healthcare, finance contexts needing trust, children's, any context where aggressive typography feels inappropriate
**Light Mode ✓:** ✓ Dark Primary
**Dark Mode ✓:** ◐ Dark only (inverted sections)
**Performance:** ⚡ Excellent (native driver required)
**Accessibility:** ⚠ WCAG AA (verify zinc body text on dark bg)
**Mobile-Friendly:** ✓ Mobile-First
**Conversion-Focused:** ✓ High energy
**Framework Compatibility:** React Native 10/10, Expo 10/10, Reanimated 10/10, NativeWind 9/10
**Era/Origin:** 2020s Mobile Brutalism
**Complexity:** High
**AI Prompt Keywords:** Design a Kinetic Brutalism mobile app. Canvas: #09090B. Primary accent: Acid Yellow #DFE104 (text: #000000). Typography: Space Grotesk BOLD. Display text: 60–120pt, uppercase, letterSpacing -1, lineHeight 0.9–1.1x. Body: 18–20pt. Labels: 12pt uppercase letterSpacing +2. Add infinite marquee rows (Reanimated, no easing, hard edge clip). Hero text parallax on scroll (Interpolate: scale 1.0→1.3, opacity 1→0). Card press: instantly flood to #DFE104 + flip text to #000. Haptic Medium on every press. 0px radius. 2px solid borders. NO shadows. No gradients. Scale all fonts by (windowWidth / 375 * size) for responsiveness.
**CSS/Technical Keywords:** borderRadius: 0, borderWidth: 2, borderColor: '#3F3F46', backgroundColor: '#09090B', color: '#FAFAFA', fontWeight: '800 or 900', letterSpacing: -1 (large) or 2 (labels), lineHeight: 0.9–1.1 * fontSize, Reanimated withRepeat marquee timing 5000ms Easing.linear, Interpolate scroll→scale + opacity, Haptics.impactAsync(Medium), scale press: 0.95, 100ms color transitions
**Implementation Checklist:** ☐ Infinite marquee rows (Reanimated, no fade edges), ☐ Hero parallax scroll (scale+opacity Interpolate), ☐ All display text uppercase, ☐ 0px border-radius, ☐ 2px borders, ☐ Acid yellow card flood on press, ☐ Haptic Medium on every interaction, ☐ Font scale helper (windowWidth/375*size), ☐ Safe area for massive headers, ☐ Reduced motion stops marquees
**Design System Variables:** --bg: #09090B, --fg: #FAFAFA, --muted: #27272A, --muted-fg: #A1A1AA, --accent: #DFE104, --accent-fg: #000000, --border: #3F3F46, --radius: 0px, --border-width: 2px, --shadow: none, --marquee-speed: 5000ms, --press-duration: 100ms, --font: Space Grotesk or Inter
