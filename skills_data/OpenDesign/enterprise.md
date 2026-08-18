---
name: Design System: enterprise
source: OpenDesign
version: 1.0.0
description: Category: Professional & Corporate
tags: ["design-system", "enterprise"]
triggers: ["enterprise"]
license: Apache-2.0
target_agent: design
category: design_system
---

# Design System Inspired by Enterprise

> Category: Professional & Corporate
> Clean, high-contrast enterprise design for data-driven workflows with intuitive drag-and-drop patterns and structured layouts.

## 1. Visual Theme & Atmosphere

Clean, high-contrast enterprise design for data-driven workflows with intuitive drag-and-drop patterns and structured layouts.

- **Visual style:** clean, high-contrast, enterprise
- **Color stance:** primary, success, warning, danger
- **Design intent:** Keep outputs recognizable to this style family while preserving usability and readability.

## 2. Color

- **Primary:** `#072C2C` — Token from style foundations.
- **Secondary:** `#FF5F03` — Token from style foundations.
- **Success:** `#16A34A` — Token from style foundations.
- **Warning:** `#D97706` — Token from style foundations.
- **Danger:** `#DC2626` — Token from style foundations.
- **Surface:** `#EDEADE` — Token from style foundations.
- **Text:** `#111827` — Token from style foundations.
- **Neutral:** `#EDEADE` — Derived from the surface token for official format compatibility.

- Favor Primary (#072C2C) for CTA emphasis.
- Use Surface (#EDEADE) for large backgrounds and cards.
- Keep body copy on Text (#111827) for legibility.

## 3. Typography

- **Scale:** desktop-first expressive scale
- **Families:** primary=Ubuntu, display=Oswald, mono=Ubuntu Mono
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

- Buttons: primary action uses `#072C2C`; secondary actions stay neutral.
- Inputs: strong focus-visible states, clear labels, and predictable error messaging.
- Cards/sections: use consistent radii, spacing, and elevation strategy across the page.

## 7. Motion & Interaction

- Use subtle transitions that emphasize Primary (#072C2C) as the interaction signal.
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
  --bg: #f8fafc;
  --surface: #ffffff;
  --surface-warm: #eef2f7;
  --fg: #0f172a;
  --fg-2: #334155;
  --muted: #64748b;
  --meta: #1d4ed8;
  --border: #d8dee8;
  --border-soft: #edf1f6;
  --accent: #1d4ed8;
  --accent-on: #ffffff;
  --accent-hover: color-mix(in oklab, var(--accent), black 8%);
  --accent-active: color-mix(in oklab, var(--accent), black 14%);
  --success: #15803d;
  --warn: #b45309;
  --danger: #b91c1c;
  --font-display: Inter, system-ui, sans-serif;
  --font-body: Inter, system-ui, sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 16px;
  --text-lg: 18px;
  --text-xl: 24px;
  --text-2xl: 34px;
  --text-3xl: 48px;
  --text-4xl: 64px;
  --leading-body: 1.52;
  --leading-tight: 1.08;
  --tracking-display: -0.018em;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --section-y-desktop: 96px;
  --section-y-tablet: 68px;
  --section-y-phone: 48px;
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --radius-pill: 9999px;
  --elev-flat: none;
  --elev-ring: 0 0 0 1px var(--border);
  --elev-raised: 0 20px 52px rgba(15, 23, 42, 0.10);
  --focus-ring: 0 0 0 4px rgba(29, 78, 216, 0.22);
  --motion-fast: 150ms;
  --motion-base: 230ms;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --container-max: 1240px;
  --container-gutter-desktop: 36px;
  --container-gutter-tablet: 24px;
  --container-gutter-phone: 16px;
}
```
