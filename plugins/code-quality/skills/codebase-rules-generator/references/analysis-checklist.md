# Codebase Analysis Checklist

Quick checklist for extracting rule-worthy information from a codebase.

## Phase 1: Structure Discovery (5 min)

- [ ] Primary language(s): ___
- [ ] Framework(s): ___
- [ ] Package manager / build tool: ___
- [ ] Source directories: ___
- [ ] Test directories: ___
- [ ] Config location: ___

## Phase 2: Pattern Identification (10 min)

### Architecture
- [ ] Pattern name: ___
- [ ] Layer names and paths: ___
- [ ] Dependency direction: ___
- [ ] Key abstraction (interfaces): ___

### Conventions
- [ ] File naming: ___
- [ ] Function naming: ___
- [ ] Error handling pattern: ___
- [ ] Import organization: ___

### Testing
- [ ] Test location: co-located / separate
- [ ] Test framework: ___
- [ ] Mock location: ___
- [ ] Integration test setup: ___

## Phase 3: Path Mapping (5 min)

Map directories to rule files:

| Directory Pattern | Rule File |
|-------------------|-----------|
| `internal/api/**/*` | api.md |
| `internal/domain/**/*` | domain.md |
| `internal/infra/**/*` | database.md |
| `**/*_test.go` | testing.md |
| (global) | architecture.md |
| (global) | workflow.md |

## Phase 4: Key Constraints (5 min)

List the most important "don't do" rules:

1. ___
2. ___
3. ___
4. ___
5. ___

## Phase 5: Commands (2 min)

| Task | Command |
|------|---------|
| Run | |
| Build | |
| Test | |
| Lint | |
| Format | |
| Migrate | |

## Existing Documentation

Files to reference with `@path`:

- [ ] README.md: ___
- [ ] CONTRIBUTING.md: ___
- [ ] Architecture docs: ___
- [ ] API docs: ___

## Size Check

Before generating:
- Target total lines: 250-400
- Max per file: 60 lines
- Avoid: code examples > 3 lines
