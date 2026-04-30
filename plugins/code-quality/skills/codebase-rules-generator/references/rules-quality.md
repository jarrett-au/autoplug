# Rule Quality Guidelines

Standards for evaluating and improving generated rules.

## The 3C Principle

**Concise** → **Contextual** → **Constraint-focused**

### Concise (CRITICAL)
- **One rule = one line** (non-negotiable)
- **Maximum 50 lines per rule file** (was 60)
- **NO code blocks** (use file references instead)
- **NO paragraphs** (convert to bullets)

### Contextual
- Every non-global file has `paths:` frontmatter
- Reference existing docs via `@path`, don't duplicate
- Use project-specific terminology only

### Constraint-focused
- Focus on what NOT to do (forbidden patterns)
- Highlight exceptions to common patterns
- Describe boundaries, not tutorials

---

## Anti-Pattern: The "Tutorial Trap"

**Symptom**: Your rule file explains "how" and "why" instead of "what".

**Example of BAD rule** (40 lines):
```markdown
## Thread-Safe Tests and pytest-xdist

**Problem**: Thread-heavy tests cause thread explosion under pytest-xdist
process-level parallelization. When xdist workers (default: 12) run tests
that create multiple threads (10 threads × 10 iterations), this results
in 120+ threads competing for resources...

**Identify Thread-Heavy Tests**:
- Tests using `threading.Thread` with multiple concurrent threads
- Tests with large iteration counts (e.g., `for _ in range(100):`)
- Tests explicitly named `test_*_thread_safe` or `test_*_concurrent`

**Solutions** (in order of preference):

1. **Reduce Thread Count**: Use smaller thread/iteration counts...
[continues with code examples for 25 more lines]
```

**Example of GOOD rule** (5 lines):
```markdown
## Thread-Safe Tests and pytest-xdist

**Problem**: xdist workers × test threads = thread explosion (12×10=120+)

**Solutions**:
1. Reduce counts: Use `THREAD_COUNT_XDIST_SAFE=3` from constants
2. Makefile exclusion: `pytest --ignore=thread_heavy.py -n 0`
3. Reference: `tests/services/evaluation/test_progress_tracker.py`
```

**Fix process**:
1. Delete all code examples
2. Delete all explanatory paragraphs
3. Convert solutions to bullet points
4. Add file references only
5. Keep only actionable items

---

## Good vs Bad Rules

### Naming Rules

**Bad:**
```markdown
When naming files in Go, you should use snake_case. This means words are 
separated by underscores and all letters are lowercase. For example, 
`user_service.go` instead of `UserService.go`.
```

**Good:**
```markdown
- Files: `snake_case.go`
- Tests: `*_test.go` co-located
```

### Pattern Rules

**Bad:**
```markdown
## Error Handling Pattern

In this project, we handle errors using the following pattern. First, 
you wrap the error with context using fmt.Errorf:

​```go
if err != nil {
    return fmt.Errorf("failed to create user: %w", err)
}
​```

Then in the calling code, you check for specific errors using errors.Is():

​```go
if errors.Is(err, domain.ErrNotFound) {
    return nil, errno.ErrNotFound
}
​```
```

**Good:**
```markdown
## Errors
- Wrap: `fmt.Errorf("[action]: %w", err)`
- Check: `errors.Is(err, domain.Err[X])`
- Define in: `internal/domain/errors.go`
```

### Architecture Rules

**Bad:**
```markdown
## Clean Architecture

This project follows Clean Architecture principles. The architecture 
consists of four layers:

1. Domain Layer - Contains business entities and interfaces
2. Service Layer - Contains business logic
3. API Layer - Contains HTTP handlers
4. Infrastructure Layer - Contains external implementations

Dependencies should only point inward...
[continues for 50 more lines]
```

**Good:**
```markdown
## Layers
- Domain (`internal/domain/`): entities, interfaces — zero dependencies
- Service (`internal/service/`): business logic — depends on domain only
- API (`internal/api/`): HTTP handlers — depends on service
- Infra (`internal/infra/`): implementations — implements domain interfaces

## Forbidden Imports
- Domain must NOT import service/api/infra
- Service must NOT import api/infra
```

---

## Paths Configuration Examples

### Match by Directory

```yaml
paths:
  - "internal/api/**/*"          # All files in api tree
  - "internal/handlers/**/*"     # All files in handlers tree
```

### Match by Extension

```yaml
paths:
  - "**/*.go"                    # All Go files
  - "**/*.{ts,tsx}"              # TypeScript + TSX files
```

### Match Test Files

```yaml
paths:
  - "**/*_test.go"               # Go tests
  - "**/*.test.{ts,js}"          # JS/TS tests
  - "**/test/**/*"               # Test directory
```

### Match Config Files

```yaml
paths:
  - "configs/**/*"
  - "**/*.yaml"
  - "**/*.json"
```

### Multiple Related Paths

```yaml
paths:
  - "internal/infra/persistence/**/*"
  - "internal/repository/**/*"
  - "db/migrations/**/*"
```

---

## When NOT to Use Paths

Only these types of rules should be global (no paths):

1. **Architecture rules** - Layer structure applies everywhere
2. **Git/workflow rules** - Not code-specific
3. **Project overview** - CLAUDE.md main file
4. **Cross-cutting patterns** - Logging, error handling philosophy

Everything else should have `paths:` frontmatter.

---

## Size Guidelines

| File Type | Target Lines | Max Lines |
|-----------|--------------|-----------|
| CLAUDE.md | 50-70 | 80 |
| architecture.md | 25-40 | 50 |
| api.md | 25-40 | 50 |
| database.md | 25-40 | 50 |
| testing.md | 25-35 | 45 |
| domain.md | 20-35 | 40 |
| workflow.md | 30-50 | 60 |
| **Total all files** | **200-350** | **400** |

---

## Review Checklist

Before finalizing rules, verify:

### Structure
- [ ] `paths:` frontmatter on all non-global files
- [ ] No file exceeds 60 lines
- [ ] Total rules < 500 lines

### Content
- [ ] **NO code blocks** (use `@path/file` reference instead)
- [ ] **NO explanatory paragraphs** (delete all "why" explanations)
- [ ] Each bullet is actionable ("do X" or "use Y")
- [ ] Uses `@path` to reference existing docs, not copy content

### Specificity
- [ ] Rules are project-specific, not generic
- [ ] Actual paths/commands from this project
- [ ] Mentions specific patterns used here

### Completeness
- [ ] Key architectural constraints captured
- [ ] Critical "don't do" rules included
- [ ] Development workflow covered
