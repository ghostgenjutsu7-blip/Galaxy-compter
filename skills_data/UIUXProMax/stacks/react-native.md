---
name: react-native Best Practices
source: UIUXProMax
version: 1.0.0
description: 51 curated react-native guidelines (state, perf, a11y, patterns)
tags: ["stack", "react-native"]
triggers: ["react-native"]
license: MIT
target_agent: 
category: tech_stack
---

# react-native — Best Practices (51 guidelines)

## Use functional components
Hooks-based components are standard
- **Do:** Functional components with hooks
- **Don't:** Class components
- Severity: Medium

## Keep components small
Single responsibility principle
- **Do:** Split into smaller components
- **Don't:** Large monolithic components
- Severity: Medium

## Use TypeScript
Type safety for props and state
- **Do:** TypeScript for new projects
- **Don't:** JavaScript without types
- Severity: Medium

## Colocate component files
Keep related files together
- **Do:** Component folder with styles
- **Don't:** Flat structure
- Severity: Low

## Use StyleSheet.create
Optimized style objects
- **Do:** StyleSheet for all styles
- **Don't:** Inline style objects
- Severity: High

## Avoid inline styles
Prevent object recreation
- **Do:** Styles in StyleSheet
- **Don't:** Inline style objects in render
- Severity: Medium

## Use flexbox for layout
React Native uses flexbox
- **Do:** flexDirection alignItems justifyContent
- **Don't:** Absolute positioning everywhere
- Severity: Medium

## Handle platform differences
Platform-specific styles
- **Do:** Platform.select or .ios/.android files
- **Don't:** Same styles for both platforms
- Severity: Medium

## Use responsive dimensions
Scale for different screens
- **Do:** Dimensions or useWindowDimensions
- **Don't:** Fixed pixel values
- Severity: Medium

## Use React Navigation
Standard navigation library
- **Do:** React Navigation for routing
- **Don't:** Manual navigation management
- Severity: Medium

## Type navigation params
Type-safe navigation
- **Do:** Typed navigation props
- **Don't:** Untyped navigation
- Severity: Medium

## Use deep linking
Support URL-based navigation
- **Do:** Configure linking prop
- **Don't:** No deep link support
- Severity: Medium

## Handle back button
Android back button handling
- **Do:** useFocusEffect with BackHandler
- **Don't:** Ignore back button
- Severity: High

## Use useState for local state
Simple component state
- **Do:** useState for UI state
- **Don't:** Class component state
- Severity: Medium

## Use useReducer for complex state
Complex state logic
- **Do:** useReducer for related state
- **Don't:** Multiple useState for related values
- Severity: Medium

## Use context sparingly
Context for global state
- **Do:** Context for theme auth locale
- **Don't:** Context for frequently changing data
- Severity: Medium

## Consider Zustand or Redux
External state management
- **Do:** Zustand for simple Redux for complex
- **Don't:** useState for global state
- Severity: Medium

## Use FlatList for long lists
Virtualized list rendering
- **Do:** FlatList for 50+ items
- **Don't:** ScrollView with map
- Severity: High

## Provide keyExtractor
Unique keys for list items
- **Do:** keyExtractor with stable ID
- **Don't:** Index as key
- Severity: High

## Optimize renderItem
Memoize list item components
- **Do:** React.memo for list items
- **Don't:** Inline render function
- Severity: High

## Use getItemLayout for fixed height
Skip measurement for performance
- **Do:** getItemLayout when height known
- **Don't:** Dynamic measurement for fixed items
- Severity: Medium

## Implement windowSize
Control render window
- **Do:** Smaller windowSize for memory
- **Don't:** Default windowSize for large lists
- Severity: Medium

## Use React.memo
Prevent unnecessary re-renders
- **Do:** memo for pure components
- **Don't:** No memoization
- Severity: Medium

## Use useCallback for handlers
Stable function references
- **Do:** useCallback for props
- **Don't:** New function on every render
- Severity: Medium

## Use useMemo for expensive ops
Cache expensive calculations
- **Do:** useMemo for heavy computations
- **Don't:** Recalculate every render
- Severity: Medium

## Avoid anonymous functions in JSX
Prevent re-renders
- **Do:** Named handlers or useCallback
- **Don't:** Inline arrow functions
- Severity: Medium

## Use Hermes engine
Improved startup and memory
- **Do:** Enable Hermes in build
- **Don't:** JavaScriptCore for new projects
- Severity: Medium

## Use expo-image
Modern performant image component for React Native
- **Do:** Use expo-image for caching, blurring, and performance
- **Don't:** Use default Image for heavy lists or unmaintained libraries
- Severity: Medium

## Specify image dimensions
Prevent layout shifts
- **Do:** width and height for remote images
- **Don't:** No dimensions for network images
- Severity: High

## Use resizeMode
Control image scaling
- **Do:** resizeMode cover contain
- **Don't:** Stretch images
- Severity: Low

## Use controlled inputs
State-controlled form fields
- **Do:** value + onChangeText
- **Don't:** Uncontrolled inputs
- Severity: Medium

## Handle keyboard
Manage keyboard visibility
- **Do:** KeyboardAvoidingView
- **Don't:** Content hidden by keyboard
- Severity: High

## Use proper keyboard types
Appropriate keyboard for input
- **Do:** keyboardType for input type
- **Don't:** Default keyboard for all
- Severity: Low

## Use Pressable
Modern touch handling
- **Do:** Pressable for touch interactions
- **Don't:** TouchableOpacity for new code
- Severity: Low

## Provide touch feedback
Visual feedback on press
- **Do:** Ripple or opacity change
- **Don't:** No feedback on press
- Severity: Medium

## Set hitSlop for small targets
Increase touch area
- **Do:** hitSlop for icons and small buttons
- **Don't:** Tiny touch targets
- Severity: Medium

## Use Reanimated
High-performance animations
- **Do:** react-native-reanimated
- **Don't:** Animated API for complex
- Severity: Medium

## Run on UI thread
worklets for smooth animation
- **Do:** Run animations on UI thread
- **Don't:** JS thread animations
- Severity: High

## Use gesture handler
Native gesture recognition
- **Do:** react-native-gesture-handler
- **Don't:** JS-based gesture handling
- Severity: Medium

## Handle loading states
Show loading indicators
- **Do:** ActivityIndicator during load
- **Don't:** Empty screen during load
- Severity: Medium

## Handle errors gracefully
Error boundaries and fallbacks
- **Do:** Error UI for failed requests
- **Don't:** Crash on error
- Severity: High

## Cancel async operations
Cleanup on unmount
- **Do:** AbortController or cleanup
- **Don't:** Memory leaks from async
- Severity: High

## Add accessibility labels
Describe UI elements
- **Do:** accessibilityLabel for all interactive
- **Don't:** Missing labels
- Severity: High

## Use accessibility roles
Semantic meaning
- **Do:** accessibilityRole for elements
- **Don't:** Wrong roles
- Severity: Medium

## Support screen readers
Test with TalkBack/VoiceOver
- **Do:** Test with screen readers
- **Don't:** Skip accessibility testing
- Severity: High

## Use React Native Testing Library
Component testing
- **Do:** render and fireEvent
- **Don't:** Enzyme or manual testing
- Severity: Medium

## Test on real devices
Real device behavior
- **Do:** Test on iOS and Android devices
- **Don't:** Simulator only
- Severity: High

## Use Detox for E2E
End-to-end testing
- **Do:** Detox for critical flows
- **Don't:** Manual E2E testing
- Severity: Medium

## Use native modules carefully
Bridge has overhead
- **Do:** Batch native calls
- **Don't:** Frequent bridge crossing
- Severity: High

## Use Expo when possible
Simplified development
- **Do:** Expo for standard features
- **Don't:** Bare RN for simple apps
- Severity: Low

## Handle permissions
Request permissions properly
- **Do:** Check and request permissions
- **Don't:** Assume permissions granted
- Severity: High
