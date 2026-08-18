---
name: angular Best Practices
source: UIUXProMax
version: 1.0.0
description: 50 curated angular guidelines (state, perf, a11y, patterns)
tags: ["stack", "angular"]
triggers: ["angular"]
license: MIT
target_agent: 
category: tech_stack
---

# angular — Best Practices (50 guidelines)

## Use standalone components
Angular 17+ default; no NgModule needed
- **Do:** Standalone components for all new code
- **Don't:** NgModule-based components for new projects
- Severity: High

## Use signals for state
Signals are Angular's reactive primitive for fine-grained reactivity
- **Do:** Signals for component state over class properties
- **Don't:** Mutable class properties without signals
- Severity: High

## Use @if/@for/@switch control flow
Built-in control flow syntax replaces *ngIf/*ngFor directives
- **Do:** @if and @for in templates
- **Don't:** *ngIf and *ngFor structural directives
- Severity: High

## Use input() and output() signals
Signal-based inputs/outputs replace @Input()/@Output() decorators
- **Do:** input() and output() for component API
- **Don't:** @Input() and @Output() decorators
- Severity: High

## Use content projection
ng-content for flexible component composition
- **Do:** ng-content with select for named slots
- **Don't:** Rigid templates that can't be customized
- Severity: Medium

## Keep components small
Single responsibility; components should do one thing
- **Do:** Extract sub-components when template exceeds 50 lines
- **Don't:** Monolithic components handling multiple concerns
- Severity: Medium

## Use OnPush change detection
Reduces re-renders by only checking on input changes or signal updates
- **Do:** OnPush for all components
- **Don't:** Default change detection strategy
- Severity: High

## Avoid direct DOM manipulation
Use renderer or ElementRef sparingly; prefer template bindings
- **Do:** Template bindings and Angular directives
- **Don't:** Direct document.querySelector or innerHTML
- Severity: High

## Lazy load feature routes
Load route chunks on demand to reduce initial bundle
- **Do:** loadComponent() for all feature routes
- **Don't:** Eager-loaded routes in app config
- Severity: High

## Use route guards with functional API
Protect routes with canActivate/canMatch functional guards
- **Do:** Functional guards returning boolean or UrlTree
- **Don't:** Class-based guards with CanActivate interface
- Severity: High

## Use route resolvers for data
Pre-fetch data before route activation using resolve
- **Do:** ResolveFn for route data
- **Don't:** Fetching data in ngOnInit causing flash of empty state
- Severity: Medium

## Type route params with inject
Use inject(ActivatedRoute) with signals or toSignal
- **Do:** Typed route params via ActivatedRoute
- **Don't:** Untyped route.snapshot.params string access
- Severity: Medium

## Use nested routes for layouts
Compose shared layouts using router-outlet nesting
- **Do:** Nested routes with shared layout components
- **Don't:** Duplicating layout code across routes
- Severity: Medium

## Configure preloading strategies
Preload lazy modules in background after initial load
- **Do:** PreloadAllModules or custom strategy
- **Don't:** No preloading causing delayed navigation
- Severity: Low

## Use signals for local state
Signals provide synchronous reactive state without RxJS overhead
- **Do:** signal() for component-local reactive state
- **Don't:** BehaviorSubject for simple local state
- Severity: High

## Use computed() for derived state
Lazily evaluated derived values that update when dependencies change
- **Do:** computed() for values derived from other signals
- **Don't:** Duplicated state or manual sync
- Severity: High

## Use effect() carefully
Effects run side effects when signals change; avoid overuse
- **Do:** effect() for side effects like logging or localStorage sync
- **Don't:** effect() for deriving state (use computed instead)
- Severity: Medium

## Use NgRx Signal Store for complex state
NgRx Signal Store is the modern lightweight state management for Angular
- **Do:** @ngrx/signals SignalStore for feature state
- **Don't:** Full NgRx reducer/action/effect boilerplate for simple state
- Severity: Medium

## Inject services for shared state
Services with signals share state across components without a store
- **Do:** Injectable service with signals for cross-component state
- **Don't:** Prop drilling or @Input chains for shared state
- Severity: Medium

## Avoid mixing RxJS and signals unnecessarily
Use toSignal() to bridge RxJS into signal world at the boundary
- **Do:** toSignal() to convert observable to signal at component edge
- **Don't:** Subscribing in components and storing in signal manually
- Severity: Medium

## Use typed reactive forms
FormGroup/FormControl with explicit generics for compile-time safety
- **Do:** FormBuilder with typed controls
- **Don't:** Untyped FormControl or any casts
- Severity: High

## Use reactive forms over template-driven
Reactive forms scale better and are fully testable
- **Do:** ReactiveFormsModule for all non-trivial forms
- **Don't:** FormsModule with ngModel for complex forms
- Severity: Medium

## Write custom validators as functions
Functional validators are composable and tree-shakeable
- **Do:** ValidatorFn functions for custom validation
- **Don't:** Class-based validators implementing Validator interface
- Severity: Medium

## Use updateOn for performance
Control when validation runs to avoid per-keystroke validation overhead
- **Do:** updateOn: 'blur' or 'submit' for expensive validators
- **Don't:** Default updateOn: 'change' for async validators
- Severity: Low

## Use FormArray for dynamic fields
FormArray manages variable-length lists of controls
- **Do:** FormArray for add/remove field scenarios
- **Don't:** Manually tracking index-based controls
- Severity: Medium

## Display validation errors clearly
Use form control touched and dirty states to show errors at the right time
- **Do:** Show errors after field is touched
- **Don't:** Show all errors on page load
- Severity: Medium

## Apply OnPush to all components
OnPush + signals eliminates most unnecessary change detection cycles
- **Do:** OnPush change detection everywhere
- **Don't:** Default strategy which checks entire tree on every event
- Severity: High

## Use trackBy in @for blocks
Stable identity for list items prevents full DOM re-creation on change
- **Do:** track item.id in @for
- **Don't:** track $index for dynamic data
- Severity: High

## Use @defer for below-the-fold content
Defer blocks lazy-load components when they enter the viewport
- **Do:** @defer with on viewport for non-critical UI
- **Don't:** Eagerly loading all components at startup
- Severity: High

## Use NgOptimizedImage
Enforces image best practices: lazy loading LCP hints and proper sizing
- **Do:** NgOptimizedImage for all img tags
- **Don't:** Plain img tags for CMS or user content
- Severity: High

## Tree-shake unused Angular features
Import only what you use from Angular packages
- **Do:** Import specific Angular modules needed
- **Don't:** Import BrowserAnimationsModule when not using animations
- Severity: Medium

## Avoid subscribe in components
Subscriptions leak and cause bugs; prefer async pipe or toSignal
- **Do:** toSignal() or async pipe instead of manual subscribe
- **Don't:** Manual subscribe without unsubscribe in ngOnDestroy
- Severity: High

## Use SSR with Angular Universal
Pre-render pages for faster LCP and better SEO
- **Do:** SSR or SSG for public-facing routes
- **Don't:** Pure CSR for SEO-critical pages
- Severity: Medium

## Minimize bundle with standalone APIs
Standalone components + provideRouter() eliminate dead NgModule code
- **Do:** provideRouter() and provideHttpClient() in app.config
- **Don't:** Root AppModule with all imports
- Severity: Medium

## Use TestBed for component tests
TestBed sets up Angular DI for realistic component testing
- **Do:** TestBed.configureTestingModule for component tests
- **Don't:** Instantiate components with new keyword
- Severity: High

## Use Angular CDK component harnesses
Harnesses provide a stable testing API that survives template refactors
- **Do:** MatButtonHarness and custom HarnessLoader
- **Don't:** Direct native element queries that break on template changes
- Severity: Medium

## Use Spectator for less boilerplate
Spectator wraps TestBed with a cleaner API reducing test setup noise
- **Do:** Spectator for unit tests
- **Don't:** Raw TestBed for every test
- Severity: Low

## Mock services with jasmine.createSpyObj
Isolate unit tests by providing mock implementations of dependencies
- **Do:** SpyObj or jest.fn() mocks for services
- **Don't:** Real HTTP calls in unit tests
- Severity: High

## Write integration tests for routes
Test full route navigation including guards and resolvers
- **Do:** RouterTestingHarness for route integration tests
- **Don't:** Mock all routing behavior in unit tests
- Severity: Medium

## Test signal-based components
Signals update synchronously; no async flush needed in most cases
- **Do:** Read signal value directly in test assertions
- **Don't:** TestBed.tick() or fakeAsync for signal reads
- Severity: Medium

## Use ViewEncapsulation.Emulated
Default emulation scopes styles to component preventing global leaks
- **Do:** Emulated or None for intentional global styles
- **Don't:** ViewEncapsulation.None for component-specific styles
- Severity: Medium

## Use :host selector
Style the component's host element using :host pseudo-class
- **Do:** :host for host element styles
- **Don't:** Adding wrapper div just for styling
- Severity: Medium

## Use CSS custom properties for theming
CSS variables work across component boundaries and enable dynamic theming
- **Do:** CSS custom properties for colors and spacing
- **Don't:** Hardcoded hex values in component styles
- Severity: Medium

## Integrate Tailwind with Angular
Tailwind utilities work alongside Angular's ViewEncapsulation via global stylesheet
- **Do:** Add Tailwind in styles.css and use utility classes in templates
- **Don't:** Custom CSS for layout that Tailwind already handles
- Severity: Low

## Use Angular Material theming tokens
Material 3 uses design tokens for systematic theming
- **Do:** M3 token-based theming for Angular Material
- **Don't:** Overriding Angular Material CSS with deep selectors
- Severity: Medium

## Use injection tokens for config
Provide configuration via InjectionToken for testability and flexibility
- **Do:** InjectionToken for environment-specific values
- **Don't:** Importing environment.ts directly in services
- Severity: Medium

## Use HTTP interceptors
Intercept requests for auth headers error handling and logging
- **Do:** Functional interceptors with withInterceptors()
- **Don't:** Service-level header management in every request
- Severity: High

## Organize by feature not type
Feature-based folder structure scales better than type-based
- **Do:** Feature folders with collocated component service and routes
- **Don't:** Flat folders: all-components/ all-services/
- Severity: Medium

## Use environment configurations
Separate environment values for dev staging and prod via Angular build configs
- **Do:** angular.json fileReplacements for env configs
- **Don't:** Hardcoded API URLs or feature flags in source
- Severity: High

## Prefer inject() over constructor DI
inject() function is composable and works in more contexts than constructor injection
- **Do:** inject() for dependency injection
- **Don't:** Constructor parameters for new code
- Severity: Medium
