---
name: laravel Best Practices
source: UIUXProMax
version: 1.0.0
description: 50 curated laravel guidelines (state, perf, a11y, patterns)
tags: ["stack", "laravel"]
triggers: ["laravel"]
license: MIT
target_agent: 
category: tech_stack
---

# laravel — Best Practices (50 guidelines)

## Use Blade components for reusable UI
Extract repeated markup into named Blade components
- **Do:** Use x-* components with @props for all reusable UI
- **Don't:** Duplicate HTML blocks across views
- Severity: High

## Use layouts with @extends and @section
Define one master layout and extend it per page
- **Do:** @extends layout with named @section blocks
- **Don't:** Duplicate header/footer HTML in every view
- Severity: High

## Use @props for component type-safety
Declare accepted props inside components with @props
- **Do:** @props with defaults to document component API
- **Don't:** Pass arbitrary variables without declaration
- Severity: Medium

## Use conditional CSS classes with @class
Build class strings conditionally without ternary noise
- **Do:** @class directive for conditional class binding
- **Don't:** String concatenation or nested ternaries
- Severity: Medium

## Use named slots for flexible layouts
Named slots let callers inject content into specific regions
- **Do:** @slot('header') and $slot for flexible component APIs
- **Don't:** Hard-code all sub-sections inside components
- Severity: Medium

## Use Blade directives instead of raw PHP
Blade directives are readable and IDE-supported
- **Do:** @if @foreach @forelse @empty instead of <?php ?>
- **Don't:** Raw PHP tags inside Blade templates
- Severity: High

## Escape output with {{ }}
Use double curly braces for XSS-safe output
- **Do:** {{ }} for all user-supplied or dynamic text
- **Don't:** {!! !!} for untrusted data
- Severity: High

## Use @vite for asset loading
Vite integration handles cache busting and HMR automatically
- **Do:** @vite(['resources/css/app.css' 'resources/js/app.js'])
- **Don't:** Manual script/link tags with hardcoded paths
- Severity: High

## Bind inputs with wire:model
Two-way data binding keeps component state in sync
- **Do:** wire:model for all form inputs managed by Livewire
- **Don't:** Manual JavaScript listeners syncing to component
- Severity: High

## Use wire:model.live for real-time validation
Validate on input rather than only on submit
- **Do:** wire:model.live + #[Validate] for instant feedback
- **Don't:** Only validate on form submit
- Severity: Medium

## Use wire:click for actions
Bind UI events to component methods cleanly
- **Do:** wire:click for buttons and interactive elements
- **Don't:** JavaScript fetch calls replicating Livewire actions
- Severity: High

## Use lifecycle hooks appropriately
mount() for init; updated() for reactive side effects
- **Do:** mount() for initialization updatedFoo() for property changes
- **Don't:** Heavy logic in render() or __construct()
- Severity: Medium

## Use lazy loading for heavy components
Defer render of expensive components until visible
- **Do:** wire:init or lazy attribute on components
- **Don't:** Load all Livewire components on page load
- Severity: Medium

## Integrate Alpine.js for local UI state
Use Alpine.js for UI-only state that doesn't need server round-trips
- **Do:** x-data / x-show / x-transition for tooltips dropdowns
- **Don't:** Livewire server calls for purely visual toggle state
- Severity: Medium

## Use wire:loading for feedback
Always indicate to users when a server action is in progress
- **Do:** wire:loading.attr="disabled" and wire:loading elements
- **Don't:** Provide no feedback while Livewire request is in flight
- Severity: High

## Handle file uploads with WithFileUploads
Livewire's trait manages chunked upload and temp storage
- **Do:** WithFileUploads trait + wire:model for file inputs
- **Don't:** Manual multipart form submissions for Livewire pages
- Severity: Medium

## Use Inertia page components as route endpoints
Each page is a Vue/React component rendered server-side via Inertia::render()
- **Do:** Inertia::render('Dashboard' ['data' => $data]) in controllers
- **Don't:** Return JSON and fetch from JavaScript
- Severity: High

## Share global data via HandleInertiaRequests
Middleware share() provides auth user and flash to every page
- **Do:** Share auth/flash in HandleInertiaRequests middleware
- **Don't:** Pass auth to every Inertia::render() call
- Severity: High

## Use <Link> for client-side navigation
Inertia Link intercepts clicks for SPA-like transitions
- **Do:** <Link href="/dashboard"> instead of <a href>
- **Don't:** Regular <a> tags for internal navigation
- Severity: High

## Use useForm for form state and submission
Inertia's useForm manages progress errors and transforms
- **Do:** useForm for all page-level forms, form.post() for submit
- **Don't:** Axios/fetch for form submissions on Inertia pages
- Severity: High

## Use persistent layouts to preserve state
Wrap pages in a persistent layout so header/sidebar don't remount
- **Do:** layout property on page component for persistent UI
- **Don't:** Re-render full layout on every page visit
- Severity: Medium

## Enable SSR for public pages
Server-side rendering improves SEO and first paint
- **Do:** Enable Inertia SSR for marketing and public pages
- **Don't:** Client-only rendering for all pages including public
- Severity: Medium

## Set up Tailwind CSS via Vite
Use Vite + tailwindcss plugin for fast HMR and optimized builds
- **Do:** Install tailwindcss @tailwindcss/vite and configure vite.config.js
- **Don't:** Laravel Mix or manual PostCSS pipeline for new projects
- Severity: High

## Purge unused styles via content config
Tailwind scans Blade and JS files to tree-shake unused classes
- **Do:** content: ['./resources/views/**/*.blade.php', './resources/js/**/*.{js,vue}']
- **Don't:** No content config — ship all 3MB of CSS
- Severity: High

## Use dark mode class strategy
class-based dark mode integrates with server-rendered preference
- **Do:** darkMode: 'class' with a toggle that sets class on <html>
- **Don't:** Media query only — no user override possible
- Severity: Medium

## Use @apply sparingly in component CSS
Extract only truly repeated multi-class patterns
- **Do:** @apply for BEM base classes shared across many components
- **Don't:** @apply for every single element — defeats Tailwind's purpose
- Severity: Low

## Configure custom design tokens in CSS
Define brand colors spacing fonts as CSS variables consumed by Tailwind
- **Do:** Custom @theme tokens matched to brand guidelines
- **Don't:** Magic color hex codes scattered across Blade templates
- Severity: Medium

## Use anonymous Blade components for UI primitives
Blade files in resources/views/components/ auto-register as x-* components
- **Do:** Anonymous components for buttons alerts badges cards
- **Don't:** Blade @includes for anything reusable
- Severity: Medium

## Use class-based components for complex logic
PHP class components can inject services and pre-process data
- **Do:** app/View/Components/ class when component needs PHP logic
- **Don't:** Blade @php blocks for business logic inside templates
- Severity: Medium

## Forward extra attributes with $attributes
Pass through HTML attributes like class id aria to root element
- **Do:** $attributes->merge() on root element of components
- **Don't:** Ignore caller-provided HTML attributes silently
- Severity: High

## Separate variant logic from templates
Keep variant/size/color logic in a PHP class or helper not in Blade
- **Do:** Variant class or match() expression in component class
- **Don't:** Long @if chains for variants inside Blade templates
- Severity: Medium

## Provide default slot content
Use {{ $slot ?? '' }} or named slot defaults so components are usable empty
- **Do:** Default content in slots for optional regions
- **Don't:** Require every slot to be filled — throws errors on empty usage
- Severity: Low

## Use component namespacing for packages
Prefix third-party or module components to avoid collisions
- **Do:** Register custom prefix via Blade::componentNamespace()
- **Don't:** Mix first-party and package component names with no prefix
- Severity: Low

## Validate with Form Request classes
Move validation rules out of controllers into dedicated FormRequest classes
- **Do:** php artisan make:request and define rules() + authorize()
- **Don't:** Inline validate() in controller actions
- Severity: High

## Preserve old input on validation failure
Use old() to repopulate form fields after server-side error redirect
- **Do:** old('field') as default value on all form inputs
- **Don't:** Empty form fields when validation fails
- Severity: High

## Display validation errors with @error
Use the @error directive for inline field-level error messages
- **Do:** @error('field') to show per-field messages
- **Don't:** Dump $errors->all() in one block at top of form
- Severity: Medium

## Use CSRF token on all forms
CSRF protection is enabled by default — include @csrf in every form
- **Do:** @csrf in every POST/PUT/PATCH/DELETE form
- **Don't:** Disable VerifyCsrfToken middleware for convenience
- Severity: High

## Use method spoofing for PUT/PATCH/DELETE
HTML forms only support GET/POST — use @method for REST actions
- **Do:** @method('PUT') inside form for update/delete routes
- **Don't:** Route::post for all mutations including updates
- Severity: Medium

## Display flash messages consistently
Flash success/error in controller; read in layout with session()
- **Do:** session('status') in layout for global flash display
- **Don't:** Re-query DB or pass flash from every controller individually
- Severity: Medium

## Eager load relationships to prevent N+1
Always eager load related models used in views with with()
- **Do:** with() in queries before passing collections to views
- **Don't:** Lazy-load relations inside Blade loops
- Severity: High

## Cache rendered Blade fragments
Use cache() helper to wrap expensive rendered partials
- **Do:** cache() around slow partials that change infrequently
- **Don't:** Re-render identical content on every request
- Severity: Medium

## Paginate large data sets
Always paginate collections in list views
- **Do:** ->paginate() or ->simplePaginate() with {{ $items->links() }}
- **Don't:** ->get() for large tables in views
- Severity: High

## Queue slow background tasks
Offload emails notifications and heavy processing to queues
- **Do:** Dispatch jobs for anything taking >200ms
- **Don't:** Block HTTP request with slow operations
- Severity: High

## Use route model binding
Laravel resolves models automatically — avoids manual find()
- **Do:** Type-hint model in controller method
- **Don't:** Manual User::findOrFail($id) in every method
- Severity: Medium

## Enable HTTP response caching for static content
Cache control headers for pages that rarely change
- **Do:** Cache-Control headers via middleware for public pages
- **Don't:** No caching — serve every response fresh
- Severity: Medium

## Escape all output in Blade
{{ }} auto-escapes HTML — never use {!! !!} on user data
- **Do:** {{ }} for all untrusted or dynamic content
- **Don't:** {!! !!} for user-controlled strings
- Severity: High

## Protect routes with Gate and Policy
Use policies for authorization — never inline permission checks in views
- **Do:** @can / Gate::allows() for UI visibility; policy()->authorize() for actions
- **Don't:** Hardcode role checks inline across templates
- Severity: High

## Validate and authorize file uploads
Check MIME type size and store outside public root
- **Do:** Store in storage/app/private + validate mimes and max
- **Don't:** Store raw upload in public/ without validation
- Severity: High

## Use signed URLs for temporary links
Generate expiring URLs for private downloads or email confirmations
- **Do:** URL::signedRoute() or temporarySignedRoute()
- **Don't:** Expose sequential IDs in download URLs without auth
- Severity: High

## Set a strict Content Security Policy
CSP headers prevent XSS injection of external scripts
- **Do:** spatie/laravel-csp or custom middleware to emit CSP header
- **Don't:** No CSP — browser runs any injected script
- Severity: Medium
