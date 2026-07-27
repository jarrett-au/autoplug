---
name: edd-review-loop
description: |
  Evidence-Driven 并行审查闭环：先确定用户意图和修复模式，再按风险拆分 change units，审查、去重、证伪、分类修复，并通过复杂度闸门和增量复审闭环。
  当用户提到 review loop、审查循环、自动审查修复、循环审查，或说“帮我审查并修复这个分支”时触发。
allowed-tools: Agent Read Grep Glob Bash Write Edit
model: opus
---

# EDD Review Loop

执行“意图定界 → 并行审查 → 去重 → 证据审计 → 动作分类 → 范围闸门 → 修复 → 验证 → 增量复审”闭环。

两个不可混淆的结论：

- `accepted` 只表示 finding 的事实和归因成立。
- `fix-now` 才表示本轮应修改代码。

不得把测试覆盖、运营能力或规格完整性自动翻译成生产代码。并行用于缩短独立工作，不用于重复审查完整 diff。

## Invocation

```text
/edd-review-loop [auto|low|medium|high] [review-only|fix-critical|spec-compliance]
```

Profile 默认 `auto`。Execution mode 按用户意图推断：

| 用户意图 | Execution mode | Complexity budget |
|---|---|---|
| “只审查”“给 review report” | `review-only` | `no-code-change` |
| “审查并修复” | `fix-critical` | `standard` |
| “审查并简化” | `fix-critical` | `non-positive` |
| “严格按 spec 补齐”“完成全部验收项” | `spec-compliance` | `spec-bounded` |
| 未说明，但调用本自动闭环 | `fix-critical` | `standard` |

冲突时选择侵入性更低的模式并记录推断，不静默选择 `spec-compliance`。用户显式指定 profile 或 mode 时必须遵循；profile 运行中只允许升级，不静默降级。

### Execution modes

#### review-only

完成 review、dedup、audit 和 action classification，不修改源码、不提交 commit。所有成立 finding 进入报告或 deferred list。

#### fix-critical

默认只自动修复事实成立且影响以下不变量的问题：

- correctness
- security
- data integrity
- existing public contract

`requirement_gap` 只有在需求已明确存在且最小修复不扩展产品范围时可自动修复。test coverage、operations、deployment、maintainability 和 speculative performance 默认记录而不自动实现。

#### spec-compliance

在 `fix-critical` 基础上修复明确 acceptance criteria 的 requirement gaps。未绑定显式需求的运营平台、部署扩展和大型测试体系仍不自动进入修复。

## Runtime State

所有运行产物写入：

```text
.claude-plugins-data/code-quality/review-loop/${CLAUDE_SESSION_ID}/
```

目录结构：

```text
context.json
change-plan.json
round-1/
├── tasks/
│   ├── review-auth.json
│   ├── audit-auth.json
│   └── audit-challenge.json
├── reviews/
│   └── auth.md
├── merged-review.md
├── audits/
│   └── auth.md
├── merged-verdict.md
├── action-plan.json
└── closure-matrix.md
round-2/
└── ...
summary-{timestamp}.md
```

并行 agent 不得写同一个文件。`context.json` 由 orchestrator 串行更新。

## Phase 0: Initialize and Plan

### 0.1 Establish baseline

```bash
git status --short
git rev-parse HEAD
git merge-base main HEAD
git diff main...HEAD --stat
git diff main...HEAD --numstat
git diff main...HEAD --name-status
git diff main...HEAD --dirstat=files,0
```

工作区必须完全干净。`git status --short` 有任何输出时停止，让用户先 commit 或 stash。所有 review ranges 都基于 commit SHA；不要自动 stash、提交或丢弃用户改动。

需求上下文按以下顺序获取：

1. 用户本轮提供的需求和动词，例如“只审查”“修复”“简化”“补齐 spec”
2. PR description
3. PR 关联 issue
4. commit messages
5. 无需求时记录 `requirements: []`

不得把 reviewer 自己建议的最佳实践升级为用户需求。

### 0.2 Persist intent contract

在读 diff 前确定并记录：

```json
{
  "requested_profile": "auto",
  "selected_profile": "medium",
  "requested_mode": null,
  "selected_mode": "fix-critical",
  "intent_source": "inferred from 'review and simplify'",
  "complexity_budget": "non-positive"
}
```

`non-positive` 的含义：允许恢复核心不变量所需的最小修改，但禁止借 finding 新增独立运行时子系统、部署面或平台能力；修复后还必须对本轮修改执行一次行为保持型简化。

### 0.3 Remove review noise

默认不逐行审查：

- generated files
- vendored code
- minified assets
- lockfile 的机械变化
- formatter-only changes
- snapshots 的大块机械输出

如果这些文件承担契约、安全或供应链风险，将其加入专门 unit，不得静默排除。

### 0.4 Select review profile

Profile 是执行计划，不是“仔细程度”的提示词。

#### low

- reviewer 并发：1
- review units：1
- cross-cutting lane：关闭
- categories：requirements、correctness、security red flags、obvious contract gaps
- audit：blocking only
- rounds：1
- tests：受影响测试

#### medium

- reviewer 并发：最多 2
- review units：最多 2 个 coherent units
- cross-cutting lane：存在接口或模块交互时开启
- categories：requirements、correctness、security、contracts、tests、明确性能风险
- audit：blocking + 显式 `audit_candidate: true` 的 risk
- audit 并发：最多 2
- rounds：2
- tests：相关单测和必要集成测试

#### high

- reviewer 并发：最多 4
- review units：按模块或行为边界拆分
- cross-cutting lane：开启
- categories：全部工程风险，nit 仍不阻塞
- audit：blocking + `audit_candidate: true` 的 risk
- audit 并发：最多 3
- rounds：3
- tests：相关测试，最后执行完整 gate 或 CI 等价命令
- finish：轻量 final integration pass

`auto` 综合风险，不单纯按 LOC：

High-risk signals：auth、permissions、secrets、schema、migration、data deletion、concurrency、idempotency、transaction、public API、wire format、多模块状态流。

Medium-risk signals：普通 feature 跨多个文件、局部接口及调用方变化、新失败路径或状态变化、需要单测和集成测试共同验证。

Low-risk signals：局部且可逆、不改变公共契约或持久化数据、纯测试/文档/样式/隔离配置变化。

大 diff 可通过切片处理，不自动等同 high；小 diff 命中 high-risk signal 时仍为 high。Reviewer 发现未计划的 high-risk boundary 时请求升级，orchestrator 追加必要 lane，不重跑仍有效的 unit。

### 0.5 Build coherent change units

按模块、行为和依赖关系切片，不按固定行数分块。同一 unit 包含：

- 实现及直接调用方
- 对应测试
- 相关配置或 schema
- 理解行为所需的少量上下文文件

Cross-cutting lane 只检查：

- API compatibility
- shared contracts
- end-to-end data flow
- schema/use-site consistency
- integration coverage

### 0.6 Define applicable closure dimensions

只为当前改动实际存在的维度建矩阵，写入 `change-plan.json`。不要创建无意义占位行。

状态或 workflow 改动检查终态入口：

```text
success | permanent failure | retry exhaustion | lease exhaustion | cancellation | recovery
```

Producer/consumer 契约检查消费链：

```text
storage | serializer | API producer | API consumer | UI parser | UI render
```

错误处理改动检查上游失败源：

```text
external service | session/context | retrieval/cache | persistence | finalization
```

每个维度记录适用项和明确不适用项。后续 final-delta 与 integration pass 必须检查修复影响到的矩阵行，而不是只检查修改文件。

### 0.7 Initialize artifact directories

```bash
ROOT=".claude-plugins-data/code-quality/review-loop/${CLAUDE_SESSION_ID}"
mkdir -p "$ROOT"
git check-ignore -q "$ROOT/"
```

如果未被忽略，将 `.claude-plugins-data/code-quality/review-loop/` 加入当前仓库 `.git/info/exclude`，不要修改项目 `.gitignore`。再次确认忽略后继续。

每轮开始时创建：

```bash
mkdir -p "$ROOT/round-${ROUND}/tasks" \
         "$ROOT/round-${ROUND}/reviews" \
         "$ROOT/round-${ROUND}/audits"
```

### 0.8 Persist plan

`context.json`：

```json
{
  "session_id": "...",
  "requested_profile": "auto",
  "selected_profile": "medium",
  "requested_mode": null,
  "selected_mode": "fix-critical",
  "intent_source": "inferred from user request",
  "complexity_budget": "standard",
  "base_sha": "...",
  "initial_head_sha": "...",
  "reviewed_head_sha": null,
  "round_review_head_sha": null,
  "last_fix_commit_sha": null,
  "rounds_completed": 0,
  "requirements": [],
  "finding_history": [],
  "needs_human_findings": [],
  "needs_decision_findings": [],
  "deferred_findings": []
}
```

`finding_history` 分离事实、动作和闭环状态：

```json
{
  "fingerprint_key": "contract|src/token.py|refresh_token|expired-token-accepted",
  "audit_verdict": "accepted | downgraded | rejected | needs_human",
  "action": "fix-now | defer | needs-decision | no-change",
  "closure_status": "open | fixed | verified | not-applicable",
  "first_seen_round": 1,
  "last_seen_round": 2,
  "evidence_digest": "stable-summary"
}
```

`change-plan.json`：

```json
{
  "profile": "medium",
  "execution_mode": "fix-critical",
  "complexity_budget": "standard",
  "reasons": ["changes local API and two callers"],
  "excluded_files": [{"path": "package-lock.json", "reason": "mechanical lockfile change"}],
  "units": [
    {
      "id": "auth-api",
      "title": "Authentication API behavior",
      "risk": "medium",
      "changed_files": ["src/auth.py", "tests/test_auth.py"],
      "context_files": ["src/token.py"],
      "categories": ["correctness", "security", "public_contract"]
    }
  ],
  "cross_cutting": {
    "enabled": true,
    "focus": ["API compatibility", "integration coverage"]
  },
  "closure_dimensions": {
    "state_transitions": [],
    "producer_consumers": ["API producer", "API consumer"],
    "failure_sources": []
  },
  "action_policy": {
    "auto_fix_categories": ["correctness", "security", "data_integrity", "public_contract"],
    "default_defer_categories": ["test_gap", "operations", "deployment", "maintainability"],
    "complexity_gate": {
      "max_production_files": 5,
      "max_estimated_production_loc": 300,
      "max_broad_test_harness_loc": 300,
      "forbid_new_runtime_subsystem": true
    }
  },
  "max_review_concurrency": 2,
  "max_audit_concurrency": 2,
  "max_rounds": 2
}
```

## Phase 1: Parallel Evidence-Backed Review

### 1.1 Determine review range

启动 reviewer 前将当前 `git rev-parse HEAD` 写入 `context.round_review_head_sha`。所有本轮 task 使用同一固定终点。

Round 1：

```text
base_sha...round_review_head_sha
```

后续 round：

```text
context.reviewed_head_sha...round_review_head_sha
```

后续 round 只检查：

1. 新增 diff
2. 上轮 `fix-now` finding 是否关闭
3. 修复触及的直接依赖面
4. 适用 closure matrix 行
5. 新增或改变的需求覆盖状态

不得重新逐行审查未变化 unit。

### 1.2 Create review tasks

每个 lane 写入唯一 `round-{N}/tasks/review-{task-id}.json`：

```json
{
  "session_id": "...",
  "round": 1,
  "task_id": "auth-api",
  "task_type": "unit",
  "profile": "medium",
  "execution_mode": "fix-critical",
  "review_range": "<base_sha>...<round_review_head_sha>",
  "review_head_sha": "<round_review_head_sha>",
  "changed_files": ["src/auth.py", "tests/test_auth.py"],
  "context_files": ["src/token.py"],
  "categories": ["correctness", "security", "public_contract"],
  "requirements": [],
  "closure_dimensions": {"producer_consumers": ["API producer", "API consumer"]},
  "prior_findings": [],
  "allowed_commands": ["pytest tests/test_auth.py"],
  "environment": {
    "parallel_safe": true,
    "notes": "read-only isolated unit test; no shared database or fixed port"
  },
  "output_path": ".../round-1/reviews/auth-api.md"
}
```

Cross-cutting task 使用 `task_type: "cross_cutting"`，只读取接口、调用关系和必要 diff。

Command contract：

- `allowed_commands` 列安全的测试或复现命令；task scope 内 Git 只读命令始终可用
- 有明确 reproduction 且命令可隔离时，不得故意把 `allowed_commands` 留空
- `parallel_safe: true` 只用于不会争用数据库、端口、snapshot、Docker 或工作区文件的命令
- `parallel_safe: false` task 串行运行，不能因此自动退化为纯静态审计
- 不确定时按 `false` 处理
- reviewer 禁止修改源码、snapshot、数据库基线和 lockfile

### 1.3 Launch concurrently

同一响应发出本批独立 Agent calls，受 `max_review_concurrency` 限制。使用 `subagent_type: code-quality:edd-reviewer`，prompt 只提供 task 路径。Reviewer 写入唯一 `output_path`。

## Phase 2: Merge, Provenance Check and Deduplicate

读取 `reviews/*.md`，生成 `merged-review.md`。

### 2.1 Provenance gate

Finding 进入 audit 前必须证明：

1. `fingerprint.primary_path` 在 `review_head_sha` 中是 tracked 文件；使用 `git ls-files --error-unmatch -- <path>` 和 `git cat-file -e <review_head_sha>:<path>`
2. `scope_binding` 是 `changed_file`、有调用关系说明的 `direct_dependency`，或 `explicit_requirement`
3. 证据来自 review range 的 commit 内容，不来自本地未跟踪或 ignored 文件
4. 如果引用配置默认值，必须读取 review head 中的 tracked 配置/model/example，而不是本机 override

未通过 provenance 的 finding 不进入 audit，记录为 `rejected: invalid_provenance`。纯 requirement finding 允许 `primary_path` 指向最直接的实现入口，但仍必须绑定明确 requirement。

### 2.2 Dedup rules

1. fingerprint 相同视为同一 finding
2. 保留证据最强、复现最具体版本
3. 合并互补证据和 affected files
4. severity 由证据决定，不取最高喊价
5. 已 rejected fingerprint 只有新 evidence digest 才能重开
6. nit 不进入 audit
7. 未绑定当前 diff、需求或直接依赖面的 finding 丢弃
8. `test_gap`、`operations`、`deployment` 和 `maintainability` 不因“值得做”升级为 blocking

每个 finding 使用简洁 evidence packet；不要在 review、audit 和 verdict 中重复整段源码。完整命令输出引用 artifact。

如果没有 blocking，也没有 `audit_candidate: true` risk，则跳过 auditor，进入 action classification。

## Phase 3: Parallel Falsification Audit

Auditor 的目标是主动寻找 reviewer 可能错误的原因，不是第二遍确认 review。

### 3.1 Group findings

按模块、测试命令、根因和 evidence environment 分组，不机械地一 finding 一个 agent。

Task schema：

```json
{
  "session_id": "...",
  "round": 1,
  "group_id": "auth",
  "audit_mode": "standard",
  "finding_ids": ["R1", "R3"],
  "review_head_sha": "<round_review_head_sha>",
  "review_range": "<base_sha>...<round_review_head_sha>",
  "merged_review_path": ".../round-1/merged-review.md",
  "context_path": ".../context.json",
  "allowed_commands": ["pytest tests/test_auth.py"],
  "static_only_reason": null,
  "environment": {
    "parallel_safe": true,
    "notes": "read-only tests; no shared database"
  },
  "output_path": ".../round-1/audits/auth.md"
}
```

若 `allowed_commands` 为空，必须填写 `static_only_reason`，说明为何 static proof 是无条件且足够的；“为了并行”不是理由。

### 3.2 Audit standard

每个 finding 必须：

1. 重做 provenance 检查
2. 写出最强 counter-hypothesis，例如现有 guard、另一条调用路径、配置覆盖或重复 finding
3. 有安全 reproduction 时执行真实命令
4. 只有无条件静态证明才可在未运行命令时 `accepted/high`
5. 检查归因、category 和 severity，不判断用户是否应立即修复
6. 估计最小 remediation shape 和复杂度信号，供 orchestrator 分类

`reasoning_only` 不得 accepted。不能验证时 downgraded、rejected 或 needs_human，不能猜测。

### 3.3 Concurrency safety

可并行：static proof、Git provenance、read-only checks、隔离单元测试。

需要串行或资源隔离：共享数据库、固定端口、snapshot 更新、Docker Compose、会写工作区的命令、全量 build/test gate。

优先隔离或串行执行必要证据，不要仅为提高并行度禁止全部命令。

### 3.4 Acceptance challenge

当单轮至少审计 5 个 finding，且标准 audit 的 `accepted / (accepted + downgraded + rejected)` 大于 80% 时，必须创建一个串行 `audit_mode: "challenge"` task，对 accepted findings 再检查：

- provenance
- duplicate/root-cause overlap
- strongest counter-evidence
- category inflation
- severity inflation

Challenge pass 不重新泛化 review，也不重复昂贵测试；它可以推翻或降级标准 verdict。最终 `merged-verdict.md` 以 challenge verdict 为准，并记录是否触发。

### 3.5 Merge verdicts

合并 `audits/*.md`：

- `accepted`：事实、归因和 evidence severity 成立
- `downgraded`： concern 存在，但证据不支持原 severity
- `rejected`：证据失败、归因错误、重复、taste-only 或 provenance 无效
- `needs_human`：需要外部数据、权限或环境才能判断事实

Auditor 不生成 Developer Action List。`merged-verdict.md` 只陈述事实 verdict；同一 finding 只出现一次。

## Phase 4: Action Classification and Complexity Gate

Orchestrator 根据 mode 生成 `round-{N}/action-plan.json`。这是唯一允许驱动代码修改的 artifact。

### 4.1 Action values

- `fix-now`：本轮自动修复
- `defer`：事实成立，但不属于本轮修复目标
- `needs-decision`：修复会改变产品或运行时范围，需要用户明确选择
- `no-change`：rejected，或 finding 无需代码修改

### 4.2 Mode policy

#### review-only

Accepted/downgraded findings 设为 `defer`；rejected 设为 `no-change`。不修改源码。

#### fix-critical

只有 accepted blocking 且 category 属于以下集合时默认 `fix-now`：

```text
correctness | security | data_integrity | public_contract
```

`requirement_gap` 只有绑定用户明确需求且最小修复不扩展产品范围时可 `fix-now`。以下默认 `defer`：

```text
test_gap | operations | deployment | maintainability
```

Performance 只有存在已证明的严重退化且修复局部时可 `fix-now`。Downgraded risk 默认 `defer`。

#### spec-compliance

除核心类别外，绑定明确 acceptance criterion 的 accepted requirement gap 可 `fix-now`。未绑定 spec 的 platform/operations/deployment 仍 `defer`。

### 4.3 Complexity gate

任何 proposed remediation 命中以下信号时必须过闸：

- 新增 service、daemon、worker 类型或常驻进程
- 新增监听端口或部署拓扑
- 新增数据库表或独立持久化子系统
- 新增 metrics、logging、tracing 等运行时子系统
- 预计修改超过 5 个非测试文件
- 预计增加超过 300 行生产代码
- 新增超过 300 行的 broad integration harness
- 新增外部依赖或非必要 public API

处理规则：

- `review-only`：`defer`
- `fix-critical`：默认 `needs-decision`；继续其他安全修复，不自动扩大范围
- `spec-compliance`：只有该复杂度被显式 acceptance criterion 直接要求时可 `fix-now`，否则 `needs-decision`
- `non-positive` budget：除恢复核心不变量不可避免的最小改动外，一律 `defer` 或 `needs-decision`

先寻找更小的 source fix。阈值只是触发复核，不是把 299 行当作安全证明。

若用户要求“所有问题必须修完”且存在 `needs-decision`，请求用户决策；否则继续修复 `fix-now` 并在最终报告列出 deferred/needs-decision，不让旁支问题阻塞核心修复。

### 4.4 Action plan schema

```json
{
  "execution_mode": "fix-critical",
  "complexity_budget": "non-positive",
  "challenge_pass": true,
  "actions": [
    {
      "finding_id": "auth-api-R1",
      "audit_verdict": "accepted",
      "category": "public_contract",
      "action": "fix-now",
      "reason": "Restores an existing token contract with a local change",
      "minimum_change": "Reject expired token before issuing a refresh",
      "expected_files": ["src/token.py", "tests/test_token.py"],
      "complexity_signals": [],
      "verification_to_close": "pytest tests/test_token.py -k expired"
    }
  ]
}
```

## Phase 5: Fix, Simplify and Verify

只修复 `action-plan.json` 中的 `fix-now`。规则：

- 小而精确，修根因
- 不顺手处理 defer、nit 或 operations debt
- 开始修改前核对 expected files 和 complexity signals
- 实际修复超出 action plan 时停止该 finding，重新过 complexity gate
- 每项执行 `verification_to_close`
- 测试只保护 observable contract；不为满足 test count 建大型 harness
- 不覆盖 `reviewed_head_sha` 或 `round_review_head_sha`

测试分两层：

1. finding-specific reproduction / verification
2. profile 要求的 affected/full gate

共享环境和最终 gate 串行执行。测试失败时判断是否由修复引入；不能安全修复则报告真实证据。

当修改已 smoke-tested 后，对本轮修改范围执行一次 `code-simplifier`：删除不必要抽象、配置和 allocation，保持行为不变。`non-positive` budget 必须确认没有新增独立运行时 surface。

### 5.1 Fix commit gate

完成 finding verification、simplification 和 profile gate 后：

1. `git status --short` 和 `git diff` 确认只有 `fix-now` 改动
2. 提交范围明确的 fix commit，不夹带 review artifacts 或用户原改动
3. 将 HEAD 写入 `context.last_fix_commit_sha`
4. 再次执行 `git status --short`
5. tracked worktree 不干净时 fail closed 为 `BLOCKED_DIRTY_WORKTREE`

`review-only` 不进入 commit gate。忽略的 review artifacts 可以存在。

## Phase 6: Delta Closure and Stop

每轮完成后：

1. `reviewed_head_sha` 更新为本轮保存的 `round_review_head_sha`，不是修复后 HEAD
2. 清空 `round_review_head_sha`
3. 更新每个 finding 的 `audit_verdict`、`action` 和 `closure_status`
4. 更新 deferred、needs-decision 和 needs-human lists
5. `rounds_completed += 1`

如果产生 fix commit，当前 HEAD 仍未被 reviewer 看过；下一轮 review range 必须覆盖该 delta。

继续下一轮仅当：

- 有 `fix-now` 产生新 diff
- `spec-compliance` 仍有明确 missing requirement
- auditor 要求补充证据

终止前若 `reviewed_head_sha != HEAD`，创建串行 `final_delta` review task：

```json
{
  "task_id": "final-delta",
  "task_type": "final_delta",
  "profile": "low",
  "execution_mode": "fix-critical",
  "review_range": "<reviewed_head_sha>...<last_fix_commit_sha>",
  "review_head_sha": "<last_fix_commit_sha>",
  "changed_files": ["<files changed by final fix commit>"],
  "context_files": ["<direct callers, producers, consumers or contracts>"],
  "categories": ["correctness", "security", "data_integrity", "public_contract"],
  "prior_findings": ["<all fix-now findings with closure_status fixed>"],
  "closure_dimensions": {"<applicable dimensions only>": []},
  "allowed_commands": ["<safe targeted verification commands>"],
  "environment": {"parallel_safe": false, "notes": "final safety pass runs alone"},
  "output_path": "<round-dir>/reviews/final-delta.md"
}
```

Final-delta 必须：

1. 检查 fix commit 新引入的 correctness、security、data-integrity、contract regression
2. 对所有 `fixed` finding 做 closure check
3. 检查修复影响到的每个 transition、producer/consumer 和 failure-source matrix row
4. 不重新检查 nit、deferred operations 或完整未变化 diff
5. 未关闭则最终状态 `BLOCKED`；通过后将 `reviewed_head_sha` 更新为 HEAD

High profile 再执行一次轻量 integration pass，按 closure matrix 检查跨 unit 契约和最终 requirements，不逐行重审完整 diff。

### Stop conditions

- `review-only`：audit 和 action classification 完成
- 无 `fix-now`，且无必须立即决策的 finding
- 所有 `fix-now` 已 verified，requirements 在所选 mode 下无 missing
- 达到 max rounds 时仍有 blocker：`BLOCKED`
- Evidence 本身需要外部环境：`NEEDS_HUMAN`
- 用户要求全量完成但 scope 需要选择：`NEEDS_DECISION`

## Reviewer and Auditor Contracts

Reviewer：

- blocking 必须有 failing test、repro、requirement mismatch、static proof、security exploit path 或 contract violation
- 每个 finding 提供 provenance 和稳定 fingerprint
- test/operations/deployment gap 默认不是 blocking
- 只审 task scope；final-delta 按 closure dimensions 扩展到明确消费者或终态
- 不为显得有用制造 finding

Auditor：

- 只验证列出的 findings，不泛化 review
- 主动寻找反证，accepted 不等于 fix-now
- provenance 和命令结果必须真实
- static-only accepted 必须是无条件证明
- 不生成 Developer Action List

Orchestrator：

- 唯一负责 action classification
- 不把 accepted 直接翻译成代码
- 复杂度闸门优先于修复冲动
- deferred risk 必须如实报告，不能伪装成已解决

## Final Report

```markdown
## EDD Review Loop 完成

- Profile / mode: medium / fix-critical
- Complexity budget: non-positive
- Rounds / lanes: 2 / 3
- Findings: blocking 2 / risk 3 / nit 1
- Provenance rejected: 1
- Audit: accepted 2 / downgraded 1 / rejected 1 / needs-human 0
- Acceptance challenge: triggered, 1 verdict downgraded
- Actions: fix-now 1 / deferred 2 / needs-decision 0
- Fixed and delta-verified: 1
- Complexity delta: production LOC -12 / test LOC +18 / services +0 / ports +0 / tables +0
- Tests: <真实命令和结果>
- Remaining risks: <明确列出 deferred 和 needs-decision>
- Artifacts: .claude-plugins-data/code-quality/review-loop/<session-id>/
```

不要用逐行 diff 代替结论。复杂度数字无法精确自动计算时标记为 estimate，不得编造。

## Quality Check

- [ ] 用户意图、execution mode 和 complexity budget 已在读 diff 前记录
- [ ] profile 由风险而非 LOC 决定
- [ ] change units 按行为或模块边界切分
- [ ] closure dimensions 只包含适用状态、消费者和失败源
- [ ] 并行 agent 没有写同一文件
- [ ] findings 已按 fingerprint 去重
- [ ] 每个进入 audit 的 finding 通过 Git provenance gate
- [ ] auditor 主动检查反证，未因并行而禁止所有可执行证据
- [ ] 高接受率批次已执行 challenge pass
- [ ] accepted 与 fix-now 分开记录
- [ ] test/operations/deployment gap 未自动变成生产代码
- [ ] complexity gate 已拦截新子系统和大范围 remediation
- [ ] 每个 fix-now 都通过 verification 和增量 closure matrix
- [ ] non-positive 模式已执行行为保持型简化
- [ ] 最终测试结果来自真实执行
