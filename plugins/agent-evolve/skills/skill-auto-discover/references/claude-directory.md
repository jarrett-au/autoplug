# 探索 .claude 目录

> 来源：<https://code.claude.com/docs/zh-CN/claude-directory>

## 目录结构概览

```
.claude/
├── settings.json          # 项目设置（提交到版本控制）
├── settings.local.json    # 个人项目设置（不提交）
├── commands/              # 自定义斜杠命令
│   └── review.md
├── skills/                # 项目 Skills
│   └── deploy/
│       └── SKILL.md
├── agents/                # 项目 Subagents
│   └── code-reviewer.md
└── rules/                 # 路径限定规则
    └── api/
        └── _parent_.md

~/.claude/
├── settings.json          # 全局用户设置
├── skills/                # 个人 Skills
├── agents/                # 个人 Agents
├── commands/              # 个人命令
├── rules/                 # 个人规则
├── teams/                 # Agent teams 配置
│   └── {team-name}/config.json
└── tasks/                 # 团队任务列表
    └── {team-name}/
```

## 关键文件用途

| 文件 | 作用 | 何时加载 |
|------|------|----------|
| `settings.json` | 项目/全局设置（hooks、权限等） | 会话启动 |
| `settings.local.json` | 个人本地覆盖 | 会话启动 |
| `commands/*.md` | `/command` 自定义命令 | 用户调用时 |
| `skills/*/SKILL.md` | 可复用知识和工作流 | 会话启动（描述）+ 调用时（全文） |
| `agents/*.md` | Subagent 定义 | 生成时 |
| `rules/**/*.md` | 路径限定规则 | 匹配文件被读取时 |

## 加载时机

- **会话启动**：settings.json、CLAUDE.md、skill 描述、MCP 工具名
- **文件读取时**：路径限定规则自动加载
- **工具调用时**：skill 全文、subagent 定义
- **事件触发时**：hooks 作为外部脚本运行

## 选择正确的文件

| 你想做什么 | 使用什么 |
|-----------|---------|
| 持久项目约定 | `CLAUDE.md` |
| 可复用工作流 | `skills/*/SKILL.md` |
| 自动化检查 | `hooks`（在 settings.json 中） |
| 外部服务连接 | `MCP`（.mcp.json） |
| 按需参考资料 | `skills`（设置 `disable-model-invocation: true`） |
| 文件夹限定规则 | `.claude/rules/<path>/_parent_.md` |

## MCP 配置位置

| 范围 | 位置 | 共享方式 |
|------|------|---------|
| 本地 | `~/.claude.json`（按项目路径） | 仅自己 |
| 项目 | `.mcp.json`（项目根目录） | 团队共享（提交到版本控制） |
| 用户 | `~/.claude.json`（全局 mcpServers） | 跨项目 |

## 插件目录结构

```
.claude-plugin/
├── plugin.json            # 清单文件
├── skills/                # 插件 skills（命名空间）
├── agents/                # 插件 subagents
├── commands/              # 插件命令
├── hooks/
│   └── hooks.json         # 插件 hooks
├── .mcp.json              # 插件 MCP 服务器
└── servers/               # MCP 服务器二进制
```

## 关键原则

1. **优先级**：本地 > 项目 > 用户 > 托管（settings、MCP、skills）
2. **累加**：CLAUDE.md 和 hooks 在所有级别累加
3. **覆盖**：同名 skills/agents/MCP 按优先级覆盖
4. **命名空间**：插件 skills 自动加前缀 `/plugin-name:skill`
5. **`_parent_.md`**：规则文件用下划线前缀避免被直接匹配
