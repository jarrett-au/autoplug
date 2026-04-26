# 上下文窗口管理

> 来源：<https://code.claude.com/docs/en/context-window>

## 核心概念

Claude Code 的上下文窗口保存会话中所有信息：指令、文件内容、输出、CLAUDE.md、记忆、skills 和系统说明。

## 会话加载顺序

1. **你输入之前**（静默加载）：
   - System prompt + output style
   - CLAUDE.md（项目根 + 上级目录）
   - Auto memory（MEMORY.md）
   - MCP 工具名（仅名称，定义延迟加载）
   - Skill 描述

2. **Claude 工作时**：
   - 文件读取 → 上下文增长
   - 路径限定规则 → 随匹配文件自动加载
   - PostToolUse hook → 编辑后触发

3. **使用 subagent**：
   - 独立上下文窗口，不影响主对话
   - 仅返回摘要 + 元数据

4. **compaction（/compact）**：
   - 对话历史压缩为结构化摘要
   - 大部分启动内容自动重载

## Compaction 后各机制表现

| 机制 | compaction 后 |
|------|--------------|
| System prompt + output style | **不变**（非消息历史） |
| 项目根 CLAUDE.md + 无路径规则 | **从磁盘重注入** |
| Auto memory | **从磁盘重注入** |
| 有路径的规则（frontmatter） | **丢失**，直到匹配文件再次被读取 |
| 子目录 CLAUDE.md | **丢失**，直到该子目录文件被读取 |
| 已调用 skill 内容 | **重注入**，上限 5000 tok/skill、25000 tok 总计；超出截断开头 |
| Hooks | **不适用**（代码执行，非上下文） |

## 关键要点

- **Skill 截断策略**：保持开头内容。最重要的指令放在 SKILL.md 顶部。
- **持久规则**：必须放在项目根 CLAUDE.md 中（不受 compaction 影响）。
- **诊断命令**：`/context` 查看上下文分布；`/memory` 检查启动加载内容。
- **MCP 工具**：默认延迟加载，仅工具名消耗上下文。

## 上下文优化建议

1. CLAUDE.md 控制在 200 行以下
2. 参考材料放入 skills（按需加载）
3. 不常用的 skill 设置 `disable-model-invocation: true`
4. 大型研究任务用 subagent 隔离
5. 用 `/compact focus on ...` 控制压缩保留内容
6. 用 `/context` 检查各项占用
