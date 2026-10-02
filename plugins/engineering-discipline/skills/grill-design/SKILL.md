---
name: grill-design
description: Use when the user explicitly requests design grilling or decision clarification before implementation. Resolve consequential ambiguities with concrete scenarios and evidence, then stop at a bounded handoff.
disable-model-invocation: true
user-invocable: true
---

# Grill Design

## Scope

Enter only when the user selects this workflow. Clarify the requested design; do not start implementation, a full specification, or another workflow automatically. This skill works alone. Reading guidance does not expand permission to act.

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
- Do not create a glossary, ADR or report by default. Keep a short decision summary in the response. Update existing project documents only within the authorized scope; propose a new durable record only when reuse or a meaningful trade-off warrants it.
- Do not modify agent instruction files or runtime configuration to make these rules persistent.

## Handoff

Return only what is useful for the next step:

- Outcome and scope.
- Confirmed decisions and their sources; assumptions still unconfirmed.
- Affected interface/ownership and observable acceptance examples.
- Remaining blocker, or the smallest implementation/specification step the user can choose next.

Do not call the design “validated” merely because its description is coherent. Distinguish a reviewed proposal from executed evidence.
