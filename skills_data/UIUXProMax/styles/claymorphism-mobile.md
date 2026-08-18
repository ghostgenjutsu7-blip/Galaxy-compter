---
name: UI Style: Claymorphism (Mobile)
source: UIUXProMax
version: 1.0.0
description: Children education apps, teen social products, crypto gamification, creative tools, brand mascot-led apps
tags: ["style", "ui"]
triggers: ["Claymorphism (Mobile)"]
license: MIT
target_agent: design
category: ui_style
---

**No:** 82
**Style Category:** Claymorphism (Mobile)
**Type:** Mobile
**Keywords:** claymorphism, clay, 3d, soft, bubbly, candy, playful, rounded, squish, tactile, inflate, silicone, haptic, spring
**Primary Colors:** Vivid Violet #7C3AED, Hot Pink #DB2777
**Secondary Colors:** Canvas #F4F1FA, Soft Charcoal #332F3A, Emerald #10B981, Amber #F59E0B, Lavender-Gray #635F69
**Effects & Animation:** Multi-layer shadow stacks (nested View) to simulate clay depth, LinearGradient #A78BFA→#7C3AED buttons, borderRadius 40–50 outer / 32 cards / 20 buttons, Reanimated spring squish (scale 0.92 on press), BlurView glass-clay hybrid cards, floating blobs with slow ±20px drift, Haptics Light on every press
**Best For:** Children education apps, teen social products, crypto gamification, creative tools, brand mascot-led apps
**Do Not Use For:** Serious enterprise, high-density data, editorial reading apps, fintech trust signals
**Light Mode ✓:** ✓ Light
**Dark Mode ✓:** ⚠ Dark (adjusted)
**Performance:** ⚠ Moderate–Heavy (shadows+blur)
**Accessibility:** ✓ WCAG AA (careful)
**Mobile-Friendly:** ✓ Mobile-First (thumb zone)
**Conversion-Focused:** ✓ High
**Framework Compatibility:** React Native 10/10, Reanimated 10/10, Expo 10/10
**Era/Origin:** Consumer/Education
**Complexity:** High
**AI Prompt Keywords:** Design a high-fidelity Claymorphism mobile app. Background #F4F1FA (cool lavender-white, never pure white). Primary CTA: LinearGradient #A78BFA to #7C3AED, borderRadius 20, height 56. Cards: borderRadius 32, backgroundColor rgba(255,255,255,0.7) with BlurView. Multi-layer shadow: outer offset(12,12) rgba(160,150,180,0.2) + highlight offset(-8,-8) white. Typography: Nunito Black 900 for headings (48px hero, 32px section, 22px card), DM Sans Medium 500 for body 16px. Spring animations: scale 0.92 on press, spring back damping 10. Background blobs drift ±20px over 8–10s. Bento 2-column grid with hero card spanning full width. Haptics.impactAsync Light on every button press.
**CSS/Technical Keywords:** backgroundColor: '#F4F1FA', cardBg: 'rgba(255,255,255,0.7)', textPrimary: '#332F3A', textMuted: '#635F69', accentPrimary: '#7C3AED', accentSecondary: '#DB2777', success: '#10B981', warning: '#F59E0B', radiusOuter: 50, radiusCard: 32, radiusButton: 20, shadowStack: 'nested View', gradientButton: ['#A78BFA', '#7C3AED'], springDamping: 10
**Implementation Checklist:** ☐ Background uses #F4F1FA (no pure white), ☐ Multi-layer clay shadow stack applied, ☐ Cards use blurred glass-clay hybrid, ☐ Buttons squish to scale 0.92 on press, ☐ Spring physics on all interactions, ☐ Nunito Black for headings, ☐ Background blobs drifting, ☐ Haptics on every press, ☐ Nested border radius (card 32, inner 24), ☐ Bento layout with hero span
**Design System Variables:** --bg: #F4F1FA, --card-bg: rgba(255,255,255,0.7), --text: #332F3A, --muted: #635F69, --accent: #7C3AED, --accent2: #DB2777, --success: #10B981, --warning: #F59E0B, --radius-outer: 50px, --radius-card: 32px, --radius-button: 20px, --font-heading: Nunito Black, --font-body: DM Sans
