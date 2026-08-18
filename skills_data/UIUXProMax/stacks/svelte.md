---
name: svelte Best Practices
source: UIUXProMax
version: 1.0.0
description: 53 curated svelte guidelines (state, perf, a11y, patterns)
tags: ["stack", "svelte"]
triggers: ["svelte"]
license: MIT
target_agent: 
category: tech_stack
---

# svelte — Best Practices (53 guidelines)

## Use $: for reactive statements
Automatic dependency tracking
- **Do:** $: for derived values
- **Don't:** Manual recalculation
- Severity: Medium

## Trigger reactivity with assignment
Svelte tracks assignments not mutations
- **Do:** Reassign arrays/objects to trigger update
- **Don't:** Mutate without reassignment
- Severity: High

## Use $state in Svelte 5
Runes for explicit reactivity
- **Do:** let count = $state(0)
- **Don't:** Implicit reactivity in Svelte 5
- Severity: Medium

## Use $derived for computed values
$derived replaces $: in Svelte 5
- **Do:** let doubled = $derived(count * 2)
- **Don't:** $: in Svelte 5
- Severity: Medium

## Use $effect for side effects
$effect replaces $: side effects
- **Do:** Use $effect for subscriptions
- **Don't:** $: for side effects in Svelte 5
- Severity: Medium

## Export let for props
Declare props with export let
- **Do:** export let propName
- **Don't:** Props without export
- Severity: High

## Use $props in Svelte 5
$props rune for prop access
- **Do:** let { name } = $props()
- **Don't:** export let in Svelte 5
- Severity: Medium

## Provide default values
Default props with assignment
- **Do:** export let count = 0
- **Don't:** Required props without defaults
- Severity: Low

## Use spread props
Pass through unknown props
- **Do:** {...$$restProps} on elements
- **Don't:** Manual prop forwarding
- Severity: Low

## Use bind: for two-way binding
Simplified input handling
- **Do:** bind:value for inputs
- **Don't:** on:input with manual update
- Severity: Low

## Bind to DOM elements
Reference DOM nodes
- **Do:** bind:this for element reference
- **Don't:** querySelector in onMount
- Severity: Medium

## Use bind:group for radios/checkboxes
Simplified group handling
- **Do:** bind:group for radio/checkbox groups
- **Don't:** Manual checked handling
- Severity: Low

## Use on: for event handlers
Event directive syntax
- **Do:** on:click={handler}
- **Don't:** addEventListener in onMount
- Severity: Medium

## Forward events with on:event
Pass events to parent
- **Do:** on:click without handler
- **Don't:** createEventDispatcher for DOM events
- Severity: Low

## Use createEventDispatcher
Custom component events
- **Do:** dispatch for custom events
- **Don't:** on:event for custom events
- Severity: Medium

## Use onMount for initialization
Run code after component mounts
- **Do:** onMount for setup and data fetching
- **Don't:** Code in script body for side effects
- Severity: High

## Return cleanup from onMount
Automatic cleanup on destroy
- **Do:** Return function from onMount
- **Don't:** Separate onDestroy for paired cleanup
- Severity: Medium

## Use onDestroy sparingly
Only when onMount cleanup not possible
- **Do:** onDestroy for non-mount cleanup
- **Don't:** onDestroy for mount-related cleanup
- Severity: Low

## Avoid beforeUpdate/afterUpdate
Usually not needed
- **Do:** Reactive statements instead
- **Don't:** beforeUpdate for derived state
- Severity: Low

## Use writable for mutable state
Basic reactive store
- **Do:** writable for shared mutable state
- **Don't:** Local variables for shared state
- Severity: Medium

## Use readable for read-only state
External data sources
- **Do:** readable for derived/external data
- **Don't:** writable for read-only data
- Severity: Low

## Use derived for computed stores
Combine or transform stores
- **Do:** derived for computed values
- **Don't:** Manual subscription for derived
- Severity: Medium

## Use $ prefix for auto-subscription
Automatic subscribe/unsubscribe
- **Do:** $storeName in components
- **Don't:** Manual subscription
- Severity: High

## Clean up custom subscriptions
Unsubscribe when component destroys
- **Do:** Return unsubscribe from onMount
- **Don't:** Leave subscriptions open
- Severity: High

## Use slots for composition
Content projection
- **Do:** <slot> for flexible content
- **Don't:** Props for all content
- Severity: Medium

## Name slots for multiple areas
Multiple content areas
- **Do:** <slot name="header">
- **Don't:** Single slot for complex layouts
- Severity: Low

## Check slot content with $$slots
Conditional slot rendering
- **Do:** $$slots.name for conditional rendering
- **Don't:** Always render slot wrapper
- Severity: Low

## Use scoped styles by default
Styles scoped to component
- **Do:** <style> for component styles
- **Don't:** Global styles for component
- Severity: Medium

## Use :global() sparingly
Escape scoping when needed
- **Do:** :global for third-party styling
- **Don't:** Global for all styles
- Severity: Medium

## Use CSS variables for theming
Dynamic styling
- **Do:** CSS custom properties
- **Don't:** Inline styles for themes
- Severity: Low

## Use built-in transitions
Svelte transition directives
- **Do:** transition:fade for simple effects
- **Don't:** Manual CSS transitions
- Severity: Low

## Use in: and out: separately
Different enter/exit animations
- **Do:** in:fly out:fade for asymmetric
- **Don't:** Same transition for both
- Severity: Low

## Add local modifier
Prevent ancestor trigger
- **Do:** transition:fade|local
- **Don't:** Global transitions for lists
- Severity: Medium

## Use actions for DOM behavior
Reusable DOM logic
- **Do:** use:action for DOM enhancements
- **Don't:** onMount for each usage
- Severity: Medium

## Return update and destroy
Lifecycle methods for actions
- **Do:** Return { update, destroy }
- **Don't:** Only initial setup
- Severity: Medium

## Pass parameters to actions
Configure action behavior
- **Do:** use:action={params}
- **Don't:** Hardcoded action behavior
- Severity: Low

## Use {#if} for conditionals
Template conditionals
- **Do:** {#if} {:else if} {:else}
- **Don't:** Ternary in expressions
- Severity: Low

## Use {#each} for lists
List rendering
- **Do:** {#each} with key
- **Don't:** Map in expression
- Severity: Medium

## Always use keys in {#each}
Proper list reconciliation
- **Do:** (item.id) for unique key
- **Don't:** Index as key or no key
- Severity: High

## Use {#await} for promises
Handle async states
- **Do:** {#await} for loading/error states
- **Don't:** Manual promise handling
- Severity: Medium

## Use +page.svelte for routes
File-based routing
- **Do:** +page.svelte for route components
- **Don't:** Custom routing setup
- Severity: Medium

## Use +page.js for data loading
Load data before render
- **Do:** load function in +page.js
- **Don't:** onMount for data fetching
- Severity: High

## Use +page.server.js for server-only
Server-side data loading
- **Do:** +page.server.js for sensitive data
- **Don't:** +page.js for API keys
- Severity: High

## Use form actions
Server-side form handling
- **Do:** +page.server.js actions
- **Don't:** API routes for forms
- Severity: Medium

## Use $app/stores for app state
$page $navigating $updated
- **Do:** $page for current page data
- **Don't:** Manual URL parsing
- Severity: Medium

## Use {#key} for forced re-render
Reset component state
- **Do:** {#key id} for fresh instance
- **Don't:** Manual destroy/create
- Severity: Low

## Avoid unnecessary reactivity
Not everything needs $:
- **Do:** $: only for side effects
- **Don't:** $: for simple assignments
- Severity: Low

## Use immutable compiler option
Skip equality checks
- **Do:** immutable: true for large lists
- **Don't:** Default for all components
- Severity: Low

## Use lang="ts" in script
TypeScript support
- **Do:** <script lang="ts">
- **Don't:** JavaScript for typed projects
- Severity: Medium

## Type props with interface
Explicit prop types
- **Do:** interface $$Props for types
- **Don't:** Untyped props
- Severity: Medium

## Type events with createEventDispatcher
Type-safe events
- **Do:** createEventDispatcher<Events>()
- **Don't:** Untyped dispatch
- Severity: Medium

## Use semantic elements
Proper HTML in templates
- **Do:** button nav main appropriately
- **Don't:** div for everything
- Severity: High

## Add aria to dynamic content
Accessible state changes
- **Do:** aria-live for updates
- **Don't:** Silent dynamic updates
- Severity: Medium
