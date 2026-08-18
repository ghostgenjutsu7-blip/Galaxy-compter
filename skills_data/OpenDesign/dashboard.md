---
name: Design System: dashboard
source: OpenDesign
version: 1.0.0
description: Category: Professional & Corporate
tags: ["design-system", "dashboard"]
triggers: ["dashboard"]
license: Apache-2.0
target_agent: design
category: design_system
---

# Design System Inspired by Dashboard

> Category: Professional & Corporate
> Dark-themed cloud-platform aesthetic with modular grids, glass-like panels, and strong data hierarchy for productivity dashboards.

## 1. Visual Theme & Atmosphere

Dark-themed cloud-platform aesthetic with modular grids, glass-like panels, and strong data hierarchy for productivity dashboards.

- **Visual style:** modern, clean, cloud-platform aesthetic (Heroku/Vercel/GitHub inspired), dark theme, subtle gradients, soft shadows, glass-like panels, rounded components
- **Color stance:** primary, neutral, success, warning, danger
- **Design intent:** Keep outputs recognizable to this style family while preserving usability and readability.

## 2. Color

- **Primary:** `#0C5CAB` — Token from style foundations.
- **Secondary:** `#0A4A8A` — Token from style foundations.
- **Success:** `#10B981` — Token from style foundations.
- **Warning:** `#F59E0B` — Token from style foundations.
- **Danger:** `#EF4444` — Token from style foundations.
- **Surface:** `#09090B` — Token from style foundations.
- **Text:** `#FAFAFA` — Token from style foundations.
- **Neutral:** `#09090B` — Derived from the surface token for official format compatibility.

- Favor Primary (#0C5CAB) for CTA emphasis.
- Use Surface (#09090B) for large backgrounds and cards.
- Keep body copy on Text (#FAFAFA) for legibility.

## 3. Typography

- **Scale:** 12/14/16/20/24/32
- **Families:** primary=IBM Plex Sans, display=IBM Plex Sans, mono=IBM Plex Sans
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

- Buttons: primary action uses `#0C5CAB`; secondary actions stay neutral.
- Inputs: strong focus-visible states, clear labels, and predictable error messaging.
- Cards/sections: use consistent radii, spacing, and elevation strategy across the page.

## 7. Motion & Interaction

- Use subtle transitions that emphasize Primary (#0C5CAB) as the interaction signal.
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
  --bg: #f4f7fb;
  --surface: #ffffff;
  --surface-warm: #eef6ff;
  --fg: #111827;
  --fg-2: #334155;
  --muted: #64748b;
  --meta: #0ea5e9;
  --border: #d8e2ee;
  --border-soft: #edf3f8;
  --accent: #0ea5e9;
  --accent-on: #04131d;
  --accent-hover: color-mix(in oklab, var(--accent), black 8%);
  --accent-active: color-mix(in oklab, var(--accent), black 14%);
  --success: #10b981;
  --warn: #f59e0b;
  --danger: #ef4444;
  --font-display: Inter, system-ui, sans-serif;
  --font-body: Inter, system-ui, sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
  --text-xs: 11px;
  --text-sm: 13px;
  --text-base: 15px;
  --text-lg: 17px;
  --text-xl: 22px;
  --text-2xl: 30px;
  --text-3xl: 42px;
  --text-4xl: 56px;
  --leading-body: 1.48;
  --leading-tight: 1.1;
  --tracking-display: -0.015em;
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
  --section-y-phone: 42px;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 18px;
  --radius-pill: 9999px;
  --elev-flat: none;
  --elev-ring: 0 0 0 1px var(--border);
  --elev-raised: 0 18px 46px rgba(15, 23, 42, 0.10);
  --focus-ring: 0 0 0 4px rgba(14, 165, 233, 0.22);
  --motion-fast: 120ms;
  --motion-base: 200ms;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --container-max: 1280px;
  --container-gutter-desktop: 36px;
  --container-gutter-tablet: 24px;
  --container-gutter-phone: 16px;
}
```
