---
name: Design System: glassmorphism
source: OpenDesign
version: 1.0.0
description: Category: Morphism & Effects
tags: ["design-system", "glassmorphism"]
triggers: ["glassmorphism"]
license: Apache-2.0
target_agent: design
category: design_system
---

# Design System Inspired by Glassmorphism

> Category: Morphism & Effects
> Frosted glass effect with translucent layers, subtle blur, and luminous borders for depth and modern elegance.

## 1. Visual Theme & Atmosphere

Frosted glass effect with translucent layers, subtle blur, and luminous borders for depth and modern elegance.

- **Visual style:** clean, high-contrast, bold, enterprise, liquidglass effect, glassmorphism
- **Color stance:** primary, neutral, success, warning, danger, info, surface/subtle layers
- **Design intent:** Keep outputs recognizable to this style family while preserving usability and readability.

## 2. Color

- **Primary:** `#1856FF` — Token from style foundations.
- **Secondary:** `#3A344E` — Token from style foundations.
- **Success:** `#07CA6B` — Token from style foundations.
- **Warning:** `#E89558` — Token from style foundations.
- **Danger:** `#EA2143` — Token from style foundations.
- **Surface:** `#FFFFFF` — Token from style foundations.
- **Text:** `#141414` — Token from style foundations.
- **Neutral:** `#FFFFFF` — Derived from the surface token for official format compatibility.

- Favor Primary (#1856FF) for CTA emphasis.
- Use Surface (#FFFFFF) for large backgrounds and cards.
- Keep body copy on Text (#141414) for legibility.

## 3. Typography

- **Scale:** mobile-first compact scale
- **Families:** primary=Plus Jakarta Sans, display=Plus Jakarta Sans, mono=JetBrains Mono
- **Weights:** 100, 200, 300, 400, 500, 600, 700, 800, 900
- Headings should carry the style personality; body text should optimize scanability and contrast.

## 4. Spacing & Grid

- **Spacing scale:** comfortable density mode
- Keep vertical rhythm consistent across sections and components.
- Align columns and modules to a predictable grid; avoid ad-hoc offsets.

## 5. Layout & Composition

- Prefer clear content blocks with consistent internal padding.
- Keep hierarchy obvious: headline → support text → primary action.
- Use whitespace to separate concerns before adding borders or shadows.

## 6. Components

- Buttons: primary action uses `#1856FF`; secondary actions stay neutral.
- Inputs: strong focus-visible states, clear labels, and predictable error messaging.
- Cards/sections: use consistent radii, spacing, and elevation strategy across the page.

## 7. Motion & Interaction

- Use subtle transitions that emphasize Primary (#1856FF) as the interaction signal.
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
  --bg: #eef6ff;
  --surface: rgba(255, 255, 255, 0.74);
  --surface-warm: rgba(238, 246, 255, 0.72);
  --fg: #102033;
  --fg-2: #34465f;
  --muted: #60708a;
  --meta: #4f8cff;
  --border: rgba(255, 255, 255, 0.64);
  --border-soft: rgba(255, 255, 255, 0.38);
  --accent: #4f8cff;
  --accent-on: #ffffff;
  --accent-hover: color-mix(in oklab, var(--accent), black 8%);
  --accent-active: color-mix(in oklab, var(--accent), black 14%);
  --success: #22c55e;
  --warn: #f59e0b;
  --danger: #ef4444;
  --font-display: Inter, system-ui, sans-serif;
  --font-body: Inter, system-ui, sans-serif;
  --font-mono: "SF Mono", ui-monospace, Menlo, monospace;
  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 16px;
  --text-lg: 18px;
  --text-xl: 24px;
  --text-2xl: 36px;
  --text-3xl: 54px;
  --text-4xl: 76px;
  --leading-body: 1.55;
  --leading-tight: 1.04;
  --tracking-display: -0.025em;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --section-y-desktop: 104px;
  --section-y-tablet: 72px;
  --section-y-phone: 52px;
  --radius-sm: 16px;
  --radius-md: 24px;
  --radius-lg: 36px;
  --radius-pill: 9999px;
  --elev-flat: none;
  --elev-ring: 0 0 0 1px var(--border);
  --elev-raised: 0 24px 80px rgba(79, 140, 255, 0.18);
  --focus-ring: 0 0 0 4px rgba(79, 140, 255, 0.28);
  --motion-fast: 180ms;
  --motion-base: 280ms;
  --ease-standard: cubic-bezier(0.22, 1, 0.36, 1);
  --container-max: 1180px;
  --container-gutter-desktop: 36px;
  --container-gutter-tablet: 24px;
  --container-gutter-phone: 16px;
}
```
