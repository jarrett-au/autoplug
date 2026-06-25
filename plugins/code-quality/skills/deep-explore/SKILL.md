---
name: deep-explore
description: "Multi-dimensional parallel codebase analysis — spawns 3-4 Explore SubAgents concurrently from different angles to deeply analyze a project, then synthesizes a structured report"
argument-hint: "<query> [--file path]"
user-invocable: true
allowed-tools: Agent Bash(ls *) Read Glob Grep
---

# Deep Explore

Parallel multi-dimensional codebase deep analysis tool.

## Trigger

```
/deep-explore <query> [--file <output-path>]
```

- `<query>`: What the user wants to understand (e.g., "认证系统是怎么设计的", "这个项目的整体架构", "handlePayment 的完整调用链")
- `--file <path>`: Optional. If provided, write the full report to this file instead of only outputting in chat.

## Core Workflow

### Step 1: Analyze Query & Determine Dimensions

Based on the user's query, determine 3-4 analysis dimensions. Do NOT use a fixed template — adapt dimensions to the query type:

**Examples of dimension adaptation:**

- Query "项目整体架构" → dimensions: module structure, entry points & routing, data layer, cross-cutting concerns
- Query "认证系统设计" → dimensions: auth flow & middleware, token/session management, permission model, security boundaries
- Query "handlePayment 调用链" → dimensions: caller chain (who calls it), callee chain (what it calls), error/edge cases, related tests
- Query "这个 API 怎么用" → dimensions: endpoint signatures & params, request/response examples, middleware pipeline, validation logic

**Principles for dimension selection:**
- Each dimension should be independently explorable (no dependency between agents)
- Dimensions should be complementary, not overlapping
- Prefer concrete angles over vague ones ("entry points & routing" > "general structure")
- Scale depth to query scope: a function-level query needs fewer/tighter dimensions than a system-level query

### Step 2: Determine Analysis Target

- Default: current working directory (CWD)
- If the user's query mentions a specific path, directory, or sub-project, use that as the analysis root
- If unsure, default to CWD

### Step 3: Determine Thoroughness

Automatically select based on query scope:
- **Function/file level query** → "medium" thoroughness, 2-3 agents
- **Module/feature level query** → "thorough" thoroughness, 3-4 agents  
- **System/architecture level query** → "very thorough" thoroughness, 3-4 agents

### Step 4: Launch Parallel Explore SubAgents

Spawn ALL agents in a **single message** with multiple Agent tool calls. Each agent:
- Uses `subagent_type: "Explore"`
- Uses `model: "sonnet"`
- Has a focused, self-contained prompt describing exactly what dimension to explore
- Includes the analysis target path context

**Agent prompt template:**

```
You are analyzing [target path] to understand: [user's original query]

Your specific dimension: [dimension name]
Focus on: [2-3 specific things to look for]

Provide a structured findings report with:
1. Key discoveries (with file paths and line numbers)
2. How things connect/flow
3. Notable patterns or concerns

Be thorough. Search broadly — use multiple grep/glob patterns, read key files, trace connections. Report in Chinese if the query is in Chinese.
```

### Step 5: Synthesize Report

After all agents return, synthesize their findings into a unified structured report:

```markdown
## Deep Explore: [query summary]

### Overview
[1-2 sentence executive summary of findings]

### Dimension 1: [name]
[Key findings from agent 1, with file:line references]

### Dimension 2: [name]
[Key findings from agent 2]

### Dimension 3: [name]
[Key findings from agent 3]

### (Dimension 4 if applicable)

### Connections & Insights
[Cross-cutting observations that emerge from combining dimensions]

### Key Files
[List of most important files discovered, with brief role descriptions]
```

**Output rules:**
- Default: output the full report in the conversation
- If `--file <path>` was specified: write to file AND show a brief summary in chat
- Use the same language as the user's query (Chinese query → Chinese report)
- Include concrete file paths and line numbers, not vague descriptions

## Important Notes

- NEVER ask the user clarifying questions before starting — just analyze the query and go
- If the query is ambiguous about scope, prefer broader analysis over asking for clarification
- All SubAgents run in parallel (single message, multiple Agent tool calls) — this is the core value proposition
- The synthesis step is YOUR job (main conversation) — don't delegate summarization to another agent
- Keep individual agent prompts focused and specific — a vague prompt defeats the purpose
