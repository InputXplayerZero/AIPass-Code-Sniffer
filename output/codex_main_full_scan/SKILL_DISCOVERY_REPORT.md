# Skill Discovery Report

**Generated:** 2025-07-19T01:11:44.366727  
**Codebase:** `C:\Source-Codebase\research_review\pending\codex-main`  
**Files Analyzed:** 195  
**Skills Detected:** 146

## Executive Summary

This codebase contains **146 extractable skills** across 11 categories. 
**20 high-priority skills** have been identified for immediate extraction.

## Category Breakdown

| Category | Skills | Priority |
|----------|---------|----------|
| Cli Operations | 38 | 📋 Medium |
| File Operations | 34 | 🔥 High |
| Code Processing | 22 | 📋 Medium |
| Prompt Engineering | 12 | 📋 Medium |
| Natural Language | 11 | 📋 Medium |
| Api Frameworks | 9 | 📋 Medium |
| Configuration | 6 | 📋 Medium |
| Error Handling | 6 | 📋 Medium |
| Memory Systems | 5 | 📋 Medium |
| Mcp Integration | 2 | 📋 Medium |
| Indexing Systems | 1 | 📋 Medium |

## High-Priority Skills (20)

These skills are recommended for immediate extraction:

1. **tryParseApplyPatch** (code_processing)
   - File: `C:\Source-Codebase\research_review\pending\codex-main\codex-cli\src\approvals.ts`
   - Confidence: 90.0% | Priority: 100.0%
   - Code processor: tryParseApplyPatch

2. **isParseEntryWithOp** (code_processing)
   - File: `C:\Source-Codebase\research_review\pending\codex-main\codex-cli\src\approvals.ts`
   - Confidence: 90.0% | Priority: 100.0%
   - Code processor: isParseEntryWithOp

3. **parseApplyPatch** (code_processing)
   - File: `C:\Source-Codebase\research_review\pending\codex-main\codex-cli\src\parse-apply-patch.ts`
   - Confidence: 90.0% | Priority: 100.0%
   - Code processor: parseApplyPatch

4. **parse** (code_processing)
   - File: `C:\Source-Codebase\research_review\pending\codex-main\codex-cli\src\typings.d.ts`
   - Confidence: 90.0% | Priority: 100.0%
   - Code processor: parse

5. **TerminalChatPastRollout** (code_processing)
   - File: `C:\Source-Codebase\research_review\pending\codex-main\codex-cli\src\components\chat\terminal-chat-past-rollout.tsx`
   - Confidence: 90.0% | Priority: 100.0%
   - Code processor: TerminalChatPastRollout

6. **generateCommandExplanation** (code_processing)
   - File: `C:\Source-Codebase\research_review\pending\codex-main\codex-cli\src\components\chat\terminal-chat.tsx`
   - Confidence: 90.0% | Priority: 100.0%
   - Code processor: generateCommandExplanation

7. **lastIndex** (code_processing)
   - File: `C:\Source-Codebase\research_review\pending\codex-main\codex-cli\src\components\select-input\select-input.tsx`
   - Confidence: 90.0% | Priority: 100.0%
   - Code processor: lastIndex

8. **generateCompactSummary** (code_processing)
   - File: `C:\Source-Codebase\research_review\pending\codex-main\codex-cli\src\utils\compact-summary.ts`
   - Confidence: 90.0% | Priority: 100.0%
   - Code processor: generateCompactSummary

9. **generatePKCECodes** (code_processing)
   - File: `C:\Source-Codebase\research_review\pending\codex-main\codex-cli\src\utils\get-api-key.tsx`
   - Confidence: 90.0% | Priority: 100.0%
   - Code processor: generatePKCECodes

10. **parseToolCallOutput** (code_processing)
   - File: `C:\Source-Codebase\research_review\pending\codex-main\codex-cli\src\utils\parsers.ts`
   - Confidence: 90.0% | Priority: 100.0%
   - Code processor: parseToolCallOutput

## Extraction Recommendations

### 1. File Operations

- **Priority:** Medium
- **Skills Available:** 34
- **Extraction Effort:** Low
- **Integration Value:** 42.0%
- **Action:** Extract as core utility modules

**Top Skills:**
- isWritePatchConstrainedToWritablePaths
- isPathConstrainedTowritablePaths
- resolvePathAgainstWorkdir
- pathContains
- createTwoFilesPatch

### 2. Code Processing

- **Priority:** Medium
- **Skills Available:** 22
- **Extraction Effort:** Low
- **Integration Value:** 28.0%
- **Action:** Evaluate for potential extraction

**Top Skills:**
- tryParseApplyPatch
- isParseEntryWithOp
- parseApplyPatch
- parse
- TerminalChatPastRollout

### 3. Natural Language

- **Priority:** Medium
- **Skills Available:** 11
- **Extraction Effort:** Low
- **Integration Value:** 26.0%
- **Action:** Evaluate for potential extraction

**Top Skills:**
- createEnvContext
- MultilineTextEditorInner
- TextInput
- UncontrolledTextInput
- calculateContextPercentRemaining

### 4. Cli Operations

- **Priority:** Medium
- **Skills Available:** 38
- **Extraction Effort:** Low
- **Integration Value:** 26.0%
- **Action:** Evaluate for potential extraction

**Top Skills:**
- processLabelConfig
- processLabel
- runCommand
- isSafeCommand
- formatCommandForDisplay

### 5. Prompt Engineering

- **Priority:** Medium
- **Skills Available:** 12
- **Extraction Effort:** Low
- **Integration Value:** 26.0%
- **Action:** Evaluate for potential extraction

**Top Skills:**
- renderPromptTemplate
- loadPromptHistory
- savePromptHistory
- InputPrompt
- ConfirmationPrompt

### 6. Memory Systems

- **Priority:** Medium
- **Skills Available:** 5
- **Extraction Effort:** Low
- **Integration Value:** 26.0%
- **Action:** Evaluate for potential extraction

**Top Skills:**
- loadSessions
- SessionsOverlay
- setSessionId
- getSessionId
- createInMemoryFS

### 7. Api Frameworks

- **Priority:** Medium
- **Skills Available:** 9
- **Extraction Effort:** Low
- **Integration Value:** 26.0%
- **Action:** Evaluate for potential extraction

**Top Skills:**
- capitalize
- setApiKey
- getApiKey
- getApiKey
- fetchModels

### 8. Configuration

- **Priority:** Medium
- **Skills Available:** 6
- **Extraction Effort:** Low
- **Integration Value:** 22.0%
- **Action:** Evaluate for potential extraction

**Top Skills:**
- getOidcConfiguration
- loadConfig
- loadConfig
- getDefaultConfig
- saveConfig

### 9. Error Handling

- **Priority:** Medium
- **Skills Available:** 6
- **Extraction Effort:** Low
- **Integration Value:** 22.0%
- **Action:** Evaluate for potential extraction

**Top Skills:**
- isExecSyncError
- abortHandler
- handleCallback
- isTooManyTokensError
- isRateLimitError

## Integration Roadmap

### Phase 3: Advanced Features - AI & Data

- **Duration:** 3-6 weeks
- **Effort:** High
- **Value:** Very High
- **Description:** Extract AI tools and data processing capabilities

**Skills to Extract:**
- isServerError
- isNetworkOrServerError


---
*Generated by AIPass-Code-Sniffer Skill Discovery Engine*
