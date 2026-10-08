---
name: grill-design
description: Use when the user explicitly requests design grilling or decision clarification before implementation. Resolve consequential ambiguities with concrete scenarios and evidence, then stop at a bounded handoff.
disable-model-invocation: true
user-invocable: true
---

# Grill Design

## Scope

Enter only when the user selects this workflow. Clarify the requested design; do not start implementation, a full specification, or another workflow automatically. This skill works alone. Reading guidance does not expand permission to act.

## Project records

Before acting or resuming, follow project guidance and existing document maps to the relevant glossary (including a legacy `CONTEXT.md`), ADRs and task/spec. If no map exists, inspect root and affected-area documentation. Reconcile these with current code and evidence; surface conflicts instead of silently treating either as authoritative. Reuse existing files without renaming them or creating parallel records. Missing records are not a reason to scaffold empty documents.

When task-related document writes are authorized, save settled knowledge as it emerges:

- **Meaning:** update the existing glossary; otherwise use `GLOSSARY.md` in the relevant context. Record only confirmed, reusable domain definitions, not implementation or progress.
- **Decision:** write a short ADR only when the choice is costly to reverse, surprising without context, and involves real alternatives. Follow existing naming; otherwise use the next unused `docs/adr/NNNN-slug.md`. State context, decision, rejected alternative and reason.
- **Task:** for cross-stage/session work, maintain one existing issue/spec or task record; without one use `docs/tasks/<slug>.md`. Keep scope, acceptance criteria, linked glossary/ADRs, verified progress, blockers and next step. Do not duplicate long-term knowledge here.

Separate observations, accepted decisions and hypotheses; preserve the source or confirming request. Mark replaced decisions as superseded and link successors rather than erasing history. Re-read targets before editing and preserve unrelated changes. In read-only/no-file mode, provide proposed edits and identify unsaved state. Obtain authorization for external tracker writes; otherwise return a proposed update, not a claim of synchronization. At handoff, give record paths and evidence locations, marking unverified work explicitly.

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
- Persist confirmed reusable terms and qualifying decisions during clarification using Project records. For staged work, update the task record before handing off; a chat summary alone is insufficient unless writes are disallowed. Do not generate a full specification or a separate interview report.
- Do not modify agent instruction files or runtime configuration to make these rules persistent.

## Handoff

Return only what is useful for the next step:

- Outcome and scope.
- Confirmed decisions and their sources; assumptions still unconfirmed.
- Affected interface/ownership and observable acceptance examples.
- Remaining blocker, or the smallest implementation/specification step the user can choose next.

Do not call the design “validated” merely because its description is coherent. Distinguish a reviewed proposal from executed evidence.
