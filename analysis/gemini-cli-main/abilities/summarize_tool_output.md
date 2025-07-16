# Ability: Summarize Tool Output

**Project:** gemini-cli-main
**Category:** Code Analysis & Understanding
**Description:** Summarizes the output of tool executions, especially for large outputs, using a Gemini model to extract main points, errors, and warnings. It provides a concise summary to the LLM.

---

## 🎯 Entry Points

*   `packages/core/src/utils/summarizer.ts`: `llmSummarizer` - The primary entry point for summarizing tool results using an LLM.
*   `packages/core/src/utils/summarizer.ts`: `summarizeToolOutput` - The core asynchronous function that performs the summarization using the Gemini client.

---

## ⚙️ Dissection & Granular Operations

### Component: defaultSummarizer
**Description:** A basic, fallback summarizer that simply converts the `llmContent` of a `ToolResult` to a JSON string. Used when no LLM-based summarization is needed or available.
**Source Code Location:** `packages/core/src/utils/summarizer.ts` - `defaultSummarizer`
**Inputs:** `result: ToolResult`, `geminiClient: GeminiClient`, `abortSignal: AbortSignal`
**Outputs:** `Promise<string>` (JSON string representation of `llmContent`)
**Dependencies:** `ToolResult`
**Notes:** Serves as a simple, non-LLM-dependent summarization option.

### Component: partToString
**Description:** A utility function to convert various types of `PartListUnion` (content parts from Gemini API) into a single string. Handles strings, arrays of parts, and parts with a `text` property.
**Source Code Location:** `packages/core/src/utils/summarizer.ts` - `partToString`
**Inputs:** `part: PartListUnion`
**Outputs:** `string`
**Dependencies:** None (pure utility function)
**Notes:** Essential for preparing LLM content for summarization or display.

### Component: getResponseText
**Description:** Extracts the text content from a `GenerateContentResponse` object received from the Gemini API. It looks for the first candidate's content parts and concatenates their text.
**Source Code Location:** `packages/core/src/utils/summarizer.ts` - `getResponseText`
**Inputs:** `response: GenerateContentResponse`
**Outputs:** `string | null`
**Dependencies:** `GenerateContentResponse`
**Notes:** A common pattern for processing LLM text responses.

### Component: SUMMARIZE_TOOL_OUTPUT_PROMPT
**Description:** A string template that defines the prompt sent to the Gemini model for summarization. It includes instructions on how to summarize different types of tool output (directory listings, text content, shell command output with errors/warnings) and placeholders for `maxOutputTokens` and `textToSummarize`.
**Source Code Location:** `packages/core/src/utils/summarizer.ts` - `SUMMARIZE_TOOL_OUTPUT_PROMPT`
**Inputs:** None (static string)
**Outputs:** `string`
**Dependencies:** None
**Notes:** The quality of the summarization heavily depends on this prompt's effectiveness.

### Component: summarizeToolOutput
**Description:** The core asynchronous function that performs the LLM-based summarization. It first checks if the `textToSummarize` is already within the `maxOutputTokens` limit; if so, it returns the original text. Otherwise, it constructs a prompt using `SUMMARIZE_TOOL_OUTPUT_PROMPT`, sends it to the Gemini client, and extracts the summarized text from the response.
**Source Code Location:** `packages/core/src/utils/summarizer.ts` - `summarizeToolOutput`
**Inputs:** `textToSummarize: string`, `geminiClient: GeminiClient`, `abortSignal: AbortSignal`, `maxOutputTokens: number`
**Outputs:** `Promise<string>` (summarized text or original text if no summarization needed/failed)
**Dependencies:** `GeminiClient`, `SUMMARIZE_TOOL_OUTPUT_PROMPT`, `partToString`, `getResponseText`
**Notes:** This function embodies the intelligent summarization logic, leveraging the LLM for complex text processing.

---

## ✨ Best Practices & Patterns

*   **Conditional Processing:** Summarization is only performed if the input text exceeds a certain length, optimizing token usage and latency.
*   **LLM-Driven Summarization:** Delegates complex summarization tasks to a powerful language model, allowing for nuanced and context-aware summaries.
*   **Structured Prompting:** Uses a detailed prompt template to guide the LLM on how to summarize different types of content, including specific instructions for error and warning extraction.
*   **Clear Input/Output Handling:** Utility functions (`partToString`, `getResponseText`) ensure consistent handling of LLM input and output formats.
*   **Error Handling for LLM Calls:** Includes a `try-catch` block for `geminiClient.generateContent` to gracefully handle LLM failures and return the original text.

---

## 💡 Potential for AIPass-Echosystem

*   **Generic LLM Summarization Module:** The `summarizeToolOutput` function (and its dependencies like `partToString`, `getResponseText`, and the prompt structure) can be adapted into a reusable module for any part of AIPass-Echosystem that needs to condense large text outputs using an LLM.
*   **Context-Aware Prompt Engineering:** The `SUMMARIZE_TOOL_OUTPUT_PROMPT` serves as an excellent example of how to craft detailed, multi-faceted prompts to achieve specific summarization goals, which is directly applicable to designing prompts for AIPass-Echosystem's AI agents.
*   **LLM Response Parsing Utilities:** `partToString` and `getResponseText` are valuable utilities for working with LLM API responses, which can be generalized for broader use in AIPass-Echosystem.
*   **Dynamic Output Management:** The concept of summarizing based on output size can be extended to other output processing steps in AIPass-Echosystem to manage information density and token usage.

---

## 🔗 Related Files & Resources

*   `packages/core/src/tools/tools.ts`
*   `packages/core/src/core/client.ts`
*   `packages/core/src/config/models.ts`
*   `packages/core/src/utils/summarizer.test.ts` (for testing insights)
