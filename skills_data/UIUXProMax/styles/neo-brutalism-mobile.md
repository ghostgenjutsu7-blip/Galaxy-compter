---
name: UI Style: Neo Brutalism (Mobile)
source: UIUXProMax
version: 1.0.0
description: Creative tools, collab platforms, Gen Z marketing & e-commerce, portfolio sites, sticker-book style content apps
tags: ["style", "ui"]
triggers: ["Neo Brutalism (Mobile)"]
license: MIT
target_agent: design
category: ui_style
---

**No:** 77
**Style Category:** Neo Brutalism (Mobile)
**Type:** Mobile
**Keywords:** neo brutalism, pop art, stickers, thick borders, cream background, hot red, vivid yellow, soft violet, hard offset shadow, mechanical press, collage
**Primary Colors:** Cream #FFFDF5, Hot Red #FF6B6B, Vivid Yellow #FFD93D
**Secondary Colors:** Soft Violet #C4B5FD, Pure Black #000000, White #FFFFFF
**Effects & Animation:** Thick 4px black borders on all major elements, hard offset shadows (4–8px, no blur), mechanical press: translateX/Y equal to shadow offset, slightly rotated cards/badges (-2deg/2deg), high-saturation color blocking, spring/linear animations only
**Best For:** Creative tools, collab platforms, Gen Z marketing & e-commerce, portfolio sites, sticker-book style content apps
**Do Not Use For:** Serious enterprise apps, conservative industries, sober fintech, accessibility-first contexts (must tune contrast)
**Light Mode ✓:** ✓ Light-first
**Dark Mode ✓:** ✗ Dark
**Performance:** ⚠ Moderate (shadows + transforms)
**Accessibility:** ⚠ Requires careful contrast tuning
**Mobile-Friendly:** ✓ Mobile-First
**Conversion-Focused:** ✓ High
**Framework Compatibility:** React Native 10/10, Expo 10/10, NativeWind 9/10
**Era/Origin:** 2020s Neo-Brutalism
**Complexity:** High
**AI Prompt Keywords:** Design a Mobile Neo-Brutalist app. Background: Cream #FFFDF5. All content blocks: white or violet with borderWidth 4 borderColor #000. Shadows are solid offset blocks (no blur) using an extra View behind offset by 4px or 8px. Typography: Space Grotesk Bold/Black only (700–900). Buttons: 56px tall, 4px border, 0 radius; press animation translates button to cover the shadow. Cards slightly rotated (-1deg, 2deg). Colors: Hot Red #FF6B6B for primary, Yellow #FFD93D for focus/badges, Soft Violet #C4B5FD as tertiary. Animation: spring/linear only, no ease-out luxury motion.
**CSS/Technical Keywords:** borderWidth: 4 (primary), 2 (secondary), borderRadius: 0 or 999 (badges only), backgroundColor: '#FFFDF5', shadow implemented as offset View, transform: [{translateX:4},{translateY:4}] on PressIn, fontFamily: 'SpaceGrotesk-Bold', fontWeight: '700/900', transform: [{ rotate: '-1deg' }] on cards, padding: 20
**Implementation Checklist:** ☐ 4px borders on major elements, ☐ Hard offset shadow implemented via extra View, ☐ Mechanical press hides shadow, ☐ Cream canvas background, ☐ Pop-art color palette used, ☐ Cards/badges slightly rotated, ☐ No gradients or soft shadows, ☐ Only bold/black type weights, ☐ Badges slapped with absolute positioning, ☐ Anti-patterns (no subtle gray, no blur) avoided
**Design System Variables:** --bg: #FFFDF5, --ink: #000000, --accent-primary: #FF6B6B, --accent-secondary: #FFD93D, --accent-muted: #C4B5FD, --white: #FFFFFF, --border-primary: 4px solid #000000, --shadow-offset-small: 4px, --shadow-offset-medium: 8px, --radius: 0px, --radius-pill: 999px, --font: Space Grotesk
