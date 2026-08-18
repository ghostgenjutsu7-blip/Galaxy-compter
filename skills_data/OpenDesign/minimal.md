---
name: Design System: minimal
source: OpenDesign
version: 1.0.0
description: Category: Modern & Minimal
tags: ["design-system", "minimal"]
triggers: ["minimal"]
license: Apache-2.0
target_agent: design
category: design_system
---

# Design System Inspired by Minimal

> Category: Modern & Minimal
> Stripped-back design emphasizing whitespace, clean typography, and restrained color for maximum clarity and focus.

## 1. Visual Theme & Atmosphere

Stripped-back design emphasizing whitespace, clean typography, and restrained color for maximum clarity and focus.

- **Visual style:** minimal, clean, bold
- **Color stance:** primary, neutral, success, warning, danger
- **Design intent:** Keep outputs recognizable to this style family while preserving usability and readability.

## 2. Color

- **Primary:** `#0C0C09` — Token from style foundations.
- **Secondary:** `#312C85` — Token from style foundations.
- **Success:** `#16A34A` — Token from style foundations.
- **Warning:** `#D97706` — Token from style foundations.
- **Danger:** `#DC2626` — Token from style foundations.
- **Surface:** `#F4F4F1` — Token from style foundations.
- **Text:** `#0C0C09` — Token from style foundations.
- **Neutral:** `#F4F4F1` — Derived from the surface token for official format compatibility.

- Favor Primary (#0C0C09) for CTA emphasis.
- Use Surface (#F4F4F1) for large backgrounds and cards.
- Keep body copy on Text (#0C0C09) for legibility.

## 3. Typography

- **Scale:** desktop-first expressive scale
- **Families:** primary=Open Sans, display=Inter, mono=Inconsolata
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

- Buttons: primary action uses `#0C0C09`; secondary actions stay neutral.
- Inputs: strong focus-visible states, clear labels, and predictable error messaging.
- Cards/sections: use consistent radii, spacing, and elevation strategy across the page.

## 7. Motion & Interaction

- Use subtle transitions that emphasize Primary (#0C0C09) as the interaction signal.
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
  --surface: #fafafa;
  --surface-warm: #f5f5f5;
  --fg: #111111;
  --fg-2: #3a3a3a;
  --muted: #777777;
  --meta: #111111;
  --border: #e2e2e2;
  --border-soft: #eeeeee;
  --accent: #111111;
  --accent-on: #ffffff;
  --accent-hover: color-mix(in oklab, var(--accent), black 8%);
  --accent-active: color-mix(in oklab, var(--accent), black 14%);
  --success: #168a46;
  --warn: #b7791f;
  --danger: #c53030;
  --font-display: Inter, system-ui, sans-serif;
  --font-body: Inter, system-ui, sans-serif;
  --font-mono: "SF Mono", ui-monospace, Menlo, monospace;
  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 16px;
  --text-lg: 18px;
  --text-xl: 22px;
  --text-2xl: 32px;
  --text-3xl: 48px;
  --text-4xl: 64px;
  --leading-body: 1.55;
  --leading-tight: 1.08;
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
  --radius-sm: 2px;
  --radius-md: 4px;
  --radius-lg: 8px;
  --radius-pill: 9999px;
  --elev-flat: none;
  --elev-ring: 0 0 0 1px var(--border);
  --elev-raised: 0 12px 30px rgba(0, 0, 0, 0.08);
  --focus-ring: 0 0 0 3px rgba(17, 17, 17, 0.18);
  --motion-fast: 140ms;
  --motion-base: 220ms;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --container-max: 1120px;
  --container-gutter-desktop: 36px;
  --container-gutter-tablet: 24px;
  --container-gutter-phone: 16px;
}
```
