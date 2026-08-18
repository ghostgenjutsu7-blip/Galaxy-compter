---
name: Design System: wechat
source: OpenDesign
version: 1.0.0
description: Category: Social & Messaging
tags: ["design-system", "wechat"]
triggers: ["wechat"]
license: Apache-2.0
target_agent: design
category: design_system
---

# WeChat Design System

> Category: Social & Messaging
> Brand visual language for WeChat Mini Programs, official accounts, and open ecosystem extensions.

## Brand Identity

WeChat's identity is built on simplicity, cleanness, and trust — reflecting its role as a super-app that connects people, services, and businesses.

---

## Color Palette

### Brand Colors

| Token | Hex | Usage |
|---|----|----|
| `--wechat-green` | `#07C160` | Primary brand, CTA buttons, active states |
| `--wechat-green-light` | `#10B160` | Hover state for primary actions |
| `--wechat-green-dark` | `#059050` | Pressed/active state |

### Chat Bubble Colors

| Token | Hex | Usage |
|---|----|----|
| `--wechat-bubble-self` | `#95EC69` | Outgoing message bubbles |
| `--wechat-bubble-other` | `#FFFFFF` | Incoming message bubbles |
| `--wechat-bubble-text` | `#1A1A1A` | Primary text in bubbles |

### UI Neutrals

| Token | Hex | Usage |
|---|----|----|
| `--wechat-bg` | `#EDEDED` | Page/app background |
| `--wechat-surface` | `#F7F7F7` | Card, modal surfaces |
| `--wechat-border` | `#E0E0E0` | Dividers, borders |
| `--wechat-ink` | `#1A1A1A` | Primary text |
| `--wechat-muted` | `#888888` | Secondary text, timestamps |

### Functional Colors

| Token | Hex | Usage |
|---|----|----|
| `--wechat-red` | `#FA5151` | Errors, destructive actions |
| `--wechat-orange` | `#FAB702` | Warnings |
| `--wechat-blue` | `#576B95` | Links, info states |

---

## Typography

### Font Stack

```
font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", Helvetica, Arial, sans-serif;
```

### Type Scale

| Role | Size | Weight | Line Height |
|---|---|---|---|
| Page Title | 18px | 600 | 1.3 |
| Section Header | 16px | 600 | 1.4 |
| Body Text | 15px | 400 | 1.6 |
| Secondary Text | 13px | 400 | 1.5 |
| Caption/Timestamp | 11px | 400 | 1.4 |
| Button Label | 16px | 500 | 1.0 |

---

## Spacing System

4px base unit.

| Token | Value |
|---|-----|
| `--space-xs` | 4px |
| `--space-sm` | 8px |
| `--space-md` | 12px |
| `--space-lg` | 16px |
| `--space-xl` | 24px |
| `--space-2xl` | 32px |

### Border Radius

| Token | Value |
|---|-----|
| `--radius-sm` | 4px |
| `--radius-md` | 8px |
| `--radius-lg` | 16px |
| `--radius-bubble` | 16px (with directional corner clip) |
| `--radius-full` | 9999px (avatars, pills) |

---

## Components

### Chat Bubble

```css
.wechat-bubble {
  max-width: 70%;
  padding: 10px 14px;
  border-radius: var(--radius-bubble);
  font-size: 15px;
  line-height: 1.6;
  position: relative;
}

.wechat-bubble.self {
  background: var(--wechat-bubble-self);
  color: var(--wechat-bubble-text);
  border-top-right-radius: 4px;
  margin-left: auto;
}

.wechat-bubble.other {
  background: var(--wechat-bubble-other);
  color: var(--wechat-bubble-text);
  border-top-left-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);
}
```

### Primary Button (Send / Confirm)

```css
.btn-wechat-primary {
  background: var(--wechat-green);
  color: #fff;
  border: none;
  border-radius: var(--radius-md);
  padding: 12px 32px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.15s;
}

.btn-wechat-primary:hover {
  background: var(--wechat-green-light);
}

.btn-wechat-primary:active {
  background: var(--wechat-green-dark);
}
```

### Tab Bar

```css
.tab-bar {
  display: flex;
  background: var(--wechat-surface);
  border-top: 1px solid var(--wechat-border);
  padding: 8px 0 calc(8px + env(safe-area-inset-bottom));
}

.tab-bar-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  color: var(--wechat-muted);
  font-size: 10px;
  cursor: pointer;
  transition: color 0.15s;
}

.tab-bar-item.active {
  color: var(--wechat-green);
}

.tab-bar-item svg {
  width: 24px;
  height: 24px;
}
```

### Message Input Bar

```css
.input-bar {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  padding: 10px 12px calc(10px + env(safe-area-inset-bottom));
  background: var(--wechat-surface);
  border-top: 1px solid var(--wechat-border);
}

.input-bar textarea {
  flex: 1;
  min-height: 36px;
  max-height: 100px;
  padding: 8px 12px;
  background: var(--wechat-bg);
  border: 1px solid var(--wechat-border);
  border-radius: var(--radius-lg);
  font-size: 15px;
  line-height: 1.5;
  resize: none;
  outline: none;
}

.input-bar textarea:focus {
  border-color: var(--wechat-green);
}
```

### Avatar

```css
.avatar {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  object-fit: cover;
  background: var(--wechat-border);
}

.avatar.sm { width: 32px; height: 32px; }
.avatar.lg { width: 56px; height: 56px; }
```

### Timestamp Badge

```css
.timestamp {
  display: inline-block;
  padding: 4px 8px;
  background: rgba(0, 0, 0, 0.08);
  border-radius: var(--radius-sm);
  font-size: 11px;
  color: var(--wechat-muted);
  text-align: center;
}
```

---

## Motion & Animation

| Token | Value |
|---|-----|
| `--duration-instant` | 100ms |
| `--duration-fast` | 200ms |
| `--duration-normal` | 300ms |
| `--ease-default` | cubic-bezier(0.25, 0.1, 0.25, 1) |

Chat message entry: fade-in + slight slide up, 200ms.

---

## Dark Mode

| Token | Light | Dark |
|---|---|---|
| `--wechat-bg` | `#EDEDED` | `#1A1A1A` |
| `--wechat-surface` | `#F7F7F7` | `#2C2C2C` |
| `--wechat-ink` | `#1A1A1A` | `#F7F7F7` |
| `--wechat-bubble-self` | `#95EC69` | `#4CAF50` |
| `--wechat-bubble-other` | `#FFFFFF` | `#2C2C2C` |

---

## Usage

```css
:root {
  --wechat-green: #07C160;
  --wechat-green-light: #10B160;
  --wechat-green-dark: #059050;
  --wechat-bubble-self: #95EC69;
  --wechat-bubble-other: #FFFFFF;
  --wechat-bubble-text: #1A1A1A;
  --wechat-bg: #EDEDED;
  --wechat-surface: #F7F7F7;
  --wechat-border: #E0E0E0;
  --wechat-ink: #1A1A1A;
  --wechat-muted: #888888;
  --wechat-red: #FA5151;
  --wechat-orange: #FAB702;
  --wechat-blue: #576B95;
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 12px;
  --space-lg: 16px;
  --space-xl: 24px;
  --space-2xl: 32px;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  --radius-bubble: 16px;
  --radius-full: 9999px;
  --duration-instant: 100ms;
  --duration-fast: 200ms;
  --duration-normal: 300ms;
  --ease-default: cubic-bezier(0.25, 0.1, 0.25, 1);
}
```


## Machine-readable tokens (paste verbatim into `:root`)
```css
:root {
  --bg: #ededed (chat-list gray, DESIGN.md §UI Neutrals).
 *   - --surface: #f7f7f7 (card / sheet lift on bg).
 *   - --surface-warm: var(--surface) — single surface tier.
 *   - --fg: #1a1a1a (ink);
  --muted: #888888 (secondary + timestamps);
  --meta: var(--muted) — DESIGN.md does not separate the tier.
 *   - --border: #e0e0e0;
  --accent: #07c160 + hover #10b160 + active #059050 (DESIGN.md).
 *   - --success: #07c160 (brand-as-success — green is "done" in WeChat).
 *   - --warn: #fab702;
  --danger: #fa5151 (DESIGN.md functional palette).
 *   - --font-display / --font-body: identical apple-system + CJK stack.
 *     DESIGN.md uses a single family across the app;
  --leading-body: 1.6 (DESIGN.md body, generous for CJK density).
 *   - Radius: 4 / 8 / 16 / pill (DESIGN.md §Border Radius).
 *   - Motion: 100ms hover, 200ms message-entry, cubic-bezier(0.25, 0.1,
 *     0.25, 1) — DESIGN.md §Motion (instant + fast + ease-default).
 * ─────────────────────────────────────────────────────────────────── */

:root {
  /* ─── Surface ──────────────────────────────────────────────────────
   * Light-friendly canvas: the muted #EDEDED chat-list gray is the
   * WeChat user's home colour. Surfaces lift one tone above it. */
  --bg:           #ededed;
  --surface:      #f7f7f7;
  --surface-warm: var(--surface);
  --fg:    #1a1a1a;
  --fg-2:  var(--fg);
  --muted: #888888;
  --meta:  var(--muted);
  --border:      #e0e0e0;
  --border-soft: var(--border);
  --accent:        #07c160;
  --accent-on:     #ffffff;
  --accent-hover:  #10b160;
  --accent-active: #059050;
  --success: #07c160;
  --warn:    #fab702;
  --danger:  #fa5151;
  --font-display: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans SC", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-body:    -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans SC", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-mono:    ui-monospace, "SF Mono", "JetBrains Mono", Menlo, Monaco, Consolas, monospace;
  --text-xs:   11px;
  --text-sm:   13px;
  --text-base: 15px;
  --text-lg:   16px;
  --text-xl:   18px;
  --text-2xl:  24px;
  --text-3xl:  32px;
  --text-4xl:  48px;
  --leading-body:     1.6;
  --leading-tight:    1.3;
  --tracking-display: -0.01em;
  --space-1:  4px;
  --space-2:  8px;
  --space-3:  12px;
  --space-4:  16px;
  --space-5:  20px;
  --space-6:  24px;
  --space-8:  32px;
  --space-12: 48px;
  --section-y-desktop: 72px;
  --section-y-tablet:  48px;
  --section-y-phone:   32px;
  --radius-sm:   4px;
  --radius-md:   8px;
  --radius-lg:   16px;
  --radius-pill: 9999px;
  --elev-flat:   none;
  --elev-ring:   0 0 0 1px var(--border);
  --elev-raised: 0 1px 2px rgba(0, 0, 0, 0.06);
  --focus-ring: 0 0 0 3px color-mix(in oklab, var(--accent), transparent 70%);
  --motion-fast:   100ms;
  --motion-base:   200ms;
  --ease-standard: cubic-bezier(0.25, 0.1, 0.25, 1);
  --container-max:            1200px;
  --container-gutter-desktop: 24px;
  --container-gutter-tablet:  16px;
}
```
