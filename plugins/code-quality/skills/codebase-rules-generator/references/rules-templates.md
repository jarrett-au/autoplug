# Lean Rule Templates

Templates for generating concise, targeted rule files.

---

## Template: CLAUDE.md

**Location: `./CLAUDE.md`**

**Target: 50-80 lines**

```markdown
# [Project Name]

[One sentence description]

## Commands

| Command | Purpose |
|---------|---------|
| `[cmd]` | [purpose] |

## Architecture

- Pattern: [Architecture name]
- Layers: [Layer flow, e.g., API → Service → Domain ← Infra]
- Key constraint: [Most critical rule]

## Quick Reference

- Config: `[config path]`
- Tests: `[test command]`
- Docs: @README.md, @docs/[main doc]

## Detailed Rules

See `.claude/rules/` for domain-specific guidelines.
```

---

## Template: architecture.md (Global)

**Target: 30-50 lines, NO paths (global)**

```markdown
# Architecture

## Layer Structure

- [Layer1] (`path/`): [responsibility]
- [Layer2] (`path/`): [responsibility]

## Dependency Rules

- [Layer] depends only on [Layer]
- Never import [X] from [Y]

## Key Patterns

- [Pattern]: [one-line description]
- [Pattern]: [one-line description]

## DI/Wiring

- Config location: `[path]`
- Regenerate: `[command]`
```

---

## Template: api.md (Path-Scoped)

**Target: 30-50 lines**

```markdown
---
paths:
  - "internal/api/**/*"
  - "internal/handlers/**/*"
---

# API Rules

## Endpoints

- Base path: `[/api/v1]`
- Naming: [convention, e.g., kebab-case, plural nouns]
- Versioning: [strategy]

## Request Handling

- Bind with: `[method]`
- Validate via: [approach]
- Context: use `c.Request.Context()`

## Response Format

- Success: `{code: 0, msg: "success", data: ...}`
- Error: `{code: [N], msg: "[error]"}`

## Error Mapping

- `ErrNotFound` → 404
- `ErrInvalidArg` → 400

## Documentation

- Annotate with: [Swagger/OpenAPI comments]
- Generate: `[command]`
```

---

## Template: database.md (Path-Scoped)

**Target: 30-50 lines**

```markdown
---
paths:
  - "internal/infra/persistence/**/*"
  - "internal/repository/**/*"
  - "db/migrations/**/*"
---

# Database Rules

## ORM

- Use: [GORM/sqlx/etc]
- Models: define in `[path]`

## Queries

- Always use `WithContext(ctx)`
- Handle `ErrRecordNotFound` explicitly
- Use parameterized queries only

## Transactions

- Interface: `TransactionManager.Transaction(ctx, fn)`
- Scope: wrap multi-step operations

## Migrations

- Location: `[path]`
- Naming: `[version]_[description].[up|down].sql`
- Commands: `[migrate-up]`, `[migrate-down]`

## Indexes

- Add via migrations, never modify schema directly
- Use `IF NOT EXISTS` for safety
```

---

## Template: domain.md (Path-Scoped)

**Target: 25-40 lines**

```markdown
---
paths:
  - "internal/domain/**/*"
  - "internal/models/**/*"
---

# Domain Rules

## Entities

- Location: `[path]`
- Zero external dependencies
- Define `TableName()` for ORM mapping

## Interfaces

- All repository interfaces in `[file]`
- Keep interfaces minimal and focused

## Errors

- Define at package level: `var Err[Name] = errors.New("[msg]")`
- Wrap with context: `fmt.Errorf("[action]: %w", err)`

## Status Enums

- Use typed constants: `type [Name]Status string`
- Define valid transitions in comments
```

---

## Template: testing.md (Path-Scoped)

**Target: 30-45 lines**

```markdown
---
paths:
  - "**/*_test.go"
  - "**/test/**/*"
  - "**/testing/**/*"
---

# Testing Rules

## Organization

- Unit tests: co-located with source
- Integration tests: `test/integration/`
- Mocks: `[mock location]`

## Patterns

- Use table-driven tests for multiple cases
- Structure: Arrange → Act → Assert
- Name: `Test[Unit]_[Scenario]`

## Mocks

- Import from: `[mock package]`
- Configure via function fields
- Verify calls when behavior matters

## Commands

- Unit: `[command]`
- Integration: `[command]`
- Coverage: `[command]`
```

---

## Template: workflow.md (Global)

**Target: 40-60 lines, NO paths (global)**

```markdown
# Development Workflow

## Commands

| Task | Command |
|------|---------|
| Run | `[cmd]` |
| Build | `[cmd]` |
| Test | `[cmd]` |
| Lint | `[cmd]` |
| Format | `[cmd]` |

## Adding Features

1. [Step 1]
2. [Step 2]
3. ...

## Git

- Branch: `feat/*`, `fix/*`
- Commit: `type: description`
- Pre-commit: `[command]`

## Config

- Files: `[path]`
- Env override: `[VAR_NAME]=value`
- Select env: `ENV=[name] [command]`
```

---

## Template: security.md (Path-Scoped)

**Target: 20-30 lines**

```markdown
---
paths:
  - "internal/auth/**/*"
  - "internal/middleware/**/*"
---

# Security Rules

## Sensitive Fields

- Mark internal: `json:"-"`
- Never log: passwords, tokens, keys

## Validation

- Validate all inputs at API layer
- Sanitize file paths for traversal

## Auth

- [Auth mechanism description]
- Token location: [header/cookie]
```

---

## Quality Checklist

Before finalizing any rule file:

- [ ] Has `paths:` frontmatter (unless truly global)
- [ ] < 60 lines total
- [ ] No code blocks > 3 lines
- [ ] Each rule is one line or short bullet
- [ ] References existing docs with `@path`
- [ ] No generic/obvious advice
- [ ] Project-specific patterns only
