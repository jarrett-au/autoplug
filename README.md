# AutoPlug

Claude Code 自动化能力插件集 — Coding Pipeline + Code Quality + Agent Evolution。

## 安装

```bash
claude plugin marketplace add jarrett-au/autoplug
claude plugin install auto-issue
claude plugin install code-quality
claude plugin install agent-evolve
```

每个 plugin 可单独安装，按需选用。

## Plugins

### auto-issue — 全自动 Coding Pipeline

单 issue 自动开发 + 大需求拆分。

| 命令 | 用途 |
|------|------|
| `/auto-issue <issue>` | 单 issue 自动开发：分析 → TDD → 验证 → 审查 → PR |
| `/auto-epic <大需求>` | 大需求拆分 → GitHub Issues |

4 Agents：scope (plan) → developer (acceptEdits) → reviewer (auto) → planner (plan)

### code-quality — 代码质量工具集

深度审查、自动修复、测试编写、规格文档生成，7 个技能覆盖代码质量全链路。

| 命令 | 用途 |
|------|------|
| `/review-loop` | 审查 → 验证 → 修复 → 测试的自动化循环，持续改进代码质量 |
| `/code-review` | 自主资深级代码审查，作为质量守门人 |
| `/check-comment` | 对 AI 生成的 review 报告进行二次审查，独立判断问题真实性和严重程度 |
| `/write-tests` | 基于项目上下文编写高质量测试 |
| `/spec-forge` | 将高层需求转化为详细的规格文档（迭代式） |
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

## 设计原则

- **零侵入**：所有 plugin 不修改项目 CLAUDE.md、rules、settings.json
- **Plan vs Auto**：决策点用 plan，评估点用 auto
- **独立分发**：每个 plugin 可单独安装，不需要整个 marketplace

## License

MIT
