
# Ability Card: Server

**Project:** `DesktopCommanderMCP`

**Description:**
(A brief, one-sentence description of the ability's primary function, to be filled in manually).

---

## Entry Points

*   `server.ts`

---

## Components

### Code Summary

# Analysis for `DesktopCommanderMCP-main/src/server.ts`



### Dependency Graph

```dot
digraph dependencies {
    rankdir=LR;
    node [shape=box, style="rounded,filled", fillcolor=lightgrey];
    graph [splines=ortho];
    "@modelcontextprotocol/sdk/server/index.js" [fillcolor=lightblue];
    "@modelcontextprotocol/sdk/types.js" [fillcolor=lightblue];
    "C:\Source-Codebase\DesktopCommanderMCP-main\src\handlers\index.js" [fillcolor=lightblue];
    "C:\Source-Codebase\DesktopCommanderMCP-main\src\tools\config.js" [fillcolor=lightblue];
    "C:\Source-Codebase\DesktopCommanderMCP-main\src\tools\feedback.js" [fillcolor=lightblue];
    "C:\Source-Codebase\DesktopCommanderMCP-main\src\tools\schemas.js" [fillcolor=lightblue];
    "C:\Source-Codebase\DesktopCommanderMCP-main\src\tools\usage.js" [fillcolor=lightblue];
    "C:\Source-Codebase\DesktopCommanderMCP-main\src\types.js" [fillcolor=lightblue];
    "C:\Source-Codebase\DesktopCommanderMCP-main\src\utils\capture.js" [fillcolor=lightblue];
    "C:\Source-Codebase\DesktopCommanderMCP-main\src\utils\system-info.js" [fillcolor=lightblue];
    "C:\Source-Codebase\DesktopCommanderMCP-main\src\utils\trackTools.js" [fillcolor=lightblue];
    "C:\Source-Codebase\DesktopCommanderMCP-main\src\utils\usageTracker.js" [fillcolor=lightblue];
    "C:\Source-Codebase\DesktopCommanderMCP-main\src\version.js" [fillcolor=lightblue];
    "server";
    "zod-to-json-schema" [fillcolor=lightblue];
    "server" -> "@modelcontextprotocol/sdk/server/index.js";
    "server" -> "@modelcontextprotocol/sdk/types.js";
    "server" -> "zod-to-json-schema";
    "server" -> "C:\Source-Codebase\DesktopCommanderMCP-main\src\utils\system-info.js";
    "server" -> "C:\Source-Codebase\DesktopCommanderMCP-main\src\tools\schemas.js";
    "server" -> "C:\Source-Codebase\DesktopCommanderMCP-main\src\tools\config.js";
    "server" -> "C:\Source-Codebase\DesktopCommanderMCP-main\src\tools\usage.js";
    "server" -> "C:\Source-Codebase\DesktopCommanderMCP-main\src\tools\feedback.js";
    "server" -> "C:\Source-Codebase\DesktopCommanderMCP-main\src\utils\trackTools.js";
    "server" -> "C:\Source-Codebase\DesktopCommanderMCP-main\src\utils\usageTracker.js";
    "server" -> "C:\Source-Codebase\DesktopCommanderMCP-main\src\version.js";
    "server" -> "C:\Source-Codebase\DesktopCommanderMCP-main\src\utils\capture.js";
    "server" -> "C:\Source-Codebase\DesktopCommanderMCP-main\src\handlers\index.js";
    "server" -> "C:\Source-Codebase\DesktopCommanderMCP-main\src\types.js";
}
```

---

## Best Practices & Observations

*   (To be filled in manually)

---

## Potential for AIPass-Echosystem

*   (To be filled in manually)

