---
name: cq-check-comment
description: |
  Evidence audit for AI review reports — 验证 reviewer 的证据链是否成立，而不是再发表一次泛泛意见。
  对每个 finding 输出 accepted / downgraded / rejected，并生成 developer action list。
context: fork
agent: cq-comment-checker
allowed-tools: Read, Grep, Glob, Bash
---

# Check Comment — Evidence Audit 任务指令

## 核心原则

check-comment 的职责不是“判断 reviewer 像不像对”，而是验证 reviewer 给出的证据是否成立。

> 不验证观点，验证证据。

如果 reviewer 的 blocking finding 没有可验证证据，必须降级或驳回。

## Step 0: 加载审查输入

**从 review-loop 调用时**（`$ARGUMENTS` 为 session ID）：
1. 读取 `.claude-plugins-data/code-quality/review-loop/$ARGUMENTS/` 目录下最新的 `round-*-review.md`
2. 读取 `.claude-plugins-data/code-quality/review-loop/$ARGUMENTS/context.json`（如果存在）
3. 如果有上一轮 `round-*-verdict.md`，检查是否重复提出已 rejected 的 finding

**独立使用时**（无 `$ARGUMENTS`）：审查报告应在对话上下文中。

## Step 1: 收集代码上下文

读取报告中涉及的所有源文件当前代码，以及必要的：

- 调用方代码
- 配置和初始化逻辑
- 测试文件
- 项目的架构规则和设计文档（如果存在）

如果 review 提供了复现命令或测试命令，在安全、低成本的前提下执行并记录结果。

## Step 2: 逐项验证 finding

对每个 finding，独立判断：

1. **证据存在吗？** blocking 是否包含非 `reasoning_only` 的证据？
2. **证据可执行/可检查吗？** 命令、测试、静态证据、需求映射是否具体？
3. **证据成立吗？** 当前代码是否真的触发该失败或不匹配？
4. **归因准确吗？** 失败是否由当前 diff 或需求缺口导致？
5. **严重程度准确吗？** 是否真的应该 blocking？
6. **修复期望合理吗？** 是否小而精确，避免过度工程化？

## 判定规则

### accepted

证据成立，claim 准确，严重程度合理。accepted blocking 会进入 developer action list。

### downgraded

问题可能存在，但证据不足以 blocking，或更适合 risk/nit。

### rejected

证据无法复现、与 claim 无关、和当前 diff 无关、严重性夸大，或只是 taste。

## 输出格式

````markdown
# Evidence Audit Verdict

## Summary

- accepted blocking: N
- downgraded: N
- rejected: N
- risks noted: N

## Findings

### R1 — [标题]
```yaml
finding_id: R1
reviewer_severity: blocking | risk | nit
verdict: accepted | downgraded | rejected
final_severity: blocking | risk | nit | none
confidence: high | medium | low
verification:
  evidence_checked: failing_test | repro_command | requirement_mismatch | static_proof | security_exploit_path | contract_violation | reasoning_only
  commands_run:
    - command: ...
      result: passed | failed | not_run
      notes: ...
  code_checked:
    - path: path/to/file
      notes: ...
reason: >
  为什么采纳、降级或驳回。必须引用证据。
fix_recommendation: >
  仅当 accepted 或 downgraded 且值得修时填写。否则写 none。
```

## Developer Action List

只列 accepted blocking 和明确值得修的 downgraded risk：

1. R1 — [应修什么]
   - verification to close: [修复后如何验证]
````

## 输出行为

**从 review-loop 调用时**（`$ARGUMENTS` 已提供 session ID）：
1. 将完整结论保存至 `.claude-plugins-data/code-quality/review-loop/$ARGUMENTS/round-{N}-verdict.md`（N 与 review 轮次一致）
2. 仅向主对话返回：
   ```
   证据审计完成：accepted blocking {A} 个 | downgraded {D} 个 | rejected {R} 个 | 结论已保存 round-{N}-verdict.md
   ```

**独立使用时**（无 `$ARGUMENTS`）：直接在对话中输出完整结论。
