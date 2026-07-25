# Conventional Commits Reference

Conventional commits provide a standardized format for commit messages and PR titles.

## Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Types

| Type | Description | Examples |
|------|-------------|----------|
| `feat` | New feature | `feat: add user authentication` |
| `fix` | Bug fix | `fix: handle null pointer exception` |
| `docs` | Documentation changes | `docs: update API documentation` |
| `style` | Code style changes (formatting, semicolons, etc.) | `style: format code with prettier` |
| `refactor` | Code refactoring | `refactor: simplify data processing logic` |
| `perf` | Performance improvements | `perf: optimize database queries` |
| `test` | Adding or updating tests | `test: add unit tests for auth module` |
| `build` | Build system or dependencies | `build: upgrade to webpack 5` |
| `ci` | CI/CD configuration changes | `ci: add GitHub Actions workflow` |
| `chore` | Other changes (maintenance, config updates) | `chore: update .gitignore` |
| `revert` | Revert a previous commit | `revert: feat(user login)` |

## Scopes

Scopes provide additional context about the part of the codebase affected:

```
feat(auth): add OAuth2 login support
fix(api): handle rate limiting errors
docs(readme): update installation instructions
```

## Examples

```
feat: add dark mode support

Implement dark mode toggle in settings.
Includes theme persistence and system preference detection.

Closes #123
```

```
fix(database): resolve connection pool exhaustion

Add proper connection cleanup and increase pool size
to prevent timeout errors under high load.

Fixes #456
```

```
refactor(components): extract shared button logic

Create base Button component to reduce code duplication
across primary and secondary button variants.
```

## Best Practices

1. **Use imperative mood**: "add" not "added" or "adds"
2. **Keep it concise**: Limit title to 50-72 characters
3. **Capitalize first letter**: "Add feature" not "add feature"
4. **Don't end with period**: Title should not end with "."
5. **Be specific**: Describe what and why, not how
6. **Reference issues**: Use "Closes #123" or "Fixes #456" in footer
