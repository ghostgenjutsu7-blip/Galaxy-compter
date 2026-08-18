---
name: Design System: premium
source: OpenDesign
version: 1.0.0
description: Category: Professional & Corporate
tags: ["design-system", "premium"]
triggers: ["premium"]
license: Apache-2.0
target_agent: design
category: design_system
---

# Design System Inspired by Premium

> Category: Professional & Corporate
> Apple-inspired premium aesthetic with precise spacing, modern typography, and a refined, polished visual language.

## 1. Visual Theme & Atmosphere

Apple-inspired premium aesthetic with precise spacing, modern typography, and a refined, polished visual language.

- **Visual style:** modern
- **Color stance:** primary, neutral, success, warning, danger
- **Design intent:** Keep outputs recognizable to this style family while preserving usability and readability.

## 2. Color

- **Primary:** `#3B82F6` — Token from style foundations.
- **Secondary:** `#8B5CF6` — Token from style foundations.
- **Success:** `#16A34A` — Token from style foundations.
- **Warning:** `#D97706` — Token from style foundations.
- **Danger:** `#DC2626` — Token from style foundations.
- **Surface:** `#FFFFFF` — Token from style foundations.
- **Text:** `#111827` — Token from style foundations.
- **Neutral:** `#FFFFFF` — Derived from the surface token for official format compatibility.

- Favor Primary (#3B82F6) for CTA emphasis.
- Use Surface (#FFFFFF) for large backgrounds and cards.
- Keep body copy on Text (#111827) for legibility.

## 3. Typography

- **Scale:** 12/14/16/18/24/30/36
- **Families:** primary=Inter, display=Inter, mono=JetBrains Mono
- **Weights:** 100, 200, 300, 400, 500, 600, 700, 800, 900
- Headings should carry the style personality; body text should optimize scanability and contrast.

## 4. Spacing & Grid

- **Spacing scale:** 4/8/12/16/24/32
- Keep vertical rhythm consistent across sections and components.
- Align columns and modules to a predictable grid; avoid ad-hoc offsets.

## 5. Layout & Composition

- Prefer clear content blocks with consistent internal padding.
- Keep hierarchy obvious: headline → support text → primary action.
- Use whitespace to separate concerns before adding borders or shadows.

## 6. Components

- Buttons: primary action uses `#3B82F6`; secondary actions stay neutral.
- Inputs: strong focus-visible states, clear labels, and predictable error messaging.
- Cards/sections: use consistent radii, spacing, and elevation strategy across the page.

## 7. Motion & Interaction

- Use subtle transitions that emphasize Primary (#3B82F6) as the interaction signal.
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
  --bg: #faf8f4;
  --surface: #ffffff;
  --surface-warm: #f0e7d8;
  --fg: #1c1b19;
  --fg-2: #4b4740;
  --muted: #746d63;
  --meta: #a06a3b;
  --border: #ded6c9;
  --border-soft: #eee7dc;
  --accent: #a06a3b;
  --accent-on: #ffffff;
  --accent-hover: color-mix(in oklab, var(--accent), black 8%);
  --accent-active: color-mix(in oklab, var(--accent), black 14%);
  --success: #3f8f5f;
  --warn: #c4872c;
  --danger: #b84a4a;
  --font-display: "Canela", Georgia, serif;
  --font-body: Inter, system-ui, sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 16px;
  --text-lg: 19px;
  --text-xl: 26px;
  --text-2xl: 40px;
  --text-3xl: 60px;
  --text-4xl: 84px;
  --leading-body: 1.58;
  --leading-tight: 1.02;
  --tracking-display: -0.02em;
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
  --radius-lg: 28px;
  --radius-pill: 9999px;
  --elev-flat: none;
  --elev-ring: 0 0 0 1px var(--border);
  --elev-raised: 0 24px 64px rgba(28, 27, 25, 0.12);
  --focus-ring: 0 0 0 4px rgba(160, 106, 59, 0.24);
  --motion-fast: 170ms;
  --motion-base: 280ms;
  --ease-standard: cubic-bezier(0.22, 1, 0.36, 1);
  --container-max: 1160px;
  --container-gutter-desktop: 36px;
  --container-gutter-tablet: 24px;
  --container-gutter-phone: 16px;
}
```
