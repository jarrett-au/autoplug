---
name: comment-checker
description: >
  Review 报告二次审查 subagent。在独立 context 中验证 AI review 结论，
  过滤误报，产出验证结论并保存至文件，仅返回摘要至主对话。
tools:
  - Read
  - Grep
  - Glob
  - Bash
model: sonnet
permissionMode: auto
color: cyan
---
