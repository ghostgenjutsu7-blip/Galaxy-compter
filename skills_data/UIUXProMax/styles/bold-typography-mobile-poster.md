---
name: UI Style: Bold Typography (Mobile Poster)
source: UIUXProMax
version: 1.0.0
description: Creative brand heroes, reading-focused apps, event/exhibition pages, editorial mobile experiences, landing hero sections
tags: ["style", "ui"]
triggers: ["Bold Typography (Mobile Poster)"]
license: MIT
target_agent: design
category: ui_style
---

**No:** 78
**Style Category:** Bold Typography (Mobile Poster)
**Type:** Mobile
**Keywords:** bold typography, editorial, poster, broadsheet, vermillion, negative space, edge-to-edge type, underline CTA, near-black, warm white
**Primary Colors:** Near Black #0A0A0A, Warm White #FAFAFA
**Secondary Colors:** Muted #1A1A1A, Secondary Text #737373, Accent Vermillion #FF3D00, Border #262626
**Effects & Animation:** Hero headlines 48–72px (5:1 vs body size), tight tracking (-1.5px), edge-to-edge type, massive vertical spacing (60px+), underline CTAs (2–3px accent line), instant 200ms transitions (no bounce), strictly 0px radius containers, color shifts for active state instead of elevation
**Best For:** Creative brand heroes, reading-focused apps, event/exhibition pages, editorial mobile experiences, landing hero sections
**Do Not Use For:** Utility dashboards, kids apps, playful consumer products, contexts needing many icons or heavy imagery
**Light Mode ✓:** ✓ Dark Mode Primary
**Dark Mode ✓:** ◐ Light sections optional
**Performance:** ⚡ Excellent
**Accessibility:** ✓ Contrast 18:1 achievable
**Mobile-Friendly:** ✓ Mobile-First
**Conversion-Focused:** ✓ High
**Framework Compatibility:** React Native 10/10, Expo 10/10
**Era/Origin:** Editorial 2020s
**Complexity:** Medium
**AI Prompt Keywords:** Design a Bold Typography mobile screen. Background #0A0A0A, text #FAFAFA, accent #FF3D00. Use Inter Tight/Inter 600+ for all type; JetBrains Mono for labels. Headline: 56–72px, tracking -1.5, lineHeight 1.1, full-bleed width with slight bleed off-screen. Body: 16–18px, leading 1.6. Buttons: underline CTA (accent text + 2px underline block), or inverted box with 0 radius. No shadows, no rounded corners. Layout: single column, paddingHorizontal 24, vertical gaps 64 between sections. Animation: 200ms, Easing.bezier(0.25,0,0,1), slight slide-up 10px + fade on mount.
**CSS/Technical Keywords:** backgroundColor: '#0A0A0A', color: '#FAFAFA', accent: '#FF3D00', borderColor: '#262626', borderRadius: 0, paddingHorizontal: 24, headline style: fontSize:56–72, fontWeight:'700/800', letterSpacing:-1.5, lineHeight:1.1*fontSize, body: fontSize:16–18, lineHeight:1.6*fontSize, underline CTA: 2–3px height View under text, transition: 200ms cubic-bezier(0.25,0,0,1)
**Implementation Checklist:** ☐ H1 at least 4–5× body size, ☐ All containers 0 radius, ☐ Underline CTA pattern used, ☐ Large vertical gaps between sections, ☐ No shadows or soft corners, ☐ Accent used only for interaction, ☐ Text bleeds to/over screen edges, ☐ Animation timings 200ms, ☐ Accessible contrast ≥ 18:1, ☐ Body text never below 16px
**Design System Variables:** --bg: #0A0A0A, --fg: #FAFAFA, --muted: #1A1A1A, --muted-fg: #737373, --accent: #FF3D00, --accent-fg: #0A0A0A, --border: #262626, --font-primary: Inter Tight, --font-display: Playfair Display Italic, --font-mono: JetBrains Mono
