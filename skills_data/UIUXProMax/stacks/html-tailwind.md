---
name: html-tailwind Best Practices
source: UIUXProMax
version: 1.0.0
description: 55 curated html-tailwind guidelines (state, perf, a11y, patterns)
tags: ["stack", "html-tailwind"]
triggers: ["html-tailwind"]
license: MIT
target_agent: 
category: tech_stack
---

# html-tailwind — Best Practices (55 guidelines)

## Use Tailwind animate utilities
Built-in animations are optimized and respect reduced-motion
- **Do:** Use animate-pulse animate-spin animate-ping
- **Don't:** Custom @keyframes for simple effects
- Severity: Medium

## Limit bounce animations
Continuous bounce is distracting and causes motion sickness
- **Do:** Use animate-bounce sparingly on CTAs only
- **Don't:** Multiple bounce animations on page
- Severity: High

## Transition duration
Use appropriate transition speeds for UI feedback
- **Do:** duration-150 to duration-300 for UI
- **Don't:** duration-1000 or longer for UI elements
- Severity: Medium

## Hover transitions
Add smooth transitions on hover state changes
- **Do:** Add transition class with hover states
- **Don't:** Instant hover changes without transition
- Severity: Low

## Use Tailwind z-* scale
Consistent stacking context with predefined scale
- **Do:** z-0 z-10 z-20 z-30 z-40 z-50
- **Don't:** Arbitrary z-index values
- Severity: Medium

## Fixed elements z-index
Fixed navigation and modals need explicit z-index
- **Do:** z-50 for nav z-40 for dropdowns
- **Don't:** Relying on DOM order for stacking
- Severity: High

## Negative z-index for backgrounds
Use negative z-index for decorative backgrounds
- **Do:** z-[-1] for background elements
- **Don't:** Positive z-index for backgrounds
- Severity: Low

## Container max-width
Limit content width for readability
- **Do:** max-w-7xl mx-auto for main content
- **Don't:** Full-width content on large screens
- Severity: Medium

## Responsive padding
Adjust padding for different screen sizes
- **Do:** px-4 md:px-6 lg:px-8
- **Don't:** Same padding all sizes
- Severity: Medium

## Grid gaps
Use consistent gap utilities for spacing
- **Do:** gap-4 gap-6 gap-8
- **Don't:** Margins on individual items
- Severity: Medium

## Flexbox alignment
Use flex utilities for alignment
- **Do:** items-center justify-between
- **Don't:** Multiple nested wrappers
- Severity: Low

## Aspect ratio
Maintain consistent image aspect ratios
- **Do:** aspect-video aspect-square
- **Don't:** No aspect ratio on containers
- Severity: Medium

## Object fit
Control image scaling within containers
- **Do:** object-cover object-contain
- **Don't:** Stretched distorted images
- Severity: Medium

## Lazy loading
Defer loading of off-screen images
- **Do:** loading='lazy' on images
- **Don't:** All images eager load
- Severity: High

## Responsive images
Serve appropriate image sizes
- **Do:** srcset and sizes attributes
- **Don't:** Same large image all devices
- Severity: High

## Prose plugin
Use @tailwindcss/typography for rich text
- **Do:** prose prose-lg for article content
- **Don't:** Custom styles for markdown
- Severity: Medium

## Line height
Use appropriate line height for readability
- **Do:** leading-relaxed for body text
- **Don't:** Default tight line height
- Severity: Medium

## Font size scale
Use consistent text size scale
- **Do:** text-sm text-base text-lg text-xl
- **Don't:** Arbitrary font sizes
- Severity: Low

## Text truncation
Handle long text gracefully
- **Do:** truncate or line-clamp-*
- **Don't:** Overflow breaking layout
- Severity: Medium

## Opacity utilities
Use color opacity utilities
- **Do:** bg-black/50 text-white/80
- **Don't:** Separate opacity class
- Severity: Low

## Dark mode
Support dark mode with dark: prefix
- **Do:** dark:bg-gray-900 dark:text-white
- **Don't:** No dark mode support
- Severity: Medium

## Semantic colors
Use semantic color naming in config
- **Do:** primary secondary danger success
- **Don't:** Generic color names in components
- Severity: Medium

## Consistent spacing scale
Use Tailwind spacing scale consistently
- **Do:** p-4 m-6 gap-8
- **Don't:** Arbitrary pixel values
- Severity: Low

## Negative margins
Use sparingly for overlapping effects
- **Do:** -mt-4 for overlapping elements
- **Don't:** Negative margins for layout fixing
- Severity: Medium

## Space between
Use space-y-* for vertical lists
- **Do:** space-y-4 on flex/grid column
- **Don't:** Margin on each child
- Severity: Low

## Focus states
Always show focus indicators
- **Do:** focus:ring-2 focus:ring-blue-500
- **Don't:** Remove focus outline
- Severity: High

## Input sizing
Consistent input dimensions
- **Do:** h-10 px-3 for inputs
- **Don't:** Inconsistent input heights
- Severity: Medium

## Disabled states
Clear disabled styling
- **Do:** disabled:opacity-50 disabled:cursor-not-allowed
- **Don't:** No disabled indication
- Severity: Medium

## Placeholder styling
Style placeholder text appropriately
- **Do:** placeholder:text-gray-400
- **Don't:** Dark placeholder text
- Severity: Low

## Mobile-first approach
Start with mobile styles and add breakpoints
- **Do:** Default mobile + md: lg: xl:
- **Don't:** Desktop-first approach
- Severity: Medium

## Breakpoint testing
Test at standard breakpoints
- **Do:** 320 375 768 1024 1280 1536
- **Don't:** Only test on development device
- Severity: High

## Hidden/shown utilities
Control visibility per breakpoint
- **Do:** hidden md:block
- **Don't:** Different content per breakpoint
- Severity: Low

## Button sizing
Consistent button dimensions
- **Do:** px-4 py-2 or px-6 py-3
- **Don't:** Inconsistent button sizes
- Severity: Medium

## Touch targets
Minimum 44px touch target on mobile
- **Do:** min-h-[44px] on mobile
- **Don't:** Small buttons on mobile
- Severity: High

## Loading states
Show loading feedback
- **Do:** disabled + spinner icon
- **Don't:** Clickable during loading
- Severity: High

## Icon buttons
Accessible icon-only buttons
- **Do:** aria-label on icon buttons
- **Don't:** Icon button without label
- Severity: High

## Card structure
Consistent card styling
- **Do:** rounded-lg shadow-md p-6
- **Don't:** Inconsistent card styles
- Severity: Low

## Card hover states
Interactive cards should have hover feedback
- **Do:** hover:shadow-lg transition-shadow
- **Don't:** No hover on clickable cards
- Severity: Medium

## Card spacing
Consistent internal card spacing
- **Do:** space-y-4 for card content
- **Don't:** Inconsistent internal spacing
- Severity: Low

## Screen reader text
Provide context for screen readers
- **Do:** sr-only for hidden labels
- **Don't:** Missing context for icons
- Severity: High

## Focus visible
Show focus only for keyboard users
- **Do:** focus-visible:ring-2
- **Don't:** Focus on all interactions
- Severity: Medium

## Reduced motion
Respect user motion preferences
- **Do:** motion-reduce:animate-none
- **Don't:** Ignore motion preferences
- Severity: High

## Configure content paths
Tailwind needs to know where classes are used
- **Do:** Use 'content' array in config
- **Don't:** Use deprecated 'purge' option (v2)
- Severity: High

## JIT mode
Use JIT for faster builds and smaller bundles
- **Do:** JIT enabled (default in v3)
- **Don't:** Full CSS in development
- Severity: Medium

## Avoid @apply bloat
Use @apply sparingly
- **Do:** Direct utilities in HTML
- **Don't:** Heavy @apply usage
- Severity: Low

## Official plugins
Use official Tailwind plugins
- **Do:** @tailwindcss/forms typography aspect-ratio
- **Don't:** Custom implementations
- Severity: Medium

## Custom utilities
Create utilities for repeated patterns
- **Do:** Custom utility in config
- **Don't:** Repeated arbitrary values
- Severity: Medium

## Container Queries
Use @container for component-based responsiveness
- **Do:** Use @container and @lg: etc.
- **Don't:** Media queries for component internals
- Severity: Medium

## Group and Peer
Style based on parent/sibling state
- **Do:** group-hover peer-checked
- **Don't:** JS for simple state interactions
- Severity: Low

## Arbitrary Values
Use [] for one-off values
- **Do:** w-[350px] for specific needs
- **Don't:** Creating config for single use
- Severity: Low

## Theme color variables
Define colors in Tailwind theme and use directly
- **Do:** bg-primary text-success border-cta
- **Don't:** bg-[var(--color-primary)] text-[var(--color-success)]
- Severity: Medium

## Use bg-linear-to-* for gradients
Tailwind v4 uses bg-linear-to-* syntax for gradients
- **Do:** bg-linear-to-r bg-linear-to-b
- **Don't:** bg-gradient-to-* (deprecated in v4)
- Severity: Medium

## Use shrink-0 shorthand
Shorter class name for flex-shrink-0
- **Do:** shrink-0 shrink
- **Don't:** flex-shrink-0 flex-shrink
- Severity: Low

## Use size-* for square dimensions
Single utility for equal width and height
- **Do:** size-4 size-8 size-12
- **Don't:** Separate h-* w-* for squares
- Severity: Low

## SVG explicit dimensions
Add width/height attributes to SVGs to prevent layout shift before CSS loads
- **Do:** <svg class='size-6' width='24' height='24'>
- **Don't:** SVG without explicit dimensions
- Severity: High
