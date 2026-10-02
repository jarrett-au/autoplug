---
name: feedback-loop
description: Use when an active task needs evidence that distinguishes correct behavior from a specific defect or regression. Build and execute a scoped check, account for noise, and state what the result cannot establish.
disable-model-invocation: false
user-invocable: false
---

# Feedback Loop

## Apply within the current task

Use the smallest useful observation loop for the current claim. Do not initiate another workflow, expand edit permissions or build a test platform by default. This reference works alone.

## Build the loop

1. **State the claim.** Identify the behavior and source of the expected result. Write down what observation would contradict the claim. “The command exited zero” is sufficient only when that is the relevant behavior.
2. **Choose the observation point.** Reuse an existing test or check when it reaches the actual risk. Otherwise choose a focused test, request, replay, browser action, benchmark, trace or structured human comparison. Minimize setup without removing the failure mechanism.
3. **Check sensitivity.** Where safe, demonstrate that the check detects the known defect or an independently constructed negative example. Do not overwrite user work to recreate old code; use an isolated fixture/worktree when needed. Never deploy a deliberately broken version. If sensitivity cannot be shown, state the limitation instead of treating a green result as strong evidence.
4. **Execute and capture.** Record the actual command or human procedure, relevant inputs/environment, result and artifact location when useful. Read the result; merely launching a job is not verification. Keep expectations and observed results separate. Redact secrets and personal data.
5. **Compare like with like.** After a change, repeat the same check under equivalent conditions. Include neighboring behavior or the original full scenario if the focused check omits relevant risk. Do not silently move the acceptance threshold after seeing the result.
6. **Bound the conclusion.** Name what the evidence supports, what it does not, and whether remaining uncertainty blocks completion. A check that cannot run is unavailable evidence, not a pass.

## Handle imperfect signals

- **Deterministic behavior:** control inputs, time, randomness and dependencies when doing so preserves the behavior under test. Distinguish test setup failure from the defect.
- **Races and performance:** choose a workload, repetitions and useful metric before comparing. Record failures/attempts or distribution, environment and known confounders. Use repeatable interleavings when possible; zero observed failures does not prove impossibility.
- **LLM outputs:** define the task rubric, sample set, model/configuration and sampling budget. Separate format validity from task correctness. Keep held-out cases separate from examples used to tune the solution. A model judging itself is not independent evidence.
- **Visual or manual checks:** specify the view/state, comparison criteria and who must inspect it. Report inspected samples and subjective limits. If the required human judgment is pending, mark it pending rather than inventing a verdict.

Prefer fast automated feedback where it is representative. Do not reject useful slower, noisy or human evidence merely because it cannot be reduced to a deterministic test.

## Bound cost and authority

Use an effort budget appropriate to the task. Stop or ask when further probing adds little information, requires missing access or would consume unapproved resources. Do not run destructive probes, production replays, paid evaluations or external mutations without authorization. Do not modify agent instruction files/configuration to persist this guidance.

## Exit

Return a compact claim → observation → conclusion, with real commands/results and remaining gaps. Save durable evidence only when the project or risk warrants it, using project conventions. Do not create a report merely to fill a template or claim behavioral improvement from packaging checks.
