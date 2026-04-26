     1|---
     2|name: skill-auto-discover
     3|description: 提取当前对话中的有价值知识点（最佳实践、解决流程），并自动创建或更新 Skill、Hook、Agent 或 Plugin 配置。
     4|when_to_use: 当用户说"从这次对话中学习"、"提炼经验"、"更新skill"、"记录这个pattern"或明确要求从 session 中捕获知识时触发。
     5|allowed-tools: Read, Edit, Write, Bash
     6|---
     7|
     8|# Skill/Ecosystem Refiner
     9|
    10|从当前对话历史中提取有价值的知识点，并智能地创建或更新 Claude Code 生态组件（Skills、Agents、Hooks、Plugins）。
    11|
    12|## 1. 知识提取与组件决策
    13|
    14|首先全面回顾当前对话，提取知识并决定最佳载体：
    15|
    16|### 1.1 Skill（最常用）
    17|**适用场景**：常规最佳实践、多步骤任务流程、检查清单、专业领域知识。
    18|
    19|| 位置 | 路径 | 适用范围 |
    20||------|------|----------|
    21|| 个人 | `~/.claude/skills/<name>/SKILL.md` | 所有项目 |
    22|| 项目 | `.claude/skills/<name>/SKILL.md` | 仅此项目 |
    23|
    24|**判断依据**：
    25|- 跨项目通用 → 个人 Skill
    26|- 项目特有但可复用 → 项目 Skill
    27|- 内容是程序/流程（不是纯事实）→ Skill（而非 CLAUDE.md）
    28|- 长参考资料 → Skill（仅在调用时加载，零上下文成本）
    29|
    30|### 1.2 Hook（强制卡点）
    31|**适用场景**：必须拦截或自动执行的检查（如安全审计、格式校验）。
    32|
    33|**作用域决策**：
    34|- **组件级 Hook**（局部）：仅在特定 Skill/Agent 活跃时需要 → 写入 YAML frontmatter 的 `hooks` 字段，组件完成后自动清理。
    35|- **项目级 Hook**（通用）：如"拦截任何 `rm -rf`" → 写入 `.claude/settings.json` 或 `.claude/settings.local.json`。
    36|- **个人级 Hook**（全局）：适用于所有项目 → 写入 `~/.claude/settings.json`。
    37|
    38|**Hook 事件速查**（参考 `references/hooks.md`）：
    39|- `PreToolUse`：工具执行前（可阻止）
    40|- `PostToolUse`：工具执行后
    41|- `UserPromptSubmit`：用户提交提示时（可阻止）
    42|- `Stop`：Claude 完成响应时（可阻止）
    43|- `PermissionRequest`：权限请求时（可自定义决定）
    44|
    45|**Hook 处理程序类型**：
    46|- `command`：Shell 命令，stdin 接收 JSON，退出码 2 = 阻止
    47|- `http`：HTTP POST 端点
    48|- `prompt`：发送给 Claude 的提示验证
    49|- `agent`：生成 subagent 验证（实验性）
    50|
    51|### 1.3 Subagent（高容量/独立任务）
    52|**适用场景**：包含繁杂日志分析、大范围代码探索、或需要不同工具权限/模型的任务。
    53|
    54|| 位置 | 路径 | 适用范围 |
    55||------|------|----------|
    56|| 个人 | `~/.claude/agents/<name>.md` | 所有项目 |
    57|| 项目 | `.claude/agents/<name>.md` | 仅此项目 |
    58|
    59|**Skill 中的 Subagent**：在 Skill frontmatter 设置 `context: fork` + `agent: <type>`。
    60|
    61|**关键能力**：
    62|- 独立 context window，仅返回摘要
    63|- 可限制工具、权限模式、模型
    64|- 支持持久内存（`memory: user/project/local`）
    65|- 支持隔离 git worktree（`isolation: worktree`）
    66|
    67|### 1.4 Plugin（团队共享）
    68|**适用场景**：需要与团队共享、跨项目复用、版本控制的组件集合。
    69|
    70|**从独立配置迁移**：
    71|1. 创建 `.claude-plugin/plugin.json`
    72|2. 复制 skills/agents/commands
    73|3. 迁移 hooks（settings.json → `hooks/hooks.json`）
    74|4. 用 `claude --plugin-dir` 测试
    75|5. 删除 `.claude/` 原始文件避免重复
    76|
    77|## 2. 变更前强制备份
    78|
    79|在修改任何现存文件之前，**必须**压缩备份：
    80|
    81|```bash
    82|mkdir -p <path>/backups
    83|zip -r "<path>/backups/<name>-$(date +%Y%m%d)-1.zip" SKILL.md reference/ 2>/dev/null || true
    84|```
    85|
    86|如果涉及多版本演进，可选创建 `CHANGES.md` 记录变更历史。
    87|
    88|## 3. 组件生成规范
    89|
    90|### 3.1 SKILL.md 格式
    91|
    92|```yaml
    93|---
    94|name: skill-name                    # 小写+连字符，最多 64 字符
    95|description: 简洁描述用途             # Claude 据此决定何时使用
    96|when_to_use: 触发上下文/短语示例       # 可选，辅助触发判断
    97|argument-hint: "[issue-number]"      # 可选，自动完成提示
    98|arguments: [name, repo]              # 可选，命名参数
    99|disable-model-invocation: false       # true 阻止自动调用
   100|user-invocable: true                  # false 从 / 菜单隐藏
   101|allowed-tools: Bash(git *) Read      # 免权限工具
   102|context: fork                         # 在 subagent 中运行
   103|agent: Explore                        # context:fork 时使用的 subagent
   104|model: sonnet                         # 可选，覆盖模型
   105|hooks:                                # 可选，限定 hooks
   106|  PreToolUse:
   107|    - matcher: "Bash"
   108|      hooks:
   109|        - type: command
   110|          command: "./scripts/check.sh"
   111|---
   112|```
   113|
   114|**动态参数**：`$ARGUMENTS`、`$ARGUMENTS[0]`、`$1`、`$name`、`${CLAUDE_SESSION_ID}`、`${CLAUDE_SKILL_DIR}`。
   115|
   116|**动态上下文注入**：`` !`command` `` 语法，发送前运行并替换输出。
   117|
   118|### 3.2 Subagent 文件格式
   119|
   120|```yaml
   121|---
   122|name: code-reviewer
   123|description: 何时使用此 subagent 的描述
   124|tools: Read, Grep, Glob, Bash         # 允许列表
   125|disallowedTools: Write, Edit          # 拒绝列表
   126|model: sonnet                         # sonnet/opus/haiku/inherit
   127|permissionMode: default               # default/acceptEdits/auto/dontAsk/bypassPermissions/plan
   128|maxTurns: 50                          # 最大轮数
   129|skills: [api-conventions]             # 预加载 skills
   130|mcpServers:                           # MCP 绑定
   131|  - github                            # 引用或内联定义
   132|memory: project                       # user/project/local
   133|background: false                     # 始终后台
   134|isolation: worktree                   # git worktree 隔离
   135|color: blue                           # 显示颜色
   136|---
   137|```
   138|
   139|### 3.3 Hook 配置格式
   140|
   141|```json
   142|{
   143|  "hooks": {
   144|    "<HookEvent>": [
   145|      {
   146|        "matcher": "Bash",
   147|        "hooks": [
   148|          {
   149|            "type": "command",
   150|            "command": "path/to/script.sh",
   151|            "timeout": 600
   152|          }
   153|        ]
   154|      }
   155|    ]
   156|  }
   157|}
   158|```
   159|
   160|### 3.4 Plugin 清单格式
   161|
   162|```json
   163|{
   164|  "name": "my-plugin",
   165|  "description": "插件描述",
   166|  "version": "1.0.0",
   167|  "author": { "name": "Your Name" }
   168|}
   169|```
   170|
   171|## 4. 参考文档
   172|
   173|生成组件时，参考 `references/` 目录下的官方文档提炼：
   174|
   175|**核心组件参考（第一批）**：
   176|- `permissions.md` — 权限系统、allowed-tools 语法、沙箱隔离
   177|- `hooks.md` — Hook 事件生命周期、处理程序类型、matcher 语法
   178|- `skills.md` — SKILL.md 格式、动态参数、调用控制、发现机制
   179|- `plugins.md` — Plugin 结构、从独立配置迁移、分发方式
   180|- `sub-agents.md` — Subagent 配置、工具/权限控制、worktree 隔离
   181|
   182|**概念与最佳实践（第二批）**：
   183|- `best-practices.md` — 验证驱动、探索→规划→编码、会话管理、常见失败模式
   184|- `memory.md` — CLAUDE.md 多层体系、自动记忆、.claude/rules/ 路径范围
   185|- `common-workflows.md` — 代码库探索、调试、Plan Mode、测试/PR、worktrees
   186|- `claude-directory.md` — .claude/ 目录结构、关键文件、配置层次
   187|- `context-window.md` — 上下文加载顺序、compaction 机制、优化策略
   188|- `how-claude-code-works.md` — 代理循环、模型选择、工具体系、执行环境
   189|- `mcp.md` — MCP 安装方式、.mcp.json 配置、服务器管理
   190|- `features-overview.md` — 七大扩展机制对比、Skill vs Subagent 选择指南
   191|- `agent-teams.md` — 多会话协调、队友管理、共享任务、显示模式
   192|
   193|## 5. 输出反馈要求
   194|
   195|完成后按类别清晰输出变更列表：
   196|
   197|```markdown
   198|## 🧠 生态提炼与进化完成
   199|
   200|### 🔄 更新的组件
   201|1. **[skill-name]** (vYYYYMMDD-n)
   202|   - 增强说明：[新增了哪些认知]
   203|
   204|### ✨ 新建的组件
   205|1. **[组件名]** (Skill / Agent / Hook / Plugin)
   206|   - 路径：`[完整路径]`
   207|   - 用途：[用途描述]
   208|   - 技术特性：[动态参数/context:fork/hooks/工具限制 等]
   209|
   210|### 📚 新增参考文档
   211|1. `references/xxx.md` — [来源 URL]
   212|
   213|### ⏭️ 未记录的内容
   214|- [指出哪些因属于项目特定业务逻辑而建议写入 CLAUDE.md / .claude/rules/]
   215|```
   216|