---
name: Design System: editorial
source: OpenDesign
version: 1.0.0
description: Category: Creative & Artistic
tags: ["design-system", "editorial"]
triggers: ["editorial"]
license: Apache-2.0
target_agent: design
category: design_system
---

# Design System Inspired by Editorial

> Category: Creative & Artistic
> Magazine-inspired editorial layout with refined serif typography, structured grids, and elegant reading experiences.

## 1. Visual Theme & Atmosphere

Magazine-inspired editorial layout with refined serif typography, structured grids, and elegant reading experiences.

- **Visual style:** modern, editorial
- **Color stance:** primary, secondary, neutral, success
- **Design intent:** Keep outputs recognizable to this style family while preserving usability and readability.

## 2. Color

- **Primary:** `#111111` — Token from style foundations.
- **Secondary:** `#F1F1F1` — Token from style foundations.
- **Success:** `#16A34A` — Token from style foundations.
- **Warning:** `#D97706` — Token from style foundations.
- **Danger:** `#DC2626` — Token from style foundations.
- **Surface:** `#FFFFFF` — Token from style foundations.
- **Text:** `#111827` — Token from style foundations.
- **Neutral:** `#FFFFFF` — Derived from the surface token for official format compatibility.

- Favor Primary (#111111) for CTA emphasis.
- Use Surface (#FFFFFF) for large backgrounds and cards.
- Keep body copy on Text (#111827) for legibility.

## 3. Typography

- **Scale:** 14/16/18/24/32/40
- **Families:** primary=Gelasio, display=Gelasio, mono=Ubuntu Mono
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

- Buttons: primary action uses `#111111`; secondary actions stay neutral.
- Inputs: strong focus-visible states, clear labels, and predictable error messaging.
- Cards/sections: use consistent radii, spacing, and elevation strategy across the page.

## 7. Motion & Interaction

- Use subtle transitions that emphasize Primary (#111111) as the interaction signal.
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
  --bg: #fbf7f0;
  --surface: #fffdf8;
  --surface-warm: #f1e6d6;
  --fg: #1f1a16;
  --fg-2: #4b4038;
  --muted: #7d7168;
  --meta: #9a5a2f;
  --border: #ded3c5;
  --border-soft: #eee5da;
  --accent: #9a5a2f;
  --accent-on: #ffffff;
  --accent-hover: color-mix(in oklab, var(--accent), black 8%);
  --accent-active: color-mix(in oklab, var(--accent), black 14%);
  --success: #4f8a4f;
  --warn: #c9822f;
  --danger: #b33a3a;
  --font-display: Georgia, "Times New Roman", serif;
  --font-body: "Source Serif Pro", Georgia, serif;
  --font-mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 18px;
  --text-lg: 21px;
  --text-xl: 30px;
  --text-2xl: 44px;
  --text-3xl: 66px;
  --text-4xl: 92px;
  --leading-body: 1.65;
  --leading-tight: 1;
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
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-pill: 9999px;
  --elev-flat: none;
  --elev-ring: 0 0 0 1px var(--border);
  --elev-raised: 0 20px 50px rgba(31, 26, 22, 0.12);
  --focus-ring: 0 0 0 4px rgba(154, 90, 47, 0.24);
  --motion-fast: 180ms;
  --motion-base: 280ms;
  --ease-standard: cubic-bezier(0.22, 1, 0.36, 1);
  --container-max: 1120px;
  --container-gutter-desktop: 36px;
  --container-gutter-tablet: 24px;
  --container-gutter-phone: 16px;
}
```
