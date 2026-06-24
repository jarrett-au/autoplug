---
name: issue-capture
description: |
  将当前工作中发现的旁支问题、技术债、bug 线索或改进点，整理为有事实依据的 GitHub issue。
  当用户要求记录 issue、先记下来、后面单独处理、不要污染当前分支时触发。
argument-hint: "要记录什么问题？是否直接创建 issue？"
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Issue Capture

## Scope

Capture out-of-scope findings as evidence-backed GitHub issues.

Use for:
- findings unrelated to the current branch objective
- bugs, risks, technical debt, missing tests, or follow-up work discovered during implementation or review
- work that should be handled later in a separate branch

Do not use for:
- issues already in scope for the current branch
- vague ideas without evidence
- implementation or refactoring work unless the user explicitly asks

## Rules

- Do not fix the finding while capturing it.
- Do not create an issue without evidence.
- Separate observed facts from inference.
- Search for existing issues before creating a new one.
- Draft first by default. Create the GitHub issue only if the user explicitly asks to create it or confirms the draft.

## Evidence Requirements

At least one evidence item is required:
- file path and relevant line range
- diff hunk or changed file showing the observation
- failing command or test output
- reproducible UI/API steps
- log excerpt
- screenshot or artifact URL
- explicit user report or requirement

If evidence is insufficient, stop with:

```text
Not enough evidence to create a good issue yet.

Need one of:
1. file path + line range
2. failing command or test output
3. reproduction steps
4. log / screenshot / artifact URL
5. explicit user-confirmed behavior
```

## Default Draft Location

```bash
ISSUE_CAPTURE_DIR=".claude-plugins-data/code-quality/issue-capture"
mkdir -p "$ISSUE_CAPTURE_DIR"
ISSUE_DRAFT="$ISSUE_CAPTURE_DIR/issue-$(date +%Y%m%d-%H%M%S).md"
```

## Process

### 1. Identify current scope

Check the current work context:

```bash
git status --short
git branch --show-current
git log --oneline -5
```

If available, also inspect:
- current PR title/body
- issue or ticket linked to the current branch
- plan/spec files relevant to the current work
- user-provided acceptance criteria

Record why the finding is out of scope for the current branch.

### 2. Gather evidence

Collect only facts that can be cited.

Useful commands:

```bash
git diff --stat
git diff --name-only
git diff -- <path>
```

For code references, prefer exact paths and line ranges. For runtime behavior, include the command or steps that produced the observation.

### 3. Search for duplicates

Infer repo from the current git remote unless the user specifies one.

```bash
REMOTE_URL=$(git remote get-url origin)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
```

Search before creating:

```bash
gh issue list --repo "$OWNER_REPO" --state open --search "<keywords>"
gh issue list --repo "$OWNER_REPO" --state all --search "<keywords>"
```

If a matching issue exists:
- do not create a duplicate
- draft a comment with the new evidence
- ask before posting the comment unless the user requested direct action

### 4. Classify

Use one primary type:
- `bug`
- `test-gap`
- `technical-debt`
- `docs`
- `enhancement`
- `follow-up`

Use severity only when evidence supports it:
- `blocking`: proven severe failure or security/data risk
- `risk`: plausible issue with partial evidence
- `follow-up`: useful work, not urgent

### 5. Draft issue

Write the draft to `$ISSUE_DRAFT`.

````markdown
# <concise title>

## Summary

<1-2 sentences.>

## Observed Facts

- <fact> — evidence: `<path:line>` / `<command>` / <URL>

## Impact

<What this affects. Use `Unknown` if not established.>

## Reproduction / Verification

```bash
<command, if applicable>
```

Steps, if applicable:
1. <step>
2. <step>
3. <step>

Expected:
- <expected behavior or signal>

Actual:
- <observed behavior or signal>

## Out of Scope for Current Work

Current branch / task: `<branch or task>`

Reason to defer:
- <why this should not be handled in the current branch>

## Suggested Next Step

- <first concrete action for a future branch>

## Metadata

- Type: `<bug | test-gap | technical-debt | docs | enhancement | follow-up>`
- Severity: `<blocking | risk | follow-up>`
- Evidence level: `<strong | partial>`
- Duplicate search: `<query used>`
````

### 6. Create issue only after confirmation

Default response after drafting:

```text
Issue draft 已写好：<path>

建议标题：<title>
类型：<type>
证据等级：<strong|partial>
重复 issue：<none|#number>

确认后我再创建 GitHub issue。
```

If the user explicitly requested direct creation:

```bash
gh issue create \
  --repo "$OWNER_REPO" \
  --title "<title>" \
  --body-file "$ISSUE_DRAFT" \
  --label "<label>"
```

Return the issue URL after creation.

## Quality Check

Before creating or returning a draft, verify:
- the finding is outside the current branch objective
- at least one evidence item is present
- facts and inference are separated
- duplicate search was performed or skipped with a stated reason
- title is specific and searchable
- suggested next step is concrete
- no secrets or sensitive raw data are included
