---
name: Design System: warm-editorial
source: OpenDesign
version: 1.0.0
description: Category: Starter
tags: ["design-system", "warm-editorial"]
triggers: ["warm-editorial"]
license: Apache-2.0
target_agent: design
category: design_system
---

# Warm Editorial

> Category: Starter
> A serif-led magazine aesthetic. Terracotta accent on warm off-white paper —
> good for long-form, editorial, and brand-led marketing pages.

## Visual Theme & Atmosphere
Warm, unhurried, magazine-like. Think "a New Yorker interview column online." Generous whitespace, long-form readability, restrained chrome. Playful but never novelty.

## Color Palette & Roles
- **Background:** `#FAF7F2` (warm off-white paper)
- **Foreground:** `#1C1A17` (near-black, slightly warm)
- **Accent (primary):** `#C0512F` (terracotta) — used for links, primary CTAs, 1 hero element max per page
- **Accent (secondary):** `#2F5B4F` (forest) — section dividers, tags
- **Muted:** `#8A817A` (mid-warm-grey) — timestamps, metadata
- **Surface:** `#FFFFFF` — elevated cards only
Never use pure black or pure white anywhere user-facing.

## Typography Rules
- **Display / headings:** "GT Sectra" or fallback serif (`'GT Sectra', 'Times New Roman', serif`)
- **Body:** "Söhne" or fallback sans (`'Söhne', -apple-system, system-ui, sans-serif`)
- **Mono:** `'JetBrains Mono', ui-monospace, monospace` for code only
- Scale (px): 12 · 14 · 16 · 20 · 28 · 40 · 56 · 80
- Line-height: 1.6 for body, 1.2 for display
- Letter-spacing: -0.02em for display sizes above 40px; default elsewhere

## Component Stylings
- **Buttons:** flat fill, 12px radius, 14px padding-block, 20px padding-inline. Primary = terracotta fill, off-white label. Secondary = outlined 1px foreground, transparent fill.
- **Cards:** off-white background, 1px forest-at-8%-opacity border, 16px radius, 24–32px internal padding. No shadow except hover (y+2px, blur 16, foreground-at-6%).
- **Inputs:** underline only (no box), 1px muted baseline, terracotta baseline on focus, 16px vertical padding.
- **Links:** terracotta, 1px terracotta-at-40% underline, no underline on hover (swap for terracotta-at-8% background).

## Layout Principles
- 12-column grid, 1200px max-width, 24px gutters.
- Hero sections: 72vh minimum, 120vh maximum. Content top-biased, never centered vertically.
- Body sections: 80px top+bottom spacing at desktop; 48px at tablet; 32px at phone.
- One accent color per screen. If a page has a terracotta hero, secondary CTAs are foreground-only, not forest.

## Depth & Elevation
Minimal. Only two elevation levels:
- **Flat (0):** everything by default.
- **Raised (1):** cards on hover, dropdown menus, floating CTAs. 2px y-offset, 16px blur, foreground at 6% opacity.
No shadows on inputs. No shadows on the hero. No neumorphism, no glassmorphism.

## Do's and Don'ts
- ✅ Let whitespace breathe. A short headline on 50% of the viewport height is correct.
- ✅ Use serif for numbers when they matter (pricing, stats).
- ✅ Draw one accent element per page; the rest is foreground.
- ❌ No gradients.
- ❌ No emojis in product copy.
- ❌ No sentence-case for headings — use title case for H1/H2, sentence case for H3 and below.
- ❌ No border-radius above 24px; no border-radius below 8px.

## Responsive Behavior
- **Desktop ≥ 1024px:** 12-col grid, full hero heights, side-by-side columns.
- **Tablet 640–1023px:** 8-col grid; hero drops to 60vh; columns stack at 3+.
- **Phone < 640px:** 4-col grid; single-column layout; hero drops to 50vh; all padding -33%.

## Agent Prompt Guide
When generating artifacts against this design system:
- Lead with typography and whitespace; chrome (borders, shadows) is subtractive.
- If you need more than one accent element on a screen, you're doing too much — cut one.
- When asked for "professional" or "serious," lean harder on serif + whitespace. When asked for "modern," this system isn't the right answer; pick a different DESIGN.md.
- Color tokens are non-negotiable. Do not invent new hex values. If the request needs a color outside this palette, produce a warning comment in the artifact and use the closest existing token.
- Prefer 1 hero + 3–5 body sections over 1 hero + 8+ sections. Editorial means restraint.


## Machine-readable tokens (paste verbatim into `:root`)
```css
:root {
  --bg: #fbf6ee;
  --surface: #fffdf8;
  --surface-warm: #f1e3cf;
  --fg: #201914;
  --fg-2: #4c4037;
  --muted: #7a6d63;
  --meta: #9b5b32;
  --border: #ded2c3;
  --border-soft: #eee4d7;
  --accent: #9b5b32;
  --accent-on: #ffffff;
  --accent-hover: color-mix(in oklab, var(--accent), black 8%);
  --accent-active: color-mix(in oklab, var(--accent), black 14%);
  --success: #4f8a4f;
  --warn: #c9822f;
  --danger: #b33a3a;
  --font-display: Georgia, "Times New Roman", serif;
  --font-body: Inter, system-ui, sans-serif;
  --font-mono: "SF Mono", ui-monospace, Menlo, monospace;
  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 17px;
  --text-lg: 20px;
  --text-xl: 28px;
  --text-2xl: 42px;
  --text-3xl: 64px;
  --text-4xl: 88px;
  --leading-body: 1.62;
  --leading-tight: 1;
  --tracking-display: -0.025em;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --section-y-desktop: 112px;
  --section-y-tablet: 80px;
  --section-y-phone: 56px;
  --radius-sm: 10px;
  --radius-md: 16px;
  --radius-lg: 24px;
  --radius-pill: 9999px;
  --elev-flat: none;
  --elev-ring: 0 0 0 1px var(--border);
  --elev-raised: 0 20px 52px rgba(32, 25, 20, 0.12);
  --focus-ring: 0 0 0 4px rgba(155, 91, 50, 0.24);
  --motion-fast: 150ms;
  --motion-base: 240ms;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --container-max: 1180px;
  --container-gutter-desktop: 36px;
  --container-gutter-tablet: 24px;
  --container-gutter-phone: 16px;
}
```
