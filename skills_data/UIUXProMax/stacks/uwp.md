---
name: uwp Best Practices
source: UIUXProMax
version: 1.0.0
description: 55 curated uwp guidelines (state, perf, a11y, patterns)
tags: ["stack", "uwp"]
triggers: ["uwp"]
license: MIT
target_agent: 
category: tech_stack
---

# uwp — Best Practices (55 guidelines)

## Use x:Bind for compiled bindings
Compile-time validated bindings with better performance
- **Do:** x:Bind for type-safe performant bindings
- **Don't:** {Binding} when x:Bind is available
- Severity: High

## Use x:Load for deferred elements
Delay creation of elements until needed
- **Do:** x:Load=False for hidden or conditional panels
- **Don't:** Loading all UI elements at page load
- Severity: Medium

## Use x:Phase for incremental item rendering
Render list items in priority phases
- **Do:** x:Phase on secondary content in item DataTemplates
- **Don't:** All template content loaded in one pass
- Severity: Medium

## Use x:DefaultBindMode
Reduce repetitive Mode= declarations
- **Do:** x:DefaultBindMode=OneWay on containers
- **Don't:** Mode=OneWay on every individual x:Bind
- Severity: Low

## Use x:DeferLoadStrategy for legacy support
Deferred loading before x:Load was available
- **Do:** x:Load (preferred) or x:DeferLoadStrategy=Lazy
- **Don't:** Eagerly loading rarely shown UI
- Severity: Low

## Use NavigationView for app shell
Standard UWP navigation pattern with hamburger menu
- **Do:** NavigationView for top-level navigation
- **Don't:** Custom SplitView hamburger menu
- Severity: High

## Use CommandBar for app actions
Standard app bar for primary commands
- **Do:** CommandBar with AppBarButtons
- **Don't:** Custom StackPanel toolbar
- Severity: Medium

## Use ContentDialog for modals
System-styled modal dialogs
- **Do:** ContentDialog for confirmations and input
- **Don't:** Custom popup overlays
- Severity: Medium

## Use AutoSuggestBox for search
Built-in search box with suggestions
- **Do:** AutoSuggestBox with QuerySubmitted and SuggestionChosen
- **Don't:** TextBox with manual suggestion popup
- Severity: Medium

## Use CalendarDatePicker and TimePicker
Platform-consistent date and time selection
- **Do:** Built-in date and time pickers
- **Don't:** Custom date selection controls
- Severity: Low

## Use PersonPicture for user avatars
Consistent avatar display with fallback initials
- **Do:** PersonPicture with DisplayName and ProfilePicture
- **Don't:** Custom Ellipse with ImageBrush for avatars
- Severity: Low

## Use ThemeResource for adaptive colors
Colors that switch with light and dark theme
- **Do:** ThemeResource for all color references
- **Don't:** Hardcoded hex values that break in dark mode
- Severity: High

## Use Fluent Design materials
Acrylic translucent material for depth
- **Do:** Built-in Fluent materials for depth and motion
- **Don't:** Custom shader effects for blur and reveal
- Severity: Medium

## Use Lightweight Styling
Override control resource keys for subtle changes
- **Do:** Lightweight styling resource overrides
- **Don't:** Full ControlTemplate copy for small tweaks
- Severity: Medium

## Use implicit styles for consistency
TargetType without x:Key applies to all instances
- **Do:** Implicit Style for default control appearance
- **Don't:** Repeating Setters on every control instance
- Severity: Medium

## Use VisualStateManager for visual states
Define visual states with Setters that change properties when triggered
- **Do:** VisualStateGroup containing VisualStates with Setter targets
- **Don't:** Toggling Visibility from code-behind on SizeChanged
- Severity: High

## Use Frame for page navigation
Windows.UI.Xaml.Controls.Frame for UWP page navigation
- **Do:** Frame.Navigate with typed parameters
- **Don't:** Swapping UserControls manually
- Severity: Medium

## Handle back button correctly
Provide an in-app Back button styled with NavigationBackButtonNormalStyle and handle SystemNavigationManager.BackRequested for hardware back gamepad B and Tablet-Mode back; also handle CoreDispatcher.AcceleratorKeyActivated for Alt+Left
- **Do:** In-app NavigationBackButtonNormalStyle button plus SystemNavigationManager.BackRequested handler
- **Don't:** Relying on the deprecated title-bar back button (AppViewBackButtonVisibility) or ignoring system back signals
- Severity: High

## Support deep linking with protocol activation
Respond to URI activation and toast taps
- **Do:** OnActivated handler with proper page routing
- **Don't:** Ignoring activation arguments
- Severity: Medium

## Use ConnectedAnimations for continuity
Smooth transitions between pages
- **Do:** ConnectedAnimationService for shared element transitions
- **Don't:** Abrupt page transitions with no visual continuity
- Severity: Low

## Implement INotifyPropertyChanged
Enable UI updates on property changes
- **Do:** INotifyPropertyChanged on all ViewModels
- **Don't:** Auto-properties without notification
- Severity: High

## Use ObservableCollection for lists
Collection change notifications for ItemsSources
- **Do:** ObservableCollection<T> for bound lists
- **Don't:** List<T> for data-bound collections
- Severity: High

## Use function bindings with x:Bind
Call static methods directly in markup
- **Do:** x:Bind to static converter methods
- **Don't:** IValueConverter for trivial transforms
- Severity: Medium

## Specify Mode on x:Bind
x:Bind defaults to OneTime not OneWay
- **Do:** Mode=OneWay or TwoWay when live updates needed
- **Don't:** Omitting Mode and getting stale UI
- Severity: High

## Use CollectionViewSource for grouping
Group and sort collections declaratively
- **Do:** CollectionViewSource for grouped ListView and GridView
- **Don't:** Manual grouping logic in code-behind
- Severity: Medium

## Use ListView and GridView virtualization
Only creates containers for visible items
- **Do:** Default virtualization in ListView and GridView
- **Don't:** Setting ItemsPanel to non-virtualizing panel
- Severity: High

## Use ISupportIncrementalLoading
Load data on demand as user scrolls
- **Do:** ISupportIncrementalLoading for large datasets
- **Don't:** Loading entire collection upfront
- Severity: Medium

## Reduce XAML visual tree depth
Simpler trees layout and render faster
- **Do:** Flat templates with minimal nesting
- **Don't:** Deeply nested panels in DataTemplates
- Severity: Medium

## Use compiled bindings in DataTemplates
x:Bind in templates requires x:DataType
- **Do:** x:DataType on DataTemplate for compiled bindings
- **Don't:** {Binding} in item templates for large lists
- Severity: High

## Profile with Visual Studio diagnostics
Measure before optimizing
- **Do:** Application Timeline and Memory Usage tools
- **Don't:** Guessing at performance problems
- Severity: Medium

## Use async/await for all IO
Keep UI thread responsive
- **Do:** async/await for file network and database operations
- **Don't:** Synchronous IO blocking the UI thread
- Severity: High

## Use CoreDispatcher for UI thread access
Post work back to the UI thread from background
- **Do:** Dispatcher.RunAsync from background threads
- **Don't:** Touching UI elements from background threads
- Severity: High

## Offload CPU work with Task.Run
Keep compute-heavy work off UI thread
- **Do:** Task.Run for CPU-bound operations
- **Don't:** Heavy computation blocking UI
- Severity: High

## Use IProgress for status updates
Report progress from background operations
- **Do:** IProgress<T> for progress reporting to UI
- **Don't:** Polling shared variables for progress
- Severity: Medium

## Use AdaptiveTrigger for responsive layouts
MinWindowWidth and MinWindowHeight triggers fire at standard breakpoints (640 small / 1008 medium)
- **Do:** AdaptiveTrigger inside VisualState.StateTriggers with the 640 and 1008 breakpoints
- **Don't:** Fixed layouts for a single screen size
- Severity: High

## Design for multiple device families
Phone tablet desktop Xbox and HoloLens
- **Do:** DeviceFamily-specific views and resources
- **Don't:** Desktop-only design ignoring other form factors
- Severity: Medium

## Use RelativePanel for adaptive positioning
Controls position relative to each other
- **Do:** RelativePanel for layouts that reflow at breakpoints
- **Don't:** Absolute positioning or fixed margins
- Severity: Medium

## Support multi-window with secondary views
Open detached views with CoreApplication.CreateNewView and ApplicationViewSwitcher
- **Do:** CreateNewView and TryShowAsStandaloneAsync for multi-document scenarios
- **Don't:** Single-window assumptions when scenarios benefit from secondary views
- Severity: Medium

## Set AutomationProperties
Enable Narrator and screen reader support
- **Do:** AutomationProperties.Name on all interactive controls
- **Don't:** Controls without accessible names
- Severity: High

## Support keyboard and gamepad
All functions reachable without touch
- **Do:** Tab navigation XYFocus and access keys
- **Don't:** Touch-only interactions
- Severity: High

## Support contrast themes
Respect system contrast themes (renamed from high contrast in Windows 11)
- **Do:** ThemeResource brushes that adapt to contrast themes
- **Don't:** Hardcoded colors that vanish under contrast themes
- Severity: High

## Test with Narrator and Accessibility Insights
Validate screen reader and automation compliance
- **Do:** Regular Narrator walkthrough and Accessibility Insights scan
- **Don't:** Shipping without accessibility testing
- Severity: Medium

## Use MVVM pattern
Separate View ViewModel and Model
- **Do:** ViewModel with INotifyPropertyChanged and ICommand
- **Don't:** Business logic in code-behind
- Severity: Medium

## Use Template Studio for scaffolding
Proven project templates with navigation and services
- **Do:** Windows Template Studio for new UWP projects
- **Don't:** Blank project with manual boilerplate
- Severity: Low

## Use dependency injection
Register services for testability
- **Do:** Microsoft.Extensions.DI for service resolution
- **Don't:** Static singletons and manual construction
- Severity: Medium

## Keep platform APIs behind abstractions
Isolate WinRT APIs from business logic
- **Do:** Interfaces wrapping StorageFile FilePicker etc
- **Don't:** Direct WinRT calls in ViewModels
- Severity: Medium

## Handle suspend and resume
UWP apps are suspended when not in foreground
- **Do:** Save state in OnSuspending and restore in OnLaunched
- **Don't:** Ignoring app lifecycle losing user state
- Severity: High

## Use ExtendedExecutionSession for background work
Request extended time for unfinished operations
- **Do:** ExtendedExecutionSession for saving or uploads
- **Don't:** Assuming background work completes after suspend
- Severity: Medium

## Handle prelaunch
Apps must opt in to prelaunch via CoreApplication.EnablePrelaunch(true) starting in Windows 10 1607; check LaunchActivatedEventArgs.PrelaunchActivated to skip user-visible work
- **Do:** Opt in with EnablePrelaunch and skip heavy init when PrelaunchActivated is true
- **Don't:** Performing full initialization or navigating during prelaunch
- Severity: Medium

## Unit test ViewModels
Test logic without UI framework dependencies
- **Do:** xUnit or MSTest on ViewModel methods
- **Don't:** Testing only through the running app
- Severity: Medium

## Use WinAppDriver with Appium for UI tests
Automated UI testing for UWP (Coded UI Test was deprecated in Visual Studio 2019); WinAppDriver v1 is in low-maintenance mode and Appium 2 is the modern direction
- **Do:** WinAppDriver with Appium for end-to-end tests
- **Don't:** Manual regression testing
- Severity: Medium

## Test on multiple device families
Behavior varies across phone desktop and Xbox
- **Do:** Test on device emulators and real hardware
- **Don't:** Desktop-only testing
- Severity: Medium

## Prefer WinUI 3 for new projects
UWP is in maintenance mode and Microsoft recommends WinUI 3 and Windows App SDK for new development
- **Do:** WinUI 3 with Windows App SDK for new desktop apps
- **Don't:** Starting new projects on UWP when WinUI 3 is available
- Severity: Medium

## Plan migration to Windows App SDK
Microsoft provides migration guides from UWP to WinUI 3
- **Do:** Incremental migration using XAML Islands or full port to WinUI 3
- **Don't:** Ignoring migration path and accumulating UWP technical debt
- Severity: Medium

## Use a deferral when saving async state on suspend
Suspending grants only ~5 seconds before the OS may terminate; await work needs SuspendingOperation.GetDeferral and Complete or save returns before it finishes
- **Do:** GetDeferral around async save calls and Complete in finally
- **Don't:** Async work that returns the suspending handler before completion
- Severity: Medium
