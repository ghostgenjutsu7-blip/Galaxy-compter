---
name: wpf Best Practices
source: UIUXProMax
version: 1.0.0
description: 56 curated wpf guidelines (state, perf, a11y, patterns)
tags: ["stack", "wpf"]
triggers: ["wpf"]
license: MIT
target_agent: 
category: tech_stack
---

# wpf — Best Practices (56 guidelines)

## Use XAML for declarative UI
Define layout and visuals in XAML not code-behind
- **Do:** XAML for structure and styling
- **Don't:** Build UI trees in C# code-behind
- Severity: Low

## Set x:Class on root element
Connects XAML to its code-behind partial class
- **Do:** x:Class on Window UserControl and Page
- **Don't:** Missing x:Class or mismatched namespace
- Severity: High

## Use x:Name sparingly
Only name elements accessed from code-behind
- **Do:** x:Name when code-behind reference is needed
- **Don't:** Naming every element
- Severity: Low

## Prefer attached properties for layout
Grid.Row Grid.Column DockPanel.Dock etc
- **Do:** Attached properties for panel positioning
- **Don't:** Margin hacks for alignment
- Severity: Medium

## Use routed events for tree-wide handling
Events bubble up or tunnel down the element tree letting parents handle child events with one handler
- **Do:** Handler at parent using TypeName.EventName syntax with e.Handled=true when consumed
- **Don't:** Wiring identical handlers on every child when one parent handler suffices
- Severity: Medium

## Implement INotifyPropertyChanged
Enable UI updates when properties change
- **Do:** INotifyPropertyChanged on ViewModels
- **Don't:** Public properties without notification
- Severity: High

## Use ObservableCollection for lists
Notifies UI of add remove and reset
- **Do:** ObservableCollection<T> for bound collections
- **Don't:** List<T> or Array for bound ItemsSources
- Severity: High

## Set DataContext at the right level
Enables binding for the visual subtree
- **Do:** DataContext on Window or root container
- **Don't:** DataContext on every child control
- Severity: Medium

## Prefer Binding over code-behind assignments
Declarative binding keeps UI and logic separate
- **Do:** {Binding Path=Name} in XAML
- **Don't:** textBlock.Text = viewModel.Name in code-behind
- Severity: Medium

## Use UpdateSourceTrigger appropriately
Controls when source updates
- **Do:** PropertyChanged for instant feedback
- **Don't:** Default LostFocus when search-as-you-type is needed
- Severity: Medium

## Use IValueConverter for display transforms
Convert data for presentation without changing the model
- **Do:** IValueConverter for bool-to-visibility etc
- **Don't:** Visibility properties on ViewModel
- Severity: Medium

## Use INotifyDataErrorInfo for validation
Surface validation errors to the binding system instead of ad-hoc error UI
- **Do:** ObservableValidator with DataAnnotations attributes
- **Don't:** Throwing in setters or maintaining separate error properties
- Severity: Medium

## Use Grid for complex layouts
Rows and columns with proportional or fixed sizing
- **Do:** Grid with RowDefinitions and ColumnDefinitions
- **Don't:** Canvas with absolute positions for forms
- Severity: Medium

## Use StackPanel for linear content
Simple vertical or horizontal stacking
- **Do:** StackPanel for toolbars and simple lists
- **Don't:** Grid with single column for linear content
- Severity: Medium

## Use DockPanel for docked regions
Dock children to edges with last child filling
- **Do:** DockPanel for shell layouts (menu top sidebar left)
- **Don't:** Nested StackPanels to simulate docking
- Severity: Medium

## Avoid hardcoded sizes
Use Auto Star and MinWidth/MaxWidth
- **Do:** Proportional sizing with * and Auto
- **Don't:** Fixed pixel widths on resizable content
- Severity: Medium

## Use ScrollViewer for overflow
Wrap content that may exceed available space
- **Do:** ScrollViewer around long forms or lists
- **Don't:** Clipping content without scroll
- Severity: Medium

## Use Resource Dictionaries
Centralize colors brushes and styles
- **Do:** ResourceDictionary in App.xaml for theme values
- **Don't:** Inline colors and font sizes on every element
- Severity: Medium

## Use pack URIs for embedded resources
Reference embedded images fonts and resource dictionaries via the pack scheme
- **Do:** pack://application:,,, syntax for cross-assembly assets
- **Don't:** File-system paths for resources compiled into the assembly
- Severity: Medium

## Use implicit styles
Apply a Style to all instances of a TargetType
- **Do:** Style with TargetType and no x:Key for defaults
- **Don't:** Manually styling every Button instance
- Severity: Medium

## Use explicit styles with x:Key and BasedOn
Named variant styles that inherit from a base via BasedOn
- **Do:** x:Key styles that BasedOn an implicit or named style
- **Don't:** Duplicating setters across variants
- Severity: Medium

## Prefer StaticResource over DynamicResource
StaticResource is resolved once and faster
- **Do:** StaticResource for values that do not change at runtime
- **Don't:** DynamicResource for static theme values
- Severity: Medium

## Use ControlTemplate for full control
Override default rendering of a control
- **Do:** ControlTemplate when built-in styles are insufficient
- **Don't:** Nesting extra panels to hide the default template
- Severity: Medium

## Use DataTemplate for data presentation
Define how data objects render in ItemsControls
- **Do:** DataTemplate for ListBox ComboBox and ItemsControl items
- **Don't:** ToString overrides for display
- Severity: Medium

## Use Fluent theme on .NET 9+
ThemeMode applies the Windows 11 Fluent style; values are Light Dark System and None (default Aero2)
- **Do:** ThemeMode on Application or Window
- **Don't:** Legacy Aero2 styling for new Windows 11 apps
- Severity: Medium

## Use ICommand for user actions
Decouple UI actions from logic
- **Do:** ICommand implementations (RelayCommand DelegateCommand)
- **Don't:** Click event handlers in code-behind
- Severity: High

## Use CanExecute for enable/disable
Automatically disable controls when action unavailable; call NotifyCanExecuteChanged when state changes
- **Do:** CanExecute returning false to disable buttons
- **Don't:** IsEnabled binding to a separate bool
- Severity: Medium

## Use RelayCommand or DelegateCommand
Avoid implementing ICommand from scratch every time
- **Do:** RelayCommand (CommunityToolkit.Mvvm) or DelegateCommand (Prism)
- **Don't:** New ICommand class per command
- Severity: Medium

## Use AsyncRelayCommand for async operations
Tracks IsRunning and disables the command while it executes preventing re-entry
- **Do:** AsyncRelayCommand or [RelayCommand] on async Task method
- **Don't:** async void event handlers in code-behind
- Severity: Medium

## Use CommandParameter for context
Pass data from the UI element to the command handler
- **Do:** CommandParameter for item-specific actions
- **Don't:** Relying on SelectedItem in every command
- Severity: Low

## Use InputBindings for keyboard shortcuts
Bind keyboard gestures to commands without manual key handling
- **Do:** KeyBinding inside Window.InputBindings
- **Don't:** Custom key handling in PreviewKeyDown
- Severity: Medium

## Use VirtualizingStackPanel for large lists
Only creates UI elements for visible items. ListBox/ListView virtualize by default; TreeView requires opt-in
- **Do:** VirtualizingStackPanel.IsVirtualizing=True (set on TreeView; default for ListBox)
- **Don't:** Disabling virtualization on long lists
- Severity: High

## Freeze Freezable objects
Frozen brushes and geometries skip change tracking
- **Do:** Freeze brushes and pens that do not change
- **Don't:** Mutable brushes used as static resources
- Severity: Medium

## Use DependencyProperty for custom-control binding targets
Binding target properties on custom controls must be DependencyProperties (sources can be plain CLR properties with INPC)
- **Do:** Define DependencyProperty for properties bound TO on a custom control
- **Don't:** Plain CLR properties as binding targets on custom controls
- Severity: Medium

## Use async for long operations
Keep UI thread responsive
- **Do:** async/await with Task.Run for CPU work
- **Don't:** Synchronous operations that freeze the UI
- Severity: High

## Profile with PerfView and Visual Studio
Measure before optimizing
- **Do:** Visual Studio diagnostic tools and PerfView
- **Don't:** Guessing at performance bottlenecks
- Severity: Medium

## Use Dispatcher for UI updates
UI elements can only be accessed from the UI thread
- **Do:** Dispatcher.Invoke or BeginInvoke from background threads
- **Don't:** Accessing UI elements from background threads
- Severity: High

## Prefer async/await over Dispatcher
Modern async code returns to UI context automatically
- **Do:** async/await which resumes on captured SynchronizationContext
- **Don't:** Manual Dispatcher.BeginInvoke for every callback
- Severity: Medium

## Use Task.Run for CPU-bound work
Offload intensive work from UI thread
- **Do:** Task.Run for compute-bound work
- **Don't:** Long-running computations on UI thread
- Severity: High

## Report progress from background tasks
Update UI with progress during long operations
- **Do:** IProgress<T> with Task.Run
- **Don't:** Polling a shared variable for progress
- Severity: Medium

## Handle DispatcherUnhandledException
Catch unhandled UI-thread exceptions to log them and prevent the default WPF crash dialog
- **Do:** Subscribe in App.xaml or App.OnStartup and set e.Handled=true after logging
- **Don't:** Letting WPF show its default crash dialog and silently shut down
- Severity: High

## Set AutomationProperties
Enable screen reader support
- **Do:** AutomationProperties.Name on interactive controls
- **Don't:** Controls without automation names
- Severity: High

## Support keyboard navigation
All functionality reachable via keyboard
- **Do:** Tab order and KeyboardNavigation properties
- **Don't:** Mouse-only interactions
- Severity: High

## Support high contrast themes
Respect Windows high contrast settings
- **Do:** SystemColors and SystemFonts resources
- **Don't:** Hardcoded colors that disappear in high contrast
- Severity: Medium

## Use appropriate control types
Semantic controls convey role to assistive tech
- **Do:** Button for actions CheckBox for toggles
- **Don't:** Styled TextBlock with click handler as fake button
- Severity: High

## Support DPI scaling
Ensure UI is crisp at all display scale factors
- **Do:** Device-independent units and vector graphics
- **Don't:** Pixel-based bitmaps that blur at high DPI
- Severity: Medium

## Declare PerMonitorV2 DPI awareness
WPF defaults to System-DPI-aware unless you opt into PerMonitorV2 via app.manifest
- **Do:** app.manifest with dpiAwareness PerMonitorV2
- **Don't:** Default System DPI awareness for Windows 10/11 apps
- Severity: Medium

## Use MVVM pattern
Separate View ViewModel and Model concerns
- **Do:** MVVM with data binding and commands
- **Don't:** Logic in code-behind
- Severity: High

## Override App.OnStartup for app initialization
Wire DI build the host resolve MainWindow and parse command-line args in OnStartup
- **Do:** Override OnStartup when DI or argument parsing is needed
- **Don't:** Relying on StartupUri when MainWindow needs constructor injection
- Severity: Medium

## Use dependency injection
Wire Microsoft.Extensions.Hosting Generic Host in App.OnStartup and resolve ViewModels from the container
- **Do:** Generic Host with Microsoft.Extensions.DependencyInjection
- **Don't:** new Service() in ViewModel constructors
- Severity: Medium

## Use CommunityToolkit.Mvvm
Source generators reduce MVVM boilerplate
- **Do:** [ObservableProperty] and [RelayCommand] attributes
- **Don't:** Hand-written INotifyPropertyChanged for every property
- Severity: Medium

## Keep code-behind minimal
Code-behind should only contain view-specific logic
- **Do:** View logic like focus management and animations in code-behind
- **Don't:** Business logic and data access in code-behind
- Severity: Medium

## Use messaging for loose coupling
Communicate between ViewModels without references
- **Do:** WeakReferenceMessenger from CommunityToolkit.Mvvm
- **Don't:** Direct ViewModel-to-ViewModel references
- Severity: Medium

## Unit test ViewModels
Test business logic independent of UI
- **Do:** xUnit or NUnit tests on ViewModel methods and properties
- **Don't:** Manual testing through the UI only
- Severity: Medium

## Mock services in tests
Isolate ViewModel from external dependencies
- **Do:** Moq or NSubstitute for service interfaces
- **Don't:** Real database calls in unit tests
- Severity: Medium

## Use UI Automation for integration tests
Automated UI testing with Microsoft UI Automation
- **Do:** FlaUI or Appium 2 (appium-windows-driver) for end-to-end tests
- **Don't:** Manual regression testing only
- Severity: Medium
