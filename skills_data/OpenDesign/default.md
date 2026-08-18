---
name: Design System: default
source: OpenDesign
version: 1.0.0
description: Category: Starter
tags: ["design-system", "default"]
triggers: ["default"]
license: Apache-2.0
target_agent: design
category: design_system
---

# Neutral Modern

> Category: Starter
> A clean, product-oriented default. Use when the brief doesn't call for a
> specific mood — good for B2B tools, dashboards, and utility pages.

## Visual Theme & Atmosphere
Calm, functional, quietly confident. No ornament. Content-first, chrome-second.

## Color Palette & Roles
- **Background:** `#FAFAFA`
- **Foreground:** `#111111`
- **Accent:** `#2F6FEB` (cobalt) — primary CTAs, links, one hero element per screen
- **Muted:** `#6B6B6B` — secondary text, captions
- **Border:** `#E5E5E5`
- **Surface:** `#FFFFFF` — cards, modals
- **Success:** `#17A34A`, **Warn:** `#EAB308`, **Danger:** `#DC2626`
Never pure black; never pure white for backgrounds.

## Typography Rules
- **Display / headings:** `'Inter', -apple-system, system-ui, sans-serif`, weight 600
- **Body:** `'Inter', -apple-system, system-ui, sans-serif`, weight 400
- **Mono:** `ui-monospace, 'JetBrains Mono', monospace`
- Scale (px): 12 · 14 · 16 · 20 · 24 · 32 · 48 · 64
- Line-height: 1.5 for body, 1.2 for headings
- Letter-spacing: -0.01em on display sizes ≥32px

## Component Stylings
- **Buttons:** 8px radius, 10px padding-block, 16px padding-inline. Primary = cobalt fill, white label. Secondary = 1px border, transparent fill.
- **Cards:** white, 1px border, 12px radius, 20px internal padding, no shadow by default.
- **Inputs:** 1px border, 8px radius, 10px vertical padding, cobalt border on focus.
- **Links:** cobalt, no underline, underline on hover.

## Layout Principles
- 12-column grid, 1200px max-width, 24px gutters.
- Hero: 40–60vh. Content top-biased, never centered vertically.
- Sections: 80px top+bottom spacing desktop, 48px tablet, 32px phone.
- Use whitespace as the main separator. Dividers only between unrelated top-level sections.

## Depth & Elevation
Two levels only:
- **Flat (0):** default.
- **Raised (1):** dropdowns, modals, floating buttons. 2px y-offset, 8px blur, foreground at 8% opacity.
No neumorphism, no glassmorphism.

## Do's and Don'ts
- ✅ Let whitespace do the work.
- ✅ One accent element per screen.
- ✅ Sentence-case headings by default; title case only for brand names.
- ❌ No gradients (except the accent → accent-at-80% on a hero, sparingly).
- ❌ No drop shadows on inputs.
- ❌ No more than three type sizes on one screen.

## Responsive Behavior
- **Desktop ≥ 1024px:** 12-col grid.
- **Tablet 640–1023px:** 8-col grid, 16px gutters.
- **Phone < 640px:** 4-col grid, 12px gutters; hero drops to 40vh.

## Agent Prompt Guide
- When in doubt, subtract. Fewer boxes, less chrome, more space.
- Use the accent color sparingly — at most one hero accent and one CTA accent per screen.
- Do not invent hex values outside this palette. If the request needs one, surface a warning comment in the artifact and use the closest existing token.


## Machine-readable tokens (paste verbatim into `:root`)
```css
:root {
  --bg: #fafafa;
  --surface: #ffffff;
  --surface-warm: var(--surface);
  --fg: #111111;
  --fg-2: var(--fg);
  --muted: #6b6b6b;
  --meta: var(--muted);
  --border: #e5e5e5;
  --border-soft: var(--border);
  --accent: #2f6feb;
  --accent-on: #ffffff;
  --accent-hover: color-mix(in oklab, var(--accent), black 8%);
  --accent-active: color-mix(in oklab, var(--accent), black 14%);
  --success: #17a34a;
  --warn: #eab308;
  --danger: #dc2626;
  --font-display: "Inter", -apple-system, system-ui, sans-serif;
  --font-body: "Inter", -apple-system, system-ui, sans-serif;
  --font-mono: ui-monospace, "JetBrains Mono", monospace;
  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 16px;
  --text-lg: 20px;
  --text-xl: 24px;
  --text-2xl: 32px;
  --text-3xl: 48px;
  --text-4xl: 64px;
  --leading-body: 1.5;
  --leading-tight: 1.2;
  --tracking-display: -0.01em;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --space-20: 80px;
  --section-y-desktop: 80px;
  --section-y-tablet: 48px;
  --section-y-phone: 32px;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-pill: 9999px;
  --elev-flat: none;
  --elev-ring: 0 0 0 1px var(--border);
  --elev-raised: 0 2px 8px color-mix(in oklab, var(--fg), transparent 92%);
  --focus-ring: 0 0 0 3px color-mix(in oklab, var(--accent), transparent 70%);
  --motion-fast: 150ms;
  --motion-base: 200ms;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --container-max: 1200px;
  --container-gutter-desktop: 24px;
  --container-gutter-tablet: 16px;
  --container-gutter-phone: 12px;
}
```
