---
name: winui Best Practices
source: UIUXProMax
version: 1.0.0
description: 59 curated winui guidelines (state, perf, a11y, patterns)
tags: ["stack", "winui"]
triggers: ["winui"]
license: MIT
target_agent: 
category: tech_stack
---

# winui — Best Practices (59 guidelines)

## Use x:Bind for compiled bindings
Compile-time checked bindings with better performance
- **Do:** x:Bind for type-safe bindings
- **Don't:** {Binding} when x:Bind works
- Severity: High

## Use x:Load for deferred loading
Only instantiate UI elements when needed
- **Do:** x:Load=False for hidden panels and dialogs
- **Don't:** Loading all UI upfront
- Severity: Medium

## Use x:Phase for incremental rendering
Load list items in phases for smooth scrolling
- **Do:** x:Phase on secondary content in DataTemplates
- **Don't:** Loading all template content in phase 0
- Severity: Medium

## Use x:DefaultBindMode
Set default binding mode for a scope
- **Do:** x:DefaultBindMode=OneWay on containers with many bindings
- **Don't:** Mode=OneWay on every individual x:Bind
- Severity: Low

## Use NavigationView for app navigation
WinUI 3 NavigationView with Left Top and LeftCompact display modes plus footer items
- **Do:** NavigationView with PaneDisplayMode for main app shell
- **Don't:** Custom hamburger menu implementation
- Severity: High

## Use InfoBar for status messages
Non-intrusive informational messages
- **Do:** InfoBar for success warning and error messages
- **Don't:** Custom styled StackPanel for status
- Severity: Medium

## Use TeachingTip for onboarding
Contextual tips attached to UI elements
- **Do:** TeachingTip for feature discovery
- **Don't:** Custom popup for teaching
- Severity: Low

## Use ContentDialog for modal interactions
Standard modal dialog pattern
- **Do:** ContentDialog for confirmations and input
- **Don't:** Custom overlay Panel as dialog
- Severity: Medium

## Use BreadcrumbBar for hierarchy
Show navigation path in hierarchical apps
- **Do:** BreadcrumbBar for folder or category navigation
- **Don't:** Manual TextBlock breadcrumb chain
- Severity: Low

## Use Lightweight Styling
Override control sub-properties via resources
- **Do:** Lightweight styling resource keys to tweak controls
- **Don't:** Full ControlTemplate override for small changes
- Severity: High

## Use WinUI theme resources
Consistent Fluent Design colors and brushes
- **Do:** WinUI theme resource keys for colors
- **Don't:** Hardcoded hex color values
- Severity: High

## Support light and dark themes
Respect user and system theme preference
- **Do:** ThemeResource for theme-adaptive values
- **Don't:** Hardcoded colors that break in dark mode
- Severity: High

## Use Fluent Design system
Acrylic Mica Reveal and rounded corners
- **Do:** Built-in Fluent materials and effects
- **Don't:** Custom blur and shadow implementations
- Severity: Medium

## Use Frame for page navigation
Microsoft.UI.Xaml.Controls.Frame for WinUI 3 page navigation
- **Do:** Frame.Navigate with page types and parameters
- **Don't:** Swapping UserControls in a ContentControl
- Severity: Medium

## Pass typed navigation parameters
Type-safe data passing between pages
- **Do:** Typed parameter in OnNavigatedTo
- **Don't:** Dictionary or string parsing for parameters
- Severity: Medium

## Handle back navigation
WinUI 3 uses NavigationView.BackRequested instead of UWP SystemNavigationManager
- **Do:** Register NavigationView.BackRequested handler and manage back stack
- **Don't:** Ignoring back navigation
- Severity: Medium

## Use deep linking
Handle protocol activation so URIs route to the right page
- **Do:** Register protocol then check ExtendedActivationKind.Protocol on activation
- **Don't:** Single entry point ignoring activation context
- Severity: Medium

## Use ObservableCollection for lists
Notifies UI of collection changes
- **Do:** ObservableCollection<T> for bound ItemsSources
- **Don't:** List<T> for bound collections
- Severity: High

## Use INotifyPropertyChanged
Enable property change notification for UI updates
- **Do:** INotifyPropertyChanged on ViewModels
- **Don't:** Properties without notification
- Severity: High

## Use function binding with x:Bind
Call methods directly in bindings
- **Do:** x:Bind with method references for transforms
- **Don't:** IValueConverter for simple logic
- Severity: Medium

## Specify Mode explicitly on x:Bind
x:Bind defaults to OneTime not OneWay
- **Do:** Mode=OneWay or Mode=TwoWay when updates needed
- **Don't:** Forgetting Mode and getting stale UI
- Severity: High

## Use ItemsRepeater for custom lists
Virtualizing layout with full control
- **Do:** ItemsRepeater for custom list layouts
- **Don't:** ListView for highly customized item layouts
- Severity: Medium

## Use incremental loading
Load data on demand as user scrolls
- **Do:** ISupportIncrementalLoading for large data sets
- **Don't:** Loading entire dataset upfront
- Severity: Medium

## Reduce visual tree complexity
Simpler trees render faster
- **Do:** Minimal nesting in DataTemplates
- **Don't:** Deeply nested panels in item templates
- Severity: Medium

## Use compiled bindings over reflection
x:Bind generates code at compile time
- **Do:** x:Bind for hot paths and list items
- **Don't:** {Binding} in DataTemplates and frequently updated UI
- Severity: High

## Use DispatcherQueue not Dispatcher
WinUI 3 uses Microsoft.UI.Dispatching.DispatcherQueue instead of UWP CoreDispatcher
- **Do:** DispatcherQueue.TryEnqueue for UI thread access
- **Don't:** Dispatcher.RunAsync (UWP pattern)
- Severity: High

## Use async/await for IO operations
Keep UI responsive during file and network access
- **Do:** async/await for IO so the UI thread keeps rendering
- **Don't:** Synchronous IO on UI thread
- Severity: High

## Use Task.Run for CPU-bound work
Offload compute to thread pool
- **Do:** Task.Run for heavy computation
- **Don't:** Long-running CPU work on UI thread
- Severity: High

## Use WinAppSDK correctly
Windows App SDK provides the runtime
- **Do:** WinAppSDK NuGet package and WindowsAppSDK bootstrapper
- **Don't:** Mixing UWP and WinUI 3 APIs
- Severity: High

## Use unpackaged or packaged appropriately
Choose deployment model for your scenario
- **Do:** Packaged (MSIX) for Store distribution
- **Don't:** Unpackaged without considering API limitations
- Severity: Medium

## Use single-project MSIX
Simplified packaging for single app
- **Do:** Single-project MSIX packaging
- **Don't:** Separate WAP project when not needed
- Severity: Low

## Set AutomationProperties
Enable Narrator and screen reader support
- **Do:** AutomationProperties.Name on all interactive controls
- **Don't:** Controls without accessible names
- Severity: High

## Support keyboard navigation
Full keyboard accessibility
- **Do:** Tab navigation and access keys for all controls
- **Don't:** Mouse-only interactions
- Severity: High

## Use proper heading levels
Screen readers use headings for navigation
- **Do:** AutomationProperties.HeadingLevel on section headers
- **Don't:** All text at same heading level
- Severity: Medium

## Support high contrast
Respect system high contrast settings
- **Do:** ThemeResource brushes that adapt to high contrast
- **Don't:** Hardcoded colors ignoring high contrast
- Severity: High

## Test with Accessibility Insights
Validate accessibility compliance
- **Do:** Accessibility Insights for Windows scanning
- **Don't:** Manual accessibility checking only
- Severity: Medium

## Use MVVM with CommunityToolkit
Source generators reduce boilerplate
- **Do:** [ObservableProperty] and [RelayCommand] attributes
- **Don't:** Manual INotifyPropertyChanged and ICommand
- Severity: Medium

## Use dependency injection
Register services with Microsoft.Extensions.DI
- **Do:** IServiceProvider for ViewModel and service resolution
- **Don't:** new ViewModel() and new Service() everywhere
- Severity: Medium

## Use Template Studio patterns
Start with proven architectural templates
- **Do:** Template Studio for WinUI 3 project scaffolding
- **Don't:** Blank project with manual setup for complex apps
- Severity: Low

## Separate platform from business logic
Keep business logic in .NET Standard or shared libraries
- **Do:** Business logic in separate class library
- **Don't:** Business logic mixed with WinUI types
- Severity: Medium

## Use WinUI 3 Window management
Proper window lifecycle management
- **Do:** AppWindow API for multi-window scenarios
- **Don't:** Single Window assumption in complex apps
- Severity: Medium

## Unit test ViewModels
Test logic independent of UI framework
- **Do:** xUnit or MSTest on ViewModel properties and commands
- **Don't:** Testing through UI only
- Severity: Medium

## Use WinAppDriver for UI tests
Automated UI testing for WinUI 3
- **Do:** WinAppDriver or Appium for end-to-end tests
- **Don't:** Manual regression testing
- Severity: Medium

## Mock WinRT APIs in tests
Isolate tests from platform dependencies
- **Do:** Interface wrappers around WinRT APIs
- **Don't:** Direct WinRT API calls in testable code
- Severity: Medium

## Use NumberBox for numeric input
Built-in numeric entry with validation formatting and spin buttons
- **Do:** NumberBox with Minimum Maximum and SpinButtonPlacementMode
- **Don't:** TextBox with manual numeric parsing and validation
- Severity: Medium

## Use Expander for collapsible sections
Expandable content area with header for progressive disclosure
- **Do:** Expander for settings groups and optional content
- **Don't:** Manual visibility toggling with buttons
- Severity: Low

## Use ProgressRing and ProgressBar for loading
Built-in loading indicators for determinate and indeterminate states
- **Do:** ProgressRing for indeterminate and ProgressBar for determinate progress
- **Don't:** Custom spinning animation or text-based loading indicators
- Severity: Medium

## Use VisualStateManager for responsive layouts
Adapt UI layout to window size using adaptive triggers
- **Do:** AdaptiveTrigger with MinWindowWidth for responsive breakpoints
- **Don't:** Fixed layouts that break at different window sizes
- Severity: High

## Handle app activation and launch
WinUI 3 apps receive activation events for URI and notification launches
- **Do:** Check LaunchActivatedEventArgs in OnLaunched for activation context
- **Don't:** Ignoring activation arguments losing deep link context
- Severity: Medium

## Use single instancing with AppInstance
Prevent multiple app windows competing for resources
- **Do:** AppInstance.FindOrRegisterForKey for single-instance enforcement
- **Don't:** Multiple instances with conflicting state
- Severity: Medium

## Save and restore app state
Persist UI state across app restarts for continuity (ApplicationData APIs require packaged apps; unpackaged apps must use file IO or registry)
- **Do:** Save state to local settings on window close or navigation
- **Don't:** Losing user context on every restart
- Severity: Medium

## Choose Mica vs Acrylic by surface lifetime
Mica is for long-lived primary surfaces like main windows; Acrylic is for transient light-dismiss surfaces like flyouts and context menus
- **Do:** Mica on root window backgrounds and Acrylic on flyouts and overlays
- **Don't:** Acrylic on the main window or Mica on transient flyouts
- Severity: Medium

## Set SystemBackdrop on Window directly
WinUI 3 1.3+ exposes Window.SystemBackdrop with MicaBackdrop and DesktopAcrylicBackdrop classes replacing manual MicaController plumbing
- **Do:** Window.SystemBackdrop in XAML or code
- **Don't:** Hand-rolled MicaController wiring when SystemBackdrop API is available
- Severity: Medium

## Open secondary windows with new Window
WinUI 3 supports multiple top-level windows; each Window owns an AppWindow accessible via Window.AppWindow for size and position control
- **Do:** new Window().Activate() for secondary windows tracking them in App state
- **Don't:** Faking multi-window via main-window content swaps or ContentDialog
- Severity: Medium

## Extend client area into the title bar
Use Window.ExtendsContentIntoTitleBar with SetTitleBar to host custom XAML in the chrome while preserving caption buttons
- **Do:** ExtendsContentIntoTitleBar=true plus SetTitleBar(element) for custom drag region
- **Don't:** Hardcoded chrome height or custom caption buttons that break with theme and size changes
- Severity: Medium

## Use KeyboardAccelerator for shortcuts
Map Ctrl/Alt/Shift combinations to commands using KeyboardAccelerator on UIElement
- **Do:** KeyboardAccelerator with Modifiers and Key on relevant controls
- **Don't:** Manual KeyDown handlers swallowing shortcuts
- Severity: High

## Organize resources with merged dictionaries
Share styles and brushes via App.xaml MergedDictionaries instead of duplicating per page
- **Do:** MergedDictionaries in App.xaml for shared styles brushes and colors
- **Don't:** Duplicating SolidColorBrush definitions on every page
- Severity: Medium

## Use AsyncRelayCommand for async commands
AsyncRelayCommand exposes IsRunning and supports cancellation for IO bound work
- **Do:** [RelayCommand] on async Task method or AsyncRelayCommand for IO work
- **Don't:** async void event handlers or fire-and-forget Task.Run from button click
- Severity: Medium

## Use ILogger for structured logging
Microsoft.Extensions.Logging ILogger<T> with DI for structured leveled logs
- **Do:** ILogger<T> injected via constructor for diagnostic logging
- **Don't:** Debug.WriteLine or Console.WriteLine for app diagnostics
- Severity: Medium
