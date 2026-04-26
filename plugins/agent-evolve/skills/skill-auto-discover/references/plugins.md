# Claude Code Plugins 参考

来源：https://code.claude.com/docs/zh-CN/plugins

## 概述

Plugins 让你使用自定义功能扩展 Claude Code，这些功能可以在项目和团队中共享。

## 何时使用插件 vs 独立配置

| 方法 | Skill 名称 | 最适合 |
|------|-----------|--------|
| 独立（`.claude/`） | `/hello` | 个人工作流、项目特定、快速实验 |
| 插件（`.claude-plugin/plugin.json`） | `/plugin-name:hello` | 团队共享、社区分发、版本控制、跨项目重用 |

## 插件目录结构

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # 清单（唯一必须在 .claude-plugin 内的文件）
├── skills/                   # Agent Skills（<name>/SKILL.md）
├── agents/                   # 自定义 agent 定义
├── hooks/                    # hooks.json 事件处理程序
├── monitors/                 # monitors.json 后台监视器
├── commands/                 # 平面 Markdown 文件（旧格式，新插件用 skills/）
├── bin/                      # 添加到 Bash PATH 的可执行文件
├── .mcp.json                 # MCP server 配置
├── .lsp.json                 # LSP server 配置
└── settings.json             # 默认设置
```

⚠️ **常见错误**：不要将 skills/、agents/、hooks/ 放在 `.claude-plugin/` 内。只有 plugin.json 在其中。

## plugin.json 清单

```json
{
  "name": "my-plugin",
  "description": "插件描述",
  "version": "1.0.0",
  "author": {
    "name": "Your Name"
  },
  "homepage": "https://...",
  "repository": "https://...",
  "license": "MIT"
}
```

| 字段 | 用途 |
|------|------|
| `name` | 唯一标识符 + skill 命名空间 |
| `description` | 插件管理器显示 |
| `version` | 语义版本控制 |
| `author` | 归属（可选） |
| `settings` | 默认设置（优先于 plugin.json） |

## LSP Servers

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": { ".go": "go" }
  }
}
```

用户需自行安装语言服务器二进制文件。

## 后台监视器

```json
[
  {
    "name": "error-log",
    "command": "tail -F ./logs/error.log",
    "description": "Application error log"
  }
]
```

stdout 每行作为通知传递给 Claude。支持 `when` 触发器和变量替换。

## 默认设置

```json
{
  "agent": "security-reviewer"
}
```

`agent` 键激活自定义 agent 作为主线程。来自 settings.json 的设置优先于 plugin.json 声明。

## 测试与调试

```bash
claude --plugin-dir ./my-plugin
```

- 更改后运行 `/reload-plugins` 重新加载
- 多个插件：`claude --plugin-dir ./a --plugin-dir ./b`
- `--plugin-dir` 优先于已安装的同名市场插件

## 从独立配置迁移

1. 创建插件目录和 plugin.json
2. 复制 skills/agents
3. 迁移 hooks（settings.json → hooks/hooks.json）
4. 用 `--plugin-dir` 测试
5. 删除 .claude/ 原始文件避免重复

## 提交市场

- Claude.ai：`claude.ai/settings/plugins/submit`
- Console：`platform.claude.com/plugins/submit`

## Plugin 安全限制

- Plugin subagents 不支持 hooks、mcpServers、permissionMode frontmatter 字段
- 需要这些功能时，将 agent 文件复制到 .claude/agents/ 或 ~/.claude/agents/
