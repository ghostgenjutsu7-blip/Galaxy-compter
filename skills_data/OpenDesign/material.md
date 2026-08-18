---
name: Design System: material
source: OpenDesign
version: 1.0.0
description: Category: Professional & Corporate
tags: ["design-system", "material"]
triggers: ["material"]
license: Apache-2.0
target_agent: design
category: design_system
---

# Design System Inspired by Material

> Category: Professional & Corporate
> Google's Material Design with layered surfaces, dynamic theming, built-in motion, and responsive cross-platform patterns.

## 1. Visual Theme & Atmosphere

Google's Material Design with layered surfaces, dynamic theming, built-in motion, and responsive cross-platform patterns.

- **Visual style:** modern, minimal, clean
- **Color stance:** primary, secondary, neutral, success, warning, danger
- **Design intent:** Keep outputs recognizable to this style family while preserving usability and readability.

## 2. Color

- **Primary:** `#6442D6` — Token from style foundations.
- **Secondary:** `#C8B3FD` — Token from style foundations.
- **Success:** `#16A34A` — Token from style foundations.
- **Warning:** `#D97706` — Token from style foundations.
- **Danger:** `#DC2626` — Token from style foundations.
- **Surface:** `#FFFFFF` — Token from style foundations.
- **Text:** `#111827` — Token from style foundations.
- **Neutral:** `#FFFFFF` — Derived from the surface token for official format compatibility.

- Favor Primary (#6442D6) for CTA emphasis.
- Use Surface (#FFFFFF) for large backgrounds and cards.
- Keep body copy on Text (#111827) for legibility.

## 3. Typography

- **Scale:** 12/14/16/20/24/32
- **Families:** primary=Inter, display=Roboto, mono=Fira Code
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

- Buttons: primary action uses `#6442D6`; secondary actions stay neutral.
- Inputs: strong focus-visible states, clear labels, and predictable error messaging.
- Cards/sections: use consistent radii, spacing, and elevation strategy across the page.

## 7. Motion & Interaction

- Use subtle transitions that emphasize Primary (#6442D6) as the interaction signal.
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
  --bg: #f8fafd;
  --surface: #ffffff;
  --surface-warm: #e8f0fe;
  --fg: #202124;
  --fg-2: #3c4043;
  --muted: #5f6368;
  --meta: #1a73e8;
  --border: #dadce0;
  --border-soft: #edf0f2;
  --accent: #1a73e8;
  --accent-on: #ffffff;
  --accent-hover: color-mix(in oklab, var(--accent), black 8%);
  --accent-active: color-mix(in oklab, var(--accent), black 14%);
  --success: #188038;
  --warn: #f9ab00;
  --danger: #d93025;
  --font-display: "Google Sans", Roboto, Arial, sans-serif;
  --font-body: Roboto, Arial, sans-serif;
  --font-mono: "Roboto Mono", ui-monospace, Menlo, monospace;
  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 16px;
  --text-lg: 18px;
  --text-xl: 24px;
  --text-2xl: 32px;
  --text-3xl: 48px;
  --text-4xl: 64px;
  --leading-body: 1.5;
  --leading-tight: 1.12;
  --tracking-display: 0;
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
  --radius-sm: 4px;
  --radius-md: 12px;
  --radius-lg: 24px;
  --radius-pill: 9999px;
  --elev-flat: none;
  --elev-ring: 0 0 0 1px var(--border);
  --elev-raised: 0 3px 8px rgba(60, 64, 67, 0.18);
  --focus-ring: 0 0 0 4px rgba(26, 115, 232, 0.24);
  --motion-fast: 150ms;
  --motion-base: 250ms;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --container-max: 1200px;
  --container-gutter-desktop: 36px;
  --container-gutter-tablet: 24px;
  --container-gutter-phone: 16px;
}
```
