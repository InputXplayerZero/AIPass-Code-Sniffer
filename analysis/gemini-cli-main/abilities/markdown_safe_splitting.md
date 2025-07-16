# Ability: Markdown Safe Splitting

**Project:** gemini-cli-main
**Category:** User Interface / CLI
**Description:** Provides utilities for intelligently splitting large Markdown content, particularly from streaming LLM outputs, at "safe" points to preserve Markdown formatting integrity, especially for code blocks and paragraphs.

---

## 🎯 Entry Points

*   `packages/cli/src/ui/utils/markdownUtilities.ts`: `findLastSafeSplitPoint` - The primary function for determining an optimal index to split Markdown content without breaking its structure.

---

## ⚙️ Dissection & Granular Operations

### Component: findLastSafeSplitPoint
**Description:** The core logic for finding a safe split point in a Markdown string. It prioritizes splitting *before* an enclosing code block if the end of the content is within one. If not, it searches backward for the last double newline (`\n\n`) that is not inside a code block. If no such point is found, it returns the full content length.
**Source Code Location:** `packages/cli/src/ui/utils/markdownUtilities.ts` - `findLastSafeSplitPoint`
**Inputs:** `content: string` (the Markdown string to split)
**Outputs:** `number` (the character index at which to safely split the content)
**Dependencies:** `isIndexInsideCodeBlock`, `findEnclosingCodeBlockStart`
**Notes:** This function is critical for ensuring that streaming LLM output can be displayed incrementally without corrupting Markdown formatting, especially for code snippets.

### Component: isIndexInsideCodeBlock
**Description:** A helper function that determines if a given character index within a Markdown string falls inside a fenced code block (delimited by ` ``` `). It does this by counting code fences encountered before the index.
**Source Code Location:** `packages/cli/src/ui/utils/markdownUtilities.ts` - `isIndexInsideCodeBlock`
**Inputs:** `content: string`, `indexToTest: number`
**Outputs:** `boolean`
**Dependencies:** None
**Notes:** Essential for maintaining the integrity of code blocks during splitting.

### Component: findEnclosingCodeBlockStart
**Description:** A helper function that, given an index within a Markdown string, finds the starting index of the fenced code block that encloses it. Returns -1 if the index is not within a code block.
**Source Code Location:** `packages/cli/src/ui/utils/markdownUtilities.ts` - `findEnclosingCodeBlockStart`
**Inputs:** `content: string`, `index: number`
**Outputs:** `number` (start index of the code block or -1)
**Dependencies:** `isIndexInsideCodeBlock`
**Notes:** Used by `findLastSafeSplitPoint` to ensure splits do not occur within code blocks.

---

## ✨ Best Practices & Patterns

*   **Markdown Integrity:** Prioritizes preserving Markdown formatting, especially for critical elements like code blocks, when splitting text.
*   **Intelligent Splitting:** Avoids arbitrary splits and instead looks for natural break points (e.g., double newlines, before code blocks).
*   **Streaming UI Optimization:** Designed to support incremental rendering of large text outputs, improving perceived performance in interactive CLIs.
*   **Clear Heuristics:** The logic for determining safe split points is well-defined and prioritizes safety over strict length adherence.
*   **Utility Functions:** Breaks down the complex task into smaller, testable helper functions (`isIndexInsideCodeBlock`, `findEnclosingCodeBlockStart`).

---

## 💡 Potential for AIPass-Echosystem

*   **LLM Output Formatting Module:** The `findLastSafeSplitPoint` function is directly applicable to any component in AIPass-Echosystem that needs to display or process large, streaming Markdown content from LLMs, ensuring clean and readable output.
*   **Generic Text Splitting Utility:** The underlying logic for identifying safe break points can be generalized for other text processing tasks where content needs to be chunked while respecting structural boundaries.
*   **Streaming UI Component Integration:** This ability provides a crucial piece for building responsive streaming UI components in AIPass-Echosystem that can handle continuous text updates without visual glitches.
*   **Code Block Preservation:** The specific logic for handling code blocks is highly valuable for any AI agent that generates or modifies code, ensuring that code snippets are not broken across display boundaries.

---

## 🔗 Related Files & Resources

*   `packages/cli/src/ui/hooks/useGeminiStream.ts` (consumer of this utility)
*   `packages/cli/src/ui/utils/markdownUtilities.test.ts` (for testing insights)
