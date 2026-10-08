---
name: domain-language
description: Use when ambiguity in domain terms, states or ownership changes an active design, implementation or diagnosis. Resolve the consequential meaning without starting a separate interview or documentation workflow.
disable-model-invocation: false
user-invocable: false
---

# Domain Language

## Apply within the current task

Use this reference only where meaning affects behavior or a decision. Return to the active workflow after resolving that uncertainty. It requires no other skill; maintain relevant records within existing document-write permission, without widening the task.

## Project records

Before acting or resuming, follow project guidance and existing document maps to the relevant glossary (including a legacy `CONTEXT.md`), ADRs and task/spec. If no map exists, inspect root and affected-area documentation. Reconcile these with current code and evidence; surface conflicts instead of silently treating either as authoritative. Reuse existing files without renaming them or creating parallel records. Missing records are not a reason to scaffold empty documents.

When task-related document writes are authorized, save settled knowledge as it emerges:

- **Meaning:** update the existing glossary; otherwise use `GLOSSARY.md` in the relevant context. Record only confirmed, reusable domain definitions, not implementation or progress.
- **Decision:** write a short ADR only when the choice is costly to reverse, surprising without context, and involves real alternatives. Follow existing naming; otherwise use the next unused `docs/adr/NNNN-slug.md`. State context, decision, rejected alternative and reason.
- **Task:** for cross-stage/session work, maintain one existing issue/spec or task record; without one use `docs/tasks/<slug>.md`. Keep scope, acceptance criteria, linked glossary/ADRs, verified progress, blockers and next step. Do not duplicate long-term knowledge here.

Separate observations, accepted decisions and hypotheses; preserve the source or confirming request. Mark replaced decisions as superseded and link successors rather than erasing history. Re-read targets before editing and preserve unrelated changes. In read-only/no-file mode, provide proposed edits and identify unsaved state. Obtain authorization for external tracker writes; otherwise return a proposed update, not a claim of synchronization. At handoff, give record paths and evidence locations, marking unverified work explicitly.

## Resolve a term

1. Read existing domain documentation, accepted requirements, relevant code and callers. Prefer the project's vocabulary; do not replace familiar terms merely to fit this reference.
2. Identify the competing meanings and the smallest concrete scenario in which they produce different outcomes. Include the actor, entity/state, action and observable consequence.
3. Separate three kinds of statement:
   - **Observed fact:** what code, a test or a document currently says; cite its source. A document's claim is not automatically correct behavior.
   - **Accepted decision:** what an authorized owner or accepted requirement chose, including scope and source.
   - **Hypothesis:** a proposed interpretation, with the evidence or answer needed to confirm it.
4. Resolve ordinary terminology from unambiguous project evidence. If the ambiguity changes product behavior, responsibility or a public contract, explain the consequence and ask the decision owner. Do not turn code's current behavior into business authority.
5. Use the resolved meaning consistently in the current change and acceptance examples. Preserve unresolved interpretations as such; a user timeout does not confirm one.

## Probe relationships, not just names

Check identity, lifecycle, ownership and invariants only where relevant. Ask whether two labels name the same entity, whether one entity can outlive another, or which actor may perform a transition. Avoid exhaustive domain modeling for a local task.

Example: “cancel order” might mean stop unshipped items or refund everything. The current handler canceling every item establishes an implementation fact, not the intended rule. A partially shipped order distinguishes the meanings. Label the scenario as hypothetical until supported or confirmed.

## Record proportionally

- Persist a confirmed reusable term immediately under Project records, not only at session end. Keep task-only explanations in the task record or response.
- Use a concise entry: term, definition, relevant context and confusing aliases to avoid. Include a distinguishing example when useful; never promote a hypothesis into the glossary.
- Check existing definitions before updating; resolve contradictions with the decision owner. Do not rename legacy files or create a second glossary merely to match a preferred filename.
- Keep architectural choices in ADRs and current work in task records. Do not rename unrelated code or modify agent instruction files/configuration.

## Exit

The affected behavior has a shared meaning and an observable example, or a precise unresolved question has been returned to the decision owner. Do not keep asking once the ambiguity no longer changes the task.
