---
name: Design System: mono
source: OpenDesign
version: 1.0.0
description: Category: Modern & Minimal
tags: ["design-system", "mono"]
triggers: ["mono"]
license: Apache-2.0
target_agent: design
category: design_system
---

# Design System Inspired by Mono

> Category: Modern & Minimal
> Monospace-driven, matrix-inspired design with high-contrast elements, compact density, and a hacker-chic aesthetic.

## 1. Visual Theme & Atmosphere

Monospace-driven, matrix-inspired design with high-contrast elements, compact density, and a hacker-chic aesthetic.

- **Visual style:** minimal, clean, high-contrast, playful, matrix
- **Color stance:** primary, secondary, success, warning, danger, info
- **Design intent:** Keep outputs recognizable to this style family while preserving usability and readability.

## 2. Color

- **Primary:** `#37F712` — Token from style foundations.
- **Secondary:** `#00A6F4` — Token from style foundations.
- **Success:** `#00A63D` — Token from style foundations.
- **Warning:** `#FE9900` — Token from style foundations.
- **Danger:** `#FF2157` — Token from style foundations.
- **Surface:** `#E7E5E4` — Token from style foundations.
- **Text:** `#78716B` — Token from style foundations.
- **Neutral:** `#E7E5E4` — Derived from the surface token for official format compatibility.

- Favor Primary (#37F712) for CTA emphasis.
- Use Surface (#E7E5E4) for large backgrounds and cards.
- Keep body copy on Text (#78716B) for legibility.

## 3. Typography

- **Scale:** desktop-first expressive scale
- **Families:** primary=Space Mono, display=Space Mono, mono=JetBrains Mono
- **Weights:** 100, 200, 300, 400, 500, 600, 700, 800, 900
- Headings should carry the style personality; body text should optimize scanability and contrast.

## 4. Spacing & Grid

- **Spacing scale:** compact density mode
- Keep vertical rhythm consistent across sections and components.
- Align columns and modules to a predictable grid; avoid ad-hoc offsets.

## 5. Layout & Composition

- Prefer clear content blocks with consistent internal padding.
- Keep hierarchy obvious: headline → support text → primary action.
- Use whitespace to separate concerns before adding borders or shadows.

## 6. Components

- Buttons: primary action uses `#37F712`; secondary actions stay neutral.
- Inputs: strong focus-visible states, clear labels, and predictable error messaging.
- Cards/sections: use consistent radii, spacing, and elevation strategy across the page.

## 7. Motion & Interaction

- Use subtle transitions that emphasize Primary (#37F712) as the interaction signal.
- Default to short, purposeful transitions (150–250ms) with stable easing.
- Ensure hover, focus-visible, active, disabled, and loading states are explicit.

## 8. Voice & Brand

- Tone should reflect the visual style: concise, confident, and product-specific.
- Keep microcopy action-oriented and avoid generic filler language.
- Preserve the style identity in headlines while keeping UI labels literal and clear.

## 9. Anti-patterns

- Do not introduce off-palette colors when an existing token can solve the problem.
- Do not flatten hierarchy by using the same type size/weight for all text.
- Do not add decorative effects that reduce readability or accessibility.
- Do not mix unrelated visual metaphors in the same interface.


## Machine-readable tokens (paste verbatim into `:root`)
```css
:root {
  --bg: #ffffff;
  --surface: #f7f7f7;
  --surface-warm: #eeeeee;
  --fg: #111111;
  --fg-2: #3a3a3a;
  --muted: #707070;
  --meta: #111111;
  --border: #d9d9d9;
  --border-soft: #eeeeee;
  --accent: #111111;
  --accent-on: #ffffff;
  --accent-hover: color-mix(in oklab, var(--accent), black 8%);
  --accent-active: color-mix(in oklab, var(--accent), black 14%);
  --success: #168a46;
  --warn: #b7791f;
  --danger: #c53030;
  --font-display: "IBM Plex Mono", ui-monospace, monospace;
  --font-body: "IBM Plex Mono", ui-monospace, monospace;
  --font-mono: "IBM Plex Mono", ui-monospace, monospace;
  --text-xs: 11px;
  --text-sm: 12px;
  --text-base: 14px;
  --text-lg: 16px;
  --text-xl: 20px;
  --text-2xl: 28px;
  --text-3xl: 40px;
  --text-4xl: 56px;
  --leading-body: 1.45;
  --leading-tight: 1.06;
  --tracking-display: -0.025em;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --section-y-desktop: 80px;
  --section-y-tablet: 60px;
  --section-y-phone: 42px;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-pill: 9999px;
  --elev-flat: none;
  --elev-ring: 0 0 0 1px var(--border);
  --elev-raised: 0 16px 40px rgba(0, 0, 0, 0.10);
  --focus-ring: 0 0 0 3px rgba(17, 17, 17, 0.18);
  --motion-fast: 100ms;
  --motion-base: 180ms;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --container-max: 1280px;
  --container-gutter-desktop: 36px;
  --container-gutter-tablet: 24px;
  --container-gutter-phone: 16px;
}
```
