---
name: domain-language
description: Use when ambiguity in domain terms, states or ownership changes an active design, implementation or diagnosis. Resolve the consequential meaning without starting a separate interview or documentation workflow.
disable-model-invocation: false
user-invocable: false
---

# Domain Language

## Apply within the current task

Use this reference only where meaning affects behavior or a decision. Return to the active workflow after resolving that uncertainty. It grants no additional permission to edit, rename, document or broaden the task, and requires no other skill.

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

- Keep a resolved term in the response when it is only needed for this task.
- Reuse an existing glossary or decision record when the change is in scope. Do not create a new one by default or overwrite accepted definitions without surfacing the contradiction.
- Propose a durable glossary entry only for meaning that is likely to recur across tasks. Record a design decision only when a real, consequential trade-off was made; include alternatives, rationale and remaining uncertainty.
- Follow project document conventions. Do not impose a directory scheme, rename code across the repository, or modify agent instruction files/configuration to make the terminology persistent.

## Exit

The affected behavior has a shared meaning and an observable example, or a precise unresolved question has been returned to the decision owner. Do not keep asking once the ambiguity no longer changes the task.
