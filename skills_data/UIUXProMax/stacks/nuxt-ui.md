---
name: nuxt-ui Best Practices
source: UIUXProMax
version: 1.0.0
description: 70 curated nuxt-ui guidelines (state, perf, a11y, patterns)
tags: ["stack", "nuxt-ui"]
triggers: ["nuxt-ui"]
license: MIT
target_agent: 
category: tech_stack
---

# nuxt-ui — Best Practices (70 guidelines)

## Add Nuxt UI module
Install and configure Nuxt UI in your Nuxt project
- **Do:** pnpm add @nuxt/ui and add to modules
- **Don't:** Manual component imports
- Severity: High

## Import Tailwind and Nuxt UI CSS
Required CSS imports in main.css file
- **Do:** @import tailwindcss and @import @nuxt/ui
- **Don't:** Skip CSS imports
- Severity: High

## Wrap app with UApp component
UApp provides global configs for Toast Tooltip and overlays
- **Do:** <UApp> wrapper in app.vue
- **Don't:** Skip UApp wrapper
- Severity: High

## Use U prefix for components
All Nuxt UI components use U prefix by default
- **Do:** UButton UInput UModal
- **Don't:** Button Input Modal
- Severity: Medium

## Use semantic color props
Use semantic colors like primary secondary error
- **Do:** color="primary" color="error"
- **Don't:** Hardcoded colors
- Severity: Medium

## Use variant prop for styling
Nuxt UI provides solid outline soft subtle ghost link variants
- **Do:** variant="soft" variant="outline"
- **Don't:** Custom button classes
- Severity: Medium

## Use size prop consistently
Components support xs sm md lg xl sizes
- **Do:** size="sm" size="lg"
- **Don't:** Arbitrary sizing classes
- Severity: Low

## Use i-{collection}-{name} format for icons
Nuxt UI v4 uses Iconify i-prefix format — lucide:home is v3 legacy
- **Do:** i-lucide-home i-heroicons-user format
- **Don't:** lucide:home format (v3 syntax)
- Severity: High

## Use leadingIcon and trailingIcon props
Position icons with dedicated props for clarity
- **Do:** leadingIcon="i-lucide-plus" trailingIcon="i-lucide-arrow-right"
- **Don't:** Manual icon positioning or slots
- Severity: Low

## Configure colors in app.config.ts
Runtime color configuration without restart
- **Do:** ui.colors.primary in app.config.ts
- **Don't:** Hardcoded colors in components
- Severity: High

## Use @theme directive for custom colors
Define design tokens in CSS with Tailwind @theme
- **Do:** @theme { --color-brand-500: #xxx }
- **Don't:** Inline color definitions
- Severity: Medium

## Extend semantic colors in nuxt.config
Register new colors like tertiary in theme.colors
- **Do:** theme.colors array in ui config
- **Don't:** Use undefined colors
- Severity: Medium

## Use UForm with schema validation
UForm supports Zod Yup Joi Valibot schemas
- **Do:** :schema prop with validation schema
- **Don't:** Manual form validation
- Severity: High

## Use UFormField for field wrapper
Provides label error message and validation display
- **Do:** UFormField with name prop
- **Don't:** Manual error handling
- Severity: Medium

## Handle form submit with @submit
UForm emits submit event with validated data
- **Do:** @submit handler on UForm
- **Don't:** @click on submit button
- Severity: Medium

## Use validateOn prop for validation timing
Control when validation triggers (blur change input)
- **Do:** validateOn="['blur']" for performance
- **Don't:** Always validate on input
- Severity: Low

## Use v-model:open for overlay control
Modal Slideover Drawer use v-model:open
- **Do:** v-model:open for controlled state
- **Don't:** Manual show/hide logic
- Severity: Medium

## Use useOverlay composable for programmatic overlays
Open overlays programmatically — v4 API is create().open() not open(Component)
- **Do:** overlay.create(Component).open({ props }) pattern
- **Don't:** v3 overlay.open(Component) pattern (removed in v4)
- Severity: High

## Use title and description props
Built-in header support for overlays
- **Do:** title="Confirm" description="Are you sure?"
- **Don't:** Manual header content
- Severity: Low

## Use UDashboardSidebar for navigation
Provides collapsible resizable sidebar with mobile support
- **Do:** UDashboardSidebar with header default footer slots
- **Don't:** Custom sidebar implementation
- Severity: Medium

## Use UDashboardGroup for layout
Wraps dashboard components with sidebar state management
- **Do:** UDashboardGroup > UDashboardSidebar + UDashboardPanel
- **Don't:** Manual layout flex containers
- Severity: Medium

## Use UDashboardNavbar for top navigation
Responsive navbar with mobile menu support
- **Do:** UDashboardNavbar in dashboard layout
- **Don't:** Custom navbar implementation
- Severity: Low

## Use UTable with data and columns props
Powered by TanStack Table with built-in features
- **Do:** :data and :columns props
- **Don't:** Manual table markup
- Severity: High

## Define columns with accessorKey
Column definitions use accessorKey for data binding
- **Do:** accessorKey: 'email' in column def
- **Don't:** String column names only
- Severity: Medium

## Use cell slot for custom rendering
Customize cell content with scoped slots
- **Do:** #cell-columnName slot
- **Don't:** Override entire table
- Severity: Medium

## Enable sorting with sortable column option
Add sortable: true to column definition
- **Do:** sortable: true in column
- **Don't:** Manual sort implementation
- Severity: Low

## Use UNavigationMenu for nav links
Horizontal or vertical navigation with dropdown support
- **Do:** UNavigationMenu with items array
- **Don't:** Manual nav with v-for
- Severity: Medium

## Use UBreadcrumb for page hierarchy
Automatic breadcrumb with NuxtLink support
- **Do:** :items array with label and to
- **Don't:** Manual breadcrumb links
- Severity: Low

## Use UTabs for tabbed content
Tab navigation with content panels
- **Do:** UTabs with items containing slot content
- **Don't:** Manual tab state
- Severity: Medium

## Use useToast for notifications
Composable for toast notifications
- **Do:** useToast().add({ title description })
- **Don't:** Alert components for toasts
- Severity: High

## Use UAlert for inline messages
Static alert messages with icon and actions
- **Do:** UAlert with title description color
- **Don't:** Toast for static messages
- Severity: Medium

## Use USkeleton for loading states
Placeholder content during data loading
- **Do:** USkeleton with appropriate size
- **Don't:** Spinner for content loading
- Severity: Low

## Use UColorModeButton for theme toggle
Built-in light/dark mode toggle button
- **Do:** UColorModeButton component
- **Don't:** Manual color mode logic
- Severity: Low

## Use UColorModeSelect for theme picker
Dropdown to select system light or dark mode
- **Do:** UColorModeSelect component
- **Don't:** Custom select for theme
- Severity: Low

## Use ui prop for component styling
Override component styles via ui prop
- **Do:** ui prop with slot class overrides
- **Don't:** Global CSS overrides
- Severity: Medium

## Configure default variants in nuxt.config
Set default color and size for all components
- **Do:** theme.defaultVariants in ui config
- **Don't:** Repeat props on every component
- Severity: Medium

## Use app.config.ts for theme overrides
Runtime theme customization
- **Do:** defineAppConfig with ui key
- **Don't:** nuxt.config for runtime values
- Severity: Medium

## Enable component detection
Tree-shake unused component CSS
- **Do:** experimental.componentDetection: true
- **Don't:** Include all component CSS
- Severity: Low

## Use UTable virtualize for large data
Enable virtualization for 1000+ rows
- **Do:** :virtualize prop on UTable
- **Don't:** Render all rows
- Severity: Medium

## Use semantic component props
Components have built-in ARIA support
- **Do:** Use title description label props
- **Don't:** Skip accessibility props
- Severity: Medium

## Use UFormField for form accessibility
Automatic label-input association
- **Do:** UFormField wraps inputs
- **Don't:** Manual id and for attributes
- Severity: High

## Use UContentToc for table of contents
Automatic TOC with active heading highlight
- **Do:** UContentToc with :links
- **Don't:** Manual TOC implementation
- Severity: Low

## Use UContentSearch for docs search
Command palette for documentation search
- **Do:** UContentSearch with Nuxt Content
- **Don't:** Custom search implementation
- Severity: Low

## Use UChatMessages for chat UI
Designed for Vercel AI SDK integration
- **Do:** UChatMessages with messages array
- **Don't:** Custom chat message list
- Severity: Medium

## Use UChatPrompt for input
Enhanced textarea for AI prompts
- **Do:** UChatPrompt with v-model
- **Don't:** Basic textarea
- Severity: Medium

## Use UEditor for rich text
TipTap-based editor with toolbar support
- **Do:** UEditor with v-model:content
- **Don't:** Custom TipTap setup
- Severity: Medium

## Use to prop for navigation
UButton and ULink support NuxtLink to prop
- **Do:** to="/dashboard" for internal links
- **Don't:** href for internal navigation
- Severity: Medium

## Use external prop for outside links
Explicitly mark external links
- **Do:** target="_blank" with external URLs
- **Don't:** Forget rel="noopener"
- Severity: Low

## Use loadingAuto on buttons
Automatic loading state from @click promise
- **Do:** loadingAuto prop on UButton
- **Don't:** Manual loading state
- Severity: Low

## Use UForm loadingAuto
Auto-disable form during submit
- **Do:** loadingAuto on UForm (default true)
- **Don't:** Manual form disabled state
- Severity: Low

## Do not manually add auto-registered modules
Nuxt UI v4 auto-registers @nuxt/icon @nuxt/fonts @nuxtjs/color-mode
- **Do:** Configure via root-level keys in nuxt.config
- **Don't:** Adding them to modules array causes duplicate registration
- Severity: High

## Use official templates to bootstrap projects
Nuxt UI provides starter templates via nuxi init
- **Do:** npx nuxi init -t ui/dashboard for dashboard project
- **Don't:** Manual project setup from scratch
- Severity: Medium

## Install icon collections locally for SSR
Local Iconify JSON prevents network requests and flash
- **Do:** pnpm i @iconify-json/lucide for reliable server rendering
- **Don't:** Rely on remote icon fetching in production
- Severity: Medium

## Override default component icons globally
Components use default icons configurable via appConfig.ui.icons
- **Do:** Set loading close check icons in app.config.ts
- **Don't:** Accept default icons for all components
- Severity: Low

## Use UFileUpload for file input
Built-in drag-drop and preview support
- **Do:** UFileUpload with v-model and accept prop
- **Don't:** Custom input type=file
- Severity: Medium

## Use UInputDate for date selection
Locale-aware date picker built on UCalendar
- **Do:** UInputDate with v-model and locale prop
- **Don't:** Third-party date picker libraries
- Severity: Medium

## Use UInputTags for tag input
Multi-value tag input with keyboard support
- **Do:** UInputTags with v-model and max prop
- **Don't:** Custom chip input implementation
- Severity: Low

## Use UColorPicker for color selection
Full-featured color picker with multiple format support
- **Do:** UColorPicker with v-model and format prop
- **Don't:** Native input type=color
- Severity: Low

## Use UTree for hierarchical data
Built-in tree component with expand/collapse
- **Do:** UTree with items prop containing nested children
- **Don't:** Custom recursive component
- Severity: Low

## Use UMarquee for infinite scroll content
Animated infinite scroll band for logos or testimonials
- **Do:** UMarquee with repeat and pauseOnHover props
- **Don't:** CSS animation keyframes loop
- Severity: Low

## Use UContextMenu for right-click menus
Context menu triggered by right-click on children
- **Do:** UContextMenu wrapping target element
- **Don't:** Browser default context menu
- Severity: Medium

## Await overlay result for confirmation dialogs
useOverlay returns a result Promise resolving to user action
- **Do:** await instance.result to get confirm/cancel
- **Don't:** Emit events from overlay components
- Severity: Medium

## Use UCommandPalette with grouped items
Command palette supports grouped search with icons and kbds
- **Do:** groups array with id label items
- **Don't:** Flat list without categories
- Severity: Medium

## Use defineShortcuts with extractShortcuts
Wire keyboard shortcuts from menu item kbds automatically
- **Do:** extractShortcuts(items) + defineShortcuts to sync keybindings
- **Don't:** Manually duplicate shortcuts from menu items
- Severity: Low

## Use UHeader and UFooter for page layout
Responsive header/footer with built-in mobile menu
- **Do:** UHeader with #default slot for nav UFooter with columns
- **Don't:** Custom header/footer from scratch
- Severity: Low

## Use UPageAside for sidebar content
Sidebar that hides below lg breakpoint automatically
- **Do:** UPageAside for docs and landing page sidebars
- **Don't:** Manual hidden lg: classes
- Severity: Low

## Wrap custom color mode toggles in ClientOnly
Prevents hydration mismatch on server-rendered color mode
- **Do:** ClientOnly with fallback placeholder
- **Don't:** Direct useColorMode in template without ClientOnly
- Severity: Medium

## Read generated theme file to find slot names
Nuxt UI generates theme files listing all component slots and variants
- **Do:** Check .nuxt/ui/<component>.ts for slot names
- **Don't:** Guess slot names or use trial-and-error
- Severity: Medium

## Use defineShortcuts whenever keyword shortcut
whenever array condition prevents shortcut firing when inactive
- **Do:** whenever: [isFormValid] to guard shortcut execution
- **Don't:** Always-on shortcuts that fire in wrong context
- Severity: Low

## Use UApp locale prop for internationalization
Nuxt UI supports 50+ built-in locales via locale prop on UApp
- **Do:** Import locale from @nuxt/ui/locale and pass to UApp
- **Don't:** Manual translation of component UI strings
- Severity: Low
