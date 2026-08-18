---
name: UI Style: Modern Dark (Cinema Mobile)
source: UIUXProMax
version: 1.0.0
description: Developer tools, pro productivity apps, fintech/trading dashboards, media/streaming platforms, AI tool interfaces, high-end gaming companion apps
tags: ["style", "ui"]
triggers: ["Modern Dark (Cinema Mobile)"]
license: MIT
target_agent: design
category: ui_style
---

**No:** 71
**Style Category:** Modern Dark (Cinema Mobile)
**Type:** Mobile
**Keywords:** dark mode, cinematic, ambient light, glassmorphism, deep black, indigo, glow, blur, atmospheric, reanimated, haptic, premium, layered, frosted glass, linear gradient
**Primary Colors:** Deep #020203, Base #050506, Elevated #0a0a0c, Accent #5E6AD2
**Secondary Colors:** Foreground #EDEDEF, Muted #8A8F98, Accent Glow rgba(94 106 210/0.2), Border rgba(255 255 255/0.08), Surface rgba(255 255 255/0.05)
**Effects & Animation:** Expo.out Bezier(0.16,1,0.3,1) easing; spring modals (damping:20 stiffness:90); haptic-linked press (Impact Light/Medium); animated ambient light blobs (Reanimated translateX/Y slow oscillation); BlurView glassmorphism headers/nav (intensity 20); scale press 0.97 → 1.0; avoid pure #000000 (OLED smear)
**Best For:** Developer tools, pro productivity apps, fintech/trading dashboards, media/streaming platforms, AI tool interfaces, high-end gaming companion apps
**Do Not Use For:** Consumer apps needing warmth, children's apps, health/medical contexts where dark feels harsh, high-accessibility contexts needing maximum contrast
**Light Mode ✓:** ✓ Light mode only as exception
**Dark Mode ✓:** ✓ Dark Mode Primary
**Performance:** ⚠ Good (blur effects require native driver)
**Accessibility:** ⚠ WCAG AA (requires careful accent contrast check)
**Mobile-Friendly:** ✓ Mobile-First
**Conversion-Focused:** ◐ Medium
**Framework Compatibility:** React Native 10/10, Expo 10/10, react-native-skia 9/10, SwiftUI 8/10
**Era/Origin:** 2020s Cinematic Mobile
**Complexity:** High
**AI Prompt Keywords:** Design a cinematic dark mobile app. Background: LinearGradient from #0a0a0f (top) to #020203 (bottom). Add 2–3 absolute animated 'blob' views: circular, blurRadius 30–50, opacity 0.08–0.12, slow Reanimated oscillation. Cards: borderRadius 16, border rgba(255,255,255,0.08) hairline, subtle top-edge shine gradient. Primary button: #5E6AD2, scale press 0.97, haptic on press. BlurView (intensity 20, tint dark) for tab bar and headers. Typography: Inter 700 for headers, 400 for body. Never use pure #000000. Accent glow: rgba(94,106,210,0.2) behind primary actions.
**CSS/Technical Keywords:** borderRadius: 16 (cards/buttons), background: LinearGradient #0a0a0f→#020203, border: StyleSheet.hairlineWidth rgba(255,255,255,0.08), BlurView intensity={20} tint='dark', useAnimatedStyle + withRepeat (blob oscillation), Easing.bezier(0.16,1,0.3,1), withSpring damping:20 stiffness:90, Haptics.impactAsync(ImpactFeedbackStyle.Light), scale: 0.97 press
**Implementation Checklist:** ☐ No pure #000000 backgrounds, ☐ LinearGradient base screen, ☐ Animated ambient blobs (Reanimated, native driver), ☐ BlurView on tab bar and headers, ☐ borderRadius 16 on all cards, ☐ Haptic feedback on every Pressable, ☐ Bezier(0.16,1,0.3,1) easing used, ☐ Accent glow behind primary button, ☐ No solid grey borders (rgba only), ☐ Bottom sheets replace all modals
**Design System Variables:** --bg-deep: #020203, --bg-base: #050506, --bg-elevated: #0a0a0c, --surface: rgba(255 255 255/0.05), --foreground: #EDEDEF, --foreground-muted: #8A8F98, --accent: #5E6AD2, --accent-glow: rgba(94 106 210/0.2), --border: rgba(255 255 255/0.08), --radius: 16px, --easing: cubic-bezier(0.16 1 0.3 1), --font: Inter
