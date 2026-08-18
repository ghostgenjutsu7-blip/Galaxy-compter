---
name: nextjs Best Practices
source: UIUXProMax
version: 1.0.0
description: 52 curated nextjs guidelines (state, perf, a11y, patterns)
tags: ["stack", "nextjs"]
triggers: ["nextjs"]
license: MIT
target_agent: 
category: tech_stack
---

# nextjs — Best Practices (52 guidelines)

## Use App Router for new projects
App Router is the recommended approach in Next.js 14+
- **Do:** app/ directory with page.tsx
- **Don't:** pages/ for new projects
- Severity: Medium

## Use file-based routing
Create routes by adding files in app directory
- **Do:** page.tsx for routes layout.tsx for layouts
- **Don't:** Manual route configuration
- Severity: Medium

## Colocate related files
Keep components styles tests with their routes
- **Do:** Component files alongside page.tsx
- **Don't:** Separate components folder
- Severity: Low

## Use route groups for organization
Group routes without affecting URL
- **Do:** Parentheses for route groups
- **Don't:** Nested folders affecting URL
- Severity: Low

## Handle loading states
Use loading.tsx for route loading UI
- **Do:** loading.tsx alongside page.tsx
- **Don't:** Manual loading state management
- Severity: Medium

## Handle errors with error.tsx
Catch errors at route level
- **Do:** error.tsx with reset function
- **Don't:** try/catch in every component
- Severity: High

## Use Server Components by default
Server Components reduce client JS bundle
- **Do:** Keep components server by default
- **Don't:** Add 'use client' unnecessarily
- Severity: High

## Mark Client Components explicitly
'use client' for interactive components
- **Do:** Add 'use client' only when needed
- **Don't:** Server Component with hooks/events
- Severity: High

## Push Client Components down
Keep Client Components as leaf nodes
- **Do:** Client wrapper for interactive parts only
- **Don't:** Mark page as Client Component
- Severity: High

## Use streaming for better UX
Stream content with Suspense boundaries
- **Do:** Suspense for slow data fetches
- **Don't:** Wait for all data before render
- Severity: Medium

## Choose correct rendering strategy
SSG for static SSR for dynamic ISR for semi-static
- **Do:** generateStaticParams for known paths
- **Don't:** SSR for static content
- Severity: Medium

## Fetch data in Server Components
Fetch directly in async Server Components
- **Do:** async function Page() { const data = await fetch() }
- **Don't:** useEffect for initial data
- Severity: High

## Configure caching explicitly (Next.js 15+)
Next.js 15 changed defaults to uncached for fetch
- **Do:** Explicitly set cache: 'force-cache' for static data
- **Don't:** Assume default is cached (it's not in Next.js 15)
- Severity: High

## Deduplicate fetch requests
React and Next.js dedupe same requests
- **Do:** Same fetch call in multiple components
- **Don't:** Manual request deduplication
- Severity: Low

## Use Server Actions for mutations
Server Actions for form submissions
- **Do:** action={serverAction} in forms
- **Don't:** API route for every mutation
- Severity: Medium

## Revalidate data appropriately
Use revalidatePath/revalidateTag after mutations
- **Do:** Revalidate after Server Action
- **Don't:** 'use client' with manual refetch
- Severity: Medium

## Use next/image for optimization
Automatic image optimization and lazy loading
- **Do:** <Image> component for all images
- **Don't:** <img> tags directly
- Severity: High

## Provide width and height
Prevent layout shift with dimensions
- **Do:** width and height props or fill
- **Don't:** Missing dimensions
- Severity: High

## Use fill for responsive images
Fill container with object-fit
- **Do:** fill prop with relative parent
- **Don't:** Fixed dimensions for responsive
- Severity: Medium

## Configure remote image domains
Whitelist external image sources
- **Do:** remotePatterns in next.config.js
- **Don't:** Allow all domains
- Severity: High

## Use priority for LCP images
Mark above-fold images as priority
- **Do:** priority prop on hero images
- **Don't:** All images with priority
- Severity: Medium

## Use next/font for fonts
Self-hosted fonts with zero layout shift
- **Do:** next/font/google or next/font/local
- **Don't:** External font links
- Severity: Medium

## Apply font to layout
Set font in root layout for consistency
- **Do:** className on body in layout.tsx
- **Don't:** Font in individual pages
- Severity: Low

## Use variable fonts
Variable fonts reduce bundle size
- **Do:** Single variable font file
- **Don't:** Multiple font weights as files
- Severity: Low

## Use generateMetadata for dynamic
Generate metadata based on params
- **Do:** export async function generateMetadata()
- **Don't:** Hardcoded metadata everywhere
- Severity: Medium

## Include OpenGraph images
Add OG images for social sharing
- **Do:** opengraph-image.tsx or og property
- **Don't:** Missing social preview images
- Severity: Medium

## Use metadata API
Export metadata object for static metadata
- **Do:** export const metadata = {}
- **Don't:** Manual head tags
- Severity: Medium

## Use Route Handlers for APIs
app/api routes for API endpoints
- **Do:** app/api/users/route.ts
- **Don't:** pages/api for new projects
- Severity: Medium

## Return proper Response objects
Use NextResponse for API responses
- **Do:** NextResponse.json() for JSON
- **Don't:** Plain objects or res.json()
- Severity: Medium

## Handle HTTP methods explicitly
Export named functions for methods
- **Do:** Export GET POST PUT DELETE
- **Don't:** Single handler for all methods
- Severity: Low

## Validate request body
Validate input before processing
- **Do:** Zod or similar for validation
- **Don't:** Trust client input
- Severity: High

## Use middleware for auth
Protect routes with middleware.ts
- **Do:** middleware.ts at root
- **Don't:** Auth check in every page
- Severity: Medium

## Match specific paths
Configure middleware matcher
- **Do:** config.matcher for specific routes
- **Don't:** Run middleware on all routes
- Severity: Medium

## Keep middleware edge-compatible
Middleware runs on Edge runtime
- **Do:** Edge-compatible code only
- **Don't:** Node.js APIs in middleware
- Severity: High

## Use NEXT_PUBLIC prefix
Client-accessible env vars need prefix
- **Do:** NEXT_PUBLIC_ for client vars
- **Don't:** Server vars exposed to client
- Severity: High

## Validate env vars
Check required env vars exist
- **Do:** Validate on startup
- **Don't:** Undefined env at runtime
- Severity: High

## Use .env.local for secrets
Local env file for development secrets
- **Do:** .env.local gitignored
- **Don't:** Secrets in .env committed
- Severity: High

## Analyze bundle size
Use @next/bundle-analyzer
- **Do:** Bundle analyzer in dev
- **Don't:** Ship large bundles blindly
- Severity: Medium

## Use dynamic imports
Code split with next/dynamic
- **Do:** dynamic() for heavy components
- **Don't:** Import everything statically
- Severity: Medium

## Avoid layout shifts
Reserve space for dynamic content
- **Do:** Skeleton loaders aspect ratios
- **Don't:** Content popping in
- Severity: High

## Use Partial Prerendering
Combine static and dynamic in one route
- **Do:** Static shell with Suspense holes
- **Don't:** Full dynamic or static pages
- Severity: Low

## Use next/link for navigation
Client-side navigation with prefetching
- **Do:** <Link href=""> for internal links
- **Don't:** <a> for internal navigation
- Severity: High

## Prefetch strategically
Control prefetching behavior
- **Do:** prefetch={false} for low-priority
- **Don't:** Prefetch all links
- Severity: Low

## Use scroll option appropriately
Control scroll behavior on navigation
- **Do:** scroll={false} for tabs pagination
- **Don't:** Always scroll to top
- Severity: Low

## Use next.config.js correctly
Configure Next.js behavior
- **Do:** Proper config options
- **Don't:** Deprecated or wrong options
- Severity: Medium

## Enable strict mode
Catch potential issues early
- **Do:** reactStrictMode: true
- **Don't:** Strict mode disabled
- Severity: Medium

## Configure redirects and rewrites
Use config for URL management
- **Do:** redirects() rewrites() in config
- **Don't:** Manual redirect handling
- Severity: Medium

## Use Vercel for easiest deploy
Vercel optimized for Next.js
- **Do:** Deploy to Vercel
- **Don't:** Self-host without knowledge
- Severity: Low

## Configure output for self-hosting
Set output option for deployment target
- **Do:** output: 'standalone' for Docker
- **Don't:** Default output for containers
- Severity: Medium

## Sanitize user input
Never trust user input
- **Do:** Escape sanitize validate all input
- **Don't:** Direct interpolation of user data
- Severity: High

## Use CSP headers
Content Security Policy for XSS protection
- **Do:** Configure CSP in next.config.js
- **Don't:** No security headers
- Severity: High

## Validate Server Action input
Server Actions are public endpoints
- **Do:** Validate and authorize in Server Action
- **Don't:** Trust Server Action input
- Severity: High
