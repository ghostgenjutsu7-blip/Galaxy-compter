---
name: nuxtjs Best Practices
source: UIUXProMax
version: 1.0.0
description: 58 curated nuxtjs guidelines (state, perf, a11y, patterns)
tags: ["stack", "nuxtjs"]
triggers: ["nuxtjs"]
license: MIT
target_agent: 
category: tech_stack
---

# nuxtjs — Best Practices (58 guidelines)

## Use file-based routing
Create routes by adding files in pages directory
- **Do:** pages/ directory with index.vue
- **Don't:** Manual route configuration
- Severity: Medium

## Use dynamic route parameters
Create dynamic routes with bracket syntax
- **Do:** [id].vue for dynamic params
- **Don't:** Hardcoded routes for dynamic content
- Severity: Medium

## Use catch-all routes
Handle multiple path segments with [...slug]
- **Do:** [...slug].vue for catch-all
- **Don't:** Multiple nested dynamic routes
- Severity: Low

## Define page metadata with definePageMeta
Set page-level configuration and middleware
- **Do:** definePageMeta for layout middleware title
- **Don't:** Manual route meta configuration
- Severity: High

## Use validate for route params
Validate dynamic route parameters before rendering
- **Do:** validate function in definePageMeta
- **Don't:** Manual validation in setup
- Severity: Medium

## Use SSR by default
Server-side rendering is enabled by default
- **Do:** Keep ssr: true (default)
- **Don't:** Disable SSR unnecessarily
- Severity: High

## Use .client suffix for client-only components
Mark components to render only on client
- **Do:** ComponentName.client.vue suffix
- **Don't:** v-if with process.client check
- Severity: Medium

## Use .server suffix for server-only components
Mark components to render only on server
- **Do:** ComponentName.server.vue suffix
- **Don't:** Manual server check
- Severity: Low

## Use useFetch for simple data fetching
Wrapper around useAsyncData for URL fetching
- **Do:** useFetch for API calls
- **Don't:** $fetch in onMounted
- Severity: High

## Use useAsyncData for complex fetching
Fine-grained control over async data
- **Do:** useAsyncData for CMS or custom fetching
- **Don't:** useFetch for non-URL data sources
- Severity: Medium

## Use $fetch for non-reactive requests
$fetch for event handlers and non-component code
- **Do:** $fetch in event handlers or server routes
- **Don't:** useFetch in click handlers
- Severity: High

## Use lazy option for non-blocking fetch
Defer data fetching for better initial load
- **Do:** lazy: true for below-fold content
- **Don't:** Blocking fetch for non-critical data
- Severity: Medium

## Use server option to control fetch location
Choose where data is fetched
- **Do:** server: false for client-only data
- **Don't:** Server fetch for user-specific client data
- Severity: Medium

## Use pick to reduce payload size
Select only needed fields from response
- **Do:** pick option for large responses
- **Don't:** Fetching entire objects when few fields needed
- Severity: Low

## Use transform for data manipulation
Transform data before storing in state
- **Do:** transform option for data shaping
- **Don't:** Manual transformation after fetch
- Severity: Low

## Handle loading and error states
Always handle pending and error states
- **Do:** Check status pending error refs
- **Don't:** Ignoring loading states
- Severity: High

## Avoid side effects in script setup root
Move side effects to lifecycle hooks
- **Do:** Side effects in onMounted
- **Don't:** setInterval in root script setup
- Severity: High

## Use onMounted for DOM access
Access DOM only after component is mounted
- **Do:** onMounted for DOM manipulation
- **Don't:** Direct DOM access in setup
- Severity: High

## Use nextTick for post-render access
Wait for DOM updates before accessing elements
- **Do:** await nextTick() after state changes
- **Don't:** Immediate DOM access after state change
- Severity: Medium

## Use onPrehydrate for pre-hydration logic
Run code before Nuxt hydrates the page
- **Do:** onPrehydrate for client setup
- **Don't:** onMounted for hydration-critical code
- Severity: Low

## Use server/api for API routes
Create API endpoints in server/api directory
- **Do:** server/api/users.ts for /api/users
- **Don't:** Manual Express setup
- Severity: High

## Use defineEventHandler for handlers
Define server route handlers
- **Do:** defineEventHandler for all handlers
- **Don't:** export default function
- Severity: High

## Use server/routes for non-api routes
Routes without /api prefix
- **Do:** server/routes for custom paths
- **Don't:** server/api for non-api routes
- Severity: Medium

## Use getQuery and readBody for input
Access query params and request body
- **Do:** getQuery(event) readBody(event)
- **Don't:** Direct event access
- Severity: Medium

## Validate server input
Always validate input in server handlers
- **Do:** Zod or similar for validation
- **Don't:** Trust client input
- Severity: High

## Use useState for shared reactive state
SSR-friendly shared state across components
- **Do:** useState for cross-component state
- **Don't:** ref for shared state
- Severity: High

## Use unique keys for useState
Prevent state conflicts with unique keys
- **Do:** Descriptive unique keys for each state
- **Don't:** Generic or duplicate keys
- Severity: Medium

## Use Pinia for complex state
Pinia for advanced state management
- **Do:** @pinia/nuxt for complex apps
- **Don't:** Custom state management
- Severity: Medium

## Use callOnce for one-time async operations
Ensure async operations run only once
- **Do:** callOnce for store initialization
- **Don't:** Direct await in component
- Severity: Medium

## Use useSeoMeta for SEO tags
Type-safe SEO meta tag management
- **Do:** useSeoMeta for meta tags
- **Don't:** useHead for simple meta
- Severity: High

## Use reactive values in useSeoMeta
Dynamic SEO tags with refs or getters
- **Do:** Computed getters for dynamic values
- **Don't:** Static values for dynamic content
- Severity: Medium

## Use useHead for non-meta head elements
Scripts styles links in head
- **Do:** useHead for scripts and links
- **Don't:** useSeoMeta for scripts
- Severity: Medium

## Include OpenGraph tags
Add OG tags for social sharing
- **Do:** ogTitle ogDescription ogImage
- **Don't:** Missing social preview
- Severity: Medium

## Use defineNuxtRouteMiddleware
Define route middleware properly
- **Do:** defineNuxtRouteMiddleware wrapper
- **Don't:** export default function
- Severity: High

## Use navigateTo for redirects
Redirect in middleware with navigateTo
- **Do:** return navigateTo('/login')
- **Don't:** router.push in middleware
- Severity: High

## Reference middleware in definePageMeta
Apply middleware to specific pages
- **Do:** middleware array in definePageMeta
- **Don't:** Global middleware for page-specific
- Severity: Medium

## Use .global suffix for global middleware
Apply middleware to all routes
- **Do:** auth.global.ts for app-wide auth
- **Don't:** Manual middleware on every page
- Severity: Medium

## Use createError for errors
Create errors with proper status codes
- **Do:** createError with statusCode
- **Don't:** throw new Error
- Severity: High

## Use NuxtErrorBoundary for local errors
Handle errors within component subtree
- **Do:** NuxtErrorBoundary for component errors
- **Don't:** Global error page for local errors
- Severity: Medium

## Use clearError to recover from errors
Clear error state and optionally redirect
- **Do:** clearError({ redirect: '/' })
- **Don't:** Manual error state reset
- Severity: Medium

## Use short statusMessage
Keep statusMessage brief for security
- **Do:** Short generic messages
- **Don't:** Detailed error info in statusMessage
- Severity: High

## Use NuxtLink for internal navigation
Client-side navigation with prefetching
- **Do:** <NuxtLink to> for internal links
- **Don't:** <a href> for internal links
- Severity: High

## Configure prefetch behavior
Control when prefetching occurs
- **Do:** prefetchOn for interaction-based
- **Don't:** Default prefetch for low-priority
- Severity: Low

## Use useRouter for programmatic navigation
Navigate programmatically
- **Do:** useRouter().push() for navigation
- **Don't:** Direct window.location
- Severity: Medium

## Use navigateTo in composables
Navigate outside components
- **Do:** navigateTo() in middleware or plugins
- **Don't:** useRouter in non-component code
- Severity: Medium

## Leverage auto-imports
Use auto-imported composables directly
- **Do:** Direct use of ref computed useFetch
- **Don't:** Manual imports for Nuxt composables
- Severity: Medium

## Use #imports for explicit imports
Explicit imports when needed
- **Do:** #imports for clarity or disabled auto-imports
- **Don't:** import from 'vue' when auto-import enabled
- Severity: Low

## Configure third-party auto-imports
Add external package auto-imports
- **Do:** imports.presets in nuxt.config
- **Don't:** Manual imports everywhere
- Severity: Low

## Use defineNuxtPlugin
Define plugins properly
- **Do:** defineNuxtPlugin wrapper
- **Don't:** export default function
- Severity: High

## Use provide for injection
Provide helpers across app
- **Do:** return { provide: {} } for type safety
- **Don't:** nuxtApp.provide without types
- Severity: Medium

## Use .client or .server suffix
Control plugin execution environment
- **Do:** plugin.client.ts for client-only
- **Don't:** if (process.client) checks
- Severity: Medium

## Use runtimeConfig for env vars
Access environment variables safely
- **Do:** runtimeConfig in nuxt.config
- **Don't:** process.env directly
- Severity: High

## Use NUXT_ prefix for env override
Override config with environment variables
- **Do:** NUXT_API_SECRET NUXT_PUBLIC_API_BASE
- **Don't:** Custom env var names
- Severity: High

## Access public config with useRuntimeConfig
Get public config in components
- **Do:** useRuntimeConfig().public
- **Don't:** Direct process.env access
- Severity: High

## Keep secrets in private config
Server-only secrets in runtimeConfig root
- **Do:** runtimeConfig.apiSecret (server only)
- **Don't:** Secrets in public config
- Severity: High

## Use Lazy prefix for code splitting
Lazy load components with Lazy prefix
- **Do:** <LazyComponent> for below-fold
- **Don't:** Eager load all components
- Severity: Medium

## Use useLazyFetch for non-blocking data
Alias for useFetch with lazy: true
- **Do:** useLazyFetch for secondary data
- **Don't:** useFetch for all requests
- Severity: Medium

## Use lazy hydration for interactivity
Delay component hydration until needed
- **Do:** LazyComponent with hydration strategy
- **Don't:** Immediate hydration for all
- Severity: Low
