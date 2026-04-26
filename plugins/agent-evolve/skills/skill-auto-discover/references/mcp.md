# MCP (Model Context Protocol)

> 来源：<https://code.claude.com/docs/zh-CN/mcp>

## 概述

MCP 是 AI 工具集成的开源标准，让 Claude Code 连接外部工具和数据源（数据库、API、服务）。

## 安装三种方式

### 远程 HTTP（推荐）
```bash
claude mcp add --transport http <name> <url>
# 示例
claude mcp add --transport http notion https://mcp.notion.com/mcp
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### 远程 SSE（已弃用）
```bash
claude mcp add --transport sse <name> <url>
```

### 本地 stdio
```bash
claude mcp add --transport stdio --env KEY=value <name> -- <command> [args...]
# 示例
claude mcp add --transport stdio --env AIRTABLE_API_KEY=YOUR_KEY airtable \
  -- npx -y airtable-mcp-server
```

**重要**：所有选项在服务器名之前，`--` 分隔名与命令。

## 管理

```bash
claude mcp list                    # 列出所有
claude mcp get <name>              # 详情
claude mcp remove <name>           # 删除
/mcp                               # 在 Claude Code 中检查状态
```

## 安装范围

| 范围 | 存储位置 | 共享 |
|------|---------|------|
| local（默认） | `~/.claude.json`（按项目路径） | 仅自己 |
| project | 项目根 `.mcp.json` | 团队（提交版本控制） |
| user | `~/.claude.json`（全局） | 跨项目 |

**优先级**：本地 > 项目 > 用户

## .mcp.json 格式

```json
{
  "mcpServers": {
    "server-name": {
      "command": "/path/to/server",
      "args": [],
      "env": {}
    }
  }
}
```

## 环境变量扩展

`.mcp.json` 中支持 `${ENV_VAR}` 语法。插件的特殊变量：
- `${CLAUDE_PLUGIN_ROOT}`：插件根目录
- `${CLAUDE_PLUGIN_DATA}`：持久数据目录

## 插件提供的 MCP

插件可通过 `.mcp.json` 或 `plugin.json` 的 `mcpServers` 字段捆绑 MCP 服务器。启用插件时自动连接。

## 动态工具更新

支持 `list_changed` 通知，服务器可动态更新工具/提示/资源，无需重连。

## 频道推送

MCP 服务器可声明 `claude/channel` 功能，推送消息到会话。启用方式：启动时加 `--channels` 标志。

## 高级配置

- **OAuth**：`/mcp` 命令进行身份验证
- **超时**：`MCP_TIMEOUT=10000` 环境变量（毫秒）
- **输出限制**：默认 10,000 token 警告，`MAX_MCP_OUTPUT_TOKENS=50000` 调整
- **Windows**：npx 需 `cmd /c` 包装器

## 安全提示

使用第三方 MCP 服务器需自担风险。获取不受信任内容的 MCP 服务器可能导致提示注入风险。

## 托管 MCP 配置

组织可通过系统目录的 `managed-mcp.json` 控制 MCP 配置：
- 独占控制模式
- 基于策略的允许/拒绝列表
- 支持基于命令和 URL 的限制
