# Engineering Discipline

实验版 `0.1.0`。围绕三个检查：**Language**（含义是否一致）、**Structure**（知识和复杂性由谁承担）、**Evidence**（结论有什么证据）。不是另一套开发流水线。

## 使用

Claude Code 本地试用，在目标项目目录运行：

```bash
claude --plugin-dir /absolute/path/to/autoplug/plugins/engineering-discipline
```

显式入口使用完整插件命名空间，避免与其他插件重名：

- `/engineering-discipline:grill-design`：把影响实现的设计疑点变成已确认决策或明确阻塞；不自动生成 PRD 或开始开发。
- `/engineering-discipline:diagnose`：定位给定故障；只有用户同时授权修复才修改实现。
- `/engineering-discipline:tdd-slice`：完成约定范围内的行为切片，记录实际 red → green → refactor。

例如：`/engineering-discipline:grill-design 支持部分取消订单，先把行为边界讨论清楚，不写代码。`

其余三个是按需使用的参考原语，不默认出现在 Claude 命令菜单：

- `domain-language`：只有歧义影响当前任务时才澄清，区分事实、决策与假设。
- `module-design`：检查调用者负担、知识归属和测试边界，不要求第二个 adapter。
- `feedback-loop`：选择能区分对错的观察方法，真实执行，说明噪声与验证缺口。

每个 Skill 都可独立安装；流程已经内含所需规则，不要求加载原语或旧 Skill 才能继续。安装当前本地版本到目标项目，例如：

```bash
npx skills add /absolute/path/to/autoplug --skill tdd-slice -a codex
```

Codex 用 `$tdd-slice` 等名称显式选择。每个目录携带 `agents/openai.yaml`：三个流程关闭隐式调用，三个原语允许隐式调用。Claude 使用 `disable-model-invocation` 与 `user-invocable`。其他运行时可能不支持这些开关，正文仍要求显式进入流程；这些设置不是跨运行时的安全边界。

## 第一版边界

- 不修改现有 Plugin，不依赖 `write-tests`，不接管 `auto-issue`。
- 没有 Hook、后台任务、专用 Agent 或权限扩张，不修改项目 `AGENTS.md`、`CLAUDE.md` 或配置来强制生效。
- 不硬性规定追问轮数、假设数量、候选设计数或第二个实现。
- 普通测试边界按现有契约选择，不设置用户审批仪式；新的产品行为、公共契约和难逆转决策仍要确认。
- 有文档写入授权时，确认后及时保存可复用的领域含义与重要决策；跨阶段任务维护单一任务记录。无内容不建空文档，只读模式只提供拟议变更。
- 允许有噪声、视觉或人工反馈，但必须说明判据、实际观察和缺口。静态通过不等于行为改善。

## 项目记录：写入与读取

六个 Skill 都携带相同的最小记录约定，单独安装仍可完成交接；不需要额外 setup 或自动修改 Agent 指令文件。

**先发现、再复用。** 每次开始或恢复，按项目指引及已有文档 map 找到相关词汇表、ADR 和任务/spec，再对照当前代码与证据。兼容已有 `CONTEXT.md`，不强制改名，不重复创建 `GLOSSARY.md`，不把旧文档自动视为正确答案。没有 map 时检查根目录与涉及领域的文档。

三类信息分开保存，没有既有约定时才使用以下默认位置：

- **领域含义 → `GLOSSARY.md`**：可复用的术语确认后及时写入。词条包含名称、简短定义、适用领域和易混用称呼；不放进度、实现细节或未确认假设。
- **重要决策 → `docs/adr/NNNN-slug.md`**：同时满足难逆转、脱离背景容易困惑、有真实替代方案时才记录。短文交代背景、决定、放弃的方案与原因即可，不套长模板。编号先查现有文件；旧决定被替代时保留历史并链接新决定。
- **当前工作 → 已有 Issue/spec/任务记录**：跨阶段、跨会话工作持续更新同一份记录，不为每个 Skill 单独建报告。没有既有载体时才用 `docs/tasks/<slug>.md`，记录范围、验收条件、已验证进度、阻塞、下一步，并链接相关词条、ADR 和证据。

**更新时机：** `grill-design` 在含义和决策确认时保存，在交接前更新任务；`domain-language` 维护词条；`module-design` 记录满足条件的架构取舍；`tdd-slice` 与 `diagnose` 在阶段完成或暂停时更新真实状态；`feedback-loop` 将输入、环境、实际结果及证据位置关联到任务。没有长期知识变化、无需交接的小改动，不额外创建文件。

**授权与真实性：** “不写代码”不等于“禁止写文档”，但明确的只读/不写文件要求优先。文档写入未获授权时，只展示拟议变更并说明哪些状态尚未保存。更新外部 Issue 需要外部写入授权，未获授权不谎称同步，也不悄悄创建第二份权威任务记录。记录事实、已确认决策与假设的来源；读回目标后再编辑，保护用户的无关修改。未运行的检查不标完成，旧验证恢复时要核对是否仍对应当前代码。

**交接方式：** 回复列出实际使用/更新的记录路径和证据位置。新会话给出任务路径，例如“读取 `docs/tasks/team-space.md` 及其关联记录，继续下一个已确认阶段”。不保证任意新会话在没有任务线索时自动找对工作，也不会把文档持久化误称为自动路由或完整开发流水线。

## 与既有流程交接

`grill-design` 交付决策和验收例子，而非完整规格；已有需求流程完成的澄清不重问。`tdd-slice` 负责切片次序与反馈，不负责 issue 到 PR 的编排。`diagnose` 不顺手发动全量审查或重构。下一步由用户或当前编排流程选择，不自动调用旧 Skill。

第一版保留少量规则重复，使单 Skill 安装仍然完整；原语提供更深入的判断方法，而非强制前置依赖。

## 维护与验证

仓库根目录执行打包校验：

```bash
uv run --with PyYAML==6.0.3 python -m unittest discover -s tests -v
```

这些检查覆盖清单、YAML/JSON、调用策略、独立分发路径及文档入口，**不评估模型行为**。实际试用时重点检查：是否减少歧义和返工、是否产生可信验证、跨会话是否正确读取记录，以及额外追问和文档成本是否值得。尚未完成行为效果对照试验，不将静态通过视为效果证明。

## 设计来源

参考 Matt Pocock 的 [engineering skills](https://github.com/mattpocock/skills/tree/main/skills/engineering) 中 grilling、grill-with-docs、domain-modeling、codebase-design、diagnosing-bugs 和 tdd 的问题意识。本插件独立重写，不要求使用上游或 Autoplug 旧版测试 Skill；尤其不沿用固定假设配额、强制第二 adapter 或所有 seam 均需审批的规则。
