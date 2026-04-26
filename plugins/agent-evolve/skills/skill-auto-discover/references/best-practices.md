# Claude Code 最佳实践

> 来源：<https://code.claude.com/docs/zh-CN/best-practices>

## 核心约束

Claude 的 context window 填充速度很快，随着填充性能会下降。这是大多数最佳实践的出发点。

## 六大实践领域

### 1. 验证驱动（最高杠杆）

给 Claude 一种验证其工作的方式 — 测试、屏幕截图或预期输出。

| 策略 | 差 | 好 |
|------|-----|-----|
| 提供验证标准 | "实现验证邮箱函数" | "编写 validateEmail 函数。测试用例：user@example.com→真, invalid→假。实现后运行测试" |
| 视觉验证 UI | "让仪表板好看" | "[粘贴截图] 实现此设计。截图对比差异并修复" |
| 根因修复 | "构建失败" | "构建失败，错误：[粘贴]。修复并验证。解决根因，不抑制错误" |

### 2. 探索→规划→编码

**四阶段工作流**：
1. **探索**（Plan Mode）：Claude 读文件、回答问题，不修改
2. **规划**：要求创建详细实现计划（Ctrl+G 可在编辑器中打开计划）
3. **实现**（Normal Mode）：按计划编码，验证
4. **提交**：描述性 commit + PR

> 对于范围明确的小修复（拼写、日志、重命名），直接执行，跳过规划。

### 3. 具体上下文

| 策略 | 差 | 好 |
|------|-----|-----|
| 限定范围 | "为 foo.py 添加测试" | "为 foo.py 编写测试，涵盖用户已注销边界情况。避免 mock" |
| 指向来源 | "为什么 ExecutionFactory API 这样" | "查看 ExecutionFactory 的 git 历史并总结其 API 演变" |
| 参考模式 | "添加日历小部件" | "查看主页现有小部件实现（HotDogWidget.php），按模式实现日历小部件" |
| 描述症状 | "修复登录错误" | "用户报告会话超时后登录失败。检查 src/auth/ 的 token 刷新。写失败测试→修复" |

### 4. CLAUDE.md 编写原则

**✅ 包括**：Claude 无法猜测的 Bash 命令、与默认不同的代码风格、测试指令、存储库礼仪、架构决策、环境怪癖、常见陷阱

**❌ 排除**：Claude 可从代码推断的内容、标准语言约定、详细 API 文档（改为链接）、经常变化的信息、冗长教程、自明实践、文件逐个描述

> **关键**：如果 Claude 仍违反规则，说明文件太长导致规则被忽略。像代码一样对待 CLAUDE.md — 审查、修剪、测试。

**导入语法**：`@path/to/file` 导入其他文件，支持递归（最大 5 跳）

### 5. 通信模式

- **代码库问题**：像问资深工程师一样提问（日志如何工作、为什么调用 foo() 而不是 bar()）
- **让 Claude 采访你**：`I want to build [描述]. Interview me using AskUserQuestion.`
- **/btw**：快速问题，不进入对话历史

### 6. 会话管理

- **尽早纠正**：一旦偏离立即纠偏。Esc 停止（保留 context），Esc+Esc 或 /rewind 回退
- **/clear**：不相关任务间重置 context
- **同问题纠正 >2 次**：/clear 并用更好提示重开（包含学到的内容）
- **Subagents 调查**：`use subagents to investigate X` — 在独立 context 中探索
- **检查点 Rewind**：每个操作自动检查点，可恢复对话/代码/两者

## 自动化扩展

### 非交互模式
```bash
claude -p "prompt"                    # 纯文本
claude -p "prompt" -o json            # JSON 输出
claude -p "prompt" -o stream-json     # 流式 JSON
```

### 多会话并行
- **桌面应用**：可视化多会话管理
- **Writer/Reviewer 模式**：会话 A 写代码 → 会话 B 审查（新鲜 context 不偏向自己写的代码）

### 跨文件扇出
```bash
for file in $(cat files.txt); do
  claude -p "Migrate $file from React to Vue" \
    --allowedTools "Edit,Bash(git commit *)"
done
```

> 先在 2-3 个文件测试精化提示，再大规模运行。`--allowedTools` 限制权限。

### Auto Mode
```bash
claude --permission-mode auto -p "fix all lint errors"
```
分类器审查命令，阻止范围升级/未知基础设施/敌对内容驱动操作。

## 常见失败模式

| 模式 | 症状 | 修复 |
|------|------|------|
| 厨房水槽会话 | 不相关任务混在一起 | 任务间 /clear |
| 反复纠正 | 同问题改 >2 次 | /clear + 更好提示重开 |
| 过度指定 CLAUDE.md | 文件太长被忽略 | 无情修剪，转为 hook |
| 信任但未验证 | 产生看似合理但有缺陷的代码 | 始终提供验证（测试/脚本/截图） |
| 无限探索 | "调查"无范围限定 | 狭隘限定或用 subagents |

## CLI 工具优先

与外部服务交互优先使用 CLI（gh、aws、gcloud、sentry-cli）。Claude 能有效学习未知 CLI：
```
Use 'foo-cli-tool --help' to learn about foo tool, then use it to solve A, B, C.
```
