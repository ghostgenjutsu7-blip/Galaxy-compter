---
name: Design System: brutalism
source: OpenDesign
version: 1.0.0
description: Category: Bold & Expressive
tags: ["design-system", "brutalism"]
triggers: ["brutalism"]
license: Apache-2.0
target_agent: design
category: design_system
---

# Design System Inspired by Brutalism

> Category: Bold & Expressive
> Raw, anti-design aesthetic inspired by concrete architecture with unadorned elements, jarring layouts, and functional minimalism.

## 1. Visual Theme & Atmosphere

Raw, anti-design aesthetic inspired by concrete architecture with unadorned elements, jarring layouts, and functional minimalism.

- **Visual style:** bold
- **Color stance:** primary, secondary, neutral, success, warning, danger
- **Design intent:** Keep outputs recognizable to this style family while preserving usability and readability.

## 2. Color

- **Primary:** `#DD614C` — Token from style foundations.
- **Secondary:** `#DAA144` — Token from style foundations.
- **Success:** `#16A34A` — Token from style foundations.
- **Warning:** `#D97706` — Token from style foundations.
- **Danger:** `#DC2626` — Token from style foundations.
- **Surface:** `#FFFFFF` — Token from style foundations.
- **Text:** `#111827` — Token from style foundations.
- **Neutral:** `#FFFFFF` — Derived from the surface token for official format compatibility.

- Favor Primary (#DD614C) for CTA emphasis.
- Use Surface (#FFFFFF) for large backgrounds and cards.
- Keep body copy on Text (#111827) for legibility.

## 3. Typography

- **Scale:** desktop-first expressive scale
- **Families:** primary=Darker Grotesque, display=Darker Grotesque, mono=JetBrains Mono
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

- Buttons: primary action uses `#DD614C`; secondary actions stay neutral.
- Inputs: strong focus-visible states, clear labels, and predictable error messaging.
- Cards/sections: use consistent radii, spacing, and elevation strategy across the page.

## 7. Motion & Interaction

- Use subtle transitions that emphasize Primary (#DD614C) as the interaction signal.
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
  --bg: #f5f1e8;
  --surface: #ffffff;
  --surface-warm: #ffef5a;
  --fg: #000000;
  --fg-2: #222222;
  --muted: #555555;
  --meta: #000000;
  --border: #000000;
  --border-soft: #000000;
  --accent: #ffef5a;
  --accent-on: #000000;
  --accent-hover: color-mix(in oklab, var(--accent), black 8%);
  --accent-active: color-mix(in oklab, var(--accent), black 14%);
  --success: #00b050;
  --warn: #ff8c00;
  --danger: #ff2b2b;
  --font-display: Arial Black, Impact, sans-serif;
  --font-body: Arial, Helvetica, sans-serif;
  --font-mono: "Courier New", ui-monospace, monospace;
  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 17px;
  --text-lg: 20px;
  --text-xl: 28px;
  --text-2xl: 42px;
  --text-3xl: 64px;
  --text-4xl: 88px;
  --leading-body: 1.35;
  --leading-tight: 0.98;
  --tracking-display: 0;
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
  --elev-raised: 8px 8px 0 #000000;
  --focus-ring: 0 0 0 4px #000000, 0 0 0 8px #ffef5a;
  --motion-fast: 90ms;
  --motion-base: 140ms;
  --ease-standard: steps(2, end);
  --container-max: 1160px;
  --container-gutter-desktop: 36px;
  --container-gutter-tablet: 24px;
  --container-gutter-phone: 16px;
}
```
