---
name: tdd-slice
description: Use when the user explicitly requests test-first implementation of a bounded behavior slice. Establish meaningful red, implement minimal green, refactor under evidence, and stop at the agreed boundary.
disable-model-invocation: true
user-invocable: true
---

# TDD Slice

## Scope

Enter only when the user selects this workflow. Implement the agreed behavior, not an entire development pipeline. Work one behavior slice at a time; do not generate every test first and then all production code. This skill works alone and supplies its own testing rules.

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

Summarize behavior delivered, observed red and green (commands and outcomes), any refactor, neighboring checks and gaps. A brief response is sufficient; no default report, glossary or ADR. Use project conventions for necessary artifacts.

Do not change agent instruction files/configuration, install broad tooling, affect external systems or expand task scope merely because this workflow is loaded.
