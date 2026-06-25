---
name: git-commit-message
description: Generate a conventional commit message from staged git diff and commit. Use when asked to write a commit message, summarize staged changes, or draft a git commit.
model: haiku
user-invocable: true
allowed-tools: Bash(git diff*) Bash(git commit*)
---

## Fetch changes

!`git diff --staged`

## Generate commit message

Write a commit message following these rules exactly:

**Format**: `<type>(<scope>): <subject>`

- Types: `feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `style`, `ci`, `perf`
- Scope is optional
- Subject: lowercase, imperative mood, no trailing period

**Body** (add when the diff touches more than one concern):
- Blank line after subject
- 2–4 bullet points starting with `-`
- Brief and factual — no analysis, no narration

**Rules**:
- Base every claim on the diff content directly — do not infer from filenames
- Omit bullets for files with only formatting/whitespace changes
- If a user draft is provided, extract the intent and rewrite in this format; discard prose, analysis, or narration

## Commit

Run `git commit -m "<message>"` with the generated message.
