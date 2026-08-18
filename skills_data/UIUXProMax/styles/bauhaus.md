---
name: UI Style: Bauhaus (包豪斯)
source: UIUXProMax
version: 1.0.0
description: Mobile-first apps needing high personality, onboarding flows, branding-forward product screens, artisan/design brands, editorial mobile experiences
tags: ["style", "ui"]
triggers: ["Bauhaus (\u5305\u8c6a\u65af)"]
license: MIT
target_agent: design
category: ui_style
---

**No:** 69
**Style Category:** Bauhaus (包豪斯)
**Type:** Mobile
**Keywords:** bauhaus, geometric, constructivist, primary colors, hard shadow, bold, tactile, functional, poster, mechanical, architectural
**Primary Colors:** Primary Red #D02020, Primary Blue #1040C0, Primary Yellow #F0C020
**Secondary Colors:** Background #F0F0F0 (Off-white), Foreground #121212 (Stark Black), Muted #E0E0E0
**Effects & Animation:** Hard offset shadows (4px 4px 0px black), mechanical press active:translate, no smooth hover — instant 0ms transitions, dot grid pattern on sections, slide-over transitions
**Best For:** Mobile-first apps needing high personality, onboarding flows, branding-forward product screens, artisan/design brands, editorial mobile experiences
**Do Not Use For:** Enterprise dashboards, accessibility-critical contexts (requires extra a11y work), data-heavy screens, conservative industries
**Light Mode ✓:** ✓ Full
**Dark Mode ✓:** ◐ Partial (primary palette only)
**Performance:** ⚡ Excellent
**Accessibility:** ⚠ WCAG AA (high contrast primaries; verify yellow text separately)
**Mobile-Friendly:** ✓ Mobile-First
**Conversion-Focused:** ◐ Medium
**Framework Compatibility:** React Native 10/10, Expo 10/10, SwiftUI 9/10, Flutter 9/10, Tailwind 9/10
**Era/Origin:** 1919 Bauhaus Movement
**Complexity:** Medium
**AI Prompt Keywords:** Design a Bauhaus mobile app. Use strict geometric shapes (circles and squares only), primary color blocking (Red #D02020, Blue #1040C0, Yellow #F0C020), hard 4px offset black shadows, OFF-WHITE canvas (#F0F0F0), massive bold uppercase headlines (Outfit Black 900), rectangular full-width buttons with mechanical press animation. No gradients. No rounded cards. No soft transitions.
**CSS/Technical Keywords:** border-radius: 0px (cards/inputs) or 9999px (buttons/FAB), box-shadow: 4px 4px 0px 0px #121212, active:translate-x-[2px] active:translate-y-[2px] active:shadow-none, border: 2px solid #121212, font-family: Outfit, font-weight: 900 uppercase tracking-tighter (headlines)
**Implementation Checklist:** ☐ Geometric shapes only (circle/square), ☐ Primary color blocking applied, ☐ Hard offset shadows 4px, ☐ border-2 border-black on all elements, ☐ Mechanical press active state, ☐ Outfit Black 900 uppercase headlines, ☐ Safe area (pt-safe pb-safe) respected, ☐ Thumb-friendly h-12/h-14 touch targets, ☐ No hover states (mobile-only), ☐ Vertical rhythm single-column stack
**Design System Variables:** --color-red: #D02020, --color-blue: #1040C0, --color-yellow: #F0C020, --color-bg: #F0F0F0, --color-fg: #121212, --border-width: 2px, --shadow-hard: 4px 4px 0px 0px #121212, --radius-block: 0px, --radius-pill: 9999px, --font-display: Outfit, --font-weight-hero: 900
