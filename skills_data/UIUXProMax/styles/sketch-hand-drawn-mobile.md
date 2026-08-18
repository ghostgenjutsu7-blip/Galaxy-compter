---
name: UI Style: Sketch Hand-Drawn (Mobile)
source: UIUXProMax
version: 1.0.0
description: Low-fidelity prototyping, creative brands, children/picturebook apps, education tools, journaling apps, gamified puzzles
tags: ["style", "ui"]
triggers: ["Sketch Hand-Drawn (Mobile)"]
license: MIT
target_agent: design
category: ui_style
---

**No:** 84
**Style Category:** Sketch Hand-Drawn (Mobile)
**Type:** Mobile
**Keywords:** sketch, hand-drawn, handwriting, wobbly, imperfect, paper, kalam, organic, collage, post-it, tape, offset shadow, scribble
**Primary Colors:** Red Marker #FF4D4D, Pencil Black #2D2D2D
**Secondary Colors:** Warm Paper #FDFBF7, Old Paper #E5E0D8, Blue Ballpoint #2D5DA1, Post-it Yellow #FFF9C4
**Effects & Animation:** Wobbly borderRadius (unique per corner: 15/25/20/10), borderWidth 2–3 solid/dashed, hard offset shadow via rear View (4px,4px) #2D2D2D, Kalam Bold headings, PatrickHand Regular body, slight rotation (-1deg/1deg) on cards, absolute SVG scribble overlays (arrows/tape/tacks), jiggle -2deg↔2deg on error, LayoutAnimation spring on layout changes, Haptics on press, paper texture repeating background
**Best For:** Low-fidelity prototyping, creative brands, children/picturebook apps, education tools, journaling apps, gamified puzzles
**Do Not Use For:** Enterprise dashboards, high-density data tables, fintech precision tools, medical or legal apps
**Light Mode ✓:** ✓ Light
**Dark Mode ✓:** ⚠ Dark (requires texture inversion)
**Performance:** ✓ Lightweight
**Accessibility:** ⚠ Moderate (small/muted text risk)
**Mobile-Friendly:** ✓ Mobile-First (wobbly touch targets 48x48)
**Conversion-Focused:** ✗ Low-Conversion
**Framework Compatibility:** React Native 10/10, Reanimated 9/10, Expo 9/10
**Era/Origin:** Creative/Education
**Complexity:** Medium
**AI Prompt Keywords:** Design a Hand-Drawn (Sketch) mobile app. Background #FDFBF7 (warm paper texture). Typography: Kalam Bold for headings (high weight, felt-tip style), PatrickHand Regular for body (human but legible). Colors: Pencil Black #2D2D2D for all text and borders, Red Marker #FF4D4D for accents, Blue Ballpoint #2D5DA1for input focus. Cards: white background, wobbly corner radii (e.g., 15/25/20/10), borderWidth 3, rotate -1deg or +1deg. Hard offset shadow implemented as a second View behind the card offset 4px right and 4px down. Buttons: Post-it yellow #FFF9C4 for primary CTA, press state shifts the button (translateX 4, translateY 4) to cover the shadow. Inputs: PatrickHand font, wobbly border, focus changes to Blue Ballpoint. Add absolute SVG tape and tack decorations. Error: jiggle animation -2deg to +2deg. All touch targets minimum 48x48.
**CSS/Technical Keywords:** backgroundColor: '#FDFBF7', cardBg: '#FFFFFF', textPrimary: '#2D2D2D', accentRed: '#FF4D4D', accentBlue: '#2D5DA1', accentYellow: '#FFF9C4', border: '#2D2D2D', shadowView: 'offset 4px 4px #2D2D2D', wobblyRadius: [15,25,20,10], fontHeading: 'Kalam-Bold', fontBody: 'PatrickHand-Regular'
**Implementation Checklist:** ☐ Warm paper background texture applied, ☐ Kalam Bold headings, ☐ Wobbly corner radii on all cards, ☐ Hard offset shadow View (not blur), ☐ Cards slightly rotated, ☐ Button press shifts to cover shadow, ☐ SVG tape/tack decorations, ☐ PatrickHand for inputs, ☐ Jiggle error animation, ☐ Minimum 48x48 touch targets
**Design System Variables:** --bg: #FDFBF7, --text: #2D2D2D, --accent-red: #FF4D4D, --accent-blue: #2D5DA1, --postit: #FFF9C4, --border-width: 3px, --shadow-offset: 4px 4px, --font-heading: Kalam Bold, --font-body: Patrick Hand, --rotation-card: -1deg to 1deg
