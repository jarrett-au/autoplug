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

Read current code and project guidance; reuse locations and retention policies. Maintain knowledge for the next action, not history. No mandatory setup or scaffolding.

- **Current knowledge:** update the owner in place, replacing stale text and linking rather than copying. Start with an existing README section; split for stable reader/update boundaries, not length or feature names. Without conventions, use README for operations/checks, `docs/architecture/overview.md` for structure, `docs/architecture/client-contract.md` for callers, and `GLOSSARY.md`/`CONTEXT.md` for terms, only as needed.
- **Decisions:** actively record costly-to-reverse, surprising choices with real alternatives in existing ADRs or `docs/adr/`. No invented approvals, chronology or duplicated API details. Proposals are not implemented behavior.
- **Active work:** use the tracker or, when handoff requires it, `.scratch/<slug>.md`. Keep current scope, acceptance, confirmed choices/sources, open questions, verification gaps and next action; replace stale status.
- **Evidence:** report results in the response, including migrations/comparisons. Save only explicitly required records or artifacts needed for a concrete unresolved question or active handoff; specify purpose, scope and revision. No evidence collection or routine reports.
- **Completion:** update current knowledge, remove scope-owned stale/redundant text and repair links. Migrate valid knowledge from completed in-scope local tasks, then remove them, unless explicit retention policy differs. Preserve active/unrelated work, data, backups, images and required audit artifacts. External trackers are closed only with permission, never history-deleted.

Respect document-write permission; identify read-only proposals as unsaved. Re-read before editing; distinguish facts, decisions and hypotheses. External writes and instruction/configuration updates need explicit permission.

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
- Do not modify agent instruction files or runtime configuration to persist these rules without explicit permission.

## Handoff

Return only what is useful for the next step:

- Outcome and scope.
- Confirmed decisions and their sources; assumptions still unconfirmed.
- Affected interface/ownership and observable acceptance examples.
- Remaining blocker, or the smallest implementation/specification step the user can choose next.

Do not call the design “validated” merely because its description is coherent. Distinguish a reviewed proposal from executed evidence.

Refresh a still-active design task for handoff. If this bounded design task is complete, apply the completion rule above without implementing the proposal or deleting a task whose implementation remains active.
