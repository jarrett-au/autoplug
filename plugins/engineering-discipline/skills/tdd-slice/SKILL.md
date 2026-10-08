---
name: tdd-slice
description: Use when the user explicitly requests test-first implementation of a bounded behavior slice. Establish meaningful red, implement minimal green, refactor under evidence, and stop at the agreed boundary.
disable-model-invocation: true
user-invocable: true
---

# TDD Slice

## Scope

Enter only when the user selects this workflow. Implement the agreed behavior, not an entire development pipeline. Work one behavior slice at a time; do not generate every test first and then all production code. This skill works alone and supplies its own testing rules.

## Project records

Before acting or resuming, follow project guidance and existing document maps to the relevant glossary (including a legacy `CONTEXT.md`), ADRs and task/spec. If no map exists, inspect root and affected-area documentation. Reconcile these with current code and evidence; surface conflicts instead of silently treating either as authoritative. Reuse existing files without renaming them or creating parallel records. Missing records are not a reason to scaffold empty documents.

When task-related document writes are authorized, save settled knowledge as it emerges:

- **Meaning:** update the existing glossary; otherwise use `GLOSSARY.md` in the relevant context. Record only confirmed, reusable domain definitions, not implementation or progress.
- **Decision:** write a short ADR only when the choice is costly to reverse, surprising without context, and involves real alternatives. Follow existing naming; otherwise use the next unused `docs/adr/NNNN-slug.md`. State context, decision, rejected alternative and reason.
- **Task:** for cross-stage/session work, maintain one existing issue/spec or task record; without one use `docs/tasks/<slug>.md`. Keep scope, acceptance criteria, linked glossary/ADRs, verified progress, blockers and next step. Do not duplicate long-term knowledge here.

Separate observations, accepted decisions and hypotheses; preserve the source or confirming request. Mark replaced decisions as superseded and link successors rather than erasing history. Re-read targets before editing and preserve unrelated changes. In read-only/no-file mode, provide proposed edits and identify unsaved state. Obtain authorization for external tracker writes; otherwise return a proposed update, not a claim of synchronization. At handoff, give record paths and evidence locations, marking unverified work explicitly.

## 1. Choose the slice

Read relevant guidance, callers, test conventions and accepted requirements. State the behavior as an observable example: input/context, action, expected result and meaningful side effects. Define what is out of scope.

Use an existing supported interface when it exposes the behavior. No user approval is needed merely to select an ordinary test boundary. Ask only when new product behavior, a public-contract change or a hard-to-reverse decision is unresolved. A test must not silently decide such a question.

If the request covers several slices, identify the next one and finish it before selecting another within the authorized scope. Do not impose one test, one method or one file as a quota.

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

Run relevant neighboring tests, type/build checks or integration checks according to the change's risk. Inspect the diff. Stop when the slice meets its acceptance behavior, relevant checks pass and remaining verification limits are stated. Start another slice only if it is already in scope.

If execution is unavailable, report the exact blocker and leave the status unverified. Do not claim a red-green cycle from tests you wrote but never ran. If a pure refactor already has adequate passing coverage, use that baseline and label it behavior-preservation work rather than inventing red.

For visual, performance or probabilistic behavior, define a comparison method, acceptance rule and bounded sampling before implementation. Report actual observations and limits; do not pretend a subjective or noisy signal is a deterministic unit test.

## Handoff

Summarize behavior delivered, observed red and green (commands and outcomes), any refactor, neighboring checks and gaps. Update the active task record at each completed stage or pause, linking acceptance criteria to actual checks and remaining gaps. Persist newly settled reusable meanings and qualifying decisions under Project records. Do not write a report per test or copy raw logs into the glossary.

Do not change agent instruction files/configuration, install broad tooling, affect external systems or expand task scope merely because this workflow is loaded.
