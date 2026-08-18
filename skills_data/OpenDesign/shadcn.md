---
name: Design System: shadcn
source: OpenDesign
version: 1.0.0
description: Category: Modern & Minimal
tags: ["design-system", "shadcn"]
triggers: ["shadcn"]
license: Apache-2.0
target_agent: design
category: design_system
---

# Design System Inspired by Shadcn

> Category: Modern & Minimal
> Shadcn/ui-inspired design with minimal, clean components, monochrome palette, and utility-first patterns.

## 1. Visual Theme & Atmosphere

Shadcn/ui-inspired design with minimal, clean components, monochrome palette, and utility-first patterns.

- **Visual style:** minimal, clean
- **Color stance:** primary, secondary
- **Design intent:** Keep outputs recognizable to this style family while preserving usability and readability.

## 2. Color

- **Primary:** `#000000` — Token from style foundations.
- **Secondary:** `#111111` — Token from style foundations.
- **Success:** `#16A34A` — Token from style foundations.
- **Warning:** `#D97706` — Token from style foundations.
- **Danger:** `#DC2626` — Token from style foundations.
- **Surface:** `#FFFFFF` — Token from style foundations.
- **Text:** `#111827` — Token from style foundations.
- **Neutral:** `#FFFFFF` — Derived from the surface token for official format compatibility.

- Favor Primary (#000000) for CTA emphasis.
- Use Surface (#FFFFFF) for large backgrounds and cards.
- Keep body copy on Text (#111827) for legibility.

## 3. Typography

- **Scale:** 12/14/16/20/24/32
- **Families:** primary=Geist, display=Geist, mono=Fira Code
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

- Buttons: primary action uses `#000000`; secondary actions stay neutral.
- Inputs: strong focus-visible states, clear labels, and predictable error messaging.
- Cards/sections: use consistent radii, spacing, and elevation strategy across the page.

## 7. Motion & Interaction

- Use subtle transitions that emphasize Primary (#000000) as the interaction signal.
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
  --radius: 0.5rem` in the components.json starter). `--radius-sm`
 *      drops to `6px` so inputs and buttons feel one shade tighter
 *      than cards, matching the `calc(var(--radius) - 2px)` formula
 *      shadcn primitives use internally. The whole scale (6/8/12/9999)
 *      is restrained — shadcn rejects oversized pill cards.
 *
 *   6. Type scale tops out at `48px` (`--text-4xl`). DESIGN.md §3
 *      caps the documented scale at 32px;
  --bg: #ffffff;
  --surface: #ffffff;
  --surface-warm: var(--surface);
  --fg: #111827;
  --fg-2: var(--fg);
  --muted: #64748b;
  --meta: var(--muted);
  --border: #e5e7eb;
  --border-soft: var(--border);
  --accent: #000000;
  --accent-on: #ffffff;
  --accent-hover: color-mix(in oklab, var(--accent), white 10%);
  --accent-active: color-mix(in oklab, var(--accent), white 18%);
  --success: #16a34a;
  --warn: #d97706;
  --danger: #dc2626;
  --font-display: "Geist", "Geist Sans", -apple-system, system-ui, "Segoe UI", Arial, sans-serif;
  --font-body: "Geist", "Geist Sans", -apple-system, system-ui, "Segoe UI", Arial, sans-serif;
  --font-mono: "Fira Code", ui-monospace, "SF Mono", "JetBrains Mono", Menlo, Monaco, Consolas, monospace;
  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 16px;
  --text-lg: 20px;
  --text-xl: 24px;
  --text-2xl: 32px;
  --text-3xl: 40px;
  --text-4xl: 48px;
  --leading-body: 1.5;
  --leading-tight: 1.2;
  --tracking-display: -0.02em;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --section-y-desktop: 96px;
  --section-y-tablet: 64px;
  --section-y-phone: 48px;
  --radius: 0.5rem` (8px) and the
   * smaller variants compute as `calc(var(--radius) - Npx)`. We bind:
   *   sm 6px → buttons, inputs (the `calc(--radius - 2px)` tier)
   *   md 8px → cards, modals (the documented baseline)
   *   lg 12px → featured containers (the `calc(--radius + 4px)` tier)
   *   pill 9999px → badges, avatars, capsule chips */
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-pill: 9999px;
  --elev-flat: none;
  --elev-ring: 0 0 0 1px var(--border);
  --elev-raised:
    0 1px 2px 0 color-mix(in oklab, var(--fg), transparent 92%),
    0 1px 3px 0 color-mix(in oklab, var(--fg), transparent 88%);
  --focus-ring: 0 0 0 2px var(--bg), 0 0 0 4px var(--accent);
  --motion-fast: 150ms;
  --motion-base: 200ms;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --container-max: 1280px;
  --container-gutter-desktop: 24px;
  --container-gutter-tablet: 16px;
  --container-gutter-phone: 16px;
}
```
