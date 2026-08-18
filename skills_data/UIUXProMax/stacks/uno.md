---
name: uno Best Practices
source: UIUXProMax
version: 1.0.0
description: 59 curated uno guidelines (state, perf, a11y, patterns)
tags: ["stack", "uno"]
triggers: ["uno"]
license: MIT
target_agent: 
category: tech_stack
---

# uno — Best Practices (59 guidelines)

## Use WinUI XAML API surface
Uno implements the WinUI API across platforms
- **Do:** Microsoft.UI.Xaml namespace for all UI code
- **Don't:** WPF or Xamarin.Forms namespaces
- Severity: High

## Check API implementation status
Not all WinUI APIs are implemented on every platform
- **Do:** Uno API compatibility docs before using new APIs
- **Don't:** Assuming all WinUI APIs work everywhere
- Severity: High

## Use Uno.WinUI not Uno.UI for new projects
Uno.WinUI uses WinUI 3 APIs
- **Do:** Uno.WinUI NuGet packages for new projects
- **Don't:** Uno.UI (UWP API surface) for new projects
- Severity: Medium

## Use XAML Hot Reload
Speed up development with live XAML editing
- **Do:** Hot Reload for iterating on layouts
- **Don't:** Restarting app for every XAML change
- Severity: Medium

## Use platform-specific XAML
Conditional namespaces for platform-specific UI
- **Do:** xmlns:android xmlns:ios xmlns:wasm for platform XAML
- **Don't:** Shared XAML when platforms need different controls
- Severity: Medium

## Use partial classes for platform code
Separate platform implementations in partial files
- **Do:** Partial class files with platform-specific logic
- **Don't:** #if directives in shared code for large blocks
- Severity: Medium

## Use preprocessor symbols correctly
Target correct platforms with defines
- **Do:** __IOS__ __ANDROID__ __WASM__ __DESKTOP__ for platform checks
- **Don't:** Inventing custom symbols or checking OS at runtime
- Severity: Medium

## Minimize platform-specific code
Keep shared code maximized
- **Do:** Abstract platform differences behind interfaces
- **Don't:** Duplicating logic across platform files
- Severity: High

## Use Frame-based navigation
Standard WinUI navigation pattern
- **Do:** Frame.Navigate with page types
- **Don't:** Manual content swapping
- Severity: Medium

## Use Uno.Extensions.Navigation
Type-safe navigation with DI integration
- **Do:** Uno.Extensions navigation for complex apps
- **Don't:** Manual Frame management in large apps
- Severity: Medium

## Handle platform back navigation
SystemNavigationManager.BackRequested works on Android iOS and WASM but is unimplemented on WinAppSDK desktop where calling GetForCurrentView() throws at runtime
- **Do:** Subscribe to BackRequested only on platforms that support it or use Uno.Toolkit NavigationBar for cross-platform back UX
- **Don't:** Calling SystemNavigationManager.GetForCurrentView() on WinUI 3 desktop without a guard
- Severity: High

## Use deep linking
Support URI activation across platforms
- **Do:** Handle protocol activation and URI routing
- **Don't:** Single entry point ignoring activation
- Severity: Medium

## Understand Skia vs native rendering
Uno offers both rendering approaches
- **Do:** Skia for pixel-perfect cross-platform consistency
- **Don't:** Assuming native rendering on all platforms
- Severity: High

## Use unified net10.0-desktop target
Uno 5.2+ ships a single Skia Desktop shell that auto-selects X11 Win32 or AppKit per OS — Skia.Gtk Skia.Linux.Framebuffer and Skia.WPF heads are deprecated
- **Do:** net10.0-desktop TFM with UnoPlatformHostBuilder for cross-platform desktop
- **Don't:** Targeting the legacy Skia.Gtk or Skia.Linux.Framebuffer heads in new projects
- Severity: Medium

## Test rendering on each target
Visual differences exist between renderers
- **Do:** Visual testing on each active target platform
- **Don't:** Testing only on Windows assuming others match
- Severity: High

## Use platform-native features when needed
Access native APIs through Uno abstractions
- **Do:** Native platform APIs via platform-specific code
- **Don't:** Avoiding native features for purity
- Severity: Medium

## Optimize WASM bundle size
WebAssembly downloads can be large
- **Do:** IL linker and AOT for smaller WASM bundles
- **Don't:** Default settings for production WASM
- Severity: High

## Use x:Load for deferred XAML
Defer element creation until needed
- **Do:** x:Load=False for hidden panels and tabs
- **Don't:** Loading all UI elements upfront
- Severity: Medium

## Use x:Bind for compiled bindings
Compiled bindings eliminate runtime reflection — Uno supports x:Bind across iOS Android WASM Skia and Windows targets that compile XAML so prefer it over {Binding} for static well-typed bindings
- **Do:** x:Bind for property and event bindings; reserve {Binding} for runtime-typed DataContext scenarios
- **Don't:** {Binding} everywhere when x:Bind would compile
- Severity: High

## Profile per platform
Performance characteristics vary by target
- **Do:** Platform-specific profiling tools
- **Don't:** Assuming desktop perf equals mobile
- Severity: Medium

## Use WinUI theme resources
Consistent theming across platforms
- **Do:** ThemeResource for adaptive colors
- **Don't:** Hardcoded colors per platform
- Severity: High

## Support light and dark themes
Application.RequestedTheme accepts only ApplicationTheme.Light/Dark — to follow the system theme leave it unset entirely. ElementTheme.Default exists only on FrameworkElement.RequestedTheme not on Application
- **Do:** Omit Application.RequestedTheme so the OS theme wins; use RequestedTheme=Default on FrameworkElement to inherit from parent
- **Don't:** Setting Application.RequestedTheme=""Default"" — not a valid ApplicationTheme value and throws at parse time
- Severity: Medium

## Use Lightweight Styling
Override control sub-properties via resources
- **Do:** Lightweight styling keys for minor tweaks
- **Don't:** Full ControlTemplate for small changes
- Severity: Medium

## Test themes on each platform
Theme rendering differs across platforms
- **Do:** Visual theme testing on all targets
- **Don't:** Assuming themes look identical everywhere
- Severity: Low

## Use MVVM pattern
Separate view and logic
- **Do:** CommunityToolkit.Mvvm or Prism for MVVM
- **Don't:** Code-behind for business logic
- Severity: High

## Use Uno.Extensions
Official extension libraries for common patterns
- **Do:** Uno.Extensions for DI navigation configuration
- **Don't:** Building infrastructure from scratch
- Severity: Medium

## Use dependency injection
Register services for testability
- **Do:** Microsoft.Extensions.DI through Uno.Extensions
- **Don't:** Static service locators and singletons
- Severity: Medium

## Share code via class libraries
Maximize code reuse across targets
- **Do:** Business logic in .NET Standard or shared library
- **Don't:** Business logic in platform head projects
- Severity: Medium

## Use Uno.Resizetizer for assets
Single source SVG to multi-platform assets
- **Do:** UnoImage for automatic asset generation from SVG
- **Don't:** Manual asset export per resolution and platform
- Severity: Medium

## Set AutomationProperties
Enable screen readers across platforms
- **Do:** AutomationProperties.Name on interactive controls
- **Don't:** Controls without accessible names
- Severity: High

## Test accessibility per platform
Each platform has different assistive tech
- **Do:** Test with VoiceOver TalkBack and Narrator
- **Don't:** Testing accessibility on one platform only
- Severity: High

## Support platform text scaling
Respect user font size preferences
- **Do:** Dynamic font scaling for all text
- **Don't:** Fixed font sizes ignoring accessibility
- Severity: Medium

## Unit test ViewModels
Test business logic independently
- **Do:** xUnit or MSTest on shared ViewModel code
- **Don't:** UI testing only
- Severity: Medium

## Use Uno.UITest for integration
Cross-platform UI testing framework
- **Do:** Uno.UITest for automated UI tests across platforms
- **Don't:** Manual regression testing
- Severity: Medium

## Show an extended splash screen on WASM
WASM bundle download and runtime startup take several seconds on first load — render branded UI immediately so users do not see a blank page (AOT and trimming are covered separately)
- **Do:** Render a splash overlay in wwwroot/index.html that hides on first XAML navigation
- **Don't:** Letting the user wait on a blank white page while the runtime boots
- Severity: Medium

## Use AOT compilation for performance
Ahead-of-time compilation improves runtime speed
- **Do:** AOT for production WASM builds
- **Don't:** Interpreter mode in production
- Severity: Medium

## Handle browser limitations
WASM runs in browser sandbox
- **Do:** Feature detection for browser APIs
- **Don't:** Assuming desktop capabilities in browser
- Severity: Medium

## Use NavigationView for app shell
WinUI NavigationView for consistent navigation across platforms
- **Do:** NavigationView with MenuItems for app navigation
- **Don't:** Custom hamburger menu implementation
- Severity: High

## Use ContentDialog for modal interactions
Cross-platform modal dialogs using WinUI API
- **Do:** ContentDialog for confirmations and input
- **Don't:** Custom overlay Panel as dialog
- Severity: Medium

## Use CommandBar for app actions
Standard command bar with primary and secondary commands
- **Do:** CommandBar with AppBarButtons for toolbar actions
- **Don't:** Custom StackPanel toolbar
- Severity: Medium

## Use ToggleSwitch for boolean settings
Platform-native toggle control for on/off preferences
- **Do:** ToggleSwitch for settings and feature flags
- **Don't:** CheckBox for toggle settings
- Severity: Low

## Implement INotifyPropertyChanged
Enable UI updates when ViewModel properties change
- **Do:** CommunityToolkit.Mvvm [ObservableProperty] for auto-notification
- **Don't:** Properties without change notification
- Severity: High

## Use ObservableCollection for bound lists
Collection change notifications for ItemsSources across platforms
- **Do:** ObservableCollection<T> for data-bound lists
- **Don't:** List<T> for bound ItemsSources
- Severity: High

## Handle app suspension on mobile
iOS and Android may suspend or terminate the app — WinAppSDK desktop does not raise Suspending so use window Closed for desktop save-state
- **Do:** Save state in OnSuspending and restore on activation
- **Don't:** Ignoring lifecycle losing user state on mobile
- Severity: High

## Use Uno.Extensions.Hosting for startup
Structured app initialization with DI and configuration
- **Do:** IHost builder pattern for app startup and service registration
- **Don't:** Manual initialization in App constructor
- Severity: Medium

## Use ListView virtualization for large lists
Only renders visible items to reduce memory and layout cost
- **Do:** ListView with default ItemsStackPanel virtualization
- **Don't:** ItemsControl or StackPanel for large data sets
- Severity: High

## Support keyboard navigation on desktop
Skia and WinAppSDK targets need full keyboard operability — note TabIndex routing is not fully implemented on every Uno target
- **Do:** AccessKey and KeyboardAccelerator on Skia and WinAppSDK targets
- **Don't:** Mouse-only interactions on desktop
- Severity: High

## Use service workers for offline support
Enable PWA capabilities for WASM deployments
- **Do:** Service worker registration for caching and offline mode
- **Don't:** Online-only WASM app with no offline fallback
- Severity: Low

## Marshal to UI thread with DispatcherQueue
Cross-thread access to UI elements throws — capture the UI DispatcherQueue once and use TryEnqueue to update from background work
- **Do:** DispatcherQueue.GetForCurrentThread().TryEnqueue from background work
- **Don't:** Touching UI controls directly from a Task
- Severity: High

## Merge XamlControlsResources in App.xaml
Required for Fluent control styles to load — without it controls render with no template
- **Do:** Add XamlControlsResources at the top of Application.Resources MergedDictionaries
- **Don't:** Skipping the merged dictionary and wondering why Buttons look unstyled
- Severity: High

## Use async [RelayCommand] for I/O
AsyncRelayCommand reports CanExecute=false (raising CanExecuteChanged) and exposes IsRunning while the Task is in flight — the bound control is disabled and re-entrancy is prevented by default (AllowConcurrentExecutions=false)
- **Do:** [RelayCommand] on a Task-returning method for awaitable work
- **Don't:** async void event handlers calling .Wait() or .Result
- Severity: Medium

## Use x:Uid for localized strings
WinUI x:Uid resolves UI text from .resw resources at runtime — use it instead of hardcoded strings to support localization across iOS Android WASM and desktop from a single project
- **Do:** x:Uid on every user-facing string with matching .resw entries per language under Strings/{lang}/Resources.resw
- **Don't:** Hardcoding language-specific strings into XAML or code-behind
- Severity: High

## Wire up ILogger via Uno.Extensions.Logging
Cross-platform logging routes to platform-native sinks (OSLog on iOS Console on WASM Debug elsewhere) when configured through the IHost builder
- **Do:** Inject ILogger<T> into ViewModels and services and call UseLogging() on the host builder
- **Don't:** Console.WriteLine or platform-specific log APIs scattered across shared code
- Severity: Medium

## Enable PublishAot on net10.0-desktop
Skia Desktop on .NET 10 supports Native AOT for faster cold start and smaller deployments — opt in per-target so debug builds remain fast
- **Do:** <PublishAot>true</PublishAot> in a TFM-conditional PropertyGroup for net10.0-desktop release builds
- **Don't:** Enabling PublishAot globally and breaking debug iteration on every TFM
- Severity: Medium

## Never block on async with .Result or .Wait()
Blocking on a Task from the UI thread deadlocks because the awaiter cannot resume on the captured SynchronizationContext — always await async APIs through to the event handler
- **Do:** Await async methods all the way up; in libraries call ConfigureAwait(false) to avoid context capture
- **Don't:** Calling .Result .Wait() or GetAwaiter().GetResult() on a Task from the UI thread
- Severity: High

## Define ThemeDictionaries for Light Dark and HighContrast
Resources placed inside ResourceDictionary.ThemeDictionaries entries are automatically swapped when the system theme changes — required for theme-aware brushes
- **Do:** Wrap brushes in a ThemeDictionaries dictionary keyed by Light Dark and HighContrast in App.xaml or page resources
- **Don't:** Defining a single brush at the root and missing dark/high-contrast variants
- Severity: Medium

## Use Uno.Sdk with UnoFeatures
Uno.Sdk is the modern single-project SDK that auto-resolves Uno.WinUI Uno.Toolkit Material and other packages from a UnoFeatures property — declare features by name instead of hand-managing dozens of PackageReferences
- **Do:** Declare features in the csproj via <UnoFeatures>...</UnoFeatures> and let the SDK resolve transitive packages
- **Don't:** Hand-adding every Uno.* PackageReference and matching version numbers across packages
- Severity: Medium

## Persist desktop window state via Window.Closed
WinAppSDK and Skia desktop heads do not raise Application.Suspending — handle the Window.Closed event (and AppWindow size/position changes) to save user state when desktop apps shut down
- **Do:** Subscribe to MainWindow.Closed and persist any unsaved state before the window is destroyed
- **Don't:** Relying on Application.Suspending to fire on desktop targets
- Severity: Medium

## Use WinRT.Interop for native window handle on Windows
Calling Win32 APIs from a WinUI Window (file pickers icon embedding etc.) requires the HWND — retrieve it via WinRT.Interop.WindowNative.GetWindowHandle and guard the call so non-Windows targets stay unaffected
- **Do:** GetWindowHandle inside a #if WINDOWS block when you need the HWND
- **Don't:** Calling WinRT.Interop in shared code without a platform guard
- Severity: Medium
