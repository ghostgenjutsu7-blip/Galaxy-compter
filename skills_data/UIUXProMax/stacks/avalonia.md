---
name: avalonia Best Practices
source: UIUXProMax
version: 1.0.0
description: 56 curated avalonia guidelines (state, perf, a11y, patterns)
tags: ["stack", "avalonia"]
triggers: ["avalonia"]
license: MIT
target_agent: 
category: tech_stack
---

# avalonia — Best Practices (56 guidelines)

## Use Avalonia XAML namespace
Avalonia has its own XAML namespace not WPF
- **Do:** xmlns= for Avalonia-specific namespace
- **Don't:** WPF xmlns or UWP xmlns
- Severity: High

## Use compiled bindings with x:DataType
Enable compile-time binding validation
- **Do:** x:DataType on root or DataTemplate for compiled bindings
- **Don't:** Reflection-based bindings in production
- Severity: High

## Enable compiled bindings globally
AvaloniaUseCompiledBindingsByDefault in csproj makes every binding require x:DataType and is required for trim-safe Native AOT
- **Do:** AvaloniaUseCompiledBindingsByDefault MSBuild property in csproj
- **Don't:** Relying on runtime binding resolution
- Severity: High

## Use #name shorthand for element-to-element bindings
Compiled bindings cannot resolve {Binding ElementName=...} - use the #name shorthand which relies on NameScope lookup
- **Do:** #name shorthand referencing x:Name controls in the same NameScope
- **Don't:** ElementName binding inside a compiled-binding scope
- Severity: Medium

## Use CSS-like selectors
Avalonia uses selectors not implicit styles
- **Do:** Selectors targeting control types classes and pseudoclasses
- **Don't:** WPF-style implicit Style with TargetType
- Severity: High

## Use pseudoclass selectors for states
Target control states with colon syntax
- **Do:** :pointerover :pressed :focus for interactive states
- **Don't:** VisualStateManager or Triggers
- Severity: Medium

## Use nesting selectors
Child and descendant combinators for scoped styles
- **Do:** > for direct child and space for descendant
- **Don't:** Flat selectors that match too broadly
- Severity: Medium

## Use StyleInclude for modularity
Split styles into separate AXAML files
- **Do:** StyleInclude to import themed resource files
- **Don't:** All styles in a single monolithic App.axaml
- Severity: Medium

## Use Fluent or Simple theme
Built-in Avalonia themes
- **Do:** FluentTheme or SimpleTheme as base
- **Don't:** Custom theme from scratch
- Severity: High

## Use theme variants for dark mode
Switch between light and dark
- **Do:** RequestedThemeVariant for theme switching
- **Don't:** Hardcoded colors ignoring theme variants
- Severity: Medium

## Use DataGrid for tabular data
DataGrid is a separate Avalonia.Controls.DataGrid NuGet package and requires its theme StyleInclude in App.axaml
- **Do:** DataGrid after adding package and StyleInclude for the matching theme
- **Don't:** Custom Grid layouts for tabular data or DataGrid without the theme StyleInclude
- Severity: Medium

## Use TreeView with TreeDataTemplate
Avalonia uses TreeDataTemplate for hierarchical data - HierarchicalDataTemplate is WPF only
- **Do:** TreeDataTemplate inside TreeView.ItemTemplate with ItemsSource pointing at child collection
- **Don't:** HierarchicalDataTemplate copied from WPF or nested ItemsControls
- Severity: High

## Use NativeMenu for platform menus
Native menu bar on macOS and desktop
- **Do:** NativeMenu for cross-platform menu bar
- **Don't:** Custom menu implementation per platform
- Severity: Medium

## Implement INotifyPropertyChanged
Standard .NET property notification
- **Do:** INotifyPropertyChanged or CommunityToolkit.Mvvm
- **Don't:** Properties without change notification
- Severity: High

## Use ObservableCollection for lists
UI updates on collection changes
- **Do:** ObservableCollection<T> for bound collections
- **Don't:** List<T> for ItemsSources
- Severity: High

## Use binding to named controls
Element-to-element binding with # syntax
- **Do:** #ElementName.Property for cross-element binding
- **Don't:** Code-behind for element references
- Severity: Medium

## Use converters or FuncValueConverter
Transform data for display
- **Do:** FuncValueConverter for simple inline conversions
- **Don't:** Complex IValueConverter classes for trivial transforms
- Severity: Medium

## Use platform-specific code carefully
Isolate platform code behind abstractions
- **Do:** Interface + platform implementation pattern
- **Don't:** #if directives scattered through ViewModels
- Severity: Medium

## Test on all target platforms
Rendering and behavior varies across platforms
- **Do:** CI testing on Windows macOS and Linux
- **Don't:** Testing only on development platform
- Severity: High

## Handle platform file paths
Path separators differ across OS
- **Do:** Path.Combine and Environment.SpecialFolder
- **Don't:** Hardcoded backslashes or forward slashes
- Severity: Medium

## Use Avalonia asset system
Platform-agnostic resource loading
- **Do:** avares:// URI scheme for embedded resources
- **Don't:** File system paths for assets
- Severity: High

## Use virtualization for large lists
Only render visible items
- **Do:** ListBox and ItemsRepeater with virtualization
- **Don't:** Non-virtualizing ItemsControl for large lists
- Severity: High

## Avoid unnecessary bindings
Each binding has overhead
- **Do:** Bind only properties that change
- **Don't:** Binding static labels and headers
- Severity: Low

## Set bitmap interpolation mode on scaled images
RenderOptions.BitmapInterpolationMode controls image scaling quality vs cost; default may look aliased on upscaled or downscaled bitmaps
- **Do:** RenderOptions.SetBitmapInterpolationMode tuned to the use case
- **Don't:** Default interpolation on scaled images that look blurry or aliased
- Severity: Low

## Profile with Avalonia DevTools
Built-in diagnostic tools
- **Do:** DevTools for visual tree and binding inspection
- **Don't:** Console.WriteLine debugging
- Severity: Medium

## Use MVVM with ReactiveUI or CommunityToolkit
Proven MVVM frameworks for Avalonia
- **Do:** ReactiveUI or CommunityToolkit.Mvvm for ViewModels
- **Don't:** Code-behind for all logic
- Severity: High

## Use ViewLocator pattern
Convention-based View-ViewModel resolution
- **Do:** ViewLocator for automatic view resolution
- **Don't:** Manual view instantiation and DataContext wiring
- Severity: Medium

## Use dependency injection
Register services in a Microsoft.Extensions.DependencyInjection container during startup before any view is constructed - resolve ViewModels through the provider not via a static ServiceLocator
- **Do:** Build the ServiceProvider in BuildAvaloniaApp or OnFrameworkInitializationCompleted then resolve ViewModels from it
- **Don't:** Static ServiceLocator or new-ing ViewModels inline in code-behind
- Severity: Medium

## Separate Views from ViewModels
Keep UI and logic in separate projects
- **Do:** ViewModels in a separate class library
- **Don't:** ViewModels in the same project referencing Avalonia types
- Severity: Medium

## Set AutomationProperties
Enable screen reader support
- **Do:** AutomationProperties.Name on interactive controls
- **Don't:** Controls without accessible names
- Severity: High

## Support keyboard navigation
Full keyboard operability
- **Do:** TabIndex and KeyboardNavigation properties
- **Don't:** Mouse-only interactions
- Severity: High

## Use semantic control types
Controls convey meaning to assistive tech
- **Do:** Button for actions ListBox for selection
- **Don't:** TextBlock with PointerPressed as fake button
- Severity: High

## Use Avalonia.Headless for UI tests
Run UI tests without display server
- **Do:** Avalonia.Headless for CI-compatible UI testing
- **Don't:** Skipping UI tests in CI
- Severity: Medium

## Unit test ViewModels
Test business logic independently
- **Do:** xUnit or NUnit on ViewModel methods
- **Don't:** Testing through UI only
- Severity: Medium

## Test converters independently
Value converters contain testable logic
- **Do:** Unit tests on Convert and ConvertBack
- **Don't:** Assuming converters work without tests
- Severity: Low

## Use ReactiveUI routing for navigation
IScreen and RoutingState for page navigation
- **Do:** ReactiveUI RoutingState with IScreen on main ViewModel
- **Don't:** Manual content swapping in code-behind
- Severity: Medium

## Use UserControl for views
Pages and screens should be UserControls hosted in a ContentControl
- **Do:** UserControl for each view with RoutedViewHost or ContentControl
- **Don't:** Window per page or nested Windows
- Severity: Medium

## Use page transitions for view switching
Built-in transitions for smooth navigation
- **Do:** CrossFade PageSlide or CompositePageTransition declared as a property element
- **Don't:** Abrupt content swaps with no visual continuity
- Severity: Low

## Support back navigation
Maintain navigation history for complex apps
- **Do:** Router.NavigateBack or custom back stack
- **Don't:** No way to return to previous views
- Severity: Medium

## Use AutoCompleteBox for search
Built-in autocomplete and suggestion control
- **Do:** AutoCompleteBox with FilterMode and ItemsSource
- **Don't:** TextBox with manual Popup and ListBox for suggestions
- Severity: Medium

## Use TabControl for tabbed interfaces
Standard tabbed navigation and content switching
- **Do:** TabControl with TabItem for tabbed layouts
- **Don't:** Manual toggle buttons swapping content
- Severity: Medium

## Use SplitView for master-detail
Collapsible pane layout for navigation or panels
- **Do:** SplitView with Pane and Content areas
- **Don't:** Manual Grid with column toggling for sidebar
- Severity: Medium

## Use Flyout for contextual actions
Attach popup menus and actions to controls
- **Do:** Flyout and MenuFlyout on Button or other controls
- **Don't:** Custom Popup positioning and management
- Severity: Medium

## Use AppBuilder for app configuration
Configure platform features and services at startup
- **Do:** AppBuilder with UsePlatformDetect and fluent API
- **Don't:** Manual platform initialization
- Severity: High

## Initialize MainWindow in OnFrameworkInitializationCompleted
Override OnFrameworkInitializationCompleted on App and check ApplicationLifetime - on desktop cast to IClassicDesktopStyleApplicationLifetime to set MainWindow and ShutdownMode; never create windows in the App constructor before the framework is ready
- **Do:** Override OnFrameworkInitializationCompleted and pattern-match on IClassicDesktopStyleApplicationLifetime for desktop-only setup
- **Don't:** Creating windows in the App constructor or assuming the same lifetime type on every platform
- Severity: High

## Use CSS-like keyframe animations
Avalonia supports declarative animations in XAML and code
- **Do:** Animation with KeyFrame and Setter for property animations
- **Don't:** Manual timer-based property updates
- Severity: Medium

## Use Transitions for implicit animations
Automatic animation when property values change
- **Do:** Transitions collection on controls for smooth changes
- **Don't:** Instant property changes with no visual feedback
- Severity: Low

## Use compiled bindings and TrimmerRoots.xml for PublishAot
Avalonia 11+ supports Native AOT for self-contained desktop deployments; XAML reflection paths must use compiled bindings or be preserved via TrimmerRoots so trimming does not strip them
- **Do:** x:CompileBindings=True on every view plus TrimmerRoots.xml for runtime-resolved types
- **Don't:** PublishAot with reflection-based {Binding} markup or trimming without checking warnings
- Severity: Medium

## Marshal cross-thread work to the UI thread
Avalonia controls and bound properties are not thread-safe and touching them off the UI thread throws InvalidOperationException
- **Do:** Dispatcher.UIThread.Post or InvokeAsync to bounce work back to the UI thread
- **Don't:** Direct property writes from Task.Run or background threads
- Severity: High

## Use AsyncRelayCommand or ReactiveCommand for async work
Async-aware commands disable themselves while running and surface CancellationToken so users cannot double-invoke a long operation
- **Do:** [RelayCommand] async Task method or ReactiveCommand.CreateFromTask
- **Don't:** async void event handlers or fire-and-forget Task.Run from a click handler
- Severity: High

## Use DynamicResource for theme-aware brushes
ResourceDictionary.ThemeDictionaries entries must be looked up via DynamicResource - StaticResource resolves once at load and won't update when the active theme variant changes
- **Do:** DynamicResource for brushes and colors that follow the active theme variant
- **Don't:** Hardcoded hex colors or StaticResource for values that should follow theme
- Severity: Medium

## Use HotKey or KeyBinding for keyboard shortcuts
Built-in HotKey on ICommandSource and Window.KeyBindings handle modifier keys focus scoping and cross-platform Ctrl/Cmd mapping
- **Do:** HotKey on a command-bound control or KeyBinding on the Window
- **Don't:** Manual KeyDown handlers checking Key and KeyModifiers
- Severity: Medium

## Customize window chrome with ExtendClientAreaToDecorationsHint
Set ExtendClientAreaToDecorationsHint to extend content into the title bar area and tag a region with WindowDecorationProperties.ElementRole=TitleBar to keep native drag and maximize behavior
- **Do:** ExtendClientAreaToDecorationsHint plus a region tagged ElementRole=TitleBar
- **Don't:** SystemDecorations=None with hand-rolled PointerPressed dragging in code-behind
- Severity: Medium

## Use TopLevel.StorageProvider for file pickers
The legacy OpenFileDialog/SaveFileDialog APIs are obsolete in Avalonia 11 - use TopLevel.GetTopLevel(this).StorageProvider with OpenFilePickerAsync/SaveFilePickerAsync/OpenFolderPickerAsync which returns IStorageFile/IStorageFolder and works on desktop mobile and browser
- **Do:** TopLevel.StorageProvider with OpenFilePickerAsync and FilePickerOpenOptions
- **Don't:** OpenFileDialog or SaveFileDialog from older Avalonia samples or copied from WPF
- Severity: High

## Use TrayIcon for system tray icon
TrayIcon shows a native system tray/notification-area icon with a NativeMenu - declare it via the Application.TrayIcon.Icons attached property in App.axaml; works on Windows macOS and most Linux desktops
- **Do:** TrayIcon with NativeMenu inside TrayIcon.Icons on the Application
- **Don't:** Custom borderless window pretending to be a tray icon or per-platform native interop
- Severity: Medium

## Use OnPlatform and OnFormFactor markup for per-OS values
OnPlatform and OnFormFactor markup extensions resolve to a different value per OS or form factor at XAML load time and replace if-statements in code-behind for tweaks like fonts spacing or icon sizes
- **Do:** OnPlatform with Default Windows macOS Linux entries directly in the property setter
- **Don't:** RuntimeInformation.IsOSPlatform branches in code-behind to set XAML properties
- Severity: Medium
