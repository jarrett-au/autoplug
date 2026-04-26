# 扩展 Claude Code 功能总览

> 来源：<https://code.claude.com/docs/zh-CN/features-overview>

## 七大扩展机制

| 功能 | 作用 | 何时使用 |
|------|------|---------|
| CLAUDE.md | 每次加载的持久上下文 | 项目约定、"始终执行 X" |
| Skill | 说明、知识、工作流 | 可复用内容、可调用任务 |
| Subagent | 隔离执行上下文 | 上下文隔离、并行任务 |
| Agent teams | 多会话协调 | 并行研究、竞争假设调试 |
| MCP | 外部服务连接 | 数据库、API、浏览器 |
| Hook | 事件触发的确定性脚本 | 可预测自动化（不涉及 LLM） |
| Plugin | 打包分发层 | 团队共享、marketplace |

## 关键对比

### Skill vs Subagent

| 方面 | Skill | Subagent |
|------|-------|----------|
| 本质 | 可复用内容 | 隔离工作者 |
| 关键优势 | 上下文间共享 | 上下文隔离 |
| 最适合 | 参考资料、可调用工作流 | 大量文件读取、并行工作 |

- Skill 可以是**参考**（知识）或**操作**（工作流）
- Subagent 读取数十文件只返回摘要
- 可结合：subagent 预加载 skills；skill 用 `context: fork` 隔离运行

### Subagent vs Agent Team

| 方面 | Subagent | Agent Team |
|------|----------|------------|
| Context | 独立，结果返回调用者 | 完全独立 |
| 通信 | 仅向主代理 | 队友间直接消息 |
| 协调 | 主代理管理 | 共享任务列表 |
| 成本 | 较低 | 较高 |

## 上下文成本

| 功能 | 加载时机 | 上下文成本 |
|------|---------|-----------|
| CLAUDE.md | 会话开始 | 每请求（完整内容） |
| Skill | 开始（描述）+ 使用（全文） | 低（描述） |
| MCP | 会话开始 | 每请求（工具定义） |
| Subagent | 生成时 | 与主会话隔离 |
| Hook | 触发时 | 零（外部运行） |

**降低 Skill 成本**：设置 `disable-model-invocation: true`，上下文成本降为零。

## 功能分层优先级

- **CLAUDE.md**：累加（所有级别同时贡献）
- **Skills**：同名覆盖（托管 > 用户 > 项目）
- **MCP**：同名覆盖（本地 > 项目 > 用户）
- **Hooks**：合并（所有注册 hook 都触发）

## 常见组合模式

| 模式 | 示例 |
|------|------|
| Skill + MCP | MCP 连数据库，skill 记录架构和查询模式 |
| Skill + Subagent | `/audit` skill 启动安全性、性能、风格 subagents |
| CLAUDE.md + Skill | CLAUDE.md 说"遵循约定"，skill 包含完整指南 |
| Hook + MCP | 编辑后 hook 发 Slack 通知 |

## 最佳实践

1. CLAUDE.md 控制在 200 行以下
2. 参考材料放入 skills（按需加载）
3. 外部连接用 MCP
4. 大型研究用 subagent 隔离
5. 确定性自动化用 hook
6. 团队共享用 plugin 打包
