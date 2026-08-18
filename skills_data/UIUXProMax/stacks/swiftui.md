---
name: swiftui Best Practices
source: UIUXProMax
version: 1.0.0
description: 50 curated swiftui guidelines (state, perf, a11y, patterns)
tags: ["stack", "swiftui"]
triggers: ["swiftui"]
license: MIT
target_agent: 
category: tech_stack
---

# swiftui — Best Practices (50 guidelines)

## Use struct for views
SwiftUI views are value types
- **Do:** struct MyView: View
- **Don't:** class MyView: View
- Severity: High

## Keep views small and focused
Single responsibility for each view
- **Do:** Extract subviews for complex layouts
- **Don't:** Large monolithic views
- Severity: Medium

## Use body computed property
body returns the view hierarchy
- **Do:** var body: some View { }
- **Don't:** func body() -> some View
- Severity: High

## Prefer composition over inheritance
Compose views using ViewBuilder
- **Do:** Combine smaller views
- **Don't:** Inheritance hierarchies
- Severity: Medium

## Use @State for local state
Simple value types owned by view
- **Do:** @State for view-local primitives
- **Don't:** @State for shared data
- Severity: High

## Use @Binding for two-way data
Pass mutable state to child views
- **Do:** @Binding for child input
- **Don't:** @State in child for parent data
- Severity: Medium

## Use @StateObject for reference types
ObservableObject owned by view
- **Do:** @StateObject for view-created objects
- **Don't:** @ObservedObject for owned objects
- Severity: High

## Use @ObservedObject for injected objects
Reference types passed from parent
- **Do:** @ObservedObject for injected dependencies
- **Don't:** @StateObject for injected objects
- Severity: High

## Use @EnvironmentObject for shared state
App-wide state injection
- **Do:** @EnvironmentObject for global state
- **Don't:** Prop drilling through views
- Severity: Medium

## Use @Published in ObservableObject
Automatically publish property changes
- **Do:** @Published for observed properties
- **Don't:** Manual objectWillChange calls
- Severity: Medium

## Use @Observable macro (iOS 17+)
Modern observation without Combine
- **Do:** @Observable class for view models
- **Don't:** ObservableObject for new projects
- Severity: Medium

## Use @Bindable for @Observable
Create bindings from @Observable
- **Do:** @Bindable var vm for bindings
- **Don't:** @Binding with @Observable
- Severity: Medium

## Use VStack HStack ZStack
Standard stack-based layouts
- **Do:** Stacks for linear arrangements
- **Don't:** GeometryReader for simple layouts
- Severity: Medium

## Use LazyVStack LazyHStack for lists
Lazy loading for performance
- **Do:** Lazy stacks for long lists
- **Don't:** Regular stacks for 100+ items
- Severity: High

## Use GeometryReader sparingly
Only when needed for sizing
- **Do:** GeometryReader for responsive layouts
- **Don't:** GeometryReader everywhere
- Severity: Medium

## Use spacing and padding consistently
Consistent spacing throughout app
- **Do:** Design system spacing values
- **Don't:** Magic numbers for spacing
- Severity: Low

## Use frame modifiers correctly
Set explicit sizes when needed
- **Do:** .frame(maxWidth: .infinity)
- **Don't:** Fixed sizes for responsive content
- Severity: Medium

## Order modifiers correctly
Modifier order affects rendering
- **Do:** Background before padding for full coverage
- **Don't:** Wrong modifier order
- Severity: High

## Create custom ViewModifiers
Reusable modifier combinations
- **Do:** ViewModifier for repeated styling
- **Don't:** Duplicate modifier chains
- Severity: Medium

## Use conditional modifiers carefully
Avoid changing view identity
- **Do:** if-else with same view type
- **Don't:** Conditional that changes view identity
- Severity: Medium

## Use NavigationStack (iOS 16+)
Modern navigation with type-safe paths
- **Do:** NavigationStack with navigationDestination
- **Don't:** NavigationView for new projects
- Severity: Medium

## Use navigationDestination
Type-safe navigation destinations
- **Do:** .navigationDestination(for:)
- **Don't:** NavigationLink(destination:)
- Severity: Medium

## Use @Environment for dismiss
Programmatic navigation dismissal
- **Do:** @Environment(\.dismiss) var dismiss
- **Don't:** presentationMode (deprecated)
- Severity: Low

## Use List for scrollable content
Built-in scrolling and styling
- **Do:** List for standard scrollable content
- **Don't:** ScrollView + VStack for simple lists
- Severity: Low

## Provide stable identifiers
Use Identifiable or explicit id
- **Do:** Identifiable protocol or id parameter
- **Don't:** Index as identifier
- Severity: High

## Use onDelete and onMove
Standard list editing
- **Do:** onDelete for swipe to delete
- **Don't:** Custom delete implementation
- Severity: Low

## Use Form for settings
Grouped input controls
- **Do:** Form for settings screens
- **Don't:** Manual grouping for forms
- Severity: Low

## Use @FocusState for keyboard
Manage keyboard focus
- **Do:** @FocusState for text field focus
- **Don't:** Manual first responder handling
- Severity: Medium

## Validate input properly
Show validation feedback
- **Do:** Real-time validation feedback
- **Don't:** Submit without validation
- Severity: Medium

## Use .task for async work
Automatic cancellation on view disappear
- **Do:** .task for view lifecycle async
- **Don't:** onAppear with Task
- Severity: Medium

## Handle loading states
Show progress during async operations
- **Do:** ProgressView during loading
- **Don't:** Empty view during load
- Severity: Medium

## Use @MainActor for UI updates
Ensure UI updates on main thread
- **Do:** @MainActor on view models
- **Don't:** Manual DispatchQueue.main
- Severity: Medium

## Use withAnimation
Animate state changes
- **Do:** withAnimation for state transitions
- **Don't:** No animation for state changes
- Severity: Low

## Use .animation modifier
Apply animations to views
- **Do:** .animation(.spring()) on view
- **Don't:** Manual animation timing
- Severity: Low

## Respect reduced motion
Check accessibility settings
- **Do:** Check accessibilityReduceMotion
- **Don't:** Ignore motion preferences
- Severity: High

## Use #Preview macro (Xcode 15+)
Modern preview syntax
- **Do:** #Preview for view previews
- **Don't:** PreviewProvider protocol
- Severity: Low

## Create multiple previews
Test different states and devices
- **Do:** Multiple previews for states
- **Don't:** Single preview only
- Severity: Low

## Use preview data
Dedicated preview mock data
- **Do:** Static preview data
- **Don't:** Production data in previews
- Severity: Low

## Avoid expensive body computations
Body should be fast to compute
- **Do:** Precompute in view model
- **Don't:** Heavy computation in body
- Severity: High

## Use Equatable views
Skip unnecessary view updates
- **Do:** Equatable for complex views
- **Don't:** Default equality for all views
- Severity: Medium

## Profile with Instruments
Measure before optimizing
- **Do:** Use SwiftUI Instruments
- **Don't:** Guess at performance issues
- Severity: Medium

## Add accessibility labels
Describe UI elements
- **Do:** .accessibilityLabel for context
- **Don't:** Missing labels
- Severity: High

## Support Dynamic Type
Respect text size preferences
- **Do:** Scalable fonts and layouts
- **Don't:** Fixed font sizes
- Severity: High

## Use semantic views
Proper accessibility traits
- **Do:** Correct accessibilityTraits
- **Don't:** Wrong semantic meaning
- Severity: Medium

## Use ViewInspector for testing
Third-party view testing
- **Do:** ViewInspector for unit tests
- **Don't:** UI tests only
- Severity: Medium

## Test view models
Unit test business logic
- **Do:** XCTest for view model
- **Don't:** Skip view model testing
- Severity: Medium

## Use preview as visual test
Previews catch visual regressions
- **Do:** Multiple preview configurations
- **Don't:** No visual verification
- Severity: Low

## Use MVVM pattern
Separate view and logic
- **Do:** ViewModel for business logic
- **Don't:** Logic in View
- Severity: Medium

## Keep views dumb
Views display view model state
- **Do:** View reads from ViewModel
- **Don't:** Business logic in View
- Severity: Medium

## Use dependency injection
Inject dependencies for testing
- **Do:** Initialize with dependencies
- **Don't:** Hard-coded dependencies
- Severity: Medium
