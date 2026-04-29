# Agent Evolve

Claude Code Agent 自动进化工具。

## Skills

### self-critique-loop

自省迭代循环——从目标受众/用户视角审视产出，诚实批判，反复改进直到 genuine aha moment。

**触发：** `/self-critique-loop`

**核心流程：**
1. 预先定义可检验的 aha 标准
2. 产出完整版本
3. 换位审视（受众/用户/专家/自我视角）
4. 双标准批判（用户需求清单 + 质量/aha 标准清单）
5. 改进 → 重复直到 aha

**关键原则：**
- 不降低标准，aha 才停
- 完整重写优于碎片修补
- 防倦怠机制防止过早收敛

### session-archaeologist

跨会话模式挖掘——从项目记忆、代码历史和配置中发现你没注意到的行为模式、认知盲区、隐性体系和矛盾。

**触发：** `/session-archaeologist` 或说 "surprise me"

**核心流程：**
1. 多维数据采集（memory.md + git history + 目录结构 + 代码 grep）
2. 连接 + 矛盾分析（跨领域映射、投入产出不对称、隐性体系）
3. 自省迭代（复用 self-critique-loop）
4. 结构化输出（3-5 条犀利洞见，50 行以内）

**关键原则：**
- 不报流水账，找连接和矛盾
- 拒绝平庸洞察，只保留需要全局视角才能看到的
- 至少 1 条矛盾 + 1 条隐性体系

### skill-auto-discover

从当前对话中提取有价值的知识点，并自动创建或更新 Claude Code 生态组件。

**触发：** `/skill-auto-discover`

**能力：**
- 智能判断最佳载体：Skill / Hook / Agent / Plugin
- 变更前自动备份
- 支持个人级、项目级、团队级（Plugin）分发
- 完整的组件生成规范（SKILL.md、Hook 配置、Subagent、Plugin 清单）

**闭环：** self-critique-loop 发现改进点 → skill-auto-discover 固化为 Skill → 下次不再犯同样的错
