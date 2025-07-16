# Ability: Edit Correction

**Project:** gemini-cli-main
**Category:** Code Analysis & Understanding
**Description:** Provides sophisticated mechanisms to correct and refine AI-generated code edits, particularly focusing on issues like incorrect escaping or mismatches between intended and actual code snippets. It leverages LLM calls for intelligent correction and uses caching for efficiency.

---

## 🎯 Entry Points

*   `packages/core/src/utils/editCorrector.ts`: `ensureCorrectEdit` - Main function for correcting `EditToolParams` (old_string/new_string) based on file content and LLM feedback.
*   `packages/core/src/utils/editCorrector.ts`: `ensureCorrectFileContent` - Corrects escaping issues in a given content string using LLM feedback.

---

## ⚙️ Dissection & Granular Operations

### Component: ensureCorrectEdit
**Description:** Attempts to correct `old_string` and `new_string` parameters for an edit operation. It first checks for exact matches, then tries unescaping, and if necessary, uses LLM calls (`correctOldStringMismatch`, `correctNewString`, `correctNewStringEscaping`) to align the proposed edit with the actual file content. It also incorporates a cache (`editCorrectionCache`) to avoid redundant LLM calls.
**Source Code Location:** `packages/core/src/utils/editCorrector.ts` - `ensureCorrectEdit`
**Inputs:** `filePath: string`, `currentContent: string`, `originalParams: EditToolParams`, `client: GeminiClient`, `abortSignal: AbortSignal`
**Outputs:** `Promise<CorrectedEditResult>`
**Dependencies:** `unescapeStringForGeminiBug`, `countOccurrences`, `findLastEditTimestamp`, `correctOldStringMismatch`, `correctNewString`, `correctNewStringEscaping`, `trimPairIfPossible`, `LruCache`
**Notes:** This is a complex orchestration of multiple correction strategies, including LLM-based reasoning, to ensure the AI's proposed edits are valid and applicable.

### Component: ensureCorrectFileContent
**Description:** Specifically focuses on correcting escaping issues within a general content string. It uses `unescapeStringForGeminiBug` for initial unescaping and then `correctStringEscaping` (an LLM call) for more intelligent correction. Results are cached.
**Source Code Location:** `packages/core/src/utils/editCorre corrector.ts` - `ensureCorrectFileContent`
**Inputs:** `content: string`, `client: GeminiClient`, `abortSignal: AbortSignal`
**Outputs:** `Promise<string>`
**Dependencies:** `unescapeStringForGeminiBug`, `correctStringEscaping`, `LruCache`
**Notes:** Used when the AI generates a new file content or a large block of text that might have escaping problems.

### Component: findLastEditTimestamp
**Description:** Analyzes the Gemini client's conversation history to find the timestamp of the most recent edit made by the system to a specific file. This helps in determining if a file has been externally modified since the last AI interaction.
**Source Code Location:** `packages/core/src/utils/editCorrector.ts` - `findLastEditTimestamp`
**Inputs:** `filePath: string`, `client: GeminiClient`
**Outputs:** `Promise<number>` (timestamp or -1 if not found)
**Dependencies:** `GeminiClient.getHistory()`, `isFunctionCall`, `isFunctionResponse`, `getTimestampFromFunctionId`
**Notes:** A clever way to maintain context and detect external changes to the codebase.

### Component: correctOldStringMismatch
**Description:** An LLM-powered function that attempts to find the correct `old_string` in the file content when the initially proposed `old_string` doesn't exactly match. It guides the LLM to identify the most likely intended segment, correcting for escaping, whitespace, or minor formatting differences.
**Source Code Location:** `packages/core/src/utils/editCorrector.ts` - `correctOldStringMismatch`
**Inputs:** `geminiClient: GeminiClient`, `fileContent: string`, `problematicSnippet: string`, `abortSignal: AbortSignal`
**Outputs:** `Promise<string>` (corrected old string)
**Dependencies:** `GeminiClient.generateJson`, `OLD_STRING_CORRECTION_SCHEMA`
**Notes:** This is a key component for making AI-driven edits robust against subtle mismatches.

### Component: correctNewString
**Description:** An LLM-powered function that adjusts the `new_string` to align with a `corrected_old_string`, preserving the original intent of the change. This is used when the `old_string` had to be corrected, and the `new_string` needs to be re-evaluated in that new context.
**Source Code Location:** `packages/core/src/utils/editCorrector.ts` - `correctNewString`
**Inputs:** `geminiClient: GeminiClient`, `originalOldString: string`, `correctedOldString: string`, `originalNewString: string`, `abortSignal: AbortSignal`
**Outputs:** `Promise<string>` (corrected new string)
**Dependencies:** `GeminiClient.generateJson`, `NEW_STRING_CORRECTION_SCHEMA`
**Notes:** Ensures the proposed replacement remains semantically correct even after `old_string` adjustments.

### Component: correctNewStringEscaping / correctStringEscaping
**Description:** LLM-powered functions that specifically address over-escaping issues in strings (e.g., `\n` instead of `
`). They guide the LLM to produce syntactically valid strings for insertion into code.
**Source Code Location:** `packages/core/src/utils/editCorrector.ts`
**Inputs:** `geminiClient: GeminiClient`, `oldString: string`, `potentiallyProblematicNewString: string`, `abortSignal: AbortSignal` (for `correctNewStringEscaping`); `potentiallyProblematicString: string`, `client: GeminiClient`, `abortSignal: AbortSignal` (for `correctStringEscaping`)
**Outputs:** `Promise<string>` (string with corrected escaping)
**Dependencies:** `GeminiClient.generateJson`, `CORRECT_NEW_STRING_ESCAPING_SCHEMA`, `CORRECT_STRING_ESCAPING_SCHEMA`
**Notes:** Crucial for ensuring AI-generated code snippets are directly usable without manual fixes.

### Component: unescapeStringForGeminiBug
**Description:** A utility function that attempts to unescape strings that might have been overly escaped by an LLM. It uses regex to replace common over-escaped sequences (e.g., `\n` to `
`).
**Source Code Location:** `packages/core/src/utils/editCorrector.ts` - `unescapeStringForGeminiBug`
**Inputs:** `inputString: string`
**Outputs:** `string` (unescaped string)
**Dependencies:** None
**Notes:** A pragmatic solution for known LLM output quirks.

### Component: countOccurrences
**Description:** A simple utility function to count the number of occurrences of a substring within a larger string.
**Source Code Location:** `packages/core/src/utils/editCorrector.ts` - `countOccurrences`
**Inputs:** `str: string`, `substr: string`
**Outputs:** `number`
**Dependencies:** None
**Notes:** Used to verify if the `old_string` matches the expected number of times.

---

## ✨ Best Practices & Patterns

*   **LLM-Driven Self-Correction:** The most prominent pattern is the use of LLMs to self-correct their own outputs (e.g., `old_string` mismatches, escaping issues). This makes the AI agent more robust and autonomous.
*   **Contextual Awareness:** The `findLastEditTimestamp` function demonstrates how to use conversation history and file metadata to maintain context and detect external changes, which is vital for reliable AI-driven code modification.
*   **Layered Correction Strategies:** Combines simple string manipulations (unescaping, trimming) with complex LLM calls, applying the most appropriate strategy based on the problem.
*   **Caching for Efficiency:** Utilizes `LruCache` to store results of correction attempts, reducing redundant LLM calls and improving performance.
*   **Structured Prompting for LLM Correction:** The detailed prompts for `correctOldStringMismatch`, `correctNewString`, and `correctNewStringEscaping` are excellent examples of how to guide an LLM to perform very specific, nuanced text transformations.
*   **Robustness against LLM Quirks:** Explicitly addresses known issues like over-escaping from LLMs, making the system more resilient.

---

## 💡 Potential for AIPass-Echosystem

*   **Intelligent Code Editing Module:** The entire `editCorrector.ts` module is a goldmine for building a sophisticated code editing capability in AIPass-Echosystem. Its ability to self-correct and adapt to code changes is highly valuable.
*   **LLM Output Post-Processing Pipeline:** The various `correctStringEscaping`, `correctNewString`, and `correctOldStringMismatch` functions can be generalized into a post-processing pipeline for any LLM output that needs to be syntactically correct or aligned with specific contexts.
*   **Context-Aware Code Modification:** The `findLastEditTimestamp` pattern can be adapted to build modules that understand the history of code changes, allowing AIPass-Echosystem to make more informed and safer modifications.
*   **Prompt Engineering for Correction:** The detailed prompts used here provide excellent examples for designing prompts that guide LLMs to perform precise, self-correcting tasks within AIPass-Echosystem.
*   **Caching Strategy for AI Interactions:** The use of `LruCache` for LLM call results is a pattern that can be applied broadly across AIPass-Echosystem to optimize performance and reduce API costs.

---

## 🔗 Related Files & Resources

*   `packages/core/src/tools/edit.ts`
*   `packages/core/src/tools/write-file.ts`
*   `packages/core/src/tools/read-file.ts`
*   `packages/core/src/tools/read-many-files.ts`
*   `packages/core/src/tools/grep.ts`
*   `packages/core/src/core/client.ts`
*   `packages/core/src/utils/LruCache.ts`
*   `packages/core/src/config/models.ts`
*   `packages/core/src/utils/messageInspectors.ts`
*   `packages/core/src/utils/editCorrector.test.ts` (for testing insights)
