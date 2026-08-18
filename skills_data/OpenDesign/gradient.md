---
name: Design System: gradient
source: OpenDesign
version: 1.0.0
description: Category: Morphism & Effects
tags: ["design-system", "gradient"]
triggers: ["gradient"]
license: Apache-2.0
target_agent: design
category: design_system
---

# Design System Inspired by Gradient

> Category: Morphism & Effects
> Smooth color transitions and gradient-rich surfaces for modern, playful interfaces with visual depth.

## 1. Visual Theme & Atmosphere

Smooth color transitions and gradient-rich surfaces for modern, playful interfaces with visual depth.

- **Visual style:** modern, playful
- **Color stance:** primary, secondary, neutral, success, warning, danger
- **Design intent:** Keep outputs recognizable to this style family while preserving usability and readability.

## 2. Color

- **Primary:** `#990FFA` — Token from style foundations.
- **Secondary:** `#E60076` — Token from style foundations.
- **Success:** `#16A34A` — Token from style foundations.
- **Warning:** `#D97706` — Token from style foundations.
- **Danger:** `#DC2626` — Token from style foundations.
- **Surface:** `#FFFFFF` — Token from style foundations.
- **Text:** `#111827` — Token from style foundations.
- **Neutral:** `#FFFFFF` — Derived from the surface token for official format compatibility.

- Favor Primary (#990FFA) for CTA emphasis.
- Use Surface (#FFFFFF) for large backgrounds and cards.
- Keep body copy on Text (#111827) for legibility.

## 3. Typography

- **Scale:** 12/14/16/18/24/30/36
- **Families:** primary=Montserrat, display=Space Grotesk, mono=JetBrains Mono
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

- Buttons: primary action uses `#990FFA`; secondary actions stay neutral.
- Inputs: strong focus-visible states, clear labels, and predictable error messaging.
- Cards/sections: use consistent radii, spacing, and elevation strategy across the page.

## 7. Motion & Interaction

- Use subtle transitions that emphasize Primary (#990FFA) as the interaction signal.
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
  --bg: #f7f3ff;
  --surface: #ffffff;
  --surface-warm: #efe7ff;
  --fg: #191225;
  --fg-2: #443856;
  --muted: #746985;
  --meta: #7c3aed;
  --border: #ddd2f2;
  --border-soft: #eee6fb;
  --accent: #7c3aed;
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
  --text-lg: 19px;
  --text-xl: 26px;
  --text-2xl: 40px;
  --text-3xl: 62px;
  --text-4xl: 86px;
  --leading-body: 1.52;
  --leading-tight: 1.02;
  --tracking-display: -0.03em;
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
  --radius-sm: 12px;
  --radius-md: 20px;
  --radius-lg: 32px;
  --radius-pill: 9999px;
  --elev-flat: none;
  --elev-ring: 0 0 0 1px var(--border);
  --elev-raised: 0 24px 72px rgba(124, 58, 237, 0.20);
  --focus-ring: 0 0 0 4px rgba(124, 58, 237, 0.26);
  --motion-fast: 160ms;
  --motion-base: 260ms;
  --ease-standard: cubic-bezier(0.22, 1, 0.36, 1);
  --container-max: 1180px;
  --container-gutter-desktop: 36px;
  --container-gutter-tablet: 24px;
  --container-gutter-phone: 16px;
}
```
