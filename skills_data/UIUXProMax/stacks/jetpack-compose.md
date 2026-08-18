---
name: jetpack-compose Best Practices
source: UIUXProMax
version: 1.0.0
description: 52 curated jetpack-compose guidelines (state, perf, a11y, patterns)
tags: ["stack", "jetpack-compose"]
triggers: ["jetpack-compose"]
license: MIT
target_agent: 
category: tech_stack
---

# jetpack-compose — Best Practices (52 guidelines)

## Pure UI composables
Composable functions should only render UI
- **Do:** Accept state and callbacks
- **Don't:** Calling usecase/repo
- Severity: High

## Small composables
Each composable has single responsibility
- **Do:** Split into components
- **Don't:** Huge composable
- Severity: Medium

## Stateless by default
Prefer stateless composables
- **Do:** Hoist state
- **Don't:** Local mutable state
- Severity: High

## Single source of truth
UI state comes from one source
- **Do:** StateFlow from VM
- **Don't:** Multiple states
- Severity: High

## Model UI State
Use sealed interface/data class
- **Do:** UiState.Loading
- **Don't:** Boolean flags
- Severity: High

## remember only UI state
remember for UI-only state
- **Do:** Scroll, animation
- **Don't:** Business state
- Severity: High

## rememberSaveable
Persist state across config
- **Do:** rememberSaveable
- **Don't:** remember
- Severity: High

## derivedStateOf
Optimize recomposition
- **Do:** derivedStateOf
- **Don't:** Recompute always
- Severity: Medium

## LaunchedEffect keys
Use correct keys
- **Do:** LaunchedEffect(id)
- **Don't:** LaunchedEffect(Unit)
- Severity: High

## rememberUpdatedState
Avoid stale lambdas
- **Do:** rememberUpdatedState
- **Don't:** Capture directly
- Severity: Medium

## DisposableEffect
Clean up resources
- **Do:** onDispose
- **Don't:** No cleanup
- Severity: High

## Unidirectional data flow
UI → VM → State
- **Do:** onEvent
- **Don't:** Two-way binding
- Severity: High

## No business logic in UI
Logic belongs to VM
- **Do:** Collect state
- **Don't:** Call repo
- Severity: High

## Expose immutable state
Expose StateFlow
- **Do:** asStateFlow
- **Don't:** Mutable exposed
- Severity: High

## Lifecycle-aware collect
Use collectAsStateWithLifecycle
- **Do:** Lifecycle aware
- **Don't:** collectAsState
- Severity: High

## Event-based navigation
VM emits navigation event
- **Do:** VM: Channel + receiveAsFlow(), V: Collect with Dispatchers.Main.immediate
- **Don't:** Nav in UI
- Severity: High

## Typed routes
Use sealed routes
- **Do:** sealed class Route
- **Don't:** String routes
- Severity: Medium

## Stable parameters
Prefer immutable/stable params
- **Do:** @Immutable
- **Don't:** Mutable params
- Severity: High

## Use key in Lazy
Provide stable keys
- **Do:** key=id
- **Don't:** No key
- Severity: High

## Avoid heavy work
No heavy computation in UI
- **Do:** Precompute in VM
- **Don't:** Compute in UI
- Severity: High

## Remember expensive objects
remember heavy objects
- **Do:** remember
- **Don't:** Recreate each recomposition
- Severity: Medium

## Design system
Centralized theme
- **Do:** Material3 tokens
- **Don't:** Hardcoded values
- Severity: High

## Dark mode support
Theme-based colors
- **Do:** colorScheme
- **Don't:** Fixed color
- Severity: Medium

## Prefer Modifier over extra layouts
Use Modifier to adjust layout instead of adding wrapper composables
- **Do:** Use Modifier.padding()
- **Don't:** Wrap content with extra Box
- Severity: High

## Avoid deep layout nesting
Deep layout trees increase measure & layout cost
- **Do:** Keep layout flat
- **Don't:** Box ? Column ? Box ? Row
- Severity: High

## Use Row/Column for linear layout
Linear layouts are simpler and more performant
- **Do:** Use Row / Column
- **Don't:** Custom layout for simple cases
- Severity: High

## Use Box only for overlapping content
Box should be used only when children overlap
- **Do:** Stack elements
- **Don't:** Use Box as Column
- Severity: Medium

## Prefer LazyColumn over Column scroll
Lazy layouts are virtualized and efficient
- **Do:** LazyColumn
- **Don't:** Column.verticalScroll()
- Severity: High

## Avoid nested scroll containers
Nested scrolling causes UX & performance issues
- **Do:** Single scroll container
- **Don't:** Scroll inside scroll
- Severity: High

## Avoid fillMaxSize by default
fillMaxSize may break parent constraints
- **Do:** Use exact size
- **Don't:** Fill max everywhere
- Severity: Medium

## Avoid intrinsic size unless necessary
Intrinsic measurement is expensive
- **Do:** Explicit sizing
- **Don't:** IntrinsicSize.Min
- Severity: High

## Use Arrangement and Alignment APIs
Declare layout intent explicitly
- **Do:** Use Arrangement / Alignment
- **Don't:** Manual spacing hacks
- Severity: High

## Extract reusable layout patterns
Repeated layouts should be shared
- **Do:** Create layout composable
- **Don't:** Copy-paste layouts
- Severity: High

## No hardcoded text style
Use typography
- **Do:** MaterialTheme.typography
- **Don't:** Hardcode sp
- Severity: Medium

## Stateless UI testing
Composable easy to test
- **Do:** Pass state
- **Don't:** Hidden state
- Severity: High

## Use testTag
Stable UI selectors
- **Do:** Modifier.testTag
- **Don't:** Find by text
- Severity: Medium

## Multiple previews
Preview multiple states
- **Do:** @Preview
- **Don't:** Single preview
- Severity: Low

## Inject VM via Hilt
Use hiltViewModel
- **Do:** @HiltViewModel
- **Don't:** Manual VM
- Severity: High

## No DI in UI
Inject in VM
- **Do:** Constructor inject
- **Don't:** Inject composable
- Severity: High

## Content description
Accessible UI
- **Do:** contentDescription
- **Don't:** Ignore a11y
- Severity: Medium

## Semantics
Use semantics API
- **Do:** Modifier.semantics
- **Don't:** None
- Severity: Medium

## Compose animation APIs
Use animate*AsState
- **Do:** AnimatedVisibility
- **Don't:** Manual anim
- Severity: Medium

## Avoid animation logic in VM
Animation is UI concern
- **Do:** Animate in UI
- **Don't:** Animate in VM
- Severity: Low

## Feature-based UI modules
UI per feature
- **Do:** :feature:ui
- **Don't:** God module
- Severity: High

## Public UI contracts
Expose minimal UI API
- **Do:** Interface/Route
- **Don't:** Expose impl
- Severity: Medium

## Snapshot state only
Use Compose state
- **Do:** mutableStateOf
- **Don't:** Custom observable
- Severity: Medium

## Avoid mutable collections
Immutable list/map
- **Do:** PersistentList
- **Don't:** MutableList
- Severity: High

## RememberCoroutineScope usage
Only for UI jobs
- **Do:** UI coroutine
- **Don't:** Long jobs
- Severity: Medium

## Interop View carefully
Use AndroidView
- **Do:** Isolated usage
- **Don't:** Mix everywhere
- Severity: Low

## Avoid legacy patterns
No LiveData in UI
- **Do:** StateFlow
- **Don't:** LiveData
- Severity: Medium

## Use layout inspector
Inspect recomposition
- **Do:** Tools
- **Don't:** Blind debug
- Severity: Low

## Enable recomposition counts
Track recomposition
- **Do:** Debug flags
- **Don't:** Ignore
- Severity: Low
