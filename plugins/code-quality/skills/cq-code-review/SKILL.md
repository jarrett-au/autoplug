---
name: cq-code-review
description: |
  Evidence-backed code review — 审查 GitHub PR 或本地 git 变更，输出中文结构化报告。
  每个 blocking finding 必须带可验证证据：失败测试、复现命令、需求不匹配、静态证明、安全触发路径或契约违背。
context: fork
agent: cq-reviewer
allowed-tools: Read, Grep, Glob, Bash
---

# Code Review — Evidence-Backed 任务指令

## 核心原则

Reviewer 的任务不是“发表意见”，而是产出可验证的审查断言。

> 没有可验证证据的 finding，不允许 blocking。

blocking 必须便宜地被 checker 复核。无法验证但值得注意的问题，降级为 risk。纯风格偏好只能是 nit。

## Step 0: 加载需求上下文

**从 review-loop 调用时**（`$ARGUMENTS` 为 session ID）：

读取 `.claude-plugins-data/code-quality/review-loop/$ARGUMENTS/context.json` 获取需求上下文。

**独立使用时**（无 `$ARGUMENTS`）：跳过此步骤。

## Step 1: 获取变更

优先审查当前分支相对 main 的完整变更：

```bash
git diff main...HEAD --stat
git diff main...HEAD --name-only
git diff main...HEAD
```

如果处于 GitHub PR 上，也可使用：

```bash
gh pr diff
```

## Step 2: 深入调查

根据调查启发式主动读取文件验证假设。遵循“观察 → 假设 → 验证”循环，直到你有足够信心。

重点：如果你准备提出 blocking，必须先为它构造可验证证据。

## Step 3: 分析顺序

1. **需求覆盖**：如果存在 context.json，先核对每条需求/验收标准。
2. **正确性**：边界条件、错误处理、并发、幂等、数据一致性。
3. **安全性**：注入、权限绕过、敏感信息、危险执行路径。
4. **测试质量**：核心路径、失败路径、回归场景是否覆盖。
5. **性能/维护性**：只在有明确风险时升级，否则作为 risk/nit。

## Finding 分级

### 🔴 blocking

只能用于必须修的问题。必须满足：

- 绑定当前 diff 或需求上下文
- 影响正确性、安全、数据、需求覆盖、关键测试或严重性能
- 包含以下证据之一：
  - `failing_test`
  - `repro_command`
  - `requirement_mismatch`
  - `static_proof`
  - `security_exploit_path`
  - `contract_violation`

### 🟡 risk

问题值得关注，但不应自动阻塞：

- 缺少低成本复现
- 依赖真实环境/规模数据
- 属于维护性或可演进性风险
- 需要人类产品/架构判断

### ⚪ nit

局部风格、命名、可读性建议。nit 不进入 review-loop 自动修复清单。

## 输出格式

产出中文审查报告：

````markdown
### 📋 [PR #N 审查简报 / 本地预检]

> **状态**: 🟢 LGTM / 🟡 RISKS_NOTED / 🔴 NEEDS_CHANGES
> **风险**: 🔴/🟡/🟢
> **需求覆盖**: X/Y 项已覆盖 *(仅当存在 context.json 时)*
> **概要**: [一句话总结]

### 📋 需求覆盖检查 *(仅当存在 context.json 时)*
- ✅ R1 需求描述 — `文件路径`
- ❌ R2 需求描述 — finding `R1`
- ⚠️ R3 需求描述 — risk `R2`

### 🔴 Blocking Findings

#### R1. [问题标题]
```yaml
id: R1
severity: blocking
category: correctness | requirement_gap | test_gap | security | performance | maintainability
confidence: high | medium | low
blocks_merge: true
affected_files:
  - path: path/to/file
    lines: L10-L20
claim: >
  具体、可检验的断言。
evidence:
  type: failing_test | repro_command | requirement_mismatch | static_proof | security_exploit_path | contract_violation
  content: >
    证据内容。blocking 不允许 reasoning_only。
reproduction:
  command: 可执行命令；如无则写 none
  minimal_case: 最小输入/场景；如无则写 none
  expected_failure: 当前代码下预期如何失败；如无则写 none
fix_expectation: >
  修复后应该满足什么。
checker_instructions: >
  checker 应如何验证这个 finding。
```

### 🟡 Risks / Investigation

#### R2. [风险标题]
```yaml
id: R2
severity: risk
category: ...
confidence: medium
blocks_merge: false
claim: ...
evidence:
  type: reasoning_only | static_proof | requirement_mismatch
  content: ...
why_not_blocking: >
  说明为什么不阻塞。
```

### ⚪ Nits
- N1. [非阻塞建议]

### Reviewer Self-Check
- [ ] 每个 blocking 都有非 reasoning_only 证据
- [ ] 每个 blocking 都有 checker_instructions
- [ ] 所有 finding 都绑定当前 diff 或需求上下文
- [ ] 没有 taste-only blocking
- [ ] 证据不足的问题已降级为 risk
````

## 输出行为

**从 review-loop 调用时**（`$ARGUMENTS` 已提供 session ID）：
1. 将完整审查报告保存至 `.claude-plugins-data/code-quality/review-loop/$ARGUMENTS/round-{N}-review.md`（查看已有文件确定下一轮次 N）
2. 仅向主对话返回：
   ```
   审查完成：{状态} | 风险：{等级} | blocking {B} 个 | risks {R} 个 | nits {N} 个 | 报告已保存 round-{N}-review.md
   ```
   如有 context.json，追加 `| 需求覆盖 {M}/{K}`

**独立使用时**（无 `$ARGUMENTS`）：直接在对话中输出完整报告。
