---
name: codebase-rules-generator
description: |
  Use when generating compact project rules or coding-agent instructions from an existing codebase.
  Analyzes architecture, conventions, tests, build commands, and pitfalls, then writes minimal rules
  where every word earns its place. Trigger for 'generate CLAUDE.md rules', 'create coding rules',
  'analyze this repo for agent instructions', or 'write project rules'.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Codebase Rules Generator

Generate ultra-concise rules. **Every word must earn its place.**

## Core Principle: Delete Over Add

**Target lengths:**
- CLAUDE.md: 50-80 lines max
- Rule files: 30-60 lines max
- Total rules: <500 lines combined

**When in doubt, delete it.**

## Quality Standards

**Good rule:**
```markdown
## Thread Safety
- Use `THREAD_COUNT_XDIST_SAFE=3` for xdist compatibility
- Reference: `tests/fixtures/constants.py`
```

**Bad rule:**
```markdown
## Thread Safety and pytest-xdist

**Problem**: Thread-heavy tests cause thread explosion under pytest-xdist...
[40 lines of explanation with code examples]
```

**Difference: 3 lines vs 40 lines. Same information.**

## Rule Format

**One rule per line. Bullet points only.**

```markdown
## Section Name
- Action item 1
- Action item 2
- Reference: path/to/file
```

**Never:**
- Paragraphs explaining "why"
- Code blocks showing "how"
- Multiple levels of headings
- Tutorial-style content

## Essential vs Non-Essential

**Essential (keep):**
- Project-specific patterns
- Non-obvious constraints
- Critical file paths
- Performance targets

**Non-Essential (delete):**
- Generic programming advice
- Explanations of "why" something works
- Code examples that exist in source
- Obvious conventions
- Duplicate information

## Paths Frontmatter

Every rule file needs `paths:` to scope it:

```yaml
---
paths:
  - "tests/**/*"
---
```

**No paths? Don't create the file.**

## Validation Checklist

Before finalizing, ask:
1. Can I delete 50% of words without losing meaning?
2. Are there any code examples? Delete them.
3. Are there any paragraphs? Convert to bullets.
4. Is each line actionable? If not, delete it.
5. Would this help Claude write BETTER code for THIS project?

If answer is "no" to any, keep editing.

## Anti-Patterns

| Pattern | Fix |
|---------|-----|
| "Use clean code practices" | Delete (generic) |
| Code blocks showing examples | Replace with file reference |
| Explaining why pattern works | Delete explanation |
| >100 lines per file | Split or delete |
| Tutorial sections | Delete entirely |

## Workflow

1. **Analyze**: Find unique patterns in codebase
2. **Extract**: List only project-specific rules
3. **Compress**: Convert everything to bullets
4. **Delete**: Remove all non-essentials
5. **Validate**: Check against length limits

**Time limit**: Spend 80% of time deleting, 20% writing.
