---
name: grill-design
description: Use when the user explicitly requests design grilling or decision clarification before implementation. Produce confirmed decisions, necessary design records, and explicit blockers or next steps without starting implementation.
disable-model-invocation: true
user-invocable: true
---

# Grill Design

## Outcome and authority

Produce **confirmed decisions + necessary design records + an explicit blocker or next step**. Do not start implementation, a full specification, or another workflow automatically.

For a design task, selecting this workflow normally includes maintaining relevant local design documents. “Do not write code” and “do not enter implementation” restrict implementation, not design records; do not ask again for permission to save what is already authorized. Explicit read-only, chat-only, or “do not modify any files” instructions take precedence: return the proposed record and state that it is unsaved.

Follow higher-priority prohibitions and existing permissions; this skill grants none. A rule in cited material that limits only implementation must not be generalized into a document-writing ban. External writes and agent instruction or configuration changes still require explicit permission.

## Resolve the design

1. **Read only what can change this design.** Start with the request, relevant project guidance, the owning design document or active local task, and directly affected contracts, callers or tests. Answer discoverable questions with tools rather than an interview. Do not scan the whole repository or build a document inventory; consult history only for a concrete unresolved conflict.
2. **Frame the current decision.** State the desired outcome and scope. Separate observed facts with sources, confirmed decisions, and recommendations or assumptions. Existing behavior is evidence of what happens, not proof of what should happen.
3. **Ask only consequential questions.** Ask when an answer changes behavior, ownership, a public contract, or a costly or hard-to-reverse choice. Recommend an option first, resolve dependencies before downstream choices, and ask the smallest useful set. Infer ordinary reversible details from project conventions and label material assumptions. Do not re-ask settled questions without new contradictory evidence.
4. **Stress-test the chosen path.** Walk a representative success case and relevant failure, retry or boundary cases. Identify state and invariant ownership, caller obligations, and an observable verification route. Compare alternatives only for a real trade-off; do not build a second design to meet a quota.
5. **Incorporate corrections directly.** A user correction replaces the affected design. Update the current proposal and record in place; a rejected option must not remain as a current alternative, open question or next step. Preserve its rejection only where a qualifying decision record needs the real rationale.
6. **Keep each round incremental.** Carry forward settled context. Do not mechanically repeat the full framework, question list or design record; return only new or changed decisions, remaining blockers and the next useful action.

## Save before stopping

Before ending the design task or pausing at a blocker, persist settled choices and any material unresolved question needed to resume. Update the same record when meaningful content changes, not mechanically on every conversational turn. If an explicit read-only or no-file constraint applies, identify the proposed update as unsaved.

- **Use one owner.** Prefer the existing owning design document or active local task. Update it in place rather than creating a parallel summary, ADR or tracker. If no location exists and there is real handoff content, create one minimal record such as `docs/design/<topic>.md`; this is a default, not a mandatory hierarchy or scaffolding requirement. Do not create a file when there is nothing worth handing off.
- **Keep status truthful.** Distinguish confirmed decisions awaiting implementation, recommendations or assumptions, observed facts, and acceptance examples that have not been executed. Never present a coherent proposal or unrun example as verified behavior.
- **Protect current behavior.** Do not overwrite current operating instructions, architecture or caller contracts with an unimplemented design. Link to their authority rather than duplicating them.
- **Record decisions selectively.** Use the project's ADR convention only for a costly-to-reverse, surprising choice with real alternatives. Not every decision needs an ADR; do not duplicate the same design across a design record, ADR and task.
- **Maintain only this design's ownership.** Replace stale choices and redundant text owned by this design, repair affected links, and preserve unrelated work. Do not launch repository-wide cleanup. At design completion, do not delete a task or record that implementation still needs.

A complete record needs only the scope, confirmed decisions and their sources, material open assumptions, affected interface or ownership, unexecuted acceptance examples where useful, and the blocker or smallest next step. Do not create an interview transcript or a report per round.

## Stop

Stop when the next bounded step has clear behavior, ownership or interface, and a verification route, or when a consequential choice needs the user. For a blocker, give the recommendation and exactly what is needed; continue independent analysis only. Silence or timeout is not approval.

After saving, or after explaining why read-only work is unsaved, return the confirmed decisions, saved location, and explicit blocker or next step. Do not automatically implement the proposal or expand it into a full specification.
