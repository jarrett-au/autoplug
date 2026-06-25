---
name: explain-changes-and-verify
description: 从功能/效果层面讲清一组变更（分支/PR/改动）做了什么、为达成什么效果，并给出按成本分层、可执行的端到端验证方案。
when_to_use: 用户说"功能层面讲下这个分支/PR 做了哪些变动""解释这次改动""怎么端到端验证""how to verify""给个验证步骤"，或要求理解一段已完成的工作。
allowed-tools: Bash(git log:*) Bash(git diff:*) Bash(git show:*) Bash(git branch:*) Bash(git status:*) Bash(git merge-base:*) Bash(sc worktree status:*) Read Grep Glob
user-invocable: true
---

# 解释变更并给出端到端验证

把一堆 commit/diff 翻译成"**人能懂的效果 + 能跑的验证**"，而不是 diff 朗读机。

## 第 0 步：先界定"真正的变更集"（讲之前必做）

只评估**本分支自己的提交**。`base`（常是 main）通常已经合并了别的分支，那些内容会冒充成"你的改动"造成干扰。关键是用对 diff 语法。

### 两点 vs 三点：默认用三点 `base...HEAD`

| 写法 | 含义 | 后果 |
|------|------|------|
| `git diff base..HEAD`（两点） | HEAD 与 **base 当前 tip** 的差异 | ❌ base 领先的提交会反向算进来，泄漏别人的改动 |
| `git diff base...HEAD`（**三点**） | **共同祖先(merge-base) → HEAD** 的差异 | ✅ 恰好等于"本分支自己改了什么"，base 领先的内容不掺入 |

**默认全程用三点**。`git log base..HEAD`（两点，列提交用）是对的——它只列 HEAD 独有的提交；但 `git diff` 必须三点。两者不要混。

### 钉死范围的步骤

1. **拿基线分支**：worktree 项目用 `sc worktree status --json` 读 `target_branch`，别假设是 `main`。
2. **本分支领先的提交**（"我做了什么"，讲解只覆盖这些）：
   ```bash
   git log <base>..HEAD --format="%h | %an | %ad | %s" --date=short   # 两点：列提交 OK
   for c in <hashes>; do echo "--- $c ---"; git show --stat --format="%s" $c; done
   ```
3. **真正的文件变更集**（三点）：
   ```bash
   git diff <base>...HEAD --stat        # 三点：只含本分支改动
   ```
4. **base 反向领先了什么**（解释为何两点会有噪声）：
   ```bash
   git log --oneline HEAD..<base>                       # base 独有的提交
   git merge-base <base> HEAD | xargs git log -1 --oneline   # 共同祖先
   ```
5. **存疑文件逐一确认**（任何怀疑不属于本分支的文件）：
   ```bash
   git log <base>..HEAD -- <file>     # 输出为空 → 不是你改的，验证时忽略
   ```
6. **自检（可选但推荐）**：三点 diff 的文件集应与"本分支提交触及的文件并集"完全一致：
   ```bash
   diff <(git diff <base>...HEAD --name-only | sort) \
        <(git log <base>..HEAD --name-only --format= | sort -u | grep -v '^$') \
     && echo "IDENTICAL ✓"   # 一致即范围干净
   ```

> 真实教训（已实测）：本分支 4 个提交，`git diff main..HEAD`（两点）列出 **15 个 expert-eval 文件**——全是 main 领先合入的别人分支内容；换成 `git diff main...HEAD`（三点）**0 个泄漏**，且文件集与自己提交的并集逐字一致。**所以三点是默认，不是可选项。** 若仍有可疑文件，再用第 5 步逐一确认，并在讲解时明确标注"这些不是本分支改动，验证时忽略"，绝不张冠李戴。

> 注意"变更集"形态会变：同一任务跨多轮，可能这轮还**未提交**（看 `git status` / `git diff --cached`），下轮已**提交成多个 commit**。先 `git status` 看清当前是"工作区改动"还是"已落 commit"，再选 `git diff`（工作区）还是 `git diff base...HEAD`（已提交）。

## 三段式输出

### 1. 先说"为什么"（问题 → 效果）
- **症状**：用户/系统观察到的具体现象（最好用真实例子，如 `mini-test-...014727` 比预期晚 8 小时）。
- **根因**：一句话点透本质，而非罗列代码。
- **达成的效果**：这组变更让世界变成什么样。

### 2. 功能变动——**按行为分组，不按文件**
- 用表格呈现 `场景 → 行为 → 效果`，让读者看"它现在怎么表现"，而不是"改了哪几行"。
- 抓**本质区分**（最有信息量的那一刀），例：「机器存的（UTC，稳定）」vs「人看的（可配时区）」。
- 单独点出本次的**增量修复/边界**（如 review 轮新增的 fix），但同样讲效果。

### 3. 端到端验证——**按成本由低到高分层**
读者可从最便宜的一层开始，按需深入：

| 层 | 内容 | 典型 |
|----|------|------|
| A 最快 | 单测/纯函数证明核心逻辑 | `pytest tests/test_x.py`、`vitest run <file>` |
| B 接口 | 起服务 + curl/调接口 | `curl localhost:8000/api/...` |
| C 真实场景 | 端到端走一遍用户最初反馈的路径 | UI 跑一次，看那个值对不对 |
| D 不变量 | 校验后端/数据层约束 | 查库确认存的是 UTC、ID 未漂移 |
| E 回归/切换 | 改配置/环境重跑，确认整体跟随且无回归 | 换 `APP__TIMEZONE` 重启再验 |

每条都给**可直接粘贴执行**的命令，并写明**预期结果**。

### 浏览器端到端验证（C 层做法）

当效果体现在 UI（下拉项、菜单可见性、按角色的权限），C 层要写成读者能照着点的剧本：

- **先列启动命令**：把跑通这条路径所需的服务一次性列清（如 `make run` / `make worker` / `make ui-dev` + 端口）。
- **列出前置数据/账号**：变更涉及角色或权限时，明确需要哪几类账号（如 全局 admin / org-admin / 普通用户），以及怎么造。
- **用表格写"步骤 → 预期"**，覆盖**正例与反例**：该看到的要看到，**不该看到的要确认看不到**（隐藏项、跳转、403）。
- **可见性 ≠ 数据隔离**：UI 能进只是表象，务必再加一条"**同一页换不同角色看到的数据集合是子集关系**"的对比，证明后端真过滤，而非前端兜底。
- UI 之外能验的（请求是否带预期 query 参数、接口是否真返回过滤后数据），用 DevTools Network 或 curl 兜底，归到 B/D 层。

### 收尾：一句话本质
用一句话把整组变更的核心价值钉死。

## 硬性原则

- **先核实，再断言。** 凡是要写进解释或验证步骤的事实（默认值、env 是否覆盖、是否 fail-fast、接口是否免鉴权、commit 列表），**先用 `git`/运行命令/读代码确认**，不靠记忆或臆测。本 skill 的价值就在于验证步骤真的能跑通。
- **解释为主，代码为辅。** 只在关键处贴极少量行做佐证，绝不整段贴 diff。
- **效果导向。** 始终回答"用户/调用方能观察到什么变化"，而非"内部怎么实现"。
- 验证步骤要**分层且自给自足**——读者不必读源码就能照着跑。

## 写作对比

❌ 不好（diff 朗读）：
> 改了 orchestrator.py 第 185 行，`datetime.now()` → `now_in_app_tz()`；utils.py 删了 50 行……

✅ 好（效果 + 可验证）：
> **效果**：实验标题里的时间戳现在按 `app.timezone` 生成——UTC+8 下显示 09:47 而非 01:47；数据库仍存 UTC。
> **A 验证**：`uv run pytest tests/test_time.py -q` → 断言 `01:47:27 UTC` 格式化为 `094727`。
> **E 验证**：`APP__TIMEZONE=America/New_York` 重启后 `curl /api/v1/config` 跟随变化，DB 值不变。
