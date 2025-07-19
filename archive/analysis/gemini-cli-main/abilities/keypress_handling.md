# Ability: Keypress Handling (CLI)

**Project:** gemini-cli-main
**Category:** User Interface / CLI
**Description:** A React hook that listens for keypress events from stdin, providing structured key information including special keys and handling for bracketed paste mode.

---

## 🎯 Entry Points

*   `packages/cli/src/ui/hooks/useKeypress.ts`: `useKeypress` - The main React hook for keypress event listening.

---

## ⚙️ Dissection & Granular Operations

### Component: useKeypress (Hook)
**Description:** Sets up and tears down event listeners for `stdin` keypresses. It handles raw mode, integrates with Node's `readline` for key parsing, and includes a custom workaround for bracketed paste mode, especially for older Node.js versions.
**Source Code Location:** `packages/cli/src/ui/hooks/useKeypress.ts` - `useKeypress`
**Inputs:** `onKeypress: (key: Key) => void` (callback for key events), `{ isActive: boolean }` (option to activate/deactivate listener).
**Outputs:** None (side effect: calls `onKeypress` callback).
**Dependencies:** `react` (`useEffect`, `useRef`), `ink` (`useStdin`), `readline`, `stream` (`PassThrough`).
**Notes:** Manages raw terminal mode, crucial for capturing individual keypresses. The paste workaround is a notable feature for cross-platform compatibility.

### Component: handleKeypress
**Description:** The internal handler for processed keypress events from `readline`. It distinguishes between regular keypresses, paste-start/paste-end markers, and accumulates paste buffer content.
**Source Code Location:** `packages/cli/src/ui/hooks/useKeypress.ts` - `handleKeypress` (internal function within `useEffect`)
**Inputs:** `_: unknown`, `key: Key`
**Outputs:** None (side effect: calls `onKeypressRef.current` with processed `Key` object).
**Dependencies:** `isPaste`, `pasteBuffer`, `onKeypressRef.current`.
**Notes:** This is where the `Key` object is enriched with the `paste` flag.

### Component: handleRawKeypress
**Description:** A custom raw data handler for `stdin` that specifically detects and processes bracketed paste sequences (`\x1B[200~` and `\x1B[201~`). It extracts the paste content and emits synthetic `paste-start`/`paste-end` key events.
**Source Code Location:** `packages/cli/src/ui/hooks/useKeypress.ts` - `handleRawKeypress` (internal function within `useEffect`)
**Inputs:** `data: Buffer` (raw stdin data).
**Outputs:** None (side effect: writes to `keypressStream` or calls `handleKeypress`).
**Dependencies:** `PASTE_MODE_PREFIX`, `PASTE_MODE_SUFFIX`, `keypressStream`, `handleKeypress`.
**Notes:** This is the core of the bracketed paste workaround, allowing the CLI to correctly handle pasted text as a single event.

### Component: Key Interface
**Description:** Defines the structure of a keypress event, including the key name, modifier keys (ctrl, meta, shift), a `paste` flag, and the raw sequence.
**Source Code Location:** `packages/cli/src/ui/hooks/useKeypress.ts` - `Key` interface
**Inputs:** N/A
**Outputs:** N/A
**Dependencies:** N/A
**Notes:** Provides a standardized data structure for key events.

---

## ✨ Best Practices & Patterns

*   **Event Listener Management:** Proper setup and cleanup of `useEffect` for adding and removing event listeners, preventing memory leaks.
*   **Raw Mode Control:** Manages `stdin` raw mode for direct keypress capture, essential for interactive CLI applications.
*   **Cross-Platform Compatibility:** Includes a workaround for Node.js versions that don't natively support bracketed paste, demonstrating attention to broader usability.
*   **Ref for Callbacks:** Uses `useRef` to store the `onKeypress` callback, ensuring the `useEffect` doesn't re-run unnecessarily when the callback changes, optimizing performance.
*   **Stream Processing:** Leverages Node.js streams (`PassThrough`, `readline`) for efficient handling of raw input data.

---

## 💡 Potential for AIPass-Echosystem

*   **Generic CLI Input Handler:** The `useKeypress` hook can be adapted into a reusable module for any interactive CLI component in AIPass-Echosystem that requires fine-grained control over keyboard input, including special keys and paste events.
*   **Cross-Environment Input Normalization:** The paste workaround and general key parsing logic can inform the development of a robust input normalization layer for AIPass-Echosystem, ensuring consistent behavior across different terminal environments.
*   **Interactive UI Component Foundation:** This hook provides a fundamental building block for creating highly interactive and responsive CLI user interfaces within AIPass-Echosystem.
*   **Event-Driven Architecture:** The pattern of emitting and handling key events can be generalized for other event-driven interactions within AIPass-Echosystem.

---

## 🔗 Related Files & Resources

*   `packages/cli/src/ui/hooks/useKeypress.test.ts`
*   `packages/cli/src/ui/hooks/useInputHistory.ts` (likely consumer)
*   `ink` (React for CLIs library)
*   Node.js `readline` module documentation.
