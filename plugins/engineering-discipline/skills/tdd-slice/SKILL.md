---
name: tdd-slice
description: Use when the user explicitly requests test-first implementation of a bounded behavior slice. Establish meaningful red, implement minimal green, refactor under evidence, and stop at the agreed boundary.
disable-model-invocation: true
user-invocable: true
---

# TDD Slice

## Scope

Enter only when the user selects test-first implementation. This is not the default entry point for every feature, UI change or refactor. Work one behavior slice at a time, not all tests followed by all production code. Slices organize execution; they do not shrink the user's authorized outcome. This skill works alone.

## Project knowledge and active work

Read relevant code, project guidance and the document map. Reuse existing authorities and locations; missing optional records require neither setup nor empty files.

- **Current behavior:** update the owning contract, architecture document or README in place. Give each fact one home; link rather than duplicate it. Approved but unimplemented behavior belongs in a task or proposed decision, not current documentation.
- **Terms and decisions:** save reusable meanings in the existing glossary (`CONTEXT.md` is valid; otherwise `GLOSSARY.md`). Write an ADR only for a costly-to-reverse, surprising choice with real alternatives. Follow project naming and retention policy, not mandatory append-only history.
- **Active work:** use one task per bounded change needing a handoff. Reuse the tracker; otherwise use `.scratch/<slug>.md` when needed. Maintain current scope, acceptance, confirmed choices and sources, open questions, verification gaps and next action. Replace stale status, not append session summaries. New work does not extend completed tasks.
- **Completion:** update long-term knowledge and links, retain necessary evidence, then close or remove temporary records under project policy. Without one, leave a compact closed task linking lasting outcomes. Preserve unrelated work, required audit records and irreplaceable evidence. Version control retains committed execution history.
- **Evidence:** routine checks belong in the response. Persist only for handoff, comparison, migration or audit, with revision, environment, result and limits. Historical evidence is separate from current contracts.

Respect document-write permission; in read-only mode identify proposed updates as unsaved. Re-read before editing. Distinguish facts, accepted decisions and hypotheses. External writes require authorization; do not initiate agent-configuration changes.

## 1. Choose the slice

Read relevant guidance, callers, test conventions and accepted requirements. State the behavior as an observable example: input/context, action, expected result and meaningful side effects. Define what is out of scope.

Use an existing supported interface when it exposes the behavior. No user approval is needed merely to select an ordinary test boundary. Ask only when new product behavior, a public-contract change or a hard-to-reverse decision is unresolved. A test must not silently decide such a question.

For a multi-slice request, finish each slice before the next and continue through the already-authorized scope without asking permission at every boundary. Stop only at completion, an explicit user boundary or a material blocker. No one-test, one-method or one-file quota.

## 2. Establish meaningful red

- Write a focused check against behavior, with expected results derived independently from requirements, examples or invariants, not copied from the implementation under test.
- Prefer the narrowest interface that exercises the real path. Internal algorithm tests are reasonable when they protect a stable invariant; do not freeze incidental call order, private method names or object layout.
- Use controlled dependencies at real external boundaries. A fake should preserve the contract relevant to the test; add integration/contract coverage where the risk resides in the real dependency. Do not mock the very behavior being verified.
- Execute the check and inspect the failure. A missing declared API may be the expected initial red; an unrelated import error, absent dependency or broken test runner is not evidence of the requested behavior.
- If it passes already, determine whether behavior exists, the assertion is insensitive or the scenario is wrong. Do not manufacture a failure or weaken the requirement to perform the ceremony.

## 3. Reach green, then refactor

Implement only what this slice requires. Execute the same check and inspect the result. Do not change the expected result just to make an implementation pass; a changed requirement needs its own evidence or confirmation.

Once green, simplify touched code when there is a concrete benefit, preserving the contract. Run the check again after refactoring. Retain useful tests; remove redundant coverage only when equivalent protection is demonstrated. Do not launch a separate review pipeline or speculative architecture project.

## 4. Verify and stop

Run relevant neighboring tests, type/build or integration checks according to risk. Inspect the diff. A slice is complete when its acceptance behavior passes and verification limits are stated; continue if more authorized work remains.

If execution is unavailable, report the exact blocker and leave the status unverified. Do not claim a red-green cycle from tests you wrote but never ran. If a pure refactor already has adequate passing coverage, use that baseline and label it behavior-preservation work rather than inventing red.

For visual, performance or probabilistic behavior, define a comparison method, acceptance rule and bounded sampling before implementation. Report actual observations and limits; do not pretend a subjective or noisy signal is a deterministic unit test.

## Handoff

Summarize delivered behavior, observed red and green, relevant checks and gaps. At a pause, refresh an existing task's current state and next action. At completion, update current knowledge and close the task as above. A small change with no durable knowledge change or handoff needs no new document; never write a report per test.

Do not change agent instruction files/configuration, install broad tooling, affect external systems or expand task scope merely because this workflow is loaded.
