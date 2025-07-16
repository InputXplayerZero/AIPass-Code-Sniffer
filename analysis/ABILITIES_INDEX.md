# Cross-Project Abilities Index

This index catalogs specific functional modules ("abilities") identified and dissected across various open-source projects. It serves as a reference for understanding implementation patterns and identifying reusable components for the AIPass-Echosystem.

---

## Gemini

### Project: gemini-cli-main

#### Category: File System Interaction

*   **Read File:** Reads and returns the content of a specified file. ([Details](./gemini-cli-main/abilities/read_file.md))
*   **Write File:** Writes content to a specified file, handling creation, overwriting, and user confirmation. ([Details](./gemini-cli-main/abilities/write_file.md))
*   **Search File Content (Grep):** Searches for a regular expression pattern within file contents, with multi-strategy execution. ([Details](./gemini-cli-main/abilities/search_file_content.md))
*   **List Directory (LS Tool):** Lists files and subdirectories within a path, with filtering and `.gitignore` support. ([Details](./gemini-cli-main/abilities/list_directory.md))

#### Category: Code Analysis & Understanding

*   **Summarize Tool Output:** Summarizes tool execution output using an LLM, extracting main points, errors, and warnings. ([Details](./gemini-cli-main/abilities/summarize_tool_output.md))
*   **Code Assist Service Setup:** Orchestrates the setup and initialization of the Code Assist service, including authentication and configuration. ([Details](./gemini-cli-main/abilities/code_assist_service_setup.md))
*   **API Data Conversion:** Handles conversion of data structures between internal formats and Code Assist API formats. ([Details](./gemini-cli-main/abilities/api_data_conversion.md))
*   **Edit Correction:** Corrects and refines AI-generated code edits, addressing escaping issues and mismatches using LLM feedback. ([Details](./gemini-cli-main/abilities/edit_correction.md))

#### Category: User Interface / CLI

*   **Chat History Management:** Manages saving, listing, and resuming user conversation checkpoints. ([Details](./gemini-cli-main/abilities/chat_history_management.md))
*   **Keypress Handling (CLI):** Listens for and processes keypress events from stdin, including special keys and bracketed paste. ([Details](./gemini-cli-main/abilities/keypress_handling.md))
*   **Gemini Stream Management:** Manages the entire lifecycle of interaction with the Gemini model, including input, streaming responses, and tool orchestration. ([Details](./gemini-cli-main/abilities/gemini_stream_management.md))
*   **Status Color Formatting:** Provides utilities for applying color coding to numerical status values based on thresholds. ([Details](./gemini-cli-main/abilities/status_color_formatting.md))
*   **Markdown Safe Splitting:** Intelligently splits large Markdown content at "safe" points to preserve formatting integrity. ([Details](./gemini-cli-main/abilities/markdown_safe_splitting.md))