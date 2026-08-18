---
name: Design System: pacman
source: OpenDesign
version: 1.0.0
description: Category: Themed & Unique
tags: ["design-system", "pacman"]
triggers: ["pacman"]
license: Apache-2.0
target_agent: design
category: design_system
---

# Design System Inspired by Pacman

> Category: Themed & Unique
> Retro arcade-inspired design with pixel fonts, dotted borders, playful high-contrast colors, and 8-bit game aesthetics.

## 1. Visual Theme & Atmosphere

Retro arcade-inspired design with pixel fonts, dotted borders, playful high-contrast colors, and 8-bit game aesthetics.

- **Visual style:** high-contrast, playful, dotted borders
- **Color stance:** primary, secondary, success, warning, danger, info, surface/subtle layers
- **Design intent:** Keep outputs recognizable to this style family while preserving usability and readability.

## 2. Color

- **Primary:** `#2A3FE5` — Token from style foundations.
- **Secondary:** `#F4B9B0` — Token from style foundations.
- **Success:** `#16A34A` — Token from style foundations.
- **Warning:** `#D97706` — Token from style foundations.
- **Danger:** `#DC2626` — Token from style foundations.
- **Surface:** `#000000` — Token from style foundations.
- **Text:** `#111827` — Token from style foundations.
- **Neutral:** `#000000` — Derived from the surface token for official format compatibility.

- Favor Primary (#2A3FE5) for CTA emphasis.
- Use Surface (#000000) for large backgrounds and cards.
- Keep body copy on Text (#111827) for legibility.

## 3. Typography

- **Scale:** desktop-first expressive scale
- **Families:** primary=Press Start 2P, display=Press Start 2P, mono=Space Mono
- **Weights:** 100, 200, 300, 400, 500, 600, 700, 800, 900
- Headings should carry the style personality; body text should optimize scanability and contrast.

## 4. Spacing & Grid

- **Spacing scale:** 8pt baseline grid
- Keep vertical rhythm consistent across sections and components.
- Align columns and modules to a predictable grid; avoid ad-hoc offsets.

## 5. Layout & Composition

- Prefer clear content blocks with consistent internal padding.
- Keep hierarchy obvious: headline → support text → primary action.
- Use whitespace to separate concerns before adding borders or shadows.

## 6. Components

- Buttons: primary action uses `#2A3FE5`; secondary actions stay neutral.
- Inputs: strong focus-visible states, clear labels, and predictable error messaging.
- Cards/sections: use consistent radii, spacing, and elevation strategy across the page.

## 7. Motion & Interaction

- Use subtle transitions that emphasize Primary (#2A3FE5) as the interaction signal.
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
  --bg: #050505;
  --surface: #101014;
  --surface-warm: #1f1b08;
  --fg: #fff7d6;
  --fg-2: #f6e79c;
  --muted: #b9a85d;
  --meta: #ffcc00;
  --border: #2338ff;
  --border-soft: #17218a;
  --accent: #ffcc00;
  --accent-on: #050505;
  --accent-hover: color-mix(in oklab, var(--accent), black 8%);
  --accent-active: color-mix(in oklab, var(--accent), black 14%);
  --success: #00ff66;
  --warn: #ff9900;
  --danger: #ff3b3b;
  --font-display: "Press Start 2P", "Arial Black", system-ui, sans-serif;
  --font-body: "Inter", system-ui, sans-serif;
  --font-mono: "Press Start 2P", ui-monospace, monospace;
  --text-xs: 10px;
  --text-sm: 12px;
  --text-base: 14px;
  --text-lg: 16px;
  --text-xl: 20px;
  --text-2xl: 30px;
  --text-3xl: 44px;
  --text-4xl: 64px;
  --leading-body: 1.6;
  --leading-tight: 1.08;
  --tracking-display: 0;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --section-y-desktop: 84px;
  --section-y-tablet: 60px;
  --section-y-phone: 44px;
  --radius-sm: 10px;
  --radius-md: 18px;
  --radius-lg: 9999px;
  --radius-pill: 9999px;
  --elev-flat: none;
  --elev-ring: 0 0 0 1px var(--border);
  --elev-raised: 0 0 0 2px #2338ff, 0 22px 60px rgba(0, 0, 0, 0.46);
  --focus-ring: 0 0 0 4px rgba(255, 204, 0, 0.34);
  --motion-fast: 90ms;
  --motion-base: 160ms;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --container-max: 1080px;
  --container-gutter-desktop: 32px;
  --container-gutter-tablet: 24px;
  --container-gutter-phone: 16px;
}
```
