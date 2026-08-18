---
name: Design System: modern
source: OpenDesign
version: 1.0.0
description: Category: Modern & Minimal
tags: ["design-system", "modern"]
triggers: ["modern"]
license: Apache-2.0
target_agent: design
category: design_system
---

# Design System Inspired by Modern

> Category: Modern & Minimal
> Contemporary editorial style with serif typography, minimal palettes, and clean layouts for polished digital products.

## 1. Visual Theme & Atmosphere

Contemporary editorial style with serif typography, minimal palettes, and clean layouts for polished digital products.

- **Visual style:** modern, minimal, clean, editorial
- **Color stance:** primary, secondary
- **Design intent:** Keep outputs recognizable to this style family while preserving usability and readability.

## 2. Color

- **Primary:** `#553F83` — Token from style foundations.
- **Secondary:** `#111111` — Token from style foundations.
- **Success:** `#16A34A` — Token from style foundations.
- **Warning:** `#D97706` — Token from style foundations.
- **Danger:** `#DC2626` — Token from style foundations.
- **Surface:** `#553F83` — Token from style foundations.
- **Text:** `#FFFFFF` — Token from style foundations.
- **Neutral:** `#553F83` — Derived from the surface token for official format compatibility.

- Favor Primary (#553F83) for CTA emphasis.
- Use Surface (#553F83) for large backgrounds and cards.
- Keep body copy on Text (#FFFFFF) for legibility.

## 3. Typography

- **Scale:** 12/14/16/20/24/32
- **Families:** primary=IBM Plex Serif, display=IBM Plex Serif, mono=JetBrains Mono
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

- Buttons: primary action uses `#553F83`; secondary actions stay neutral.
- Inputs: strong focus-visible states, clear labels, and predictable error messaging.
- Cards/sections: use consistent radii, spacing, and elevation strategy across the page.

## 7. Motion & Interaction

- Use subtle transitions that emphasize Primary (#553F83) as the interaction signal.
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
  --bg: #f7f8fc;
  --surface: #ffffff;
  --surface-warm: #eef1ff;
  --fg: #111827;
  --fg-2: #374151;
  --muted: #6b7280;
  --meta: #4f46e5;
  --border: #dfe3ed;
  --border-soft: #eef1f7;
  --accent: #4f46e5;
  --accent-on: #ffffff;
  --accent-hover: color-mix(in oklab, var(--accent), black 8%);
  --accent-active: color-mix(in oklab, var(--accent), black 14%);
  --success: #10b981;
  --warn: #f59e0b;
  --danger: #ef4444;
  --font-display: Inter, system-ui, sans-serif;
  --font-body: Inter, system-ui, sans-serif;
  --font-mono: "Geist Mono", ui-monospace, Menlo, monospace;
  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 16px;
  --text-lg: 18px;
  --text-xl: 24px;
  --text-2xl: 36px;
  --text-3xl: 54px;
  --text-4xl: 76px;
  --leading-body: 1.52;
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
  --radius-sm: 10px;
  --radius-md: 16px;
  --radius-lg: 24px;
  --radius-pill: 9999px;
  --elev-flat: none;
  --elev-ring: 0 0 0 1px var(--border);
  --elev-raised: 0 22px 58px rgba(17, 24, 39, 0.11);
  --focus-ring: 0 0 0 4px rgba(79, 70, 229, 0.24);
  --motion-fast: 150ms;
  --motion-base: 240ms;
  --ease-standard: cubic-bezier(0.22, 1, 0.36, 1);
  --container-max: 1180px;
  --container-gutter-desktop: 36px;
  --container-gutter-tablet: 24px;
  --container-gutter-phone: 16px;
}
```
