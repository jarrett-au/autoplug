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
- 不自动创建 glossary、ADR 或设计报告。沿用项目记录惯例，只保存值得复用的内容。
- 允许有噪声、视觉或人工反馈，但必须说明判据、实际观察和缺口。静态通过不等于行为改善。

## 与既有流程交接

`grill-design` 交付决策和验收例子，而非完整规格；已有需求流程完成的澄清不重问。`tdd-slice` 负责切片次序与反馈，不负责 issue 到 PR 的编排。`diagnose` 不顺手发动全量审查或重构。下一步由用户或当前编排流程选择，不自动调用旧 Skill。

第一版保留少量规则重复，使单 Skill 安装仍然完整；原语提供更深入的判断方法，而非强制前置依赖。

## 校验与试验

仓库根目录执行打包校验：

```bash
uv run --with PyYAML==6.0.3 python -m unittest discover -s tests -v
```

这些检查覆盖清单、YAML/JSON、调用策略、独立分发路径及文档入口，**不评估模型行为**。真实效果用 [小样本对照协议](evaluation/cases.md) 和 [结果模板](evaluation/result-template.md) 记录，不先建评测平台。

## 设计来源

参考 Matt Pocock 的 [engineering skills](https://github.com/mattpocock/skills/tree/main/skills/engineering) 中 grilling、grill-with-docs、domain-modeling、codebase-design、diagnosing-bugs 和 tdd 的问题意识。本插件独立重写，不要求使用上游或 Autoplug 旧版测试 Skill；尤其不沿用固定假设配额、强制第二 adapter 或所有 seam 均需审批的规则。
