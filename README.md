# AutoPlug

Agent 自动化能力集 — Coding Pipeline + Code Quality + Agent Evolution + Engineering Discipline。支持 Claude Code Plugin 与 Agent Skills CLI。

## 安装

### Claude Code Plugin

```bash
claude plugin marketplace add jarrett-au/autoplug
claude plugin install auto-issue
claude plugin install code-quality
claude plugin install agent-evolve
```

每个 plugin 可单独安装，按需选用。

### Agent Skills CLI

使用 [skills](https://github.com/vercel-labs/skills) 将单个 skill 安装到 Claude Code、Codex、Cursor、OpenCode 等 agent：

```bash
# 查看可安装的 skills
npx skills add jarrett-au/autoplug --list

# 安装指定 skill
npx skills add jarrett-au/autoplug --skill code-simplifier

# 全局安装到指定 agent
npx skills add jarrett-au/autoplug --skill code-simplifier -g -a claude-code -y
```

`npx skills` 只安装 skill 及其目录内的支持文件。`auto-issue` 和 `auto-epic` 依赖 plugin 中的专用 agents，使用这两条完整 pipeline 时请通过 Claude Code Plugin 安装。

## Plugins

### auto-issue — 全自动 Coding Pipeline

单 issue 自动开发 + 大需求拆分。

| 命令 | 用途 |
|------|------|
| `/auto-issue <issue>` | 单 issue 自动开发：分析 → TDD → 验证 → 审查 → PR |
| `/auto-epic <大需求>` | 大需求拆分 → GitHub Issues |

4 Agents：scope (plan) → developer (acceptEdits) → reviewer (auto) → planner (plan)

### code-quality — 代码质量工具集

行为保持型代码精简、风险分级并行审查、证据审计、增量复审、自动修复、测试编写、规格文档、交接与证据型 Issue 捕获。

| 命令 | 用途 |
|------|------|
| `/code-simplifier [scope] [--dry-run]` | 精简近期改动：并行发现、串行修改、逐项验证行为不变 |
| `/edd-review-loop {auto,low,medium,high} {review-only,fix-critical,spec-compliance}` | 意图定界 → 风险分级审查 → 证伪审计 → 动作分类与复杂度闸门 → 修复 → 增量闭环 |
| `/edd-reviewer` | 按 change unit 审查，blocking 必须带 Git provenance、稳定 fingerprint 和可证伪证据 |
| `/edd-auditor` | 主动寻找反证，校准 finding 事实与严重性；不替 orchestrator 决定是否修复 |
| `/write-tests` | 基于项目上下文编写高质量测试 |
| `/spec-forge` | 将高层需求转化为详细的规格文档（迭代式） |
| `/handoff` | 生成高信噪比交接文档，让下一轮 agent 无缝接手 |
| `/issue-capture` | 将旁支发现整理成有证据的 GitHub issue draft |
| `/codebase-rules-generator` | 生成超精简的项目 rules 文档 |
| `/project-scaffold` | 生成生产级 Makefile、Docker 部署和 GitHub Actions CI/CD 配置 |

### agent-evolve — Agent 自动进化工具

帮助 Claude Code agent 从经验中学习，持续变强。

| 命令 | 用途 |
|------|------|
| `/self-critique-loop` | 自省迭代循环：从目标受众视角审视产出，迭代直到 genuine aha |
| `/session-archaeologist` | 跨会话模式挖掘：从项目记忆和代码历史中发现隐藏模式（"surprise me"） |
| `/skill-auto-discover` | 知识提炼：从对话中提取有价值的知识点，自动创建/更新 Skill/Agent/Hook/Plugin |

核心闭环：**做事 → 自省（发现不足） → 固化（创建 Skill） → 下次更好**。

### engineering-discipline — 实验性工程纪律

独立的设计澄清、问题诊断与行为切片 TDD，不依赖旧版测试 Skill，不自动接管现有流水线。

- `/engineering-discipline:grill-design`：澄清影响实现的决策，返回验收例子和明确边界。
- `/engineering-discipline:diagnose`：用症状敏感的证据定位问题，在授权范围内修复。
- `/engineering-discipline:tdd-slice`：按行为切片执行 red → green → refactor，并报告真实验证结果。

三个按需原语：`domain-language`（含义）、`module-design`（边界）、`feedback-loop`（证据）。每个 Skill 可独立分发，无 Hook，不依赖同伴 Skill；在授权范围内按需维护词汇表、短 ADR 与任务记录，后续阶段先读取再执行。

本地试用与调用策略见 [插件说明](plugins/engineering-discipline/README.md)。行为效果通过 [小样本对照](plugins/engineering-discipline/evaluation/cases.md) 验证，打包校验不等于效果证明。

## 设计原则

- **零侵入**：所有 plugin 不修改项目 CLAUDE.md、rules、settings.json
- **Plan vs Auto**：决策点用 plan，评估点用 auto
- **独立分发**：每个 plugin 可单独安装，不需要整个 marketplace

## License

MIT
