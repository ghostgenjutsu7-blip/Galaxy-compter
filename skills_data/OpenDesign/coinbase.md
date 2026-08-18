---
name: Design System: coinbase
source: OpenDesign
version: 1.0.0
description: Category: Fintech & Crypto
tags: ["design-system", "coinbase"]
triggers: ["coinbase"]
license: Apache-2.0
target_agent: design
category: design_system
---

# Design System Inspired by Coinbase

> Category: Fintech & Crypto
> Crypto exchange. Clean blue identity, trust-focused, institutional feel.

## 1. Visual Theme & Atmosphere

Coinbase's website is a clean, trustworthy crypto platform that communicates financial reliability through a blue-and-white binary palette. The design uses Coinbase Blue (`#0052ff`) — a deep, saturated blue — as the singular brand accent against white and near-black surfaces. The proprietary font family includes CoinbaseDisplay for hero headlines, CoinbaseSans for UI text, CoinbaseText for body reading, and CoinbaseIcons for iconography — a comprehensive four-font system.

The button system uses a distinctive 56px radius for pill-shaped CTAs with hover transitions to a lighter blue (`#578bfa`). The design alternates between white content sections and dark (`#0a0b0d`, `#282b31`) feature sections, creating a professional, financial-grade interface.

**Key Characteristics:**
- Coinbase Blue (`#0052ff`) as singular brand accent
- Four-font proprietary family: Display, Sans, Text, Icons
- 56px radius pill buttons with blue hover transition
- Near-black (`#0a0b0d`) dark sections + white light sections
- 1.00 line-height on display headings — ultra-tight
- Cool gray secondary surface (`#eef0f3`) with blue tint
- `text-transform: lowercase` on some button labels — unusual

## 2. Color Palette & Roles

### Primary
- **Coinbase Blue** (`#0052ff`): Primary brand, links, CTA borders
- **Pure White** (`#ffffff`): Primary light surface
- **Near Black** (`#0a0b0d`): Text, dark section backgrounds
- **Cool Gray Surface** (`#eef0f3`): Secondary button background

### Interactive
- **Hover Blue** (`#578bfa`): Button hover background
- **Link Blue** (`#0667d0`): Secondary link color
- **Muted Blue** (`#5b616e`): Border color at 20% opacity

### Surface
- **Dark Card** (`#282b31`): Dark button/card backgrounds
- **Light Surface** (`rgba(247,247,247,0.88)`): Subtle surface

## 3. Typography Rules

### Font Families
- **Display**: `CoinbaseDisplay` — hero headlines
- **UI / Sans**: `CoinbaseSans` — buttons, headings, nav
- **Body**: `CoinbaseText` — reading text
- **Icons**: `CoinbaseIcons` — icon font

### Hierarchy

| Role | Font | Size | Weight | Line Height | Notes |
|------|------|------|--------|-------------|-------|
| Display Hero | CoinbaseDisplay | 80px | 400 | 1.00 (tight) | Maximum impact |
| Display Secondary | CoinbaseDisplay | 64px | 400 | 1.00 | Sub-hero |
| Display Third | CoinbaseDisplay | 52px | 400 | 1.00 | Third tier |
| Section Heading | CoinbaseSans | 36px | 400 | 1.11 (tight) | Feature sections |
| Card Title | CoinbaseSans | 32px | 400 | 1.13 | Card headings |
| Feature Title | CoinbaseSans | 18px | 600 | 1.33 | Feature emphasis |
| Body Bold | CoinbaseSans | 16px | 700 | 1.50 | Strong body |
| Body Semibold | CoinbaseSans | 16px | 600 | 1.25 | Buttons, nav |
| Body | CoinbaseText | 18px | 400 | 1.56 | Standard reading |
| Body Small | CoinbaseText | 16px | 400 | 1.50 | Secondary reading |
| Button | CoinbaseSans | 16px | 600 | 1.20 | +0.16px tracking |
| Caption | CoinbaseSans | 14px | 600–700 | 1.50 | Metadata |
| Small | CoinbaseSans | 13px | 600 | 1.23 | Tags |

## 4. Component Stylings

### Buttons

**Primary Pill (56px radius)**
- Background: `#eef0f3` or `#282b31`
- Radius: 56px
- Border: `1px solid` matching background
- Hover: `#578bfa` (light blue)
- Focus: `2px solid black` outline

**Full Pill (100000px radius)**
- Used for maximum pill shape

**Blue Bordered**
- Border: `1px solid #0052ff`
- Background: transparent

### Cards & Containers
- Radius: 8px–40px range
- Borders: `1px solid rgba(91,97,110,0.2)`

## 5. Layout Principles

### Spacing System
- Base: 8px
- Scale: 1px, 3px, 4px, 5px, 6px, 8px, 10px, 12px, 15px, 16px, 20px, 24px, 25px, 32px, 48px

### Border Radius Scale
- Small (4px–8px): Article links, small cards
- Standard (12px–16px): Cards, menus
- Large (24px–32px): Feature containers
- XL (40px): Large buttons/containers
- Pill (56px): Primary CTAs
- Full (100000px): Maximum pill

## 6. Depth & Elevation

Minimal shadow system — depth from color contrast between dark/light sections.

## 7. Do's and Don'ts

### Do
- Use Coinbase Blue (#0052ff) for primary interactive elements
- Apply 56px radius for all CTA buttons
- Use CoinbaseDisplay for hero headings only
- Alternate dark (#0a0b0d) and white sections

### Don't
- Don't use the blue decoratively — it's functional only
- Don't use sharp corners on CTAs — 56px minimum

## 8. Responsive Behavior

Breakpoints: 400px, 576px, 640px, 768px, 896px, 1280px, 1440px, 1600px

## 9. Agent Prompt Guide

### Quick Color Reference
- Brand: Coinbase Blue (`#0052ff`)
- Background: White (`#ffffff`)
- Dark surface: `#0a0b0d`
- Secondary surface: `#eef0f3`
- Hover: `#578bfa`
- Text: `#0a0b0d`

### Example Component Prompts
- "Create hero: white background. CoinbaseDisplay 80px, line-height 1.00. Pill CTA (#eef0f3, 56px radius). Hover: #578bfa."
- "Build dark section: #0a0b0d background. CoinbaseDisplay 64px white text. Blue accent link (#0052ff)."


## Machine-readable tokens (paste verbatim into `:root`)
```css
:root {
  --leading-body: 1.5` rounded for
 *                  the schema's single body lh.
 *
 *   #Coinbase 7  — `--focus-ring` is a sharp 2px solid ring at
 *                  `var(--fg)` — DESIGN.md §4 specifies "Focus: 2px
 *                  solid black outline" on every interactive element.
 *                  We reproduce that as a `box-shadow` so the ring sits
 *                  outside the element without affecting layout. This
 *                  differs from the schema default (3px alpha glow at
 *                  --accent) because Coinbase's focus is mechanical,
 *                  not atmospheric.
 *
 * Brand-specific extensions (Layer C):
 *   None. The 56px pill-CTA radius from DESIGN.md §4 is *component-
 *   specific* (only primary CTAs use it) and lives inline in
 *   components.html rather than as a new token;
  --bg:           #ffffff;
  --surface:      #eef0f3;
  --surface-warm: var(--surface);
  --fg:    #0a0b0d;
  --fg-2:  var(--fg);
  --muted: #5b616e;
  --meta:  var(--muted);
  --border:      rgba(91, 97, 110, 0.2);
  --border-soft: var(--border);
  --accent:        #0052ff;
  --accent-on:     #ffffff;
  --accent-hover:  #578bfa;
  --accent-active: #0667d0;
  --success: #16a34a;
  --warn:    #eab308;
  --danger:  #dc2626;
  --font-display:
    "CoinbaseDisplay", "Coinbase Display",
    "Inter", ui-sans-serif, system-ui, -apple-system,
    "Segoe UI", Arial, sans-serif;
  --font-body:
    "CoinbaseText", "CoinbaseSans", "Coinbase Sans",
    "Inter", ui-sans-serif, system-ui, -apple-system,
    "Segoe UI", Arial, sans-serif;
  --font-mono:
    ui-monospace, "SF Mono", "JetBrains Mono",
    Menlo, Monaco, Consolas, monospace;
  --text-xs:   12px;
  --text-sm:   14px;
  --text-base: 16px;
  --text-lg:   18px;
  --text-xl:   32px;
  --text-2xl:  36px;
  --text-3xl:  52px;
  --text-4xl:  80px;
  --leading-body:     1.5;
  --leading-tight:    1.0;
  --tracking-display: -0.01em;
  --space-1:  4px;
  --space-2:  8px;
  --space-3:  12px;
  --space-4:  16px;
  --space-5:  20px;
  --space-6:  24px;
  --space-8:  32px;
  --space-12: 48px;
  --section-y-desktop: 96px;
  --section-y-tablet:  64px;
  --section-y-phone:   40px;
  --radius-sm:   8px;
  --radius-md:   16px;
  --radius-lg:   32px;
  --radius-pill: 9999px;
  --elev-flat:   none;
  --elev-ring:   0 0 0 1px var(--border);
  --elev-raised: 0 1px 2px color-mix(in oklab, var(--fg), transparent 92%);
  --focus-ring: 0 0 0 2px var(--fg);
  --motion-fast:   150ms;
  --motion-base:   200ms;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --container-max:            1280px;
  --container-gutter-desktop: 24px;
  --container-gutter-tablet:  16px;
  --container-gutter-phone:   16px;
}
```
