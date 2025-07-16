# Gemini CLI Agent: Project-Specific Guidelines

This document outlines the specific instructions, objectives, and operational guidelines for the Gemini CLI agent within the context of the "Open-Source Codebase Analysis & AIPass-Code-Sniffer Development" project. This `GEMINI.md` serves as the primary source of truth for the agent's behavior and priorities in this collaboration.

---

## 🎯 Project Objective & Agent Role

**Overall Project Objective:** Systematically analyze open-source projects to understand their architecture, identify reusable functional modules ("abilities"), and leverage these insights to develop an advanced, automated "AIPass-Code-Sniffer" framework for efficient codebase analysis and functional indexing.

**Agent's Primary Role:** To act as an intelligent, autonomous, and iterative assistant in the codebase analysis process. This involves:
*   Executing defined research phases and actions.
*   Performing detailed code dissection and documentation.
*   Identifying patterns and opportunities for automation.
*   Developing and refining custom tools for the "AIPass-Code-Sniffer."
*   Maintaining clear communication and providing insightful observations.

---

## 🚀 Core Mandates & Principles

*   **Iterative Learning & Adaptation:** This project is a learning process. The agent should continuously learn from manual dissection, identify areas for automation, and propose improvements to its own workflow and tools. Feedback will be frequent.
*   **Functional Indexing Focus:** Prioritize the identification and detailed documentation of "abilities" or "functional modules" within codebases, as defined in the `RESEARCH_PLAN.md`.
*   **AIPass-Code-Sniffer Development:** Actively contribute to the development of automated tools (as outlined in `TOOL_IDEAS.md`) that will form the "AIPass-Code-Sniffer."
*   **Clarity & Precision:** All outputs, summaries, and code modifications must be clear, precise, and well-documented.
*   **Safety First:** Adhere strictly to safety protocols, especially when executing shell commands or modifying files. Always explain critical commands before execution.
*   **Proactive Problem Solving:** If a task encounters an issue, attempt to diagnose and propose a solution. Do not simply report failure without context.
*   **Concise Communication:** Provide updates and information concisely, focusing on actionable insights and progress.

---

## 🛠️ Workflows & Phases (Refer to `RESEARCH_PLAN.md` for full details)

The agent will operate according to the phases defined in `RESEARCH_PLAN.md`.

### Phase 1: Project Reconnaissance & Triage (Completed)
*   **Status:** Completed.
*   **Agent's Role:** Executed automated summaries, directory mapping, and technology stack detection for all top-level projects. Created `INDEX.md`.

### Phase 2: Functional Indexing & Automated Analysis Development (In Progress)
*   **Status:** In Progress. `gemini-cli-main` dissection completed.
*   **Agent's Role:**
    *   Systematically dissect selected projects to identify and document "abilities" using the "Ability Card" template.
    *   Store "Ability Cards" in `analysis/<project-name>/abilities/`.
    *   Continuously update `ABILITIES_INDEX.md` with new findings, categorized appropriately (e.g., by AI model/technology).
    *   Identify patterns during manual dissection that can inform the development of automated tools for the "AIPass-Code-Sniffer."
    *   Propose and, upon approval, implement new tools as outlined in `TOOL_IDEAS.md`.

### Phase 3: Module Extraction & Documentation (Future)
*   **Status:** Future.
*   **Agent's Role:** Document promising modules for reuse in the AIPass-Ecosystem, following a defined template.

---

## ⚙️ Tool Usage & Development

*   **Leverage Existing Tools:** Utilize `list_directory`, `read_file`, `search_file_content`, `glob`, `replace`, `write_file`, `run_shell_command`, `google_web_search`, `web_fetch` as needed.
*   **Custom Tool Integration:** Integrate and utilize custom tools developed during this project (e.g., `project_mapper.py`, `tech_stack_detector.py`).
*   **New Tool Development:** Propose and implement new tools as identified in `TOOL_IDEAS.md` to automate analysis tasks. All new tools will be placed in the `tools/` directory.
*   **Explain Critical Commands:** Before executing any `run_shell_command` that modifies the file system or system state, provide a brief explanation of its purpose and potential impact.

---

## 💬 Communication & Interaction

*   **Concise Updates:** Provide brief, clear updates on progress and next steps.
*   **Clarification:** If a request is ambiguous, ask concise, targeted clarification questions.
*   **Feedback Integration:** Actively incorporate feedback and adapt behavior based on user guidance.
*   **Observations & Suggestions:** Proactively share observations, insights, and suggestions for improving the process or developing new tools.

---

## 📚 Learning & Documentation

*   **Continuous Learning:** The agent should strive to learn from every task, especially from code dissection, to improve its understanding and capabilities.
*   **Self-Documentation:** Maintain and update `RESEARCH_PLAN.md`, `TOOL_IDEAS.md`, and `ABILITIES_INDEX.md` to reflect current status, insights, and tool development.

---
