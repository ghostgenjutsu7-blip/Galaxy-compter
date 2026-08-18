---
name: UI Style: Terminal CLI (Mobile)
source: UIUXProMax
version: 1.0.0
description: Developer tools, Web3/blockchain apps, geek-culture apps, ARG games, sci-fi/noir gaming companions, hacker/security tools, creative studio portfolios
tags: ["style", "ui"]
triggers: ["Terminal CLI (Mobile)"]
license: MIT
target_agent: design
category: ui_style
---

**No:** 73
**Style Category:** Terminal CLI (Mobile)
**Type:** Mobile
**Keywords:** terminal, cli, matrix green, monospace, hacker, ascii, command line, developer, web3, crypto, sci-fi, OLED, retro-future, field operative
**Primary Colors:** Matrix Green #33FF00, OLED Black #050505
**Secondary Colors:** Amber #FFB000, Muted Green #1A3D1A, Error Red #FF3333, Border Green #33FF00
**Effects & Animation:** Blinking cursor (500ms opacity loop), typewriter text reveal hook, scanline overlay (repeating lines 0.05 opacity), ASCII art headers, instant color inversion on press (bg-green text-black), haptic on every keystroke, boot sequence splash on launch
**Best For:** Developer tools, Web3/blockchain apps, geek-culture apps, ARG games, sci-fi/noir gaming companions, hacker/security tools, creative studio portfolios
**Do Not Use For:** Consumer products, health apps, anything requiring approachability or warmth, children's apps, standard enterprise contexts
**Light Mode ✓:** ✗ No
**Dark Mode ✓:** ✓ OLED Dark Only
**Performance:** ⚡ Excellent
**Accessibility:** ✓ High contrast (green on black ≫4.5:1 ratio)
**Mobile-Friendly:** ✓ Mobile-First (OLED optimized)
**Conversion-Focused:** ✗ Low
**Framework Compatibility:** React Native 10/10, Expo 10/10, NativeWind 9/10
**Era/Origin:** Retro-Future 1980s–2020s
**Complexity:** Medium
**AI Prompt Keywords:** Design a Mobile Terminal CLI app. Background: #050505 OLED black. ALL text in Matrix Green #33FF00. Font: JetBrains Mono or SpaceMono ONLY — zero border-radius everywhere. ASCII borders using +, -, |, * characters instead of standard containers. Buttons displayed as [ EXECUTE ] or > PROCEED. On press: instantly inverts to green bg + black text + haptic. Cursor: blinking View opacity 0→1 at 500ms. Show boot sequence on launch (fake log scroll). Progress bars as [#####-----] text. Status bar footer: [BATTERY:88%] [NET:CONNECTED]. Scanline overlay: absolute View with repeating 1px horizontal lines at opacity 0.05. Typewriter effect on new data.
**CSS/Technical Keywords:** borderRadius: 0 (ALL elements), borderWidth: 1, borderColor: '#33FF00', backgroundColor: '#050505', color: '#33FF00', fontFamily: 'SpaceMono-Regular' or JetBrains Mono, fontSize: 12 or 14 or 16 only, lineHeight: 1.2x fontSize, Haptics.impactAsync(Light) on every press, useAnimatedValue blink 500ms, hitSlop: 12px all sides for bracketed buttons
**Implementation Checklist:** ☐ 0px border-radius everywhere, ☐ ASCII-style borders on cards, ☐ Boot sequence on launch, ☐ Blinking cursor component, ☐ Typewriter hook for new content, ☐ Scanline overlay (0.05 opacity), ☐ Haptic on every button press, ☐ Footer status bar component, ☐ hitSlop on all bracketed buttons (44×44dp), ☐ Reduced motion respected
**Design System Variables:** --bg: #050505, --fg-primary: #33FF00, --fg-amber: #FFB000, --fg-muted: #1A3D1A, --fg-error: #FF3333, --border: #33FF00, --radius: 0px, --font: SpaceMono-Regular or JetBrains Mono, --font-sizes: 12 14 16 only, --blink-duration: 500ms, --scanline-opacity: 0.05
