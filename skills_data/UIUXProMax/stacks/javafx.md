---
name: javafx Best Practices
source: UIUXProMax
version: 1.0.0
description: 75 curated javafx guidelines (state, perf, a11y, patterns)
tags: ["stack", "javafx"]
triggers: ["javafx"]
license: MIT
target_agent: 
category: tech_stack
---

# javafx — Best Practices (75 guidelines)

## Start UI from Application subclass
JavaFX apps should bootstrap the primary Stage through Application.start()
- **Do:** Extend Application and configure Scene in start()
- **Don't:** Create UI from a random main method without launching JavaFX
- Severity: High

## Keep work off the FX Application Thread
Long-running work blocks rendering and input when executed on the UI thread
- **Do:** Use Task or Service for background work
- **Don't:** Run network database or file work in button handlers
- Severity: High

## Update UI only on FX thread
Scene graph changes must happen on the JavaFX Application Thread
- **Do:** Use bindings task handlers or Platform.runLater for UI changes
- **Don't:** Mutate controls directly from background threads
- Severity: High

## Bind progress to background tasks
Task exposes progress and message properties for responsive feedback
- **Do:** Bind ProgressBar and Label to task properties
- **Don't:** Poll progress manually or leave users without feedback
- Severity: Medium

## Use FXML for stable declarative layouts
FXML keeps view structure readable for screens with many controls
- **Do:** Place layout in FXML and behavior in controller
- **Don't:** Build large screens entirely in one Java method
- Severity: Medium

## Keep controllers focused on view behavior
Controllers should coordinate controls and delegate business logic to services
- **Do:** Inject services or call application services from controller
- **Don't:** Put database queries and domain rules directly in controller
- Severity: High

## Use fx:id for injected controls
FXML controls need stable fx:id values that match controller fields
- **Do:** Annotate fields with @FXML and keep ids descriptive
- **Don't:** Look up controls by CSS selector for normal wiring
- Severity: Medium

## Fail fast when loading FXML
FXML load errors should surface during screen creation with clear context
- **Do:** Load resources with getResource and handle IOException explicitly
- **Don't:** Swallow loader errors and show a blank scene
- Severity: High

## Style with style classes
JavaFX CSS works best through reusable styleClass names
- **Do:** Add semantic style classes and define them in CSS
- **Don't:** Set long inline style strings throughout code
- Severity: Medium

## Use design tokens through looked-up colors
Looked-up colors keep palettes consistent across controls
- **Do:** Define named colors on root and reuse them in CSS
- **Don't:** Repeat hex values in every selector
- Severity: Medium

## Avoid overusing inline effects
Expensive CSS effects and shadows can hurt desktop UI responsiveness
- **Do:** Use subtle shadows only on important elevated surfaces
- **Don't:** Apply blur drop shadow and glow to every node
- Severity: Medium

## Choose layout panes by responsibility
Each pane solves a different layout problem and should be selected intentionally
- **Do:** Use BorderPane for app shell GridPane for forms VBox/HBox for simple stacks
- **Don't:** Use absolute positioning for resizable app screens
- Severity: High

## Prefer constraints over fixed coordinates
Responsive JavaFX layouts depend on constraints and grow priorities
- **Do:** Use hgrow vgrow column constraints and alignment
- **Don't:** Hard-code pixel positions and sizes
- Severity: High

## Set sensible min pref and max sizes
Controls should resize predictably across windows and DPI settings
- **Do:** Use Region.USE_COMPUTED_SIZE and max widths intentionally
- **Don't:** Lock every control to fixed width and height
- Severity: Medium

## Use spacing and padding consistently
Desktop UI needs scan-friendly rhythm and clear grouping
- **Do:** Set spacing padding and Insets through shared constants or CSS
- **Don't:** Use inconsistent ad hoc gaps between controls
- Severity: Low

## Use ObservableList for list controls
TableView ListView and ComboBox update automatically from observable collections
- **Do:** Back controls with FXCollections.observableArrayList()
- **Don't:** Mutate plain lists and manually refresh controls
- Severity: High

## Configure TableView cell value factories with properties
Table columns should observe stable JavaFX properties for updates
- **Do:** Expose StringProperty ObjectProperty or use ReadOnlyObjectWrapper
- **Don't:** Return transient strings without observable support
- Severity: Medium

## Use cell factories for custom rendering
Custom table or list visuals belong in reusable cell factories
- **Do:** Override updateItem and handle empty state
- **Don't:** Place complex Nodes directly in model objects
- Severity: Medium

## Virtualized controls are for large data
TableView ListView TreeView virtualize cells and outperform manual node lists
- **Do:** Use TableView or ListView for hundreds of rows
- **Don't:** Create hundreds of HBoxes inside a VBox
- Severity: High

## Handle empty states explicitly
Empty tables and lists need visible guidance or next actions
- **Do:** Set placeholder nodes for empty data views
- **Don't:** Leave blank white areas that look broken
- Severity: Low

## Use property binding for derived UI state
JavaFX binding reduces imperative synchronization bugs
- **Do:** Bind disabled visible text and progress properties to source state
- **Don't:** Manually update every dependent control in each event handler
- Severity: High

## Unbind before manual updates
Bound properties cannot be set directly without errors
- **Do:** Call unbind when switching from bound to manual state
- **Don't:** Set a bound property directly
- Severity: Medium

## Use listeners sparingly
Bindings express simple relationships more clearly than listeners
- **Do:** Use listeners for side effects and bindings for values
- **Don't:** Create listener chains for simple computed text
- Severity: Low

## Use action handlers for commands
Buttons and menu items should route to named command methods
- **Do:** Use setOnAction or @FXML handler methods with clear names
- **Don't:** Put large lambdas inline for complex operations
- Severity: Medium

## Use event filters for global shortcuts
Filters can intercept keyboard events before child controls consume them
- **Do:** Register accelerators or filters at Scene level
- **Don't:** Add duplicate key handlers to every control
- Severity: Medium

## Connect labels to inputs
Accessible desktop forms need labels associated with controls
- **Do:** Use Label.setLabelFor and clear prompt text
- **Don't:** Use placeholder-only labels
- Severity: High

## Expose accessible text for icon buttons
Icon-only controls need names for screen readers and tooltips
- **Do:** Set accessibleText and Tooltip on icon buttons
- **Don't:** Use unlabeled graphic-only buttons
- Severity: High

## Keep keyboard focus visible
Desktop users rely on focus traversal and visible focus indicators
- **Do:** Preserve focus rings and tab order
- **Don't:** Remove outlines without alternative focus state
- Severity: High

## Use mnemonics for menu and form workflows
Mnemonics make desktop workflows faster and more accessible
- **Do:** Enable mnemonicParsing and choose unique mnemonic letters
- **Don't:** Ignore keyboard alternatives for frequent actions
- Severity: Low

## Show validation near the field
Users should not hunt for form errors in desktop dialogs
- **Do:** Bind error labels or pseudo classes next to invalid controls
- **Don't:** Show only a generic alert after submit
- Severity: Medium

## Use TextFormatter for constrained input
TextFormatter prevents invalid edits before they enter the model
- **Do:** Attach TextFormatter for numeric dates and masks
- **Don't:** Parse and reject invalid text only after submit
- Severity: Medium

## Use modal ownership for dialogs
Dialogs should block only the relevant window and return structured results
- **Do:** Set owner modality and use showAndWait
- **Don't:** Open unmanaged windows for confirmations
- Severity: Medium

## Prefer custom DialogPane over ad hoc stages
Dialog gives consistent buttons focus and result handling
- **Do:** Use Dialog<T> for forms confirmations and wizards
- **Don't:** Build every modal as a new Stage manually
- Severity: Low

## Load images as resources
Packaged apps need resources resolved from the classpath or module path
- **Do:** Use getResourceAsStream for bundled assets
- **Don't:** Use absolute local file paths in production UI
- Severity: High

## Use background loading for large images
Large image decoding can pause UI startup
- **Do:** Use Image(url true) or a background Task for heavy assets
- **Don't:** Load many full-size images synchronously during startup
- Severity: Medium

## Keep animations purposeful and short
Desktop UI animations should clarify state changes without delaying work
- **Do:** Use 150-250ms transitions for reveal hover and selection
- **Don't:** Animate every layout change with long timelines
- Severity: Low

## Respect reduced-motion contexts where possible
Some users experience motion sensitivity in desktop apps
- **Do:** Provide a setting to disable decorative animations
- **Don't:** Make animation required for comprehension
- Severity: Medium

## Avoid recreating scenes for small state changes
Replacing whole scenes loses state and can flicker
- **Do:** Swap center content or update view models
- **Don't:** Rebuild the entire Stage for every navigation click
- Severity: Medium

## Reuse loaded views when appropriate
FXML loading and CSS application are not free
- **Do:** Cache stable views or controllers for frequent navigation
- **Don't:** Reload heavyweight screens repeatedly without need
- Severity: Low

## Batch observable list changes
Many single-item updates can cause repeated layout and sort work
- **Do:** Use setAll or addAll for bulk replacement
- **Don't:** Loop add items one by one to visible lists
- Severity: Medium

## Use view models for complex screens
View models keep controller state testable and separate from controls
- **Do:** Expose JavaFX properties from a screen model
- **Don't:** Store all state only inside controls
- Severity: Medium

## Separate navigation from feature controllers
Feature controllers should not know how every screen is launched
- **Do:** Use a navigator or application shell service
- **Don't:** Call FXMLLoader for unrelated screens from each controller
- Severity: Medium

## Declare required JavaFX modules
Modular JavaFX apps must require the modules they use
- **Do:** Add javafx.controls javafx.fxml and opens controller packages
- **Don't:** Depend on classpath accidents only
- Severity: High

## Use jlink or jpackage for desktop delivery
JavaFX apps should ship with the runtime they need
- **Do:** Package a runtime image or native installer
- **Don't:** Ask end users to install matching Java and JavaFX manually
- Severity: Medium

## Use TestFX for interaction tests
UI flows need automated coverage beyond controller unit tests
- **Do:** Write TestFX tests for key forms dialogs and navigation
- **Don't:** Only manually click through releases
- Severity: Medium

## Use AtlantaFX as the enterprise theme baseline
AtlantaFX provides modern JavaFX themes while preserving standard controls
- **Do:** Use AtlantaFX user-agent stylesheet plus a small app CSS layer
- **Don't:** Rewrite every standard control style from scratch
- Severity: High

## Prefer Primer for enterprise applications
PrimerLight and PrimerDark are neutral enough for dense business workflows
- **Do:** Use PrimerLight as default and PrimerDark for dark mode
- **Don't:** Use Dracula or Cupertino as the default enterprise theme
- Severity: Medium

## Layer brand CSS after AtlantaFX
Application CSS should customize brand tokens and business states after the base theme
- **Do:** Add app.css to the Scene after setting AtlantaFX
- **Don't:** Edit AtlantaFX source CSS directly
- Severity: High

## Use looked-up colors as enterprise tokens
JavaFX looked-up colors keep brand and semantic colors reusable across controls
- **Do:** Define app-primary app-success app-warning app-danger on root
- **Don't:** Repeat hex values in every selector
- Severity: High

## Keep theme switching centralized
Dark mode switching should not be scattered across controllers
- **Do:** Use a ThemeService that sets user-agent stylesheet and app CSS variants
- **Don't:** Let each controller decide its own theme
- Severity: Medium

## Validate contrast for business status colors
Enterprise screens use status colors heavily and need readable contrast
- **Do:** Check text on success warning danger and selected row backgrounds
- **Don't:** Assume brand colors are accessible
- Severity: High

## Use AtlantaFX style classes before custom CSS
AtlantaFX exposes utility styles that reduce custom CSS drift
- **Do:** Prefer Styles constants or documented style classes
- **Don't:** Create one-off class names for every button variant
- Severity: Medium

## Treat AtlantaFX as a base not the whole design system
AtlantaFX modernizes controls but enterprise UX still needs layout density and workflow rules
- **Do:** Define app shell navigation table density form and validation conventions
- **Don't:** Assume theme choice alone solves enterprise usability
- Severity: High

## Use Ikonli for consistent enterprise icons
Icon fonts integrate cleanly with JavaFX controls and avoid emoji-style UI
- **Do:** Use FontIcon with semantic style classes
- **Don't:** Use emoji as toolbar or menu icons
- Severity: Medium

## Use AtlantaFX controls for common app affordances
AtlantaFX provides useful controls such as Card Message ModalPane Popover and ToggleSwitch
- **Do:** Use built-in AtlantaFX controls before adding another dependency
- **Don't:** Add ControlsFX for components AtlantaFX already covers
- Severity: Medium

## Add ControlsFX only for missing enterprise controls
ControlsFX is useful for specialized controls but should stay optional
- **Do:** Use ControlsFX for SpreadsheetView PropertySheet CheckComboBox or StatusBar needs
- **Don't:** Add ControlsFX by default before requirements are clear
- Severity: Low

## Test theme-critical flows with TestFX
Theme and CSS changes can break focus visibility dialogs and button affordance
- **Do:** Use TestFX for login save validation and modal workflows
- **Don't:** Only inspect AtlantaFX screens manually
- Severity: Medium

## Use application shell plus feature workspaces
Enterprise JavaFX apps need stable navigation around changing work areas
- **Do:** Use BorderPane shell with navigation toolbar and central workspace
- **Don't:** Replace the whole Stage for every feature
- Severity: High

## Use MVVM for complex enterprise screens
Large forms and tables need testable state outside the controller
- **Do:** Expose JavaFX properties from view models and bind controls to them
- **Don't:** Put all screen state and validation in the controller
- Severity: High

## Inject services into controllers
Enterprise controllers should coordinate UI and call application services
- **Do:** Use a controller factory or DI container for services
- **Don't:** Create database connections inside FXML controllers
- Severity: High

## Use role-aware navigation models
Menus toolbars and shortcuts should reflect the same permission model
- **Do:** Build navigation items from commands with required roles
- **Don't:** Hide buttons in one place and leave shortcuts enabled
- Severity: High

## Represent workflow states visibly
Approval and processing screens need clear business state signals
- **Do:** Use semantic badges row styles and disabled actions by workflow state
- **Don't:** Use only free text status columns
- Severity: Medium

## Design TableView for high-density enterprise data
Enterprise users scan compare sort filter and act on rows for long periods
- **Do:** Use compact row height clear columns sorting filtering and selection summary
- **Don't:** Use card grids for large tabular datasets
- Severity: High

## Keep row actions predictable
Inline actions in dense tables should be limited and permission-aware
- **Do:** Use context menus or a side detail panel for secondary actions
- **Don't:** Place many buttons in every row
- Severity: Medium

## Use server-side paging for large enterprise datasets
Desktop clients should not load entire enterprise tables into memory
- **Do:** Fetch pages or filtered slices from services
- **Don't:** Load all records and filter in the UI
- Severity: High

## Use form sections for enterprise data entry
Long enterprise forms need grouping and progressive disclosure
- **Do:** Group fields into titled sections with validation summaries
- **Don't:** Place dozens of inputs in one unbroken GridPane
- Severity: Medium

## Provide validation summary plus field errors
Enterprise forms often need multiple corrections before submission
- **Do:** Show a summary at top and field-level messages near controls
- **Don't:** Show only one modal alert after Save
- Severity: High

## Make long operations cancellable
Enterprise imports exports sync and reports need cancel paths
- **Do:** Expose cancel button bound to Task running state
- **Don't:** Force users to wait or kill the app
- Severity: High

## Surface retryable errors without losing context
Network and service failures should preserve user input and next action
- **Do:** Show inline retry messages and keep form/table state
- **Don't:** Clear the screen on service failure
- Severity: High

## Log business actions through services
Enterprise desktop apps need traceability for sensitive changes
- **Do:** Record user action entity result and timestamp in service layer
- **Don't:** Log only UI button clicks
- Severity: Medium

## Separate user preferences from application config
Enterprise apps need deploy-time config and per-user preferences
- **Do:** Use config files for endpoints and Preferences for UI choices
- **Don't:** Hard-code environment URLs and window state
- Severity: Medium

## Package resources and themes inside the runtime image
AtlantaFX app CSS icons and FXML must be available after jpackage
- **Do:** Load resources from classpath or module resources
- **Don't:** Load theme files from developer machine paths
- Severity: High

## Write logs to user-writable locations
Installed desktop apps may not write inside the application directory
- **Do:** Use platform-specific user data directories for logs and cache
- **Don't:** Write logs beside the executable
- Severity: Medium

## Cover enterprise happy path and failure path
Enterprise UI tests should verify save validation permission and service failure flows
- **Do:** Use TestFX for core workflows and service fakes
- **Don't:** Only test controller methods without UI interaction
- Severity: High

## Keep optional UI libraries behind actual needs
AtlantaFX should be default but additional libraries should be justified
- **Do:** Start with JavaFX AtlantaFX Ikonli TestFX and add ControlsFX only for missing controls
- **Don't:** Adopt many UI libraries at project start
- Severity: Medium
