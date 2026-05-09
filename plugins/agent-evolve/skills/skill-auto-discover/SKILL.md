---
name: skill-auto-discover
description: 提取当前对话中的有价值知识点（最佳实践、解决流程），并自动创建或更新 Skill、Hook、Agent 或 Plugin 配置。
when_to_use: 当用户说"从这次对话中学习"、"提炼经验"、"更新skill"、"记录这个pattern"或明确要求从 session 中捕获知识时触发。
allowed-tools: Read, Edit, Write, Bash
---

# Skill/Ecosystem Refiner

从当前对话历史中提取有价值的知识点，并智能地创建或更新 Claude Code 生态组件（Skills、Agents、Hooks、Plugins）。

## 1. 知识提取与组件决策

首先全面回顾当前对话，提取知识并决定最佳载体：

### 1.1 Skill（最常用）
**适用场景**：常规最佳实践、多步骤任务流程、检查清单、专业领域知识。

| 位置 | 路径 | 适用范围 |
|------|------|----------|
| 个人 | `~/.claude/skills/<name>/SKILL.md` | 所有项目 |
| 项目 | `.claude/skills/<name>/SKILL.md` | 仅此项目 |

**判断依据**：
- 跨项目通用 → 个人 Skill
- 项目特有但可复用 → 项目 Skill
- 内容是程序/流程（不是纯事实）→ Skill（而非 CLAUDE.md）
- 长参考资料 → Skill（仅在调用时加载，零上下文成本）

### 1.2 Hook（强制卡点）
**适用场景**：必须拦截或自动执行的检查（如安全审计、格式校验）。

**作用域决策**：
- **组件级 Hook**（局部）：仅在特定 Skill/Agent 活跃时需要 → 写入 YAML frontmatter 的 `hooks` 字段，组件完成后自动清理。
- **项目级 Hook**（通用）：如"拦截任何 `rm -rf`" → 写入 `.claude/settings.json` 或 `.claude/settings.local.json`。
- **个人级 Hook**（全局）：适用于所有项目 → 写入 `~/.claude/settings.json`。

**Hook 事件速查**（参考 `references/hooks.md`）：
- `PreToolUse`：工具执行前（可阻止）
- `PostToolUse`：工具执行后
- `UserPromptSubmit`：用户提交提示时（可阻止）
- `Stop`：Claude 完成响应时（可阻止）
- `PermissionRequest`：权限请求时（可自定义决定）

**Hook 处理程序类型**：
- `command`：Shell 命令，stdin 接收 JSON，退出码 2 = 阻止
- `http`：HTTP POST 端点
- `prompt`：发送给 Claude 的提示验证
- `agent`：生成 subagent 验证（实验性）

### 1.3 Subagent（高容量/独立任务）
**适用场景**：包含繁杂日志分析、大范围代码探索、或需要不同工具权限/模型的任务。

| 位置 | 路径 | 适用范围 |
|------|------|----------|
| 个人 | `~/.claude/agents/<name>.md` | 所有项目 |
| 项目 | `.claude/agents/<name>.md` | 仅此项目 |

**Skill 中的 Subagent**：在 Skill frontmatter 设置 `context: fork` + `agent: <type>`。

**关键能力**：
- 独立 context window，仅返回摘要
- 可限制工具、权限模式、模型
- 支持持久内存（`memory: user/project/local`）
- 支持隔离 git worktree（`isolation: worktree`）

### 1.4 Plugin（团队共享）
**适用场景**：需要与团队共享、跨项目复用、版本控制的组件集合。

**从独立配置迁移**：
1. 创建 `.claude-plugin/plugin.json`
2. 复制 skills/agents/commands
3. 迁移 hooks（settings.json → `hooks/hooks.json`）
4. 用 `claude --plugin-dir` 测试
5. 删除 `.claude/` 原始文件避免重复

## 2. 变更前强制备份

在修改任何现存文件之前，**必须**压缩备份：

```bash
mkdir -p .claude/plugins-data/agent-evolve/backups
zip -r ".claude/plugins-data/agent-evolve/backups/<name>-$(date +%Y%m%d)-1.zip" SKILL.md reference/ 2>/dev/null || true
```

如果涉及多版本演进，可选创建 `CHANGES.md` 记录变更历史。

## 3. 组件生成规范

### 3.1 SKILL.md 格式

```yaml
---
name: skill-name                    # 小写+连字符，最多 64 字符
description: 简洁描述用途             # Claude 据此决定何时使用
when_to_use: 触发上下文/短语示例       # 可选，辅助触发判断
argument-hint: "[issue-number]"      # 可选，自动完成提示
arguments: [name, repo]              # 可选，命名参数
disable-model-invocation: false       # true 阻止自动调用
user-invocable: true                  # false 从 / 菜单隐藏
allowed-tools: Bash(git *) Read      # 免权限工具
context: fork                         # 在 subagent 中运行
agent: Explore                        # context:fork 时使用的 subagent
model: sonnet                         # 可选，覆盖模型
hooks:                                # 可选，限定 hooks
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/check.sh"
---
```

**动态参数**：`$ARGUMENTS`、`$ARGUMENTS[0]`、`$1`、`$name`、`${CLAUDE_SESSION_ID}`、`${CLAUDE_SKILL_DIR}`。

**动态上下文注入**：`` !`command` `` 语法，发送前运行并替换输出。

### 3.2 Subagent 文件格式

```yaml
---
name: code-reviewer
description: 何时使用此 subagent 的描述
tools: Read, Grep, Glob, Bash         # 允许列表
disallowedTools: Write, Edit          # 拒绝列表
model: sonnet                         # sonnet/opus/haiku/inherit
permissionMode: default               # default/acceptEdits/auto/dontAsk/bypassPermissions/plan
maxTurns: 50                          # 最大轮数
skills: [api-conventions]             # 预加载 skills
mcpServers:                           # MCP 绑定
  - github                            # 引用或内联定义
memory: project                       # user/project/local
background: false                     # 始终后台
isolation: worktree                   # git worktree 隔离
color: blue                           # 显示颜色
---
```

### 3.3 Hook 配置格式

```json
{
  "hooks": {
    "<HookEvent>": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "path/to/script.sh",
            "timeout": 600
          }
        ]
      }
    ]
  }
}
```

### 3.4 Plugin 清单格式

```json
{
  "name": "my-plugin",
  "description": "插件描述",
  "version": "1.0.0",
  "author": { "name": "Your Name" }
}
```

## 4. 参考文档

生成组件时，参考 `references/` 目录下的官方文档提炼：

**核心组件参考（第一批）**：
- `permissions.md` — 权限系统、allowed-tools 语法、沙箱隔离
- `hooks.md` — Hook 事件生命周期、处理程序类型、matcher 语法
- `skills.md` — SKILL.md 格式、动态参数、调用控制、发现机制
- `plugins.md` — Plugin 结构、从独立配置迁移、分发方式
- `sub-agents.md` — Subagent 配置、工具/权限控制、worktree 隔离

**概念与最佳实践（第二批）**：
- `best-practices.md` — 验证驱动、探索→规划→编码、会话管理、常见失败模式
- `memory.md` — CLAUDE.md 多层体系、自动记忆、.claude/rules/ 路径范围
- `common-workflows.md` — 代码库探索、调试、Plan Mode、测试/PR、worktrees
- `claude-directory.md` — .claude/ 目录结构、关键文件、配置层次
- `context-window.md` — 上下文加载顺序、compaction 机制、优化策略
- `how-claude-code-works.md` — 代理循环、模型选择、工具体系、执行环境
- `mcp.md` — MCP 安装方式、.mcp.json 配置、服务器管理
- `features-overview.md` — 七大扩展机制对比、Skill vs Subagent 选择指南
- `agent-teams.md` — 多会话协调、队友管理、共享任务、显示模式

## 5. 输出反馈要求

完成后按类别清晰输出变更列表：

```markdown
## 🧠 生态提炼与进化完成

### 🔄 更新的组件
1. **[skill-name]** (vYYYYMMDD-n)
   - 增强说明：[新增了哪些认知]

### ✨ 新建的组件
1. **[组件名]** (Skill / Agent / Hook / Plugin)
   - 路径：`[完整路径]`
   - 用途：[用途描述]
   - 技术特性：[动态参数/context:fork/hooks/工具限制 等]

### 📚 新增参考文档
1. `references/xxx.md` — [来源 URL]

### ⏭️ 未记录的内容
- [指出哪些因属于项目特定业务逻辑而建议写入 CLAUDE.md / .claude/rules/]
```
