# Claude Code Hooks 参考

来源：https://code.claude.com/docs/zh-CN/hooks

## 概述

Hooks 是用户定义的 shell 命令、HTTP 端点、LLM 提示或代理，在 Claude Code 生命周期中的特定点自动执行。

## Hook 生命周期

Hooks 在会话期间特定点触发，分三种频率：
- **每个会话一次**：SessionStart、SessionEnd
- **每轮一次**：UserPromptSubmit、Stop、StopFailure
- **每次工具调用**：PreToolUse、PostToolUse

## Hook 事件一览

| 事件 | 触发时机 | 可阻止？ |
|------|----------|----------|
| SessionStart | 会话开始或恢复 | 否 |
| InstructionsLoaded | CLAUDE.md/rules 文件加载时 | 否 |
| UserPromptSubmit | 用户提交提示时 | 是 |
| UserPromptExpansion | 命令扩展为提示时 | 是 |
| PreToolUse | 工具调用执行前 | 是 |
| PermissionRequest | 权限对话框出现时 | 是 |
| PermissionDenied | 工具调用被 auto mode 拒绝时 | 否（可用 retry: true） |
| PostToolUse | 工具调用成功后 | 否 |
| PostToolUseFailure | 工具调用失败后 | 否 |
| Notification | 通知发送时 | 否 |
| SubagentStart | Subagent 生成时 | 否 |
| SubagentStop | Subagent 完成时 | 是 |
| Stop | Claude 完成响应时 | 是 |
| StopFailure | API 错误导致轮次结束 | 否 |
| ConfigChange | 配置文件变更时 | 是 |
| CwdChanged | 工作目录变更时 | 否 |
| FileChanged | 监视文件变更时 | 否 |
| TaskCreated | 任务创建时 | 是 |
| TaskCompleted | 任务完成时 | 是 |
| PreCompact | 上下文压缩前 | 是 |
| PostCompact | 上下文压缩后 | 否 |
| SessionEnd | 会话终止时 | 否 |

## 配置结构（三级嵌套）

```json
{
  "hooks": {
    "<HookEvent>": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm *)",
            "command": "path/to/script.sh",
            "timeout": 600,
            "async": false,
            "once": false
          }
        ]
      }
    ]
  }
}
```

## Hook 位置

| 位置 | 范围 | 可共享 |
|------|------|--------|
| `~/.claude/settings.json` | 所有项目 | 否 |
| `.claude/settings.json` | 单个项目 | 是 |
| `.claude/settings.local.json` | 单个项目 | 否 |
| 托管策略设置 | 组织范围 | 是 |
| `Plugin hooks/hooks.json` | 启用插件时 | 是 |
| Skill/Agent frontmatter | 组件活跃时 | 是 |

## 匹配器模式

| 匹配器值 | 评估方式 | 示例 |
|----------|----------|------|
| `"*"`、`""` 或省略 | 匹配所有 | 每次触发 |
| 仅字母/数字/_/`|` | 精确字符串或列表 | `Bash`、`Edit\|Write` |
| 含其他字符 | JavaScript 正则 | `^Notebook`、`mcp__memory__.*` |

## Hook 处理程序类型

### 1. 命令 Hooks (`type: "command"`)
通过 stdin 接收 JSON，通过退出代码和 stdout 返回结果。

**退出代码**：
- `0`：成功，解析 stdout JSON
- `2`：阻止错误，stderr 反馈给 Claude
- 其他：非阻止错误

**JSON 输出关键字段**：
- `continue: false`：完全停止 Claude
- `stopReason`：停止原因（显示给用户）
- `systemMessage`：警告消息
- `decision: "block"`：阻止操作
- `hookSpecificOutput`：事件特定控制

### 2. HTTP Hooks (`type: "http"`)
JSON 作为 POST 请求体发送，响应体使用与命令 hooks 相同格式。
- 2xx：成功
- 非 2xx：非阻止错误

### 3. 提示 Hooks (`type: "prompt"`)
向 Claude 模型发送提示，返回 yes/no 决定。
- `prompt`：提示文本，`$ARGUMENTS` 作为输入占位符
- `model`：使用的模型（默认快速模型）

### 4. 代理 Hooks (`type: "agent"`，实验性)
生成 subagent 验证条件后返回决定。

## if 条件字段

使用权限规则语法：`"Bash(git *)"`、`"Edit(*.ts)"`。
仅对工具事件评估（PreToolUse、PostToolUse、PostToolUseFailure、PermissionRequest）。

## MCP 工具匹配

MCP 工具命名模式：`mcp__<server>__<tool>`
- `mcp__memory__.*`：匹配 memory 服务器所有工具
- `mcp__.*__write.*`：匹配任何服务器的写操作

## 环境变量引用

- `$CLAUDE_PROJECT_DIR`：项目根目录
- `${CLAUDE_PLUGIN_ROOT}`：插件安装目录
- `${CLAUDE_PLUGIN_DATA}`：插件持久数据目录

## Skills 和 Agents 中的 Hooks

直接在 frontmatter 中定义：
```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
```

## 决定控制速查

| 事件 | 决定模式 | 关键字段 |
|------|----------|----------|
| PreToolUse | hookSpecificOutput | `permissionDecision` (allow/deny/ask/defer) |
| PermissionRequest | hookSpecificOutput | `decision.behavior` (allow/deny) |
| PermissionDenied | hookSpecificOutput | `retry: true` |
| UserPromptSubmit/Stop | 顶级 decision | `decision: "block"`, `reason` |
| WorktreeCreate | 路径返回 | stdout 路径或 `hookSpecificOutput.worktreePath` |
| Elicitation | hookSpecificOutput | `action` (accept/decline/cancel) |

## 禁用 Hooks

- 移除 hook 条目
- 设置 `"disableAllHooks": true`（临时禁用所有）
