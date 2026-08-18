---
name: shadcn Best Practices
source: UIUXProMax
version: 1.0.0
description: 60 curated shadcn guidelines (state, perf, a11y, patterns)
tags: ["stack", "shadcn"]
triggers: ["shadcn"]
license: MIT
target_agent: 
category: tech_stack
---

# shadcn — Best Practices (60 guidelines)

## Use CLI for installation
Install components via shadcn CLI for proper setup
- **Do:** npx shadcn@latest add component-name
- **Don't:** Manual copy-paste from docs
- Severity: High

## Initialize project properly
Run init command to set up components.json and globals.css
- **Do:** npx shadcn@latest init before adding components
- **Don't:** Skip init and add components directly
- Severity: High

## Configure path aliases
Set up proper import aliases in tsconfig and components.json
- **Do:** Use @/components/ui path aliases
- **Don't:** Relative imports like ../../components
- Severity: Medium

## Use CSS variables for colors
Define colors as CSS variables in globals.css for theming
- **Do:** CSS variables in :root and .dark
- **Don't:** Hardcoded color values in components
- Severity: High

## Follow naming convention
Use semantic color names with foreground pattern
- **Do:** primary/primary-foreground secondary/secondary-foreground
- **Don't:** Generic color names
- Severity: Medium

## Support dark mode
Include .dark class styles for all custom CSS
- **Do:** Define both :root and .dark color schemes
- **Don't:** Only light mode colors
- Severity: High

## Use component variants
Leverage cva variants for consistent styling
- **Do:** Use variant prop for different styles
- **Don't:** Inline conditional classes
- Severity: Medium

## Compose with className
Add custom classes via className prop for overrides
- **Do:** Extend with className for one-off customizations
- **Don't:** Modify component source directly
- Severity: Medium

## Use size variants consistently
Apply size prop for consistent sizing across components
- **Do:** size="sm" size="lg" for sizing
- **Don't:** Mix size classes inconsistently
- Severity: Medium

## Prefer compound components
Use provided sub-components for complex UI
- **Do:** Card + CardHeader + CardContent pattern
- **Don't:** Single component with many props
- Severity: Medium

## Use Dialog for modal content
Dialog component for overlay modal windows
- **Do:** Dialog for confirmations forms details
- **Don't:** Alert for modal content
- Severity: High

## Handle dialog state properly
Use open and onOpenChange for controlled dialogs
- **Do:** Controlled state with useState
- **Don't:** Uncontrolled with default open only
- Severity: Medium

## Include proper dialog structure
Use DialogHeader DialogTitle DialogDescription
- **Do:** Complete semantic structure
- **Don't:** Missing title or description
- Severity: High

## Use Sheet for side panels
Sheet component for slide-out panels and drawers
- **Do:** Sheet for navigation filters settings
- **Don't:** Dialog for side content
- Severity: Medium

## Specify sheet side
Set side prop for sheet slide direction
- **Do:** Explicit side="left" or side="right"
- **Don't:** Default side without consideration
- Severity: Low

## Use Form with react-hook-form
Integrate Form component with react-hook-form for validation
- **Do:** useForm + Form + FormField pattern
- **Don't:** Custom form handling without Form
- Severity: High

## Use FormField for inputs
Wrap inputs in FormField for proper labeling and errors
- **Do:** FormField + FormItem + FormLabel + FormControl
- **Don't:** Input without FormField wrapper
- Severity: High

## Display form messages
Use FormMessage for validation error display
- **Do:** FormMessage after FormControl
- **Don't:** Custom error text without FormMessage
- Severity: Medium

## Use Zod for validation
Define form schema with Zod for type-safe validation
- **Do:** zodResolver with form schema
- **Don't:** Manual validation logic
- Severity: Medium

## Use Select for dropdowns
Select component for option selection
- **Do:** Select for choosing from list
- **Don't:** Native select element
- Severity: Medium

## Structure Select properly
Include Trigger Value Content and Items
- **Do:** Complete Select structure
- **Don't:** Missing SelectValue or SelectContent
- Severity: High

## Use Command for search
Command component for searchable lists and palettes
- **Do:** Command for command palette search
- **Don't:** Input with custom dropdown
- Severity: Medium

## Group command items
Use CommandGroup for categorized items
- **Do:** CommandGroup with heading for sections
- **Don't:** Flat list without grouping
- Severity: Low

## Use Table for data display
Table component for structured data
- **Do:** Table for tabular data display
- **Don't:** Div grid for table-like layouts
- Severity: Medium

## Include proper table structure
Use TableHeader TableBody TableRow TableCell
- **Do:** Semantic table structure
- **Don't:** Missing thead or tbody
- Severity: High

## Use DataTable for complex tables
Combine Table with TanStack Table for features
- **Do:** DataTable pattern for sorting filtering pagination
- **Don't:** Custom table implementation
- Severity: Medium

## Use Tabs for content switching
Tabs component for tabbed interfaces
- **Do:** Tabs for related content sections
- **Don't:** Custom tab implementation
- Severity: Medium

## Set default tab value
Specify defaultValue for initial tab
- **Do:** defaultValue on Tabs component
- **Don't:** No default leaving first tab
- Severity: Low

## Use Accordion for collapsible
Accordion for expandable content sections
- **Do:** Accordion for FAQ settings panels
- **Don't:** Custom collapse implementation
- Severity: Medium

## Choose accordion type
Use type="single" or type="multiple" appropriately
- **Do:** type="single" for one open type="multiple" for many
- **Don't:** Default type without consideration
- Severity: Low

## Use Sonner for toasts
Sonner integration for toast notifications
- **Do:** toast() from sonner for notifications
- **Don't:** Custom toast implementation
- Severity: Medium

## Add Toaster to layout
Include Toaster component in root layout
- **Do:** <Toaster /> in app layout
- **Don't:** Toaster in individual pages
- Severity: High

## Use toast variants
Apply toast.success toast.error for context
- **Do:** Semantic toast methods
- **Don't:** Generic toast for all messages
- Severity: Medium

## Use Popover for floating content
Popover for dropdown menus and floating panels
- **Do:** Popover for contextual actions
- **Don't:** Absolute positioned divs
- Severity: Medium

## Handle popover alignment
Use align and side props for positioning
- **Do:** Explicit alignment configuration
- **Don't:** Default alignment for all
- Severity: Low

## Use DropdownMenu for actions
DropdownMenu for action lists and context menus
- **Do:** DropdownMenu for user menu actions
- **Don't:** Popover for action lists
- Severity: Medium

## Group menu items
Use DropdownMenuGroup and DropdownMenuSeparator
- **Do:** Organized menu with separators
- **Don't:** Flat list of items
- Severity: Low

## Use Tooltip for hints
Tooltip for icon buttons and truncated text
- **Do:** Tooltip for additional context
- **Don't:** Title attribute for tooltips
- Severity: Medium

## Add TooltipProvider
Wrap app or section in TooltipProvider
- **Do:** TooltipProvider at app level
- **Don't:** TooltipProvider per tooltip
- Severity: High

## Use Skeleton for loading
Skeleton component for loading placeholders
- **Do:** Skeleton matching content layout
- **Don't:** Spinner for content loading
- Severity: Medium

## Match skeleton dimensions
Size skeleton to match loaded content
- **Do:** Skeleton same size as expected content
- **Don't:** Generic skeleton size
- Severity: Medium

## Use AlertDialog for confirms
AlertDialog for destructive action confirmation
- **Do:** AlertDialog for delete confirmations
- **Don't:** Dialog for confirmations
- Severity: High

## Include action buttons
Use AlertDialogAction and AlertDialogCancel
- **Do:** Standard confirm/cancel pattern
- **Don't:** Custom buttons in AlertDialog
- Severity: Medium

## Use Sidebar for navigation
Sidebar component for app navigation
- **Do:** Sidebar for main app navigation
- **Don't:** Custom sidebar implementation
- Severity: Medium

## Wrap in SidebarProvider
Use SidebarProvider for sidebar state management
- **Do:** SidebarProvider at layout level
- **Don't:** Sidebar without provider
- Severity: High

## Use SidebarTrigger
Include SidebarTrigger for mobile toggle
- **Do:** SidebarTrigger for responsive toggle
- **Don't:** Custom toggle button
- Severity: Medium

## Use Chart for data viz
Chart component with Recharts integration
- **Do:** Chart component for dashboards
- **Don't:** Direct Recharts without wrapper
- Severity: Medium

## Define chart config
Create chartConfig for consistent theming
- **Do:** chartConfig with color definitions
- **Don't:** Inline colors in charts
- Severity: Medium

## Use ChartTooltip
Apply ChartTooltip for interactive charts
- **Do:** ChartTooltip with ChartTooltipContent
- **Don't:** Recharts Tooltip directly
- Severity: Low

## Use blocks for scaffolding
Start from shadcn blocks for common layouts
- **Do:** npx shadcn@latest add dashboard-01
- **Don't:** Build dashboard from scratch
- Severity: Medium

## Customize block components
Modify copied block code to fit needs
- **Do:** Edit block files after installation
- **Don't:** Use blocks without modification
- Severity: Low

## Use semantic components
Shadcn components have built-in ARIA
- **Do:** Rely on component accessibility
- **Don't:** Override ARIA attributes
- Severity: High

## Maintain focus management
Dialog Sheet handle focus automatically
- **Do:** Let components manage focus
- **Don't:** Custom focus handling
- Severity: High

## Provide labels
Use FormLabel and aria-label appropriately
- **Do:** FormLabel for form inputs
- **Don't:** Placeholder as only label
- Severity: High

## Import components individually
Import only needed components
- **Do:** Named imports from component files
- **Don't:** Import all from index
- Severity: Medium

## Lazy load dialogs
Dynamic import for heavy dialog content
- **Do:** React.lazy for dialog content
- **Don't:** Import all dialogs upfront
- Severity: Medium

## Extend variants with cva
Add new variants using class-variance-authority
- **Do:** Extend buttonVariants for new styles
- **Don't:** Inline classes for variants
- Severity: Medium

## Create custom components
Build new components following shadcn patterns
- **Do:** Use cn() and cva for custom components
- **Don't:** Different patterns for custom
- Severity: Medium

## Use asChild for composition
asChild prop for component composition
- **Do:** Slot pattern with asChild
- **Don't:** Wrapper divs for composition
- Severity: Medium

## Combine with React Hook Form
Form + useForm for complete forms
- **Do:** RHF Controller with shadcn inputs
- **Don't:** Custom form state management
- Severity: High
