---
name: Design System: publication
source: OpenDesign
version: 1.0.0
description: Category: Creative & Artistic
tags: ["design-system", "publication"]
triggers: ["publication"]
license: Apache-2.0
target_agent: design
category: design_system
---

# Design System Inspired by Publication

> Category: Creative & Artistic
> Print-inspired visual language for books, magazines, and reports with editorial grids and expressive typography.

## 1. Visual Theme & Atmosphere

Print-inspired visual language for books, magazines, and reports with editorial grids and expressive typography.

- **Visual style:** modern, editorial
- **Color stance:** primary, neutral, success, warning, danger
- **Design intent:** Keep outputs recognizable to this style family while preserving usability and readability.

## 2. Color

- **Primary:** `#A855F7` — Token from style foundations.
- **Secondary:** `#0A1829` — Token from style foundations.
- **Success:** `#16A34A` — Token from style foundations.
- **Warning:** `#D97706` — Token from style foundations.
- **Danger:** `#DC2626` — Token from style foundations.
- **Surface:** `#FFFFFF` — Token from style foundations.
- **Text:** `#0A1829` — Token from style foundations.
- **Neutral:** `#FFFFFF` — Derived from the surface token for official format compatibility.

- Favor Primary (#A855F7) for CTA emphasis.
- Use Surface (#FFFFFF) for large backgrounds and cards.
- Keep body copy on Text (#0A1829) for legibility.

## 3. Typography

- **Scale:** desktop-first expressive scale
- **Families:** primary=Nunito, display=Oswald, mono=JetBrains Mono
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

- Buttons: primary action uses `#A855F7`; secondary actions stay neutral.
- Inputs: strong focus-visible states, clear labels, and predictable error messaging.
- Cards/sections: use consistent radii, spacing, and elevation strategy across the page.

## 7. Motion & Interaction

- Use subtle transitions that emphasize Primary (#A855F7) as the interaction signal.
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
  --surface: #f6f6f6;
  --surface-warm: #fff2f0;
  --fg: #0b0b0b;
  --fg-2: #333333;
  --muted: #666666;
  --meta: #c1121f;
  --border: #d6d6d6;
  --border-soft: #ececec;
  --accent: #c1121f;
  --accent-on: #ffffff;
  --accent-hover: color-mix(in oklab, var(--accent), black 8%);
  --accent-active: color-mix(in oklab, var(--accent), black 14%);
  --success: #0f8a3b;
  --warn: #d99a00;
  --danger: #b00020;
  --font-display: "Franklin Gothic", Arial, sans-serif;
  --font-body: Georgia, "Times New Roman", serif;
  --font-mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 17px;
  --text-lg: 20px;
  --text-xl: 28px;
  --text-2xl: 42px;
  --text-3xl: 64px;
  --text-4xl: 88px;
  --leading-body: 1.58;
  --leading-tight: 0.98;
  --tracking-display: -0.018em;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --section-y-desktop: 88px;
  --section-y-tablet: 64px;
  --section-y-phone: 44px;
  --radius-sm: 0px;
  --radius-md: 0px;
  --radius-lg: 0px;
  --radius-pill: 9999px;
  --elev-flat: none;
  --elev-ring: 0 0 0 1px var(--border);
  --elev-raised: 0 16px 42px rgba(0, 0, 0, 0.12);
  --focus-ring: 0 0 0 4px rgba(193, 18, 31, 0.24);
  --motion-fast: 120ms;
  --motion-base: 200ms;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --container-max: 1180px;
  --container-gutter-desktop: 36px;
  --container-gutter-tablet: 24px;
  --container-gutter-phone: 16px;
}
```
