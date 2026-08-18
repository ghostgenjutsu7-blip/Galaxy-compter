---
name: react Best Practices
source: UIUXProMax
version: 1.0.0
description: 53 curated react guidelines (state, perf, a11y, patterns)
tags: ["stack", "react"]
triggers: ["react"]
license: MIT
target_agent: 
category: tech_stack
---

# react — Best Practices (53 guidelines)

## Use useState for local state
Simple component state should use useState hook
- **Do:** useState for form inputs toggles counters
- **Don't:** Class components this.state
- Severity: Medium

## Lift state up when needed
Share state between siblings by lifting to parent
- **Do:** Lift shared state to common ancestor
- **Don't:** Prop drilling through many levels
- Severity: Medium

## Use useReducer for complex state
Complex state logic benefits from reducer pattern
- **Do:** useReducer for state with multiple sub-values
- **Don't:** Multiple useState for related values
- Severity: Medium

## Avoid unnecessary state
Derive values from existing state when possible
- **Do:** Compute derived values in render
- **Don't:** Store derivable values in state
- Severity: High

## Initialize state lazily
Use function form for expensive initial state
- **Do:** useState(() => computeExpensive())
- **Don't:** useState(computeExpensive())
- Severity: Medium

## Clean up effects
Return cleanup function for subscriptions timers
- **Do:** Return cleanup function in useEffect
- **Don't:** No cleanup for subscriptions
- Severity: High

## Specify dependencies correctly
Include all values used inside effect in deps array
- **Do:** All referenced values in dependency array
- **Don't:** Empty deps with external references
- Severity: High

## Avoid unnecessary effects
Don't use effects for transforming data or events
- **Do:** Transform data during render handle events directly
- **Don't:** useEffect for derived state or event handling
- Severity: High

## Use refs for non-reactive values
Store values that don't trigger re-renders in refs
- **Do:** useRef for interval IDs DOM elements
- **Don't:** useState for values that don't need render
- Severity: Medium

## Use keys properly
Stable unique keys for list items
- **Do:** Use stable IDs as keys
- **Don't:** Array index as key for dynamic lists
- Severity: High

## Memoize expensive calculations
Use useMemo for costly computations
- **Do:** useMemo for expensive filtering/sorting
- **Don't:** Recalculate every render
- Severity: Medium

## Memoize callbacks passed to children
Use useCallback for functions passed as props
- **Do:** useCallback for handlers passed to memoized children
- **Don't:** New function reference every render
- Severity: Medium

## Use React.memo wisely
Wrap components that render often with same props
- **Do:** memo for pure components with stable props
- **Don't:** memo everything or nothing
- Severity: Low

## Avoid inline object/array creation in JSX
Create objects outside render or memoize
- **Do:** Define style objects outside component
- **Don't:** Inline objects in props
- Severity: Medium

## Keep components small and focused
Single responsibility for each component
- **Do:** One concern per component
- **Don't:** Large multi-purpose components
- Severity: Medium

## Use composition over inheritance
Compose components using children and props
- **Do:** Use children prop for flexibility
- **Don't:** Inheritance hierarchies
- Severity: Medium

## Colocate related code
Keep related components and hooks together
- **Do:** Related files in same directory
- **Don't:** Flat structure with many files
- Severity: Low

## Use fragments to avoid extra DOM
Fragment or <> for multiple elements without wrapper
- **Do:** <> for grouping without DOM node
- **Don't:** Extra div wrappers
- Severity: Low

## Destructure props
Destructure props for cleaner component code
- **Do:** Destructure in function signature
- **Don't:** props.name props.value throughout
- Severity: Low

## Provide default props values
Use default parameters or defaultProps
- **Do:** Default values in destructuring
- **Don't:** Undefined checks throughout
- Severity: Low

## Avoid prop drilling
Use context or composition for deeply nested data
- **Do:** Context for global data composition for UI
- **Don't:** Passing props through 5+ levels
- Severity: Medium

## Validate props with TypeScript
Use TypeScript interfaces for prop types
- **Do:** interface Props { name: string }
- **Don't:** PropTypes or no validation
- Severity: Medium

## Use synthetic events correctly
React normalizes events across browsers
- **Do:** e.preventDefault() e.stopPropagation()
- **Don't:** Access native event unnecessarily
- Severity: Low

## Avoid binding in render
Use arrow functions in class or hooks
- **Do:** Arrow functions in functional components
- **Don't:** bind in render or constructor
- Severity: Medium

## Pass event handlers not call results
Pass function reference not invocation
- **Do:** onClick={handleClick}
- **Don't:** onClick={handleClick()} causing immediate call
- Severity: High

## Controlled components for forms
Use state to control form inputs
- **Do:** value + onChange for inputs
- **Don't:** Uncontrolled inputs with refs
- Severity: Medium

## Handle form submission properly
Prevent default and handle in submit handler
- **Do:** onSubmit with preventDefault
- **Don't:** onClick on submit button only
- Severity: Medium

## Debounce rapid input changes
Debounce search/filter inputs
- **Do:** useDeferredValue or debounce for search
- **Don't:** Filter on every keystroke
- Severity: Medium

## Follow rules of hooks
Only call hooks at top level and in React functions
- **Do:** Hooks at component top level
- **Don't:** Hooks in conditions loops or callbacks
- Severity: High

## Custom hooks for reusable logic
Extract shared stateful logic to custom hooks
- **Do:** useCustomHook for reusable patterns
- **Don't:** Duplicate hook logic across components
- Severity: Medium

## Name custom hooks with use prefix
Custom hooks must start with use
- **Do:** useFetch useForm useAuth
- **Don't:** fetchData or getData for hook
- Severity: High

## Use context for global data
Context for theme auth locale
- **Do:** Context for app-wide state
- **Don't:** Context for frequently changing data
- Severity: Medium

## Split contexts by concern
Separate contexts for different domains
- **Do:** ThemeContext + AuthContext
- **Don't:** One giant AppContext
- Severity: Medium

## Memoize context values
Prevent unnecessary re-renders with useMemo
- **Do:** useMemo for context value object
- **Don't:** New object reference every render
- Severity: High

## Use React DevTools Profiler
Profile to identify performance bottlenecks
- **Do:** Profile before optimizing
- **Don't:** Optimize without measuring
- Severity: Medium

## Lazy load components
Use React.lazy for code splitting
- **Do:** lazy() for routes and heavy components
- **Don't:** Import everything upfront
- Severity: Medium

## Virtualize long lists
Use windowing for lists over 100 items
- **Do:** react-window or react-virtual
- **Don't:** Render thousands of DOM nodes
- Severity: High

## Batch state updates
React 18 auto-batches but be aware
- **Do:** Let React batch related updates
- **Don't:** Manual batching with flushSync
- Severity: Low

## Use error boundaries
Catch JavaScript errors in component tree
- **Do:** ErrorBoundary wrapping sections
- **Don't:** Let errors crash entire app
- Severity: High

## Handle async errors
Catch errors in async operations
- **Do:** try/catch in async handlers
- **Don't:** Unhandled promise rejections
- Severity: High

## Test behavior not implementation
Test what user sees and does
- **Do:** Test renders and interactions
- **Don't:** Test internal state or methods
- Severity: Medium

## Use testing-library queries
Use accessible queries
- **Do:** getByRole getByLabelText
- **Don't:** getByTestId for everything
- Severity: Medium

## Use semantic HTML
Proper HTML elements for their purpose
- **Do:** button for clicks nav for navigation
- **Don't:** div with onClick for buttons
- Severity: High

## Manage focus properly
Handle focus for modals dialogs
- **Do:** Focus trap in modals return focus on close
- **Don't:** No focus management
- Severity: High

## Announce dynamic content
Use ARIA live regions for updates
- **Do:** aria-live for dynamic updates
- **Don't:** Silent updates to screen readers
- Severity: Medium

## Label form controls
Associate labels with inputs
- **Do:** htmlFor matching input id
- **Don't:** Placeholder as only label
- Severity: High

## Type component props
Define interfaces for all props
- **Do:** interface Props with all prop types
- **Don't:** any or missing types
- Severity: High

## Type state properly
Provide types for useState
- **Do:** useState<Type>() for complex state
- **Don't:** Inferred any types
- Severity: Medium

## Type event handlers
Use React event types
- **Do:** React.ChangeEvent<HTMLInputElement>
- **Don't:** Generic Event type
- Severity: Medium

## Use generics for reusable components
Generic components for flexible typing
- **Do:** Generic props for list components
- **Don't:** Union types for flexibility
- Severity: Medium

## Container/Presentational split
Separate data logic from UI
- **Do:** Container fetches presentational renders
- **Don't:** Mixed data and UI in one
- Severity: Low

## Render props for flexibility
Share code via render prop pattern
- **Do:** Render prop for customizable rendering
- **Don't:** Duplicate logic across components
- Severity: Low

## Compound components
Related components sharing state
- **Do:** Tab + TabPanel sharing context
- **Don't:** Prop drilling between related
- Severity: Low
