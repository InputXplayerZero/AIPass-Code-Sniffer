# Ability: Input History Management (CLI)

**Project:** gemini-cli-main
**Category:** User Interface / CLI
**Description:** Manages the history of user input in the command-line interface, allowing users to navigate through previous commands using arrow keys and submit them.

---

## 🎯 Entry Points

*   `packages/cli/src/ui/hooks/useInputHistory.ts`: `useInputHistory` - A React hook that provides functionality for managing and navigating input history.

---

## ⚙️ Dissection & Granular Operations

### Component: useInputHistory (Hook)
**Description:** This custom React hook encapsulates the state and logic for managing a list of `userMessages` (previous commands). It provides functions to handle input submission, navigate up and down the history, and reset the history navigation state.
**Source Code Location:** `packages/cli/src/ui/hooks/useInputHistory.ts` - `useInputHistory`
**Inputs:** 
*   `userMessages: readonly string[]` (array of past user inputs)
*   `onSubmit: (value: string) => void` (callback for submitting input)
*   `isActive: boolean` (indicates if the input component is active)
*   `currentQuery: string` (the current text in the input field)
*   `onChange: (value: string) => void` (callback for updating the input field)
**Outputs:** An object containing:
*   `handleSubmit: (value: string) => void`
*   `navigateUp: () => boolean`
*   `navigateDown: () => boolean`
**Dependencies:** `react` (`useState`, `useCallback`)
**Notes:** It maintains `historyIndex` to track the current position in the history and `originalQueryBeforeNav` to restore the query when exiting history navigation.

### Component: handleSubmit
**Description:** A memoized callback function that trims the input value and calls the `onSubmit` prop if the value is not empty. It also resets the history navigation state after submission.
**Source Code Location:** `packages/cli/src/ui/hooks/useInputHistory.ts` - `handleSubmit` (returned by `useInputHistory`)
**Inputs:** `value: string` (the input string to submit)
**Outputs:** None (side effect: calls `onSubmit` and `resetHistoryNav`)
**Dependencies:** `onSubmit`, `resetHistoryNav`
**Notes:** Ensures only non-empty, trimmed inputs are submitted and prepares the history for the next interaction.

### Component: navigateUp
**Description:** A memoized callback function that moves the `historyIndex` up (towards older messages) in the `userMessages` array. It updates the input field with the historical message and stores the `currentQuery` if starting navigation from a fresh input.
**Source Code Location:** `packages/cli/src/ui/hooks/useInputHistory.ts` - `navigateUp` (returned by `useInputHistory`)
**Inputs:** None
**Outputs:** `boolean` (true if navigation occurred, false otherwise)
**Dependencies:** `historyIndex`, `userMessages`, `currentQuery`, `onChange`, `setHistoryIndex`, `setOriginalQueryBeforeNav`
**Notes:** Handles boundary conditions (beginning of history) and ensures the input field reflects the selected history item.

### Component: navigateDown
**Description:** A memoized callback function that moves the `historyIndex` down (towards newer messages or the current input) in the `userMessages` array. It restores the `originalQueryBeforeNav` if the end of history navigation is reached.
**Source Code Location:** `packages/cli/src/ui/hooks/useInputHistory.ts` - `navigateDown` (returned by `useInputHistory`)
**Inputs:** None
**Outputs:** `boolean` (true if navigation occurred, false otherwise)
**Dependencies:** `historyIndex`, `userMessages`, `originalQueryBeforeNav`, `onChange`, `setHistoryIndex`
**Notes:** Manages the transition from history navigation back to the current input state.

---

## ✨ Best Practices & Patterns

*   **Custom React Hook:** Encapsulates stateful logic and side effects related to input history, promoting reusability and separation of concerns in React components.
*   **Controlled Component Pattern:** The hook works with `currentQuery` and `onChange` props, allowing the parent component to control the input field's value.
*   **Memoization (`useCallback`):** Prevents unnecessary re-renders of child components by memoizing callback functions, improving performance.
*   **Clear State Management:** Uses `useState` to manage `historyIndex` and `originalQueryBeforeNav` effectively, ensuring correct history navigation and restoration.
*   **User Experience Focus:** Provides intuitive navigation for command history, a common and expected feature in CLI tools.

---

## 💡 Potential for AIPass-Echosystem

*   **Reusable CLI Input Component:** The logic within `useInputHistory` can be adapted to create a generic, reusable input component for any CLI or interactive text interface in AIPass-Echosystem that requires command history.
*   **State Management for Interactive Tools:** The patterns for managing `historyIndex` and `originalQueryBeforeNav` can be applied to other interactive tools within AIPass-Echosystem that need to maintain state across user interactions.
*   **Performance Optimization in UI:** The use of `useCallback` serves as a good example for optimizing performance in React-based UI components within AIPass-Echosystem.
*   **Modular UI Logic:** This hook demonstrates how to break down complex UI logic (like input handling) into smaller, testable, and reusable units.

---

## 🔗 Related Files & Resources

*   `packages/cli/src/ui/hooks/useInputHistory.test.ts` (for testing insights)
*   `packages/cli/src/ui/hooks/useKeypress.ts` (likely consumer of this hook)
