# Claude Code Subagents 参考

来源：https://code.claude.com/docs/zh-CN/sub-agents

## 概述

Subagents 是处理特定类型任务的专门 AI 助手。在自己的 context window 中运行，具有自定义系统提示、特定工具访问和独立权限。仅返回摘要到主对话。

**核心价值**：保留主对话上下文、强制约束、跨项目复用、降低成本。

## 内置 Subagents

| 名称 | 模型 | 工具 | 用途 |
|------|------|------|------|
| Explore | Haiku | 只读 | 文件发现、代码搜索、代码库探索 |
| Plan | — | 只读 | 规划分析 |
| General-purpose | — | 全部 | 通用任务 |

Explore 支持彻底程度级别：quick、medium、very thorough。

## 配置位置

| 位置 | 范围 | 优先级 |
|------|------|--------|
| 托管设置 | 组织 | 1（最高） |
| `--agents` CLI 标志 | 当前会话 | 2 |
| `.claude/agents/` | 当前项目 | 3 |
| `~/.claude/agents/` | 所有项目 | 4 |
| Plugin `agents/` | 启用插件 | 5（最低） |

同名 subagent：高优先级位置获胜。

## Frontmatter 字段

| 字段 | 必需 | 描述 |
|------|------|------|
| `name` | ✅ | 小写字母+连字符 |
| `description` | ✅ | Claude 据此决定何时委托 |
| `tools` | ❌ | 允许列表（省略则继承全部） |
| `disallowedTools` | ❌ | 拒绝列表 |
| `model` | ❌ | sonnet/opus/haiku/完整 ID/inherit |
| `permissionMode` | ❌ | default/acceptEdits/auto/dontAsk/bypassPermissions/plan |
| `maxTurns` | ❌ | 最大轮数 |
| `skills` | ❌ | 启动时加载的 skills（注入内容） |
| `mcpServers` | ❌ | 可用 MCP servers |
| `hooks` | ❌ | 生命周期 hooks |
| `memory` | ❌ | 持久内存：user/project/local |
| `background` | ❌ | 始终后台运行 |
| `effort` | ❌ | low/medium/high/xhigh/max |
| `isolation` | ❌ | `worktree` 隔离 git 副本 |
| `color` | ❌ | 显示颜色 |
| `initialPrompt` | ❌ | 作为主会话时自动提交的首轮提示 |

## 工具控制

```yaml
# 允许列表
tools: Read, Grep, Glob, Bash

# 拒绝列表
disallowedTools: Write, Edit

# 限制可生成的 subagent 类型
tools: Agent(worker, researcher), Read, Bash
```

`tools` 和 `disallowedTools` 同时设置时：先应用 disallowedTools，再针对剩余池解析 tools。

## MCP Server 绑定

```yaml
mcpServers:
  - playwright:           # 内联定义
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  - github                # 引用已配置服务器
```

内联定义对 subagent 专属，不会出现在主对话上下文中。

## 权限模式

| 父级模式 | Subagent 可覆盖？ |
|----------|-------------------|
| bypassPermissions | ❌ 优先，无法覆盖 |
| acceptEdits | ❌ 优先，无法覆盖 |
| auto | ❌ 继承 auto，忽略 frontmatter |
| 其他 | ✅ 可覆盖 |

## 持久内存

```yaml
memory: user    # ~/.claude/agent-memory/<name>/
# memory: project  # .claude/agent-memory/<name>/
# memory: local    # .claude/agent-memory-local/<name>/
```

启用后：自动启用 Read/Write/Edit，注入 MEMORY.md 前 200 行/25KB。

## 调用方式

| 方式 | 语法 | 保证执行？ |
|------|------|-----------|
| 自然语言 | "use the code-reviewer" | Claude 决定 |
| @-mention | `@code-reviewer` | ✅ |
| 会话范围 | `claude --agent name` | ✅ |
| 设置默认 | `"agent": "name"` in settings.json | ✅ |

## 前台 vs 后台

- **前台**：阻塞主对话，权限提示传递给用户
- **后台**：并发运行，启动前预批权限，未预批则自动拒绝
- `Ctrl+B` 将运行中任务放后台
- `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` 禁用

## 常见模式

1. **隔离高容量操作**：测试、文档、日志处理
2. **并行研究**：多 subagent 独立探索
3. **链接 subagents**：多步骤顺序工作流
4. **上下文复用**：恢复 subagent 保留完整对话历史

## Subagent vs Skill 选择

| 用主对话 | 用 Subagent |
|----------|-------------|
| 频繁迭代 | 产生大量不需要的详细输出 |
| 多阶段共享上下文 | 强制工具/权限限制 |
| 低延迟重要 | 自包含可返回摘要 |

## CLI 定义（无文件）

```bash
claude --agents '{
  "reviewer": {
    "description": "...",
    "prompt": "...",
    "tools": ["Read", "Bash"],
    "model": "sonnet"
  }
}'
```

字段与文件 frontmatter 一一对应（`prompt` 等同于 markdown 正文）。

## 自动压缩

默认 ~95% 容量触发，可通过 `CLAUDE_AUTOCOMPRESS_PCT_OVERRIDE` 调整。
