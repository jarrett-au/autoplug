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

Read relevant code, project guidance and the document map. Reuse existing authorities and locations; missing optional records require neither setup nor empty files.

- **Current behavior:** update the owning contract, architecture document or README in place. Give each fact one home; link rather than duplicate it. Approved but unimplemented behavior belongs in a task or proposed decision, not current documentation.
- **Terms and decisions:** save reusable meanings in the existing glossary (`CONTEXT.md` is valid; otherwise `GLOSSARY.md`). Write an ADR only for a costly-to-reverse, surprising choice with real alternatives. Follow project naming and retention policy, not mandatory append-only history.
- **Active work:** use one task per bounded change needing a handoff. Reuse the tracker; otherwise use `.scratch/<slug>.md` when needed. Maintain current scope, acceptance, confirmed choices and sources, open questions, verification gaps and next action. Replace stale status, not append session summaries. New work does not extend completed tasks.
- **Completion:** update long-term knowledge and links, retain necessary evidence, then close or remove temporary records under project policy. Without one, leave a compact closed task linking lasting outcomes. Preserve unrelated work, required audit records and irreplaceable evidence. Version control retains committed execution history.
- **Evidence:** routine checks belong in the response. Persist only for handoff, comparison, migration or audit, with revision, environment, result and limits. Historical evidence is separate from current contracts.

Respect document-write permission; in read-only mode identify proposed updates as unsaved. Re-read before editing. Distinguish facts, accepted decisions and hypotheses. External writes require authorization; do not initiate agent-configuration changes.

## Process

1. **Bound the symptom.** Read relevant instructions, code, recent changes and existing tests. Record expected behavior and its source, actual behavior, affected environment/input and known limits. If the expectation is ambiguous, clarify it before choosing a fix. Keep observations separate from explanations.
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

Report the symptom, supported cause or ranked uncertainty, scoped change if any, commands actually run with relevant outcomes, and checks not run. Link reusable evidence using project conventions. If execution was blocked, use “unverified” rather than “fixed.”

For an investigation needing another session, maintain a current snapshot of the symptom, supported cause or remaining hypotheses, discriminating evidence and next probe, not a probe-by-probe diary. On completion, keep useful regression protection, repair affected current documentation and close the task under project policy. A routine resolved bug needs no new investigation report. Do not invoke another workflow or modify agent instruction files/configuration.
