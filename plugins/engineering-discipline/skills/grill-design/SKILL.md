---
name: grill-design
description: Use when the user explicitly requests design grilling or decision clarification before implementation. Resolve consequential ambiguities with concrete scenarios and evidence, then stop at a bounded handoff.
disable-model-invocation: true
user-invocable: true
---

# Grill Design

## Scope

Enter only when the user selects this workflow. Clarify the requested design; do not start implementation, a full specification, or another workflow automatically. This skill works alone. Reading guidance does not expand permission to act.

## Project knowledge and active work

Read relevant code, project guidance and the document map. Reuse existing authorities and locations; missing optional records require neither setup nor empty files.

- **Current behavior:** update the owning contract, architecture document or README in place. Give each fact one home; link rather than duplicate it. Approved but unimplemented behavior belongs in a task or proposed decision, not current documentation.
- **Terms and decisions:** save reusable meanings in the existing glossary (`CONTEXT.md` is valid; otherwise `GLOSSARY.md`). Write an ADR only for a costly-to-reverse, surprising choice with real alternatives. Follow project naming and retention policy, not mandatory append-only history.
- **Active work:** use one task per bounded change needing a handoff. Reuse the tracker; otherwise use `.scratch/<slug>.md` when needed. Maintain current scope, acceptance, confirmed choices and sources, open questions, verification gaps and next action. Replace stale status, not append session summaries. New work does not extend completed tasks.
- **Completion:** update long-term knowledge and links, retain necessary evidence, then close or remove temporary records under project policy. Without one, leave a compact closed task linking lasting outcomes. Preserve unrelated work, required audit records and irreplaceable evidence. Version control retains committed execution history.
- **Evidence:** routine checks belong in the response. Persist only for handoff, comparison, migration or audit, with revision, environment, result and limits. Historical evidence is separate from current contracts.

Respect document-write permission; in read-only mode identify proposed updates as unsaved. Re-read before editing. Distinguish facts, accepted decisions and hypotheses. External writes require authorization; do not initiate agent-configuration changes.

## Process

1. **Read before asking.** Inspect the request, relevant project guidance, existing decisions, interfaces and callers. Use current documentation for version-sensitive external contracts. Resolve code questions with tools, not an interview. If documents conflict or are outdated, identify the conflict rather than silently choosing one.
2. **Frame the decision.** State the desired observable outcome, affected users/callers, constraints and excluded work. Separate observed facts (with sources), accepted decisions (with authority), and hypotheses. Existing behavior is evidence of what happens, not proof of what should happen.
3. **Find consequential uncertainty.** Focus on ambiguities that change behavior, ownership, a public contract, reversibility, security or verification. Test overloaded terms with examples. For “cancel,” ask what happens to already-shipped items only if the answer changes this design. Do not impose a vocabulary foreign to the project.
4. **Recommend, then ask.** For each blocking choice, explain the consequence and recommend an option. Ask the smallest useful set of questions; group independent ones, but resolve dependencies first. Do not demand a fixed number of rounds or alternatives. Do not re-ask settled questions without new contradictory evidence.
5. **Stress-test the chosen path.** Walk a representative success case and relevant failure, retry or boundary cases. Identify who owns state and invariants, what callers must know, and how success will be observed. Compare alternatives only where there is a real trade-off. Do not build a second design merely to satisfy a quota.
6. **Close or expose the blocker.** Stop when the next bounded step has a clear behavior, owner/interface and verification route, with no unresolved high-impact choice. If a decision needs the user, stop that branch and state exactly what is needed. Continue independent analysis only. A silence or timeout is not approval.

## Decision handling

- Infer ordinary, reversible implementation details from project conventions; label material assumptions. Ask about new product behavior, changed public contracts and hard-to-reverse choices.
- Reuse accepted decisions from an existing requirements process. Do not repeat that process or automatically launch a specification or UI-design tool.
- A hypothetical scenario is a probe, not an observed customer requirement. Keep it labeled until confirmed.
- Save settled reusable knowledge in its owning document. For a cross-session design, refresh the active task into a resumable snapshot, linking current contracts instead of repeating them. Keep target behavior and unverified acceptance examples explicit. Do not create an interview transcript or a report per round.
- Do not modify agent instruction files or runtime configuration to make these rules persistent.

## Handoff

Return only what is useful for the next step:

- Outcome and scope.
- Confirmed decisions and their sources; assumptions still unconfirmed.
- Affected interface/ownership and observable acceptance examples.
- Remaining blocker, or the smallest implementation/specification step the user can choose next.

Do not call the design “validated” merely because its description is coherent. Distinguish a reviewed proposal from executed evidence.
