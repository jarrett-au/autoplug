---
name: cq-code-review
description: |
  Use when reviewing code changes, pull requests, git diffs, branches, or implementation quality.
  Builds context from files and git history, then checks correctness, security, performance,
  maintainability, tests, and hidden edge cases. Trigger for 'review this code', 'check my changes',
  'PR review', 'inspect diff', or 'code quality review'.
context: fork
agent: cq-reviewer
allowed-tools: Read, Grep, Glob, Bash
---

# Code Review — 任务指令

## Step 0: 加载需求上下文

**从 review-loop 调用时**（`$ARGUMENTS` 为 session ID）：

读取 `.claude-plugins-data/code-quality/review-loop/$ARGUMENTS/context.json` 获取需求上下文。

**独立使用时**（无 `$ARGUMENTS`）：跳过此步骤。

## Step 1: 获取变更

- **GitHub PR**: `gh pr diff`
- **本地变更**: `git diff`

## Step 2: 深入调查

根据你的调查启发式主动读取文件验证假设。遵循"观察 → 假设 → 验证"循环，直到你有足够信心。

## 输出格式

产出中文审查报告：

```markdown
### 📋 [PR #N 审查简报 / 本地预检]

> **状态**: 🟢 Ready / 🔴 Request Changes
> **风险**: 🔴/🟡/🟢
> **需求覆盖**: X/Y 项已覆盖 *(仅当存在 context.json 时)*
> **概要**: [一句话总结]

### 📋 需求覆盖检查 *(仅当存在 context.json 时)*
- ✅ 需求描述 — `文件路径`
- ❌ 需求描述 — 未找到对应实现

### 🔍 需关注问题

#### 1. [问题标题]
**文件**: `路径:行号`
**问题描述**: ...
**代码片段**:
​```语言
// 有问题的代码
​```
**修复建议**:
​```语言
// 修复后的代码
​```

<details>
<summary>💡 次要建议</summary>
- ...
</details>
```

## 输出行为

**从 review-loop 调用时**（`$ARGUMENTS` 已提供 session ID）：
1. 将完整审查报告保存至 `.claude-plugins-data/code-quality/review-loop/$ARGUMENTS/round-{N}-review.md`（查看已有文件确定下一轮次 N）
2. 仅向主对话返回：
   ```
   审查完成：{状态} | 风险：{等级} | 发现 {X} 个问题（{Y} 主要 + {Z} 次要）| 报告已保存 round-{N}-review.md
   ```
   如有 context.json，追加 `| 需求覆盖 {M}/{K}`

**独立使用时**（无 `$ARGUMENTS`）：直接在对话中输出完整报告。
