---
name: code-reviewer
description: >
  深度代码审查 subagent。在独立 context 中执行审查，大量读取代码上下文，
  产出完整审查报告并保存至文件，仅返回摘要至主对话。
tools:
  - Read
  - Grep
  - Glob
  - Bash
model: sonnet
permissionMode: auto
color: yellow
---
