---
name: module-design
description: Use when an active change needs an interface, ownership boundary or test seam decision. Place real complexity behind a usable contract without speculative adapters or a repository-wide redesign.
disable-model-invocation: false
user-invocable: false
---

# Module Design

## Apply within the current task

Inspect only the design decision the active task needs. Do not initiate a full architecture scan, refactor or implementation without authorization. This reference works alone; its vocabulary describes concepts, not mandatory project names.

## Project records

Before acting or resuming, follow project guidance and existing document maps to the relevant glossary (including a legacy `CONTEXT.md`), ADRs and task/spec. If no map exists, inspect root and affected-area documentation. Reconcile these with current code and evidence; surface conflicts instead of silently treating either as authoritative. Reuse existing files without renaming them or creating parallel records. Missing records are not a reason to scaffold empty documents.

When task-related document writes are authorized, save settled knowledge as it emerges:

- **Meaning:** update the existing glossary; otherwise use `GLOSSARY.md` in the relevant context. Record only confirmed, reusable domain definitions, not implementation or progress.
- **Decision:** write a short ADR only when the choice is costly to reverse, surprising without context, and involves real alternatives. Follow existing naming; otherwise use the next unused `docs/adr/NNNN-slug.md`. State context, decision, rejected alternative and reason.
- **Task:** for cross-stage/session work, maintain one existing issue/spec or task record; without one use `docs/tasks/<slug>.md`. Keep scope, acceptance criteria, linked glossary/ADRs, verified progress, blockers and next step. Do not duplicate long-term knowledge here.

Separate observations, accepted decisions and hypotheses; preserve the source or confirming request. Mark replaced decisions as superseded and link successors rather than erasing history. Re-read targets before editing and preserve unrelated changes. In read-only/no-file mode, provide proposed edits and identify unsaved state. Obtain authorization for external tracker writes; otherwise return a proposed update, not a claim of synchronization. At handoff, give record paths and evidence locations, marking unverified work explicitly.

## Working terms

- **Module:** code with an interface and an implementation, from a function to a subsystem.
- **Interface:** everything callers must know to use it correctly, including ordering, errors, invariants, configuration and relevant cost, not just method signatures.
- **Seam:** a place where behavior or dependencies can be substituted without editing the caller's logic.
- **Adapter:** an implementation that connects a contract to a particular dependency.
- **Depth:** useful behavior and knowledge hidden behind an understandable interface, not implementation lines divided by method count.
- **Locality:** a rule or change can be understood and maintained without coordinating unrelated callers.

## Make the decision

1. Read the affected callers, contract, implementation and tests. Name the concrete behavior or dependency creating design pressure. Keep observed coupling separate from a preference for a different style.
2. List the facts callers currently need to know. Identify who should own each invariant, state transition and failure policy. Prefer a boundary that hides knowledge callers should not have to repeat.
3. Consider retaining the existing design first. Introduce or move a seam only to isolate an actual dependency, policy, independently changing concern, lifecycle or verification need. One implementation can justify a seam. Do not create a second adapter to prove the first one deserves to exist.
4. For a nontrivial choice, compare viable options using caller burden, change locality, failure visibility, compatibility and testability. Do not require a second design when there is no meaningful alternative. Note which trade-off drives the recommendation.
5. Trace an actual caller scenario through the proposed contract. Include relevant errors and side effects. State where a test can observe the real behavior; the test surface may be internal when it protects a stable algorithmic invariant.
6. Check scope and evidence. Use existing public contracts without seeking ceremonial approval. Ask before changing public behavior or choosing a hard-to-reverse design. If authorized to implement, verify affected callers and behavior; if only advising, report a proposal rather than a tested improvement.

## Counterchecks

- If this wrapper disappears, does knowledge spread back into callers, or does unnecessary indirection simply vanish? Preserve boundaries that isolate security, compatibility or external volatility even when their implementation is small.
- Is the interface small only because it hides required configuration, ordering or errors? Hidden obligations still count as caller complexity.
- Does the test mock away the risky integration? A clean fake is not evidence that the real adapter obeys the contract.
- Does a proposed abstraction earn its maintenance cost now? Do not build generic registries, inheritance trees or interchangeable backends for hypothetical future needs.

## Exit

Return the chosen boundary or recommendation, what knowledge it owns, its compatibility implications and verification route. If no change is justified, say so. Persist an accepted boundary decision that meets the ADR criteria under Project records; retain alternatives and rationale. Link it from the active task. Ordinary local choices need no ADR, diagram or second implementation. Do not modify agent instruction files/configuration.
