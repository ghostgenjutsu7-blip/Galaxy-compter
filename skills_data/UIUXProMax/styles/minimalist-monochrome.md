---
name: UI Style: Minimalist Monochrome
source: UIUXProMax
version: 1.0.0
description: Luxury fashion e-commerce mobile, editorial publications, high-end portfolio apps, experimental/avant-garde brands, digital exhibitions
tags: ["style", "ui"]
triggers: ["Minimalist Monochrome"]
license: MIT
target_agent: design
category: ui_style
---

**No:** 70
**Style Category:** Minimalist Monochrome
**Type:** Mobile
**Keywords:** monochrome, black white, editorial, austere, typographic, sharp, zero radius, high contrast, brutalist, pocket editorial, serif, mechanical
**Primary Colors:** Pure Black #000000, Pure White #FFFFFF
**Secondary Colors:** Muted #F5F5F5, Dark Gray #525252, Border Light #E5E5E5
**Effects & Animation:** Instant inversion active state (tap → bg-black text-white, zero transition-none), no shadows (strictly 2D), full-bleed horizontal rules (4px black section dividers), subtle paper noise texture (opacity: 0.03), slide-in page transitions with hard edge
**Best For:** Luxury fashion e-commerce mobile, editorial publications, high-end portfolio apps, experimental/avant-garde brands, digital exhibitions
**Do Not Use For:** Entertainment, colorful brands, friendly consumer apps, anything requiring visual warmth or gradient
**Light Mode ✓:** ✓ Full (Light Mode Enforced)
**Dark Mode ✓:** ◐ Dark by section only (inverted sections)
**Performance:** ⚡ Excellent
**Accessibility:** ✓ WCAG AAA (pure black/white)
**Mobile-Friendly:** ✓ Mobile-First
**Conversion-Focused:** ◐ Medium
**Framework Compatibility:** React Native 10/10, Expo 10/10, SwiftUI 9/10, Tailwind 9/10
**Era/Origin:** 2020s Editorial Mobile
**Complexity:** Medium
**AI Prompt Keywords:** Design a minimalist monochrome mobile app. Use ONLY black (#000000) and white (#FFFFFF). Zero border-radius on every element. No shadows — depth is created by 1–4px black borders and color inversion only. Typography is the primary visual: Playfair Display for heroes (text-5xl–text-6xl, tracking-tighter, leading-[0.9]), Source Serif 4 for body, JetBrains Mono for labels/tags. Tap states instantly invert (bg-black text-white). Full-width horizontal rules separate sections. Use the word 'MENU' instead of hamburger icon.
**CSS/Technical Keywords:** border-radius: 0px (ALL elements including modals), box-shadow: none, active:bg-black active:text-white transition-none, border-b-4 border-black (section dividers), divide-y divide-black (lists), font-family: Playfair Display (headers) + Source Serif 4 (body) + JetBrains Mono (labels), background-image: noise SVG opacity-[0.03]
**Implementation Checklist:** ☐ 0px border-radius on ALL elements, ☐ No shadows anywhere, ☐ Instant inversion on every tap (transition-none), ☐ 4px black line separates hero from content, ☐ Safe area respected (pt-safe pb-safe), ☐ h-14 touch targets, ☐ Sticky section headers with border-b, ☐ Typography hero: word spans full screen width, ☐ Paper noise texture on backgrounds, ☐ Menu word-label instead of icon
**Design System Variables:** --color-bg: #FFFFFF, --color-fg: #000000, --color-muted: #F5F5F5, --color-muted-fg: #525252, --color-border: #000000, --color-border-light: #E5E5E5, --radius: 0px, --shadow: none, --border-hairline: 1px solid #E5E5E5, --border-thin: 1px solid #000000, --border-thick: 2px solid #000000, --border-heavy: 4px solid #000000, --font-display: Playfair Display, --font-body: Source Serif 4, --font-mono: JetBrains Mono
