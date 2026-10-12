---
name: behavior-to-context
description: >-
  Use when turning user feedback about unwanted agent behavior into reusable
  instructions for AGENTS.md, CLAUDE.md, or other context files. Trigger on
  requests to turn a complaint into a rule or decide its scope and placement.
---

# Behavior to Context

Turn concrete feedback into a minimal, reusable instruction. Return a recommended scope and location plus a ready-to-paste rule. Drafting a rule does not authorize modifying live configuration.

## Process

1. Extract the observed failure and desired replacement behavior. Separate the example from the general principle. Do not speculate about model psychology or repeat insults. If the failure is unclear, ask for the smallest useful before/after sample.
2. Choose the narrowest appropriate scope:
   - Global: stable preferences across unrelated projects.
   - Project or directory: conventions tied to that project or subtree.
   - Current task: one-off corrections; do not persist them without a request.
   Decide when intent is clear. Do not turn ordinary venting into persistent policy.
3. Identify the target agent from the user's request and project context. Do not assume that the agent running this skill is the target. Verify its official documentation before asserting paths, precedence, loading, or refresh behavior. Inspect existing context files when available. If the target remains ambiguous, ask which agent; a runtime-neutral draft can still be provided, with placement marked unresolved.
4. Prefer ordinary standing instructions for behavior preferences. Use system-level configuration only when the requirement calls for it. Do not transfer one agent's loading semantics to another or escalate solely because the user is frustrated.
5. Draft a short English Markdown section, usually a heading and 2–4 sentences, unless another language is requested. Explain scope and placement briefly in the user's language. Give one recommended location and one block, not a menu of near-duplicates. If documentation cannot be verified, state that limitation rather than inventing an exact path or activation command.
6. Check the rule against the original failure and a neighboring legitimate use case. Preserve explicit user requests, necessary explanations, and truthful reporting of limitations. This is a wording review, not a behavioral test.

## Drafting Rules

- Describe the desired action using observable criteria, not just a prohibition or an instruction to “be better”.
- Generalize the failure mechanism, not incidental objects in the example.
- Keep the rule proportional. Do not turn a disliked default into an unconditional ban.
- Omit complaint narratives, model names, duplicate prohibitions, compliance declarations, and long rationales from the rule.
- Reconcile or replace relevant existing instructions instead of appending contradictory or repetitive rules.
- Do not promise that a prompt guarantees compliance.

## Example: Handling Feedback

Feedback: after being asked to remove an ingredient, the agent labels the result a “no-ingredient edition” and explains the exclusion inside the finished work.

Scope: global standing instructions, if the user wants this preference across tasks. Resolve the actual file for the target agent before recommending a path.

```markdown
## Handling Feedback
Apply user feedback to the work itself, not as commentary within it. The revised result should read as if it had been done correctly from the start. Unless explicitly requested or necessary to the substance, omit revision labels, rejected alternatives, explanations of exclusions, and declarations of compliance. Address the intent of the feedback throughout the relevant content rather than mechanically replacing words.
```

Check: the revised dish stands on its own. An explicit request for a change log or comparison still receives one. A material limitation is still reported.

## Applying an Approved Rule

- Default to the recommendation and snippet. Do not modify context files unless explicitly asked.
- Before writing, inspect the actual target, active profile, and relevant existing instructions. Confirm the intended scope when unresolved.
- Make a targeted edit that preserves unrelated content and resolves overlap. Respect read-only requests and write restrictions.
- Report the actual file and change, plus documented activation or verification steps. Distinguish a saved edit from verified runtime loading or tested model behavior; claim only checks actually performed.
