---
name: check-comment
description: |
  审查 AI 生成的代码 review 报告——判断问题是否真实存在，给出采纳建议和修复方案。
  当用户提到 review 报告、代码审查报告、AI review、check comment、审查意见时触发。
context: fork
agent: comment-checker
allowed-tools: Read, Grep, Glob, Bash
---

# Check Comment — 任务指令

## Step 0: 加载审查输入

**从 review-loop 调用时**（`$ARGUMENTS` 为 session ID）：
1. 读取 `.review-loop/$ARGUMENTS/` 目录下最新的 `round-*-review.md`
2. 读取 `.review-loop/$ARGUMENTS/context.json`（如果存在）

**独立使用时**（无 `$ARGUMENTS`）：审查报告应在对话上下文中。

## Step 1: 收集代码上下文

读取报告中涉及的**所有源文件当前代码**，以及：
- 配置结构体和加载逻辑
- 调用方代码
- 测试文件
- 项目的架构规则和设计文档（如果存在）

## Step 2: 逐项分析

对报告中的每个问题，独立判断：

1. **问题是否真实存在？** — 引用代码是否与当前一致？在项目实际运行路径中会被触发吗？
2. **严重程度是否准确？** — 是运行时错误还是可读性改进？
3. **修复建议是否合理？** — 是否引入不必要的复杂度？有更简洁的方案吗？

## 输出格式

对每个问题给出：
- 问题真实性判断（附代码证据）
- 独立的严重程度评估
- 采纳建议：采纳 / 部分采纳 / 不采纳
- 如采纳，给出最合适的修复方式

## 输出行为

**从 review-loop 调用时**（`$ARGUMENTS` 已提供 session ID）：
1. 将完整结论保存至 `.review-loop/$ARGUMENTS/round-{N}-verdict.md`（N 与 review 轮次一致）
2. 仅向主对话返回：
   ```
   验证完成：采纳 {A} 个 | 部分采纳 {P} 个 | 不采纳 {R} 个 | 结论已保存 round-{N}-verdict.md
   ```

**独立使用时**（无 `$ARGUMENTS`）：直接在对话中输出完整结论。
