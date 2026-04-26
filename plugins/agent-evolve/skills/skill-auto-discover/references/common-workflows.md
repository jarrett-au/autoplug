# 常见工作流程

> 来源：<https://code.claude.com/docs/zh-CN/common-workflows>

## 理解新代码库

```bash
claude  # 在项目根目录
```
```
give me an overview of this codebase
explain the main architecture patterns
what are the key data models?
how is authentication handled?
```
> 从广到窄，用项目领域语言提问。安装代码智能插件获得精确导航。

## 查找相关代码

```
find the files that handle user authentication
how do these authentication files work together?
trace the login process from front-end to database
```

## 高效修复错误

```
I'm seeing an error when I run npm test
suggest a few ways to fix the @ts-ignore in user.ts
update user.ts to add the null check
```
> 提供重现命令和堆栈跟踪。注明是间歇性还是持续性。

## 重构代码

```
find deprecated API usage in our codebase
suggest how to refactor utils.js to use modern JavaScript features
refactor utils.js to use ES2024 features while maintaining the same behavior
run tests for the refactored code
```
> 小步可测试增量。要求保持向后兼容。

## 使用 Subagents

```bash
/agents  # 查看和创建 subagents
```
```
review my recent code changes for security issues
use the code-reviewer subagent to check the auth module
```
> 限制工具访问为实际需要。`description` 字段决定自动委派触发。

## Plan Mode

**切换**：Shift+Tab 循环 Normal → Auto-Accept → Plan

**何时使用**：多文件编辑、代码探索、交互式方向迭代

```bash
claude --permission-mode plan            # Plan Mode 启动
claude --permission-mode plan -p "..."   # 无头 Plan Mode
```

**默认配置**：
```json
{ "permissions": { "defaultMode": "plan" } }
```

> Ctrl+G 在编辑器中打开计划。接受计划后自动命名会话。

## 测试工作流

```
find functions in NotificationsService.swift not covered by tests
add tests for the notification service
add test cases for edge conditions
run the new tests and fix any failures
```
> Claude 匹配现有测试风格和框架。要求识别遗漏的边界情况。

## PR 工作流

```
summarize the changes I've made to the authentication module
create a pr
enhance the PR description with more context
```
> `gh pr create` 自动链接会话到 PR。`claude --from-pr 123` 恢复。

## 引用文件和目录

```
@src/utils/auth.js          # 文件内容
@src/components?            # 目录列表
@github:repos/owner/repo/issues  # MCP 资源
```

## Thinking Mode（扩展思考）

**默认启用**。Ctrl+O 切换详细模式查看推理过程。

| 配置 | 方式 |
|------|------|
| 努力级别 | `/effort` 或 `CLAUDE_CODE_EFFORT_LEVEL` |
| ultrathink | 提示中包含 "ultrathink" |
| 切换开关 | Option+T / Alt+T |
| 全局默认 | `/config` → `alwaysThinkingEnabled` |
| 令牌上限 | `MAX_THINKING_TOKENS` 环境变量 |

> "think"、"think hard" 是常规指令，不分配思考令牌。

## 会话管理

```bash
claude --continue              # 恢复最近对话
claude --resume                # 打开选择器
claude --resume auth-refactor  # 按名称恢复
claude --from-pr 123           # 恢复 PR 关联会话
claude -n feature-name         # 启动时命名
/rename feature-name           # 会话中重命名
```

**选择器快捷键**：↑↓导航、Enter选择、Space预览、Ctrl+R重命名、/搜索、Ctrl+A所有项目、Ctrl+W所有worktree、Ctrl+B当前分支

## Git Worktrees 并行

```bash
claude --worktree feature-auth   # 创建隔离 worktree + 分支
claude --worktree                # 自动命名
```

- 存储在 `.claude/worktrees/<name>/`
- 分支命名 `worktree-<name>`
- 无更改退出时自动清理；有更改提示保留/删除
- `.worktreeinclude` 文件（.gitignore 语法）自动复制 gitignored 文件
- Subagent 可配置 `isolation: worktree` 实现隔离

## 通知 Hook

```json
{
  "hooks": {
    "Notification": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "osascript -e 'display notification \"Claude needs attention\" with title \"Claude Code\"'"
      }]
    }]
  }
}
```

| matcher | 触发时机 |
|---------|---------|
| `permission_prompt` | 需要批准 |
| `idle_prompt` | 完成等待 |
| `auth_success` | 认证完成 |
| `elicitation_dialog` | 在提问 |

## 非交互 / 管道 / 自动化

```bash
# 管道
cat error.log | claude -p 'explain root cause' > output.txt

# 输出格式
claude -p "..." --output-format text|json|stream-json

# 作为 linter
claude -p 'review changes vs main for typos. filename:line, description.'
```

## 定时任务

| 选项 | 运行位置 | 适合 |
|------|---------|------|
| Routines | Anthropic 基础设施 | 机器关机也需运行的任务 |
| 桌面计划任务 | 本机 | 需访问本地文件/未提交更改 |
| GitHub Actions | CI 管道 | 仓库事件相关 |
| /loop | 当前 CLI | 快速轮询，新对话停止 |
