# Project Summary: codex-main

**Purpose:** A command-line coding agent from OpenAI that runs locally on your computer. It allows you to interact with your codebase using natural language, and it can execute commands, manipulate files, and iterate on your code.

**Directory Map:** [codex-main_map.txt](./codex-main_map.txt)

**Technology Stack:**
*   **Core Languages:** Rust, TypeScript
*   **Package Management:** `pnpm` (for the monorepo and TypeScript packages), `cargo` (for Rust, managed via Nix)
*   **Environment Management:** Nix
*   **CLI Framework:** Likely a combination of a Rust CLI framework and `pnpm` scripting.
*   **Key Tools:** `prettier` (for formatting), `husky` (for git hooks)
