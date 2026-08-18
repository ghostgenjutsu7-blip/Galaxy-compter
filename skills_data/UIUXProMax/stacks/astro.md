---
name: astro Best Practices
source: UIUXProMax
version: 1.0.0
description: 53 curated astro guidelines (state, perf, a11y, patterns)
tags: ["stack", "astro"]
triggers: ["astro"]
license: MIT
target_agent: 
category: tech_stack
---

# astro — Best Practices (53 guidelines)

## Use Islands Architecture
Astro's partial hydration only loads JS for interactive components
- **Do:** Interactive components with client directives
- **Don't:** Hydrate entire page like traditional SPA
- Severity: High

## Default to zero JS
Astro ships zero JS by default - add only when needed
- **Do:** Static components without client directive
- **Don't:** Add client:load to everything
- Severity: High

## Choose right client directive
Different directives for different hydration timing
- **Do:** client:visible for below-fold client:idle for non-critical
- **Don't:** client:load for everything
- Severity: Medium

## Use content collections
Type-safe content management for blogs docs
- **Do:** Content collections for structured content
- **Don't:** Loose markdown files without schema
- Severity: High

## Define collection schemas
Zod schemas for content validation
- **Do:** Schema with required fields and types
- **Don't:** No schema validation
- Severity: High

## Use file-based routing
Create routes by adding .astro files in pages/
- **Do:** pages/ directory for routes
- **Don't:** Manual route configuration
- Severity: Medium

## Dynamic routes with brackets
Use [param] for dynamic routes
- **Do:** Bracket notation for params
- **Don't:** Query strings for dynamic content
- Severity: Medium

## Use getStaticPaths for SSG
Generate static pages at build time
- **Do:** getStaticPaths for known dynamic routes
- **Don't:** Fetch at runtime for static content
- Severity: High

## Enable SSR when needed
Server-side rendering for dynamic content
- **Do:** output: 'server' or 'hybrid' for dynamic
- **Don't:** SSR for purely static sites
- Severity: Medium

## Keep .astro for static
Use .astro components for static content
- **Do:** Astro components for layout structure
- **Don't:** React/Vue for static markup
- Severity: High

## Use framework components for interactivity
React Vue Svelte for complex interactivity
- **Do:** Framework component with client directive
- **Don't:** Astro component with inline scripts
- Severity: Medium

## Pass data via props
Astro components receive props in frontmatter
- **Do:** Astro.props for component data
- **Don't:** Global state for simple data
- Severity: Low

## Use slots for composition
Named and default slots for flexible layouts
- **Do:** <slot /> for child content
- **Don't:** Props for HTML content
- Severity: Medium

## Colocate component styles
Scoped styles in component file
- **Do:** <style> in same .astro file
- **Don't:** Separate CSS files for component styles
- Severity: Low

## Use scoped styles by default
Astro scopes styles to component automatically
- **Do:** <style> for component-specific styles
- **Don't:** Global styles for everything
- Severity: Medium

## Use is:global sparingly
Global styles only when truly needed
- **Do:** is:global for base styles or overrides
- **Don't:** is:global for component styles
- Severity: Medium

## Integrate Tailwind properly
Use @astrojs/tailwind integration
- **Do:** Official Tailwind integration
- **Don't:** Manual Tailwind setup
- Severity: Low

## Use CSS variables for theming
Define tokens in :root
- **Do:** CSS custom properties for themes
- **Don't:** Hardcoded colors everywhere
- Severity: Medium

## Fetch in frontmatter
Data fetching in component frontmatter
- **Do:** Top-level await in frontmatter
- **Don't:** useEffect for initial data
- Severity: High

## Use Astro.glob for local files
Import multiple local files
- **Do:** Astro.glob for markdown/data files
- **Don't:** Manual imports for each file
- Severity: Medium

## Prefer content collections over glob
Type-safe collections for structured content
- **Do:** getCollection() for blog/docs
- **Don't:** Astro.glob for structured content
- Severity: High

## Use environment variables correctly
Import.meta.env for env vars
- **Do:** PUBLIC_ prefix for client vars
- **Don't:** Expose secrets to client
- Severity: High

## Preload critical assets
Use link preload for important resources
- **Do:** Preload fonts above-fold images
- **Don't:** No preload hints
- Severity: Medium

## Optimize images with astro:assets
Built-in image optimization
- **Do:** <Image /> component for optimization
- **Don't:** <img> for local images
- Severity: High

## Use picture for responsive images
Multiple formats and sizes
- **Do:** <Picture /> for art direction
- **Don't:** Single image size for all screens
- Severity: Medium

## Lazy load below-fold content
Defer loading non-critical content
- **Do:** loading=lazy for images client:visible for components
- **Don't:** Load everything immediately
- Severity: Medium

## Minimize client directives
Each directive adds JS bundle
- **Do:** Audit client: usage regularly
- **Don't:** Sprinkle client:load everywhere
- Severity: High

## Enable View Transitions
Smooth page transitions
- **Do:** <ViewTransitions /> in head
- **Don't:** Full page reloads
- Severity: Medium

## Use transition:name
Named elements for morphing
- **Do:** transition:name for persistent elements
- **Don't:** Unnamed transitions
- Severity: Low

## Handle transition:persist
Keep state across navigations
- **Do:** transition:persist for media players
- **Don't:** Re-initialize on every navigation
- Severity: Medium

## Add fallback for no-JS
Graceful degradation
- **Do:** Content works without JS
- **Don't:** Require JS for basic navigation
- Severity: High

## Use built-in SEO component
Head management for meta tags
- **Do:** Astro SEO integration or manual head
- **Don't:** No meta tags
- Severity: High

## Generate sitemap
Automatic sitemap generation
- **Do:** @astrojs/sitemap integration
- **Don't:** Manual sitemap maintenance
- Severity: Medium

## Add RSS feed for content
RSS for blogs and content sites
- **Do:** @astrojs/rss for feed generation
- **Don't:** No RSS feed
- Severity: Low

## Use canonical URLs
Prevent duplicate content issues
- **Do:** Astro.url for canonical generation
- **Don't:** No canonical tags
- Severity: Medium

## Use official integrations
Astro's integration system
- **Do:** npx astro add for integrations
- **Don't:** Manual configuration
- Severity: Medium

## Configure integrations in astro.config
Centralized configuration
- **Do:** integrations array in config
- **Don't:** Scattered configuration
- Severity: Low

## Use adapter for deployment
Platform-specific adapters
- **Do:** Correct adapter for host
- **Don't:** Wrong or no adapter
- Severity: High

## Enable TypeScript
Type safety for Astro projects
- **Do:** tsconfig.json with astro types
- **Don't:** No TypeScript
- Severity: Medium

## Type component props
Define prop interfaces
- **Do:** Props interface in frontmatter
- **Don't:** Untyped props
- Severity: Medium

## Use strict mode
Catch errors early
- **Do:** strict: true in tsconfig
- **Don't:** Loose TypeScript config
- Severity: Low

## Use MDX for components
Components in markdown content
- **Do:** @astrojs/mdx for interactive docs
- **Don't:** Plain markdown with workarounds
- Severity: Medium

## Configure markdown plugins
Extend markdown capabilities
- **Do:** remarkPlugins rehypePlugins in config
- **Don't:** Manual HTML for features
- Severity: Low

## Use frontmatter for metadata
Structured post metadata
- **Do:** Frontmatter with typed schema
- **Don't:** Inline metadata
- Severity: Medium

## Use API routes for endpoints
Server endpoints in pages/api
- **Do:** pages/api/[endpoint].ts for APIs
- **Don't:** External API for simple endpoints
- Severity: Medium

## Return proper responses
Use Response object
- **Do:** new Response() with headers
- **Don't:** Plain objects
- Severity: Medium

## Handle methods correctly
Export named method handlers
- **Do:** export GET POST handlers
- **Don't:** Single default export
- Severity: Low

## Sanitize user content
Prevent XSS in dynamic content
- **Do:** set:html only for trusted content
- **Don't:** set:html with user input
- Severity: High

## Use HTTPS in production
Secure connections
- **Do:** HTTPS for all production sites
- **Don't:** HTTP in production
- Severity: High

## Validate API input
Check and sanitize all input
- **Do:** Zod validation for API routes
- **Don't:** Trust all input
- Severity: High

## Use hybrid rendering
Mix static and dynamic pages
- **Do:** output: 'hybrid' for flexibility
- **Don't:** All SSR or all static
- Severity: Medium

## Analyze bundle size
Monitor JS bundle impact
- **Do:** Build output shows bundle sizes
- **Don't:** Ignore bundle growth
- Severity: Medium

## Use prefetch
Preload linked pages
- **Do:** prefetch integration
- **Don't:** No prefetch for navigation
- Severity: Low
