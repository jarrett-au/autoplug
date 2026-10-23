---
name: domain-language
description: Use when ambiguity in domain terms, states or ownership changes an active design, implementation or diagnosis. Resolve the consequential meaning without starting a separate interview or documentation workflow.
disable-model-invocation: false
user-invocable: false
---

# Domain Language

## Apply within the current task

Use this reference only where meaning affects behavior or a decision. Return to the active workflow after resolving that uncertainty. It requires no other skill; maintain relevant records within existing document-write permission, without widening the task.

## Knowledge ownership

Follow the project's document map to the relevant glossary (`CONTEXT.md` is valid), current contracts, decisions and active task. Reconcile conflicts with code and accepted requirements. Do not create a second glossary or rename files.

Own vocabulary, not the whole task lifecycle. Within existing write permission, update confirmed reusable definitions in place; absent a glossary, use `GLOSSARY.md` only when there is a real definition to save. Link state machines and contracts instead of copying them. Keep implementation details, progress and conversation history out. A proposed or approved future concept must not imply that it is implemented.

Leave task progress and closure to the active workflow. In read-only mode, propose the definition and mark it unsaved. Do not initiate tracker, agent-configuration or unrelated documentation changes.

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

- Save a confirmed reusable term when it settles, not a transcript of how it was discussed. Task-local explanations belong in the response or existing active task.
- Use a concise entry: term, definition, relevant context and confusing aliases to avoid. Include a distinguishing example when useful; never promote a hypothesis into the glossary.
- Re-read definitions before editing and resolve contradictions with the decision owner. Follow the project's retention policy rather than appending superseded definitions.
- Architectural rationale belongs in a qualifying ADR; current behavior belongs in its contract. Link those authorities when needed, without creating them merely to complete a template. Do not rename unrelated code or modify agent instruction files/configuration.

## Exit

The affected behavior has a shared meaning and an observable example, or a precise unresolved question has been returned to the decision owner. Do not keep asking once the ambiguity no longer changes the task.
