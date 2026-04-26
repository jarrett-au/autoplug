# Agent Teams（协调多会话团队）

> 来源：<https://code.claude.com/docs/zh-CN/agent-teams>

## 概述

Agent teams 协调多个 Claude Code 实例作为团队工作，具有共享任务、代理间消息传递和集中管理。

**状态**：实验性功能（v2.1.32+），需手动启用。

## 启用

```json
// settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## 与 Subagent 比较

| 方面 | Subagent | Agent Team |
|------|----------|------------|
| Context | 独立，结果返回调用者 | 完全独立 |
| 通信 | 仅向主代理 | 队友间直接消息 |
| 协调 | 主代理管理 | 共享任务列表 + 自我协调 |
| 最适合 | 专注任务，只需结果 | 需讨论和协作的复杂工作 |
| 成本 | 较低 | 较高（每个队友独立实例） |

## 最佳用例

1. **研究和审查**：多队友同时调查不同方面，分享发现
2. **新模块/功能**：各自独立部分，互不干扰
3. **竞争假设调试**：并行测试理论，相互质疑
4. **跨层协调**：前端、后端、测试各由不同队友负责

## 架构

| 组件 | 角色 |
|------|------|
| Team lead | 主会话，创建团队、生成队友、协调工作 |
| Teammates | 独立 Claude Code 实例，各自处理任务 |
| Task list | 共享工作项（待处理/进行中/已完成） |
| Mailbox | 代理间消息系统 |

**存储位置**：
- 团队配置：`~/.claude/teams/{team-name}/config.json`
- 任务列表：`~/.claude/tasks/{team-name}/`

## 显示模式

| 模式 | 说明 | 要求 |
|------|------|------|
| in-process | 所有队友在主终端内，Shift+Down 切换 | 无 |
| split panes | 每人独立窗格，可同时查看 | tmux 或 iTerm2 |

配置：`~/.claude.json` 中 `teammateMode` 或 `claude --teammate-mode in-process`

## 控制团队

- **生成队友**：自然语言描述角色和任务
- **指定模型**：`Use Sonnet for each teammate`
- **计划审批**：`Require plan approval before they make any changes`
- **直接对话**：Shift+Down（in-process）或点击窗格（split）
- **任务分配**：负责人显式分配 / 队友自我认领
- **关闭队友**：`Ask the researcher to shut down`
- **清理**：`Clean up the team`（先关闭所有队友）

## 使用 Subagent 定义

队友可引用任何范围的 subagent 定义：
```
Spawn a teammate using the security-reviewer agent type to audit the auth module.
```

## Hook 事件

| 事件 | 触发时机 | 退出码 2 |
|------|---------|---------|
| TeammateIdle | 队友即将空闲 | 发送反馈，保持工作 |
| TaskCreated | 任务创建 | 阻止创建 |
| TaskCompleted | 任务完成 | 阻止完成 |

## Context 和通信

- 每个队友独立 context window
- 自动加载 CLAUDE.md、MCP servers、skills
- **不继承**负责人的对话历史
- 消息自动传递（message / broadcast）
- 空闲自动通知负责人

## 最佳实践

1. **3-5 个队友**起步，平衡并行与协调
2. **每人 5-6 个任务**，避免上下文切换
3. **避免文件冲突**：分解工作使每人拥有不同文件集
4. **给足够 context**：生成提示中包含任务细节
5. **从研究/审查开始**（新手友好）
6. **监控和指导**：检查进度，重定向方法
7. **任务大小适中**：自包含、可交付成果明确

## 权限

- 所有队友从负责人的权限模式开始
- 生成后可单独更改队友模式
- 生成时无法设置每队友模式

## 当前限制

- In-process 队友无会话恢复
- 任务状态可能滞后
- 每会话一个团队，无嵌套
- 负责人固定，不可转移
- VS Code 集成终端不支持 split panes
