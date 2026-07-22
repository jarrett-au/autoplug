---
name: code-simplifier
description: User-invoked workflow to simplify recently modified code for clarity, consistency, and maintainability without changing behavior. Invoke explicitly with /code-simplifier; inspect a broader scope only when the command specifies one.
argument-hint: "[scope] [--dry-run]"
user-invocable: true
disable-model-invocation: true
allowed-tools: Agent Read Grep Glob Bash Write Edit
model: opus
---

# Code Simplifier

Refine the current change set without changing observable behavior.

Prefer explicit, debuggable code over clever compression. Make no edit when the clarity gain is marginal or the behavior-preservation claim cannot be verified.

## Invocation

```text
/code-simplifier [scope] [--dry-run]
```

- `scope`: optional file, directory, commit, staged changes, branch, or PR scope
- `--dry-run`: analyze and report candidates without editing

Run only through explicit `/code-simplifier` invocation. Do not automatically trigger after code changes or natural-language requests.

## Scope

Use the narrowest source matching the request:

1. Explicit file/directory/commit/branch scope
2. Default current tracked change set, staged plus unstaged: `git diff HEAD`
3. Only when explicitly requested: unstaged via `git diff`, staged via `git diff --staged`
4. Current committed branch against main only when the user asks for branch/PR cleanup: `git diff main...HEAD`
5. Relevant untracked files shown by `git status --short`, limited to files explicitly named or created/modified in the current session
6. Files explicitly named or modified in the current session when Git context is unavailable

Record `git status --short` before editing. Dirty worktrees are allowed because recent uncommitted changes are the normal input. Never stash, reset, checkout, commit, or discard the user's changes.

Do not expand into untouched areas except for the minimum surrounding context needed to understand behavior or reuse an existing project abstraction.

Exclude by default:

- generated and vendored files
- minified assets
- lockfiles and snapshots with mechanical changes
- formatter-only changes
- files outside the requested scope

## Behavior-Preservation Contract

Before applying a non-trivial refinement, state what must remain true.

```yaml
id: auth-flow-C1
unit: auth-flow
risk: safe | careful | risky
scope:
  - src/auth.ts:createSession
change: flatten nested token validation branches
clarity_gain: removes duplicated exits and makes the success path linear
behavior_invariants:
  - invalid tokens still return 401
  - expired tokens still emit the audit event
  - successful response shape remains unchanged
verification:
  - npm test -- auth.test.ts
```

Rules:

- No clear behavior invariants → do not edit
- No practical verification path for a non-trivial change → report only
- “Fewer lines” is not a clarity gain by itself
- Project instructions, tests, types, API contracts, and surrounding conventions outrank generic style preferences

## Candidate Risk

### SAFE

Apply when behavior equivalence is direct and local:

- remove unused imports only after proving the imported module has no registration or other import-time side effects; remove unreachable local code only when proven unused
- remove comments that only restate obvious code
- replace a pass-through local wrapper with its existing target
- flatten structurally equivalent nesting
- remove redundant local aliases or assertions
- use an existing project helper with the same established contract

Run the smallest available lint, type, compile, or focused test check.

### CAREFUL

Apply sequentially with explicit invariants and focused verification:

- restructure control flow
- extract or consolidate a helper
- merge duplicated logic
- rename local variables across a coherent unit
- remove defensive checks whose preconditions are established
- move logic across a local abstraction boundary

A CAREFUL candidate without focused verification becomes report-only.

### RISKY

Report but do not automatically apply:

- public API, route, schema, config-key, event, or wire-format changes
- concurrency, async ordering, transactions, cache, or lifecycle changes
- error swallowing, propagation, retry, or logging semantic changes
- cross-module architectural refactors
- creating new source files or moving logic into a new module
- deleting or renaming files, editing symlinks, or changing executable/file modes
- data migrations or persistence behavior
- performance rewrites that alter execution order or resource lifetime
- removals justified only by assumption, taste, or incomplete search

## Workflow

### Phase 1: Establish context and baseline

1. Identify the changed sections and observable behavior.
2. Read repository instructions and nearby code.
3. Search for existing helpers and conventions before proposing a new abstraction.
4. Identify focused verification commands.
5. Run practical baseline checks before editing and record their real result.

Baseline comparison distinguishes pre-existing failures from regressions. If no automated check exists, use static contract/type evidence and mark confidence accordingly.

Before any edit, initialize:

```text
.claude-plugins-data/code-quality/code-simplifier/${CLAUDE_SESSION_ID}/
├── context.json
├── baseline.md
├── candidates.md
├── applied.md
├── verification.md
└── before/<batch-id>/<original-path>
```

`--dry-run` does not need snapshots because it makes no edits. Every editing batch, including a single-file SAFE batch, requires the artifact root and a snapshot before the first write.

Ensure `.claude-plugins-data/code-quality/code-simplifier/` is ignored. Prefer `.git/info/exclude` when the project does not already ignore it; do not modify the project's `.gitignore` without explicit permission.

### Phase 2: Build coherent change units

Group related implementation, callers, tests, and configuration by behavior or module.

Good units:

- authentication flow and its tests
- settings state and consuming components
- parser implementation and fixtures

Bad units:

- arbitrary equal-sized line chunks
- one whole repository
- overlapping units that will propose edits to the same logic

Small or cohesive scopes stay in the main agent. Use parallel analysis only when there are at least two independent units and a single pass would blur their context.

### Phase 3: Analyze

For small scopes, analyze directly.

For large scopes, launch at most three read-only `Agent` calls in one message. Assign one coherent unit to each `Explore` subagent. Each prompt includes:

- exact changed files and diff range
- minimal context files
- project conventions
- required candidate schema
- instruction to search before claiming duplication
- instruction to make no edits and run no mutating commands

Do not send every agent the complete large diff. Add one cross-cutting analysis lane only when shared contracts, reuse, or duplicated abstractions genuinely span units.

Parallelize discovery, not edits.

Each analysis returns only material candidates with:

- concrete location
- proposed refinement
- clarity gain
- SAFE / CAREFUL / RISKY
- behavior invariants
- verification path
- confidence

Do not manufacture candidates to appear useful.

### Phase 4: Merge and select

Merge candidate reports before editing:

1. Deduplicate overlapping candidates.
2. Drop taste-only, low-confidence, and line-count-only proposals.
3. Reject abstractions that merely move complexity elsewhere.
4. Resolve conflicts using:

   ```text
   behavior preservation > project conventions > debuggability > reuse > fewer lines
   ```

5. Keep RISKY candidates report-only.
6. Order accepted candidates by coherent unit, then SAFE before CAREFUL.

If no candidate materially improves clarity with a verification path, make no edits and report that the current code should remain unchanged.

### Phase 5: Apply sequentially

Apply one coherent batch at a time.

Before changing a file:

1. Resolve the repository root with `git rev-parse --show-toplevel`.
2. Normalize the target to a repository-relative path. Reject absolute paths, `..` traversal, symlinks, and paths outside the repository.
3. Confirm the target is an existing regular file. Other file operations are RISKY and report-only.
4. Record its repository-relative path, file type, mode, device, inode, SHA-256, and pre-batch `git status --short -- <path>` in `before/<batch-id>/manifest.json`.
5. Create parent directories and copy with metadata preservation:

   ```bash
   mkdir -p "<artifact-root>/before/<batch-id>/<parent>"
   cp -p -- "<repo-relative-path>" "<artifact-root>/before/<batch-id>/<repo-relative-path>"
   ```

This per-batch snapshot represents the user's code immediately before that batch, including pre-existing uncommitted work. Never reuse an earlier batch snapshot for rollback.

Rules:

- edit only candidate-listed locations
- preserve public and error contracts
- do not mix unrelated cleanup into the batch
- do not let parallel agents write the working tree
- do not add a new abstraction unless it removes proven duplication or clarifies a real responsibility
- do not auto-format unrelated code

### Phase 6: Verify and rollback precisely

After each batch:

1. Run the candidate's focused verification.
2. Compare against baseline results.
3. Inspect the batch diff for scope creep and behavior changes.
4. Record the real command, exit status, and result.

Accept the batch only when it introduces no new failure and satisfies its behavior invariants.

If verification fails:

- verify the snapshot SHA-256 against its manifest
- immediately before restore, open the repository root as a directory file descriptor and descend every parent component with `openat` using `O_DIRECTORY | O_NOFOLLOW`; reject symlinks, non-directories, `..`, and components outside the repository
- open the destination relative to the validated parent descriptor with `O_WRONLY | O_NOFOLLOW` but without truncating it; compare `fstat` file type, device, and inode to the manifest before writing
- if any component or destination metadata differs, stop with `ROLLBACK_BLOCKED` and do not write automatically
- after validation, truncate and restore through the already-open destination file descriptor, then restore the recorded mode, flush/fsync, and close it; do not re-resolve the destination path and do not use `cp` for restore
- verify the restored file SHA-256 and mode match the manifest
- do not use broad `git reset`, `git checkout`, or stash
- preserve earlier verified batches and all user changes that existed before this simplifier batch
- report the rejected candidate and evidence

If verification or tooling changes a file outside the batch manifest, stop and report it. Do not automatically delete or restore unexpected files because they may contain concurrent user work.

After all batches, run the project's focused aggregate gate. Run the full suite only when project conventions or the breadth of the changes requires it.

## Stop Conditions

Stop when any condition is met:

- no material SAFE or verifiable CAREFUL candidate remains
- the requested scope is complete
- a candidate needs product, architecture, runtime, or public-contract judgment
- verification cannot distinguish behavior preservation
- one correction pass after a failed simplification still does not pass

Do not repeatedly simplify until the code matches personal taste. One primary pass and at most one correction pass are enough.

## Output

```markdown
## Code Simplifier 完成

- Scope: <files / diff range>
- Units analyzed: <count>
- Applied: SAFE <N> / CAREFUL <N>
- Report-only RISKY: <N>
- Rejected after verification: <N>
- Verification: <commands and real results>
- Artifacts: <path or none for dry-run>
```

Report only significant refinements. Do not narrate every renamed local or formatting adjustment.

## Quality Check

- [ ] Scope is limited to the requested or recent change set
- [ ] Every applied candidate has explicit behavior invariants
- [ ] Every CAREFUL candidate has focused verification
- [ ] Parallel agents analyzed disjoint units and did not edit
- [ ] RISKY candidates remained report-only
- [ ] Baseline and post-change results were compared
- [ ] Failed batches were rolled back without touching user changes
- [ ] No edit was made solely to reduce line count or satisfy taste
- [ ] No auto-commit, reset, stash, or broad checkout occurred

## Integration

Keep this skill independent from EDD review. When both are requested, use:

```text
code-simplifier → focused verification → user-approved commit → edd-review-loop
```

Running simplification after EDD invalidates the reviewed snapshot and requires another review pass.
