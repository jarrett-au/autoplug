# AutoPlug

Claude Code 自动化能力插件集。

## 安装

```bash
claude plugin marketplace add jarrett-au/autoplug
claude plugin install auto-issue
claude plugin install agent-evolve
```

## Plugins

### auto-issue — 全自动 Coding Pipeline

单 issue 自动开发 + 大需求拆分。

| 命令 | 用途 |
|------|------|
| `/auto-issue <issue>` | 单 issue 自动开发：分析 → TDD → 验证 → 审查 → PR |
| `/auto-epic <大需求>` | 大需求拆分 → GitHub Issues |

4 Agents：scope (plan) → developer (acceptEdits) → reviewer (auto) → planner (plan)

### agent-evolve — Agent 自动进化工具

帮助 Claude Code agent 从经验中学习，持续变强。

| Skill | 用途 |
|-------|------|
| `/self-critique-loop` | 自省迭代循环：从目标受众视角审视产出，迭代直到 genuine aha |
| `/skill-auto-discover` | 知识提炼：从对话中提取有价值的知识点，自动创建/更新 Skill/Agent/Hook/Plugin |

核心闭环：**做事 → 自省（发现不足） → 固化（创建 Skill） → 下次更好**。

## 设计原则

- **零侵入**：所有 plugin 不修改项目 CLAUDE.md、rules、settings.json
- **Plan vs Auto**：决策点用 plan，评估点用 auto
- **独立分发**：每个 plugin 可单独安装，不需要整个 marketplace

## License

MIT
