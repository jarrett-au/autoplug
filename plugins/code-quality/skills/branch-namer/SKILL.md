---
name: branch-namer
description: 从当前工作/代码变更生成符合 conventional 前缀规范的 kebab-case 分支名，给出主推荐 + 备选与重命名命令。
when_to_use: 用户想给分支起名/改名，或说"起个分支名""branch name""重命名当前分支""这功能该叫什么分支"。
allowed-tools: Bash(git log:*) Bash(git diff:*) Bash(git rev-parse:*) Bash(git branch:*) Bash(git status:*)
user-invocable: true
model: haiku
---

# 分支命名

把"这堆变更"压成一个**规范、简短、能一眼看懂意图**的分支名。

## 流程

1. **先看真实变更，不要臆测。** 用 `git log <base>..HEAD --oneline`、`git diff <base>...HEAD --stat`（base 通常是 `main`）以及当前对话里的工作，判断这条分支到底做了什么。无 commit 时就看对话里已完成/计划的改动。
2. **选前缀 = 主导变更类型**（见下表）。混合类型取**最主要**的那个：新增特性为主、夹带少量 fix/重构 → 仍是 `feat/`。若两类同等重要且割裂，提示用户分支本身可能该拆。
3. **提炼 slug**：2-4 个词的名词短语，描述"做了什么"而非"怎么做"，全小写连字符。
4. **输出 1 个主推荐 + 2-3 个备选**，每个备选一句话理由（更短 / 更强调某面 / 折中）。
5. 附上重命名命令：`git branch -m <new-name>`（仅当用户在该分支上想改名）。

## 前缀对照

| 前缀 | 用于 |
|------|------|
| `feat/` | 新增功能/能力 |
| `fix/` | 修复 bug / 运行时错误 / 逻辑缺陷 |
| `refactor/` | 等价重构，不改外部行为 |
| `perf/` | 性能优化 |
| `test/` | 仅新增/修复测试 |
| `docs/` | 仅文档 |
| `chore/` | 杂项：依赖、配置、脚手架 |
| `ci/` | CI/CD 配置 |
| `style/` | 格式/样式，无功能影响 |
| `build/` | 构建系统/打包 |

## slug 规范

- 全小写 + 连字符（kebab-case），2-4 词；够描述即可，别堆细节。
- 描述**结果/对象**，不描述实现手段：`configurable-display-timezone` ✅，不是 `replace-datetime-now` ❌。
- **不要**塞流程名/范围名/元信息：避免 `review`、`round2`、`omp`、`wip` 之类。
- 可对应核心配置项/模块名，往往最准：配置项 `app.timezone` → `app-timezone`。

## 示例（来自真实场景）

一条分支：新增"全局可配置展示时区"特性 + 两个相关小修。主导是 feat：

- 主推荐：`feat/configurable-display-timezone`
- 备选：`feat/app-timezone`（最短，对应配置项）、`feat/unified-time-handling`（强调统一全链路）、`feat/display-timezone`（折中）

```bash
git branch -m feat/configurable-display-timezone
```

## 反例

- ❌ `feat/timezone-stuff`（slug 太泛）
- ❌ `chore/omp`（流程/项目缩写，看不出内容）
- ❌ `feat/replace-datetime-now-with-utcnow`（描述实现而非效果，过长）
- ❌ `feature_AddTimezone`（错前缀分隔符、非 kebab-case）
