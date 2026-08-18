---
name: Design System: tetris
source: OpenDesign
version: 1.0.0
description: Category: Themed & Unique
tags: ["design-system", "tetris"]
triggers: ["tetris"]
license: Apache-2.0
target_agent: design
category: design_system
---

# Design System Inspired by Tetris

> Category: Themed & Unique
> Classic block-game inspired design with playful colors, bold display fonts, and compact, high-energy layouts.

## 1. Visual Theme & Atmosphere

Classic block-game inspired design with playful colors, bold display fonts, and compact, high-energy layouts.

- **Visual style:** high-contrast, playful, premium
- **Color stance:** primary, secondary, success, warning, danger, info
- **Design intent:** Keep outputs recognizable to this style family while preserving usability and readability.

## 2. Color

- **Primary:** `#1C202B` — Token from style foundations.
- **Secondary:** `#7107E7` — Token from style foundations.
- **Success:** `#16A34A` — Token from style foundations.
- **Warning:** `#D97706` — Token from style foundations.
- **Danger:** `#DC2626` — Token from style foundations.
- **Surface:** `#DFE7FF` — Token from style foundations.
- **Text:** `#1C398E` — Token from style foundations.
- **Neutral:** `#DFE7FF` — Derived from the surface token for official format compatibility.

- Favor Primary (#1C202B) for CTA emphasis.
- Use Surface (#DFE7FF) for large backgrounds and cards.
- Keep body copy on Text (#1C398E) for legibility.

## 3. Typography

- **Scale:** desktop-first expressive scale
- **Families:** primary=Bangers, display=Bangers, mono=JetBrains Mono
- **Weights:** 100, 200, 300, 400, 500, 600, 700, 800, 900
- Headings should carry the style personality; body text should optimize scanability and contrast.

## 4. Spacing & Grid

- **Spacing scale:** compact density mode
- Keep vertical rhythm consistent across sections and components.
- Align columns and modules to a predictable grid; avoid ad-hoc offsets.

## 5. Layout & Composition

- Prefer clear content blocks with consistent internal padding.
- Keep hierarchy obvious: headline → support text → primary action.
- Use whitespace to separate concerns before adding borders or shadows.

## 6. Components

- Buttons: primary action uses `#1C202B`; secondary actions stay neutral.
- Inputs: strong focus-visible states, clear labels, and predictable error messaging.
- Cards/sections: use consistent radii, spacing, and elevation strategy across the page.

## 7. Motion & Interaction

- Use subtle transitions that emphasize Primary (#1C202B) as the interaction signal.
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
  --bg: #050816;
  --surface: #10162a;
  --surface-warm: #17203a;
  --fg: #f8fafc;
  --fg-2: #cbd5e1;
  --muted: #94a3b8;
  --meta: #00f0f0;
  --border: #26324f;
  --border-soft: #1c2740;
  --accent: #00f0f0;
  --accent-on: #061018;
  --accent-hover: color-mix(in oklab, var(--accent), black 8%);
  --accent-active: color-mix(in oklab, var(--accent), black 14%);
  --success: #00f000;
  --warn: #f0f000;
  --danger: #f00000;
  --font-display: "Press Start 2P", "Arial Black", system-ui, sans-serif;
  --font-body: "Inter", system-ui, sans-serif;
  --font-mono: "Press Start 2P", ui-monospace, monospace;
  --text-xs: 10px;
  --text-sm: 12px;
  --text-base: 14px;
  --text-lg: 16px;
  --text-xl: 20px;
  --text-2xl: 28px;
  --text-3xl: 40px;
  --text-4xl: 56px;
  --leading-body: 1.6;
  --leading-tight: 1.1;
  --tracking-display: 0;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --section-y-desktop: 80px;
  --section-y-tablet: 60px;
  --section-y-phone: 44px;
  --radius-sm: 0px;
  --radius-md: 0px;
  --radius-lg: 4px;
  --radius-pill: 9999px;
  --elev-flat: none;
  --elev-ring: 0 0 0 1px var(--border);
  --elev-raised: 0 18px 0 rgba(0, 0, 0, 0.32);
  --focus-ring: 0 0 0 4px rgba(0, 240, 240, 0.32);
  --motion-fast: 80ms;
  --motion-base: 140ms;
  --ease-standard: steps(2, end);
  --container-max: 1100px;
  --container-gutter-desktop: 32px;
  --container-gutter-tablet: 24px;
  --container-gutter-phone: 16px;
}
```
