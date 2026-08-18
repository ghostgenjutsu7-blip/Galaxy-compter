---
name: Design System: application
source: OpenDesign
version: 1.0.0
description: Category: Professional & Corporate
tags: ["design-system", "application"]
triggers: ["application"]
license: Apache-2.0
target_agent: design
category: design_system
---

# Design System Inspired by Application

> Category: Professional & Corporate
> App dashboard with purple-themed aesthetic, top-bar navigation, card-based layouts, and developer-first workflows.

## 1. Visual Theme & Atmosphere

App dashboard with purple-themed aesthetic, top-bar navigation, card-based layouts, and developer-first workflows.

- **Visual style:** modern, clean, high-contrast, glass-like panels, soft shadows, rounded components
- **Color stance:** primary (purple), neutral, success, warning, danger
- **Design intent:** Keep outputs recognizable to this style family while preserving usability and readability.

## 2. Color

- **Primary:** `#9333EA` — Token from style foundations.
- **Secondary:** `#A855F7` — Token from style foundations.
- **Success:** `#10B981` — Token from style foundations.
- **Warning:** `#F59E0B` — Token from style foundations.
- **Danger:** `#EF4444` — Token from style foundations.
- **Surface:** `#FFFFFF` — Token from style foundations.
- **Text:** `#09090B` — Token from style foundations.
- **Neutral:** `#FFFFFF` — Derived from the surface token for official format compatibility.

- Favor Primary (#9333EA) for CTA emphasis.
- Use Surface (#FFFFFF) for large backgrounds and cards.
- Keep body copy on Text (#09090B) for legibility.

## 3. Typography

- **Scale:** 12/14/16/20/24/32
- **Families:** primary=Inter, display=Inter, mono=JetBrains Mono
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

- Buttons: primary action uses `#9333EA`; secondary actions stay neutral.
- Inputs: strong focus-visible states, clear labels, and predictable error messaging.
- Cards/sections: use consistent radii, spacing, and elevation strategy across the page.

## 7. Motion & Interaction

- Use subtle transitions that emphasize Primary (#9333EA) as the interaction signal.
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
  --bg: #f6f7f9;
  --surface: #ffffff;
  --surface-warm: #eef4ff;
  --fg: #172033;
  --fg-2: #3b4658;
  --muted: #6b7689;
  --meta: #2563eb;
  --border: #d8dee8;
  --border-soft: #edf1f6;
  --accent: #2563eb;
  --accent-on: #ffffff;
  --accent-hover: color-mix(in oklab, var(--accent), black 8%);
  --accent-active: color-mix(in oklab, var(--accent), black 14%);
  --success: #16a34a;
  --warn: #f59e0b;
  --danger: #dc2626;
  --font-display: Inter, system-ui, sans-serif;
  --font-body: Inter, system-ui, sans-serif;
  --font-mono: "SF Mono", ui-monospace, Menlo, monospace;
  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 16px;
  --text-lg: 18px;
  --text-xl: 22px;
  --text-2xl: 30px;
  --text-3xl: 42px;
  --text-4xl: 58px;
  --leading-body: 1.5;
  --leading-tight: 1.12;
  --tracking-display: -0.015em;
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
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 18px;
  --radius-pill: 9999px;
  --elev-flat: none;
  --elev-ring: 0 0 0 1px var(--border);
  --elev-raised: 0 16px 40px rgba(23, 32, 51, 0.10);
  --focus-ring: 0 0 0 4px rgba(37, 99, 235, 0.22);
  --motion-fast: 140ms;
  --motion-base: 220ms;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --container-max: 1200px;
  --container-gutter-desktop: 36px;
  --container-gutter-tablet: 24px;
  --container-gutter-phone: 16px;
}
```
