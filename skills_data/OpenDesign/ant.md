---
name: Design System: ant
source: OpenDesign
version: 1.0.0
description: Category: Professional & Corporate
tags: ["design-system", "ant"]
triggers: ["ant"]
license: Apache-2.0
target_agent: design
category: design_system
---

# Design System Inspired by Ant

> Category: Professional & Corporate
> Structured, enterprise-focused design system emphasizing clarity, consistency, and efficiency for data-dense web applications.

## 1. Visual Theme & Atmosphere

Structured, enterprise-focused design system emphasizing clarity, consistency, and efficiency for data-dense web applications.

- **Visual style:** data-dense, enterprise
- **Color stance:** primary, neutral, success, warning, danger
- **Design intent:** Keep outputs recognizable to this style family while preserving usability and readability.

## 2. Color

- **Primary:** `#1677FF` — Token from style foundations.
- **Secondary:** `#8B5CF6` — Token from style foundations.
- **Success:** `#16A34A` — Token from style foundations.
- **Warning:** `#D97706` — Token from style foundations.
- **Danger:** `#DC2626` — Token from style foundations.
- **Surface:** `#FFFFFF` — Token from style foundations.
- **Text:** `#111827` — Token from style foundations.
- **Neutral:** `#FFFFFF` — Derived from the surface token for official format compatibility.

- Favor Primary (#1677FF) for CTA emphasis.
- Use Surface (#FFFFFF) for large backgrounds and cards.
- Keep body copy on Text (#111827) for legibility.

## 3. Typography

- **Scale:** 12/14/16/20/24/32
- **Families:** primary=Plus Jakarta Sans, display=Plus Jakarta Sans, mono=JetBrains Mono
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

- Buttons: primary action uses `#1677FF`; secondary actions stay neutral.
- Inputs: strong focus-visible states, clear labels, and predictable error messaging.
- Cards/sections: use consistent radii, spacing, and elevation strategy across the page.

## 7. Motion & Interaction

- Use subtle transitions that emphasize Primary (#1677FF) as the interaction signal.
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
  --surface: #f7f8fa;
  --surface-warm: #fff1f0;
  --fg: #1f1f1f;
  --fg-2: #4b5563;
  --muted: #697386;
  --meta: #d32029;
  --border: #d9dce3;
  --border-soft: #eef0f4;
  --accent: #d32029;
  --accent-on: #ffffff;
  --accent-hover: color-mix(in oklab, var(--accent), black 8%);
  --accent-active: color-mix(in oklab, var(--accent), black 14%);
  --success: #22a06b;
  --warn: #faad14;
  --danger: #cf1322;
  --font-display: "Ant Sans", "Alibaba PuHuiTi", Inter, Arial, sans-serif;
  --font-body: "Ant Sans", "Alibaba PuHuiTi", Inter, Arial, sans-serif;
  --font-mono: "SF Mono", ui-monospace, Menlo, monospace;
  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 16px;
  --text-lg: 18px;
  --text-xl: 22px;
  --text-2xl: 32px;
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
  --elev-raised: 0 18px 42px rgba(31, 31, 31, 0.10);
  --focus-ring: 0 0 0 4px rgba(211, 32, 41, 0.22);
  --motion-fast: 140ms;
  --motion-base: 220ms;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --container-max: 1200px;
  --container-gutter-desktop: 36px;
  --container-gutter-tablet: 24px;
  --container-gutter-phone: 16px;
}
```
