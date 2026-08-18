---
name: flutter Best Practices
source: UIUXProMax
version: 1.0.0
description: 52 curated flutter guidelines (state, perf, a11y, patterns)
tags: ["stack", "flutter"]
triggers: ["flutter"]
license: MIT
target_agent: 
category: tech_stack
---

# flutter — Best Practices (52 guidelines)

## Use StatelessWidget when possible
Immutable widgets are simpler
- **Do:** StatelessWidget for static UI
- **Don't:** StatefulWidget for everything
- Severity: Medium

## Keep widgets small
Single responsibility principle
- **Do:** Extract widgets into smaller pieces
- **Don't:** Large build methods
- Severity: Medium

## Use const constructors
Compile-time constants for performance
- **Do:** const MyWidget() when possible
- **Don't:** Non-const for static widgets
- Severity: High

## Prefer composition over inheritance
Combine widgets using children
- **Do:** Compose widgets
- **Don't:** Extend widget classes
- Severity: Medium

## Use setState correctly
Minimal state in StatefulWidget
- **Do:** setState for UI state changes
- **Don't:** setState for business logic
- Severity: Medium

## Avoid setState in build
Never call setState during build
- **Do:** setState in callbacks only
- **Don't:** setState in build method
- Severity: High

## Use state management for complex apps
Provider Riverpod BLoC
- **Do:** State management for shared state
- **Don't:** setState for global state
- Severity: Medium

## Prefer Riverpod or Provider
Recommended state solutions
- **Do:** Riverpod for new projects
- **Don't:** InheritedWidget manually
- Severity: Medium

## Dispose resources
Clean up controllers and subscriptions
- **Do:** dispose() for cleanup
- **Don't:** Memory leaks from subscriptions
- Severity: High

## Use Column and Row
Basic layout widgets
- **Do:** Column Row for linear layouts
- **Don't:** Stack for simple layouts
- Severity: Medium

## Use Expanded and Flexible
Control flex behavior
- **Do:** Expanded to fill space
- **Don't:** Fixed sizes in flex containers
- Severity: Medium

## Use SizedBox for spacing
Consistent spacing
- **Do:** SizedBox for gaps
- **Don't:** Container for spacing only
- Severity: Low

## Use LayoutBuilder for responsive
Respond to constraints
- **Do:** LayoutBuilder for adaptive layouts
- **Don't:** Fixed sizes for responsive
- Severity: Medium

## Avoid deep nesting
Keep widget tree shallow
- **Do:** Extract deeply nested widgets
- **Don't:** 10+ levels of nesting
- Severity: Medium

## Use ListView.builder
Lazy list building
- **Do:** ListView.builder for long lists
- **Don't:** ListView with children for large lists
- Severity: High

## Provide itemExtent when known
Skip measurement
- **Do:** itemExtent for fixed height items
- **Don't:** No itemExtent for uniform lists
- Severity: Medium

## Use keys for stateful items
Preserve widget state
- **Do:** Key for stateful list items
- **Don't:** No key for dynamic lists
- Severity: High

## Use SliverList for custom scroll
Custom scroll effects
- **Do:** CustomScrollView with Slivers
- **Don't:** Nested ListViews
- Severity: Medium

## Use Navigator 2.0 or GoRouter
Declarative routing
- **Do:** go_router for navigation
- **Don't:** Navigator.push for complex apps
- Severity: Medium

## Use named routes
Organized navigation
- **Do:** Named routes for clarity
- **Don't:** Anonymous routes
- Severity: Low

## Handle back button (PopScope)
Android back behavior and predictive back (Android 14+)
- **Do:** Use PopScope widget (WillPopScope is deprecated)
- **Don't:** Use WillPopScope
- Severity: High

## Pass typed arguments
Type-safe route arguments
- **Do:** Typed route arguments
- **Don't:** Dynamic arguments
- Severity: Medium

## Use FutureBuilder
Async UI building
- **Do:** FutureBuilder for async data
- **Don't:** setState for async
- Severity: Medium

## Use StreamBuilder
Stream UI building
- **Do:** StreamBuilder for streams
- **Don't:** Manual stream subscription
- Severity: Medium

## Handle loading and error states
Complete async UI states
- **Do:** ConnectionState checks
- **Don't:** Only success state
- Severity: High

## Cancel subscriptions
Clean up stream subscriptions
- **Do:** Cancel in dispose
- **Don't:** Memory leaks
- Severity: High

## Use ThemeData
Consistent theming
- **Do:** ThemeData for app theme
- **Don't:** Hardcoded colors
- Severity: Medium

## Use ColorScheme
Material 3 color system
- **Do:** ColorScheme for colors
- **Don't:** Individual color properties
- Severity: Medium

## Access theme via context
Dynamic theme access
- **Do:** Theme.of(context)
- **Don't:** Static theme reference
- Severity: Medium

## Support dark mode
Respect system theme
- **Do:** darkTheme in MaterialApp
- **Don't:** Light theme only
- Severity: Medium

## Use implicit animations
Simple animations
- **Do:** AnimatedContainer AnimatedOpacity
- **Don't:** Explicit for simple transitions
- Severity: Low

## Use AnimationController for complex
Fine-grained control
- **Do:** AnimationController with Ticker
- **Don't:** Implicit for complex sequences
- Severity: Medium

## Dispose AnimationControllers
Clean up animation resources
- **Do:** dispose() for controllers
- **Don't:** Memory leaks
- Severity: High

## Use Hero for transitions
Shared element transitions
- **Do:** Hero for navigation animations
- **Don't:** Manual shared element
- Severity: Low

## Use Form widget
Form validation
- **Do:** Form with GlobalKey
- **Don't:** Individual validation
- Severity: Medium

## Use TextEditingController
Control text input
- **Do:** Controller for text fields
- **Don't:** onChanged for all text
- Severity: Medium

## Validate on submit
Form validation flow
- **Do:** _formKey.currentState!.validate()
- **Don't:** Skip validation
- Severity: High

## Dispose controllers
Clean up text controllers
- **Do:** dispose() for controllers
- **Don't:** Memory leaks
- Severity: High

## Use const widgets
Reduce rebuilds
- **Do:** const for static widgets
- **Don't:** No const for literals
- Severity: High

## Avoid rebuilding entire tree
Minimal rebuild scope
- **Do:** Isolate changing widgets
- **Don't:** setState on parent
- Severity: High

## Use RepaintBoundary
Isolate repaints
- **Do:** RepaintBoundary for animations
- **Don't:** Full screen repaints
- Severity: Medium

## Profile with DevTools
Measure before optimizing
- **Do:** Flutter DevTools profiling
- **Don't:** Guess at performance
- Severity: Medium

## Use Semantics widget
Screen reader support
- **Do:** Semantics for accessibility
- **Don't:** Missing accessibility info
- Severity: High

## Support large fonts
MediaQuery text scaling
- **Do:** MediaQuery.textScaleFactor
- **Don't:** Fixed font sizes
- Severity: High

## Test with screen readers
TalkBack and VoiceOver
- **Do:** Test accessibility regularly
- **Don't:** Skip accessibility testing
- Severity: High

## Use widget tests
Test widget behavior
- **Do:** WidgetTester for UI tests
- **Don't:** Unit tests only
- Severity: Medium

## Use integration tests
Full app testing
- **Do:** integration_test package
- **Don't:** Manual testing only
- Severity: Medium

## Mock dependencies
Isolate tests
- **Do:** Mockito or mocktail
- **Don't:** Real dependencies in tests
- Severity: Medium

## Use Platform checks
Platform-specific code
- **Do:** Platform.isIOS Platform.isAndroid
- **Don't:** Same code for all platforms
- Severity: Medium

## Use kIsWeb for web
Web platform detection
- **Do:** kIsWeb for web checks
- **Don't:** Platform for web
- Severity: Medium

## Use pub.dev packages
Community packages
- **Do:** Popular maintained packages
- **Don't:** Custom implementations
- Severity: Medium

## Check package quality
Quality before adding
- **Do:** Pub points and popularity
- **Don't:** Any package without review
- Severity: Medium
