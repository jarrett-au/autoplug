---
name: handoff
description: |
  生成高信噪比交接文档，让另一个 agent、人类同事或下一次会话能无缝接手当前工作。
  当用户要求 handoff、交接、上下文压缩、下一轮继续、会话快满时触发。
argument-hint: "下一轮接手者要重点继续什么？"
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Handoff

## Scope

Generate a concise handoff document for unfinished work.

The document must be standalone and portable:
- no dependency on a specific repository, plugin, private workflow, or fixed artifact directory
- no assumption that the next environment has the same skills or tools
- references to existing artifacts are allowed when the artifact actually exists

Use for:
- long-running work that needs to continue in another session
- work transferred to another agent or human teammate
- tasks with multiple artifacts, decisions, or verification steps

Do not use for:
- ordinary chat summaries
- finished work with no follow-up action
- external-facing reports, release notes, or retrospectives

## Default Output Location

Use the plugin data directory unless the user specifies a path.

```bash
HANDOFF_DIR=".claude-plugins-data/code-quality/handoffs"
mkdir -p "$HANDOFF_DIR"
HANDOFF_FILE="$HANDOFF_DIR/handoff-$(date +%Y%m%d-%H%M%S).md"
```

If the project already has an explicit handoff or artifact directory, it may be used instead.

## Process

### 1. Define the transfer boundary

Determine:
- audience: next agent, human teammate, or future self
- scope: project, PR, bug, document, research task, incident, or other work unit
- focus: `$ARGUMENTS` if provided; otherwise infer from the latest user request
- desired next outcome: what the next session should produce

### 2. Gather evidence

Use available evidence before writing.

For code work, usually check:

```bash
git status --short
git branch --show-current
git log --oneline -5
```

Other useful evidence:
- plans, specs, ADRs, docs, requirements
- issues, PRs, tickets, kanban cards
- changed files, diffs, recent commits
- test logs, CI runs, benchmark output, screenshots, QA notes
- research sources, notes, datasets, saved queries
- explicit user constraints and acceptance criteria

Only cite paths, URLs, commands, or facts that were actually observed or provided.

### 3. Distill

Keep:
- goal
- current state
- decisions that constrain future work
- artifacts to read first
- next actions
- verification steps
- risks and redactions

Remove:
- chronological chat replay
- long copied excerpts from existing artifacts
- irrelevant branches of the discussion
- unverified guesses
- secrets or sensitive raw data

## Handoff Template

````markdown
# Handoff: <short title>

Generated: <YYYY-MM-DD HH:MM local>
Focus: <focus>
Audience: <next agent | human teammate | future self>

## 1. Goal

<1-3 sentences.>

## 2. Current State

- Workspace / repo: `<path or name, if applicable>`
- Branch: `<branch or n/a>`
- Working tree: <clean / dirty / n/a>
- Last relevant commit: `<sha> <subject>` or n/a
- PR / issue / ticket: <URL or n/a>
- Status: <one-sentence state>

## 3. Decisions

- <decision> — why: <reason> — evidence: `<path, URL, command, or user instruction>`

Use `None` if there are no decisions that affect future work.

## 4. Artifacts to Read First

1. `<path or URL>` — <why it matters>
2. `<path or URL>` — <why it matters>
3. `<path or URL>` — <optional>

Reference artifacts; do not copy their contents.

## 5. Next Actions

1. <specific action: command, file, URL, or decision point>
2. <specific action>
3. <specific action>

For branches:
- If <condition>: <action>
- Else: <action>

## 6. Verification

Run / check:

```bash
<command, if applicable>
```

Expected:
- <success signal>
- <first place to inspect on failure>

For non-code work, use observable acceptance checks.

## 7. Risks / Gotchas

- <risk>: <avoidance or mitigation>

## 8. Useful Capabilities / Skills

- `<capability or known skill>` — <when to use it>

Prefer generic capability names unless a specific skill is known to exist in the current environment.

## 9. Redactions

- <type of sensitive information removed, without values>
- None, if no sensitive information was encountered.
````

## Quality Check

Before saving, verify:
- the handoff can be used without the original chat
- next actions are concrete enough to start immediately
- important claims have evidence
- existing artifacts are referenced instead of copied
- no secrets or sensitive raw data are included
- no specific repository, plugin, private workflow, or fixed directory is required
- useful capabilities / skills are limited to what helps the next action

## Response

After writing the file, return only:

```text
Handoff 已写好：<absolute path>

下一轮建议从这三件事开始：
1. ...
2. ...
3. ...
```

Do not paste the full handoff unless the user asks for it.
