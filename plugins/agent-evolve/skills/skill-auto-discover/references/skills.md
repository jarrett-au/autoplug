# Claude Code Skills 参考

来源：https://code.claude.com/docs/zh-CN/skills

## 概述

Skills 扩展 Claude 能做的事情。创建 `SKILL.md` 文件，Claude 在相关时自动使用，或通过 `/skill-name` 直接调用。

**何时创建 Skill**：
- 不断将相同的剧本、检查清单或多步骤程序粘贴到聊天中
- CLAUDE.md 的一部分已演变成程序而不是事实

Skills 与 CLAUDE.md 的区别：skill 正文仅在使用时加载，长参考资料几乎不花费上下文成本。

Skills 遵循 [Agent Skills](https://agentskills.io) 开放标准。

## Skill 位置

| 位置 | 路径 | 适用于 |
|------|------|--------|
| 企业 | 托管设置 | 组织中所有用户 |
| 个人 | `~/.claude/skills/<name>/SKILL.md` | 所有项目 |
| 项目 | `.claude/skills/<name>/SKILL.md` | 仅此项目 |
| 插件 | `<plugin>/skills/<name>/SKILL.md` | 启用插件的位置 |

优先级：企业 > 个人 > 项目。插件 skills 使用 `plugin-name:skill-name` 命名空间。

## 目录结构

```
my-skill/
├── SKILL.md           # 主要说明（必需）
├── template.md        # Claude 要填写的模板
├── examples/
│   └── sample.md      # 示例输出
└── scripts/
    └── validate.sh    # Claude 可执行的脚本
```

## Frontmatter 参考

所有字段可选，推荐 `description`：

| 字段 | 描述 |
|------|------|
| `name` | 显示名称，仅小写/数字/连字符，最多 64 字符 |
| `description` | 功能描述，Claude 据此决定何时使用 |
| `when_to_use` | 额外触发上下文，触发短语或示例请求 |
| `argument-hint` | 自动完成提示，如 `[issue-number]` |
| `arguments` | 命名参数列表，用于 `$name` 替换 |
| `disable-model-invocation` | `true` 阻止 Claude 自动调用 |
| `user-invocable` | `false` 从 `/` 菜单隐藏 |
| `allowed-tools` | 活跃时免权限工具列表 |
| `model` | 覆盖模型（单轮，不保存设置） |
| `effort` | 工作量级别：low/medium/high/xhigh/max |
| `context` | 设为 `fork` 在 subagent 中运行 |
| `agent` | `context: fork` 时使用的 subagent 类型 |
| `hooks` | 限定于 skill 生命周期的 hooks |
| `paths` | Glob 模式限制自动加载时机 |
| `shell` | `bash`（默认）或 `powershell` |

## 字符串替换

| 变量 | 描述 |
|------|------|
| `$ARGUMENTS` | 所有参数 |
| `$ARGUMENTS[N]` | 第 N 个参数（0 基） |
| `$N` | `$ARGUMENTS[N]` 简写 |
| `$name` | `arguments` 中声明的命名参数 |
| `${CLAUDE_SESSION_ID}` | 当前会话 ID |
| `${CLAUDE_SKILL_DIR}` | Skill 目录路径 |

## 动态上下文注入

`` !`<command>` `` 语法在发送给 Claude 前运行 shell 命令，输出替换占位符：

```markdown
- PR diff: !`gh pr diff`
- Changed files: !`gh pr diff --name-only`
```

多行命令用 ```` !` 开头的围栏代码块。

## 调用控制

| Frontmatter | 用户可调用 | Claude 可调用 | 描述加载 |
|-------------|-----------|---------------|----------|
| （默认） | 是 | 是 | 始终加载 |
| `disable-model-invocation: true` | 是 | 否 | 调用时加载 |
| `user-invocable: false` | 否 | 是 | 始终加载 |

## 在 Subagent 中运行

设置 `context: fork`，skill 内容变成 subagent 的任务提示：

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---
```

`agent` 可选内置（Explore、Plan、general-purpose）或自定义 subagent。

## 内容生命周期

- 调用后作为单条消息进入对话，会话剩余部分保持
- 自动压缩在 token 预算内转发，保留前 5,000 token
- 重附 skills 共享 25,000 token 预算

## 预先批准工具

```yaml
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
```

仅授予列出的工具免权限访问，不限制其他工具可用性。

## 权限控制

```json
// 禁用所有 skills
{"deny": ["Skill"]}

// 允许/拒绝特定
{"allow": ["Skill(commit)", "Skill(review-pr *)"]}
```

## 支持 Skill 内容中的 "ultrathink"

在 skill 内容任何位置包含单词 `ultrathink` 即可启用扩展思考。

## 禁用 Shell 执行

设置 `"disableSkillShellExecution": true` 可禁用 `!`command`` 执行（捆绑和托管 skills 除外）。

## 描述截断

- 组合 description + when_to_use 截断为 1,536 字符
- 可设置 `SLASH_COMMAND_TOOL_CHAR_BUDGET` 环境变量提高限制
- 前置关键用例（开头最易保留）
