---
name: diagnose
description: Use when the user explicitly selects a diagnosis workflow for a bug or regression. Establish symptom-sensitive evidence, test causal explanations, and verify a scoped fix or report the remaining uncertainty.
disable-model-invocation: true
user-invocable: true
---

# Diagnose

## Scope

Enter only when selected by the user. Diagnose the stated failure; implement a fix only if the request authorizes fixing it. Do not expand into an architecture rewrite or repository-wide review. This skill works alone; no companion workflow is required.

## Project knowledge and active work

Read current code and project guidance; reuse locations and retention policies. Maintain knowledge for the next action, not history. No mandatory setup or scaffolding.

- **Current knowledge:** update the owner in place, replacing stale text and linking rather than copying. Start with an existing README section; split for stable reader/update boundaries, not length or feature names. Without conventions, use README for operations/checks, `docs/architecture/overview.md` for structure, `docs/architecture/client-contract.md` for callers, and `GLOSSARY.md`/`CONTEXT.md` for terms, only as needed.
- **Decisions:** actively record costly-to-reverse, surprising choices with real alternatives in existing ADRs or `docs/adr/`. No invented approvals, chronology or duplicated API details. Proposals are not implemented behavior.
- **Active work:** use the tracker or, when handoff requires it, `.scratch/<slug>.md`. Keep current scope, acceptance, confirmed choices/sources, open questions, verification gaps and next action; replace stale status.
- **Evidence:** report results in the response, including migrations/comparisons. Save only explicitly required records or artifacts needed for a concrete unresolved question or active handoff; specify purpose, scope and revision. No evidence collection or routine reports.
- **Completion:** update current knowledge, remove scope-owned stale/redundant text and repair links. Migrate valid knowledge from completed in-scope local tasks, then remove them, unless explicit retention policy differs. Preserve active/unrelated work, data, backups, images and required audit artifacts. External trackers are closed only with permission, never history-deleted.

Respect document-write permission; identify read-only proposals as unsaved. Re-read before editing; distinguish facts, decisions and hypotheses. External writes and instruction/configuration updates need explicit permission.

## Process

1. **Bound the symptom from current state.** Read relevant instructions, current code/configuration, contracts and tests first. Record expected behavior and its source, actual behavior, affected environment/input and known limits. Consult history or recent changes only for a concrete question current state cannot answer, such as when a regression began. If the expectation is ambiguous, clarify it before choosing a fix. Keep observations separate from explanations.
2. **Find a useful signal.** Run the smallest safe test, request, replay, CLI or browser interaction that exercises the reported behavior. Assert the symptom, not just “did not crash.” Confirm that failure comes from that behavior rather than broken setup. Existing evidence may be sufficient; do not construct a new harness for its own sake.
3. **Test explanations.** With direct evidence, follow it. Otherwise rank plausible causes and state what observation would distinguish them. No hypothesis quota. Read code and traces even when reproduction is unavailable; label the resulting hypotheses as unverified. Choose the cheapest discriminating probe, change one meaningful variable, then update the explanation from the result. Stop repeating probes that add no information.
4. **Fix within scope.** Once evidence supports a cause, add or preserve a regression check that fails for the original defect, then make the smallest coherent correction. Use the interface that reaches the real failure, including a multi-caller or integration path when necessary. Do not invent an abstraction or fake a second implementation just to create a test boundary.
5. **Verify the claim.** Re-run the regression check, original scenario if different, and relevant neighboring checks. For intermittent/performance failures compare equivalent workloads before and after, report repeats and observations, and retain uncertainty. One green run does not establish absence of a race or performance improvement.
6. **Clean up.** Remove only instrumentation and temporary artifacts added by this investigation; preserve useful regression coverage. Inspect the diff for unrelated changes. Do not remove user changes or evidence still needed to diagnose an unresolved issue.

## Missing or noisy evidence

- Stabilize time, input, seed or dependency behavior where it preserves the real failure. Do not mock away the suspected cause.
- For concurrency or performance, choose a bounded workload/repetition budget before testing. Report counts and conditions, not “deterministic” when the signal remains noisy.
- If reproduction or execution is blocked, state what was attempted, what access/artifact is missing, and the next discriminating step. A source-level explanation can be useful but is not a verified fix.
- If an urgent mitigation is requested before diagnosis is complete, label it as mitigation, explain its risk and rollback, and stay within authorization.
- Never replay captured side effects against production, add production instrumentation, spend unapproved resources, or expose secrets. Use authorized isolated environments and redact captured artifacts.

## Finish

Report the symptom, supported cause or ranked uncertainty, scoped change if any, commands actually run with relevant outcomes, and checks not run. Link existing reusable evidence when useful; do not save a report by default. If execution was blocked, use “unverified” rather than “fixed.”

For an investigation needing another session, maintain a current snapshot of the symptom, supported cause or remaining hypotheses, discriminating evidence and next probe, not a probe-by-probe diary. On completion, keep useful regression protection and apply the documentation and local-task removal rules above; preserve any task whose work remains active. Do not invoke another workflow or modify agent instruction files/configuration without explicit permission.
