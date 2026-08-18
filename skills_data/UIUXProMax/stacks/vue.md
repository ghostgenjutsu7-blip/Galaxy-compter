---
name: vue Best Practices
source: UIUXProMax
version: 1.0.0
description: 49 curated vue guidelines (state, perf, a11y, patterns)
tags: ["stack", "vue"]
triggers: ["vue"]
license: MIT
target_agent: 
category: tech_stack
---

# vue — Best Practices (49 guidelines)

## Use Composition API for new projects
Composition API offers better TypeScript support and logic reuse
- **Do:** <script setup> for components
- **Don't:** Options API for new projects
- Severity: Medium

## Use script setup syntax
Cleaner syntax with automatic exports
- **Do:** <script setup> with defineProps
- **Don't:** setup() function manually
- Severity: Low

## Use ref for primitives
ref() for primitive values that need reactivity
- **Do:** ref() for strings numbers booleans
- **Don't:** reactive() for primitives
- Severity: Medium

## Use reactive for objects
reactive() for complex objects and arrays
- **Do:** reactive() for objects with multiple properties
- **Don't:** ref() for complex objects
- Severity: Medium

## Access ref values with .value
Remember .value in script unwrap in template
- **Do:** Use .value in script
- **Don't:** Forget .value in script
- Severity: High

## Use computed for derived state
Computed properties cache and update automatically
- **Do:** computed() for derived values
- **Don't:** Methods for derived values
- Severity: Medium

## Use shallowRef for large objects
Avoid deep reactivity for performance
- **Do:** shallowRef for large data structures
- **Don't:** ref for large nested objects
- Severity: Medium

## Use watchEffect for simple cases
Auto-tracks dependencies
- **Do:** watchEffect for simple reactive effects
- **Don't:** watch with explicit deps when not needed
- Severity: Low

## Use watch for specific sources
Explicit control over what to watch
- **Do:** watch with specific refs
- **Don't:** watchEffect for complex conditional logic
- Severity: Medium

## Clean up side effects
Return cleanup function in watchers
- **Do:** Return cleanup in watchEffect
- **Don't:** Leave subscriptions open
- Severity: High

## Define props with defineProps
Type-safe prop definitions
- **Do:** defineProps with TypeScript
- **Don't:** Props without types
- Severity: Medium

## Use withDefaults for default values
Provide defaults for optional props
- **Do:** withDefaults with defineProps
- **Don't:** Defaults in destructuring
- Severity: Medium

## Avoid mutating props
Props should be read-only
- **Do:** Emit events to parent for changes
- **Don't:** Direct prop mutation
- Severity: High

## Define emits with defineEmits
Type-safe event emissions
- **Do:** defineEmits with types
- **Don't:** Emit without definition
- Severity: Medium

## Use v-model for two-way binding
Simplified parent-child data flow
- **Do:** v-model with modelValue prop
- **Don't:** :value + @input manually
- Severity: Low

## Use onMounted for DOM access
DOM is ready in onMounted
- **Do:** onMounted for DOM operations
- **Don't:** Access DOM in setup directly
- Severity: High

## Clean up in onUnmounted
Remove listeners and subscriptions
- **Do:** onUnmounted for cleanup
- **Don't:** Leave listeners attached
- Severity: High

## Avoid onBeforeMount for data
Use onMounted or setup for data fetching
- **Do:** Fetch in onMounted or setup
- **Don't:** Fetch in onBeforeMount
- Severity: Low

## Use single-file components
Keep template script style together
- **Do:** .vue files for components
- **Don't:** Separate template/script files
- Severity: Low

## Use PascalCase for components
Consistent component naming
- **Do:** PascalCase in imports and templates
- **Don't:** kebab-case in script
- Severity: Low

## Prefer composition over mixins
Composables replace mixins
- **Do:** Composables for shared logic
- **Don't:** Mixins for code reuse
- Severity: Medium

## Name composables with use prefix
Convention for composable functions
- **Do:** useFetch useAuth useForm
- **Don't:** getData or fetchApi
- Severity: Medium

## Return refs from composables
Maintain reactivity when destructuring
- **Do:** Return ref values
- **Don't:** Return reactive objects that lose reactivity
- Severity: Medium

## Accept ref or value params
Use toValue for flexible inputs
- **Do:** toValue() or unref() for params
- **Don't:** Only accept ref or only value
- Severity: Low

## Use v-bind shorthand
Cleaner template syntax
- **Do:** :prop instead of v-bind:prop
- **Don't:** Full v-bind syntax
- Severity: Low

## Use v-on shorthand
Cleaner event binding
- **Do:** @event instead of v-on:event
- **Don't:** Full v-on syntax
- Severity: Low

## Avoid v-if with v-for
v-if has higher priority causes issues
- **Do:** Wrap in template or computed filter
- **Don't:** v-if on same element as v-for
- Severity: High

## Use key with v-for
Proper list rendering and updates
- **Do:** Unique key for each item
- **Don't:** Index as key for dynamic lists
- Severity: High

## Use Pinia for global state
Official state management for Vue 3
- **Do:** Pinia stores for shared state
- **Don't:** Vuex for new projects
- Severity: Medium

## Define stores with defineStore
Composition API style stores
- **Do:** Setup stores with defineStore
- **Don't:** Options stores for complex state
- Severity: Low

## Use storeToRefs for destructuring
Maintain reactivity when destructuring
- **Do:** storeToRefs(store)
- **Don't:** Direct destructuring
- Severity: High

## Use useRouter and useRoute
Composition API router access
- **Do:** useRouter() useRoute() in setup
- **Don't:** this.$router this.$route
- Severity: Medium

## Lazy load route components
Code splitting for routes
- **Do:** () => import() for components
- **Don't:** Static imports for all routes
- Severity: Medium

## Use navigation guards
Protect routes and handle redirects
- **Do:** beforeEach for auth checks
- **Don't:** Check auth in each component
- Severity: Medium

## Use v-once for static content
Skip re-renders for static elements
- **Do:** v-once on never-changing content
- **Don't:** v-once on dynamic content
- Severity: Low

## Use v-memo for expensive lists
Memoize list items
- **Do:** v-memo with dependency array
- **Don't:** Re-render entire list always
- Severity: Medium

## Use shallowReactive for flat objects
Avoid deep reactivity overhead
- **Do:** shallowReactive for flat state
- **Don't:** reactive for simple objects
- Severity: Low

## Use defineAsyncComponent
Lazy load heavy components
- **Do:** defineAsyncComponent for modals dialogs
- **Don't:** Import all components eagerly
- Severity: Medium

## Use generic components
Type-safe reusable components
- **Do:** Generic with defineComponent
- **Don't:** Any types in components
- Severity: Medium

## Type template refs
Proper typing for DOM refs
- **Do:** ref<HTMLInputElement>(null)
- **Don't:** ref(null) without type
- Severity: Medium

## Use PropType for complex props
Type complex prop types
- **Do:** PropType<User> for object props
- **Don't:** Object without type
- Severity: Medium

## Use Vue Test Utils
Official testing library
- **Do:** mount shallowMount for components
- **Don't:** Manual DOM testing
- Severity: Medium

## Test component behavior
Focus on inputs and outputs
- **Do:** Test props emit and rendered output
- **Don't:** Test internal implementation
- Severity: Medium

## Use v-model modifiers
Built-in input handling
- **Do:** .lazy .number .trim modifiers
- **Don't:** Manual input parsing
- Severity: Low

## Use VeeValidate or FormKit
Form validation libraries
- **Do:** VeeValidate for complex forms
- **Don't:** Manual validation logic
- Severity: Medium

## Use semantic elements
Proper HTML elements in templates
- **Do:** button nav main for purpose
- **Don't:** div for everything
- Severity: High

## Bind aria attributes dynamically
Keep ARIA in sync with state
- **Do:** :aria-expanded="isOpen"
- **Don't:** Static ARIA values
- Severity: Medium

## Use Nuxt for SSR
Full-featured SSR framework
- **Do:** Nuxt 3 for SSR apps
- **Don't:** Manual SSR setup
- Severity: Medium

## Handle hydration mismatches
Client/server content must match
- **Do:** ClientOnly for browser-only content
- **Don't:** Different content server/client
- Severity: High
