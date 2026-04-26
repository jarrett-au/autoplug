# Claude Code 权限系统

来源：https://code.claude.com/docs/zh-CN/permissions

## 权限模式

| 模式 | 说明 |
|------|------|
| `default` | 标准权限检查，带有提示 |
| `acceptEdits` | 自动接受文件编辑和工作目录或 additionalDirectories 中路径的常见文件系统命令 |
| `plan` | Plan mode（只读探索） |
| `auto` | Auto mode：后台分类器审查命令和受保护目录的写入 |
| `dontAsk` | 自动拒绝权限提示（显式允许的工具仍然工作） |
| `bypassPermissions` | 跳过权限提示（仅隔离环境） |

## 规则语法

- `Tool` 匹配全部工具调用
- `Tool(specifier)` 细粒度控制特定工具
- 支持 `*` 通配符

### 通配符细节

- `Bash(ls *)` 有单词边界（不匹配 lsof）
- `Bash(ls*)` 无边界（匹配两者）
- `:*` 等同于尾部 `*`

### 复合命令

识别 `&&`、`||`、`;`、`|`、`|&`、`&` 和换行符，每个子命令需独立匹配规则。

### 进程包装器

自动剥离 `timeout`、`time`、`nice`、`nohup`。

### 只读命令

`Bash(readonly:*)` 匹配 cat/head/tail/grep/find/wc/ls/which/pwd/echo/printf/git status/git diff/git log。

### MCP 权限

`MCP(server:tool)` 语法，例如 `MCP(memory__create_entities)`。

### Hooks 扩展权限

PreToolUse hook 可返回 `decide:allow` / `decide:deny` / `decide:ask`。

### 沙箱交互

- `sandbox.filesystem.allowRead`
- `sandbox.network.allowManagedDomainsOnly`

### 托管设置

- `disableBypassPermissionsMode`：禁用绕过权限模式
- `disableAutoMode`：禁用自动模式

## 设置优先级

托管 > CLI > 本地项目(.claude/settings.local.json) > 共享项目(.claude/settings.json) > 用户(~/.claude/settings.json)

**deny 始终优先于 allow**。

## Skill 权限控制

```json
// 拒绝所有 skills
{"permissions": {"deny": ["Skill"]}}

// 允许特定 skills
{"permissions": {"allow": ["Skill(commit)", "Skill(review-pr *)"]}}

// 拒绝特定 skills
{"permissions": {"deny": ["Skill(deploy *)"]}}
```

语法：`Skill(name)` 精确匹配，`Skill(name *)` 前缀匹配。

## Agent 权限控制

```json
{"permissions": {"deny": ["Agent(Explore)", "Agent(my-custom-agent)"]}}
```
