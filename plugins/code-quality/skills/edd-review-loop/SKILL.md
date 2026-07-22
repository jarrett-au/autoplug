---
name: edd-review-loop
description: |
  Evidence-Driven 并行审查闭环：按风险选择 low/medium/high profile，将大改动拆成 change units 并行审查，合并去重 findings，并行审计证据，修复后仅复审增量。
  当用户提到 review loop、审查循环、自动审查修复、循环审查，或说“帮我审查并修复这个分支”时触发。
allowed-tools: Agent Read Grep Glob Bash Write Edit
model: opus
---

# EDD Review Loop

执行“规划 → 并行审查 → 合并 → 并行证据审计 → 修复 → 验证 → 增量复审”闭环。

只修复证据成立的问题。并行用于缩短必要工作的耗时，不用于让多个 agent 重复读取完整 diff。

## Invocation

```text
/edd-review-loop [auto|low|medium|high]
```

默认 `auto`。用户显式指定 profile 时遵循用户选择；运行中只允许自动升级，不静默降级。

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
│   ├── review-ui.json
│   └── audit-A1.json
├── reviews/
│   ├── auth.md
│   └── ui.md
├── merged-review.md
├── audits/
│   └── A1.md
└── merged-verdict.md
round-2/
└── ...
summary-{timestamp}.md
```

并行 agent 不得写同一个文件。

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

工作区必须完全干净。`git status --short` 有任何输出时停止，并让用户先 commit 或 stash。所有 review ranges 都基于 commit SHA；允许 dirty worktree 会静默漏审未提交代码。不要自动 stash、提交或丢弃用户改动。

需求上下文按以下顺序获取：

1. 用户本轮提供的需求
2. PR description
3. PR 关联 issue
4. commit messages
5. 无需求时记录 `requirements: []`

### 0.2 Remove review noise

默认不逐行审查：

- generated files
- vendored code
- minified assets
- lockfile 的机械变化
- formatter-only changes
- snapshots 的大块机械输出

如果这些文件本身承担契约、安全或供应链风险，将其加入专门的 review unit，而不是静默排除。

### 0.3 Select review profile

Profile 是执行计划，不是“仔细程度”的提示词。

#### low

适合局部、低 blast-radius 改动。

- reviewer 并发：1
- review units：1
- cross-cutting lane：关闭
- categories：requirements、correctness、security red flags、obvious test gaps
- audit：blocking only
- rounds：1
- tests：受影响测试

#### medium

默认 profile，适合边界清楚的普通 feature。

- reviewer 并发：最多 2
- review units：最多 2 个 coherent units
- cross-cutting lane：存在接口或模块交互时开启
- categories：requirements、correctness、security、contracts、tests、明确性能风险
- audit：blocking + 显式 `audit_candidate: true` 的 risk
- audit 并发：最多 2
- rounds：2
- tests：相关单测和必要集成测试

#### high

适合高风险或跨模块改动。

- reviewer 并发：最多 4
- review units：按模块/行为边界拆分
- cross-cutting lane：开启
- categories：全部工程风险，nit 仍不阻塞
- audit：blocking + `audit_candidate: true` 的 risk
- audit 并发：最多 3
- rounds：3
- tests：相关测试，最后执行完整 gate 或 CI 等价命令
- finish：执行一次轻量 final integration pass

### 0.4 Auto profile signals

`auto` 综合以下信号，不单纯按 LOC：

High-risk signals：

- auth、authorization、permissions、secrets
- database schema、migration、data deletion
- concurrency、cache consistency、idempotency、transaction
- public API、wire format、shared contract
- dependency upgrade with runtime/security impact
- 多模块数据流或核心架构变化

Medium-risk signals：

- 普通 feature 跨多个文件
- 修改局部接口及调用方
- 新增失败路径或状态变化
- 需要单元测试和集成测试共同验证

Low-risk signals：

- 局部且可逆
- 不改变公共契约或持久化数据
- 测试、文档、样式或隔离配置变化

大 diff 可通过切片处理，不自动等同 high。小 diff 命中 high-risk signal 时仍为 high。

Low/medium reviewer 发现未纳入计划的 high-risk signal 时，在报告中输出 `escalation_required: high`。orchestrator 更新计划后追加必要 lanes，不重跑已完成且仍有效的 unit。

### 0.5 Build coherent change units

按模块、行为和依赖关系切片，不按固定行数机械分块。

同一 unit 应包含：

- 实现及直接调用方
- 对应测试
- 相关配置或 schema
- 理解行为所需的少量上下文文件

避免让多个 reviewer 各自读取完整 diff。跨 unit 风险由 cross-cutting lane 检查：

- API compatibility
- shared contracts
- end-to-end data flow
- schema/use-site consistency
- integration coverage

### 0.6 Initialize artifact directories

```bash
ROOT=".claude-plugins-data/code-quality/review-loop/${CLAUDE_SESSION_ID}"
mkdir -p "$ROOT"
```

运行目录必须被 Git 忽略。先执行：

```bash
git check-ignore -q "$ROOT/"
```

如果未被忽略，将 `.claude-plugins-data/code-quality/review-loop/` 加入当前仓库的 `.git/info/exclude`。不要自动修改项目 `.gitignore`。再次执行 `git check-ignore -q "$ROOT/"` 确认成功后再继续。

每轮开始时显式创建：

```bash
mkdir -p "$ROOT/round-${ROUND}/tasks" \
         "$ROOT/round-${ROUND}/reviews" \
         "$ROOT/round-${ROUND}/audits"
```

### 0.7 Persist plan

写入 `context.json`：

```json
{
  "session_id": "...",
  "requested_profile": "auto",
  "selected_profile": "medium",
  "base_sha": "...",
  "initial_head_sha": "...",
  "reviewed_head_sha": null,
  "round_review_head_sha": null,
  "last_fix_commit_sha": null,
  "rounds_completed": 0,
  "requirements": [],
  "finding_history": [],
  "needs_human_findings": []
}
```

写入 `change-plan.json`：

```json
{
  "profile": "medium",
  "reasons": ["changes local API and two callers"],
  "excluded_files": [{"path": "package-lock.json", "reason": "mechanical lockfile change"}],
  "units": [
    {
      "id": "auth-api",
      "title": "Authentication API behavior",
      "risk": "medium",
      "changed_files": ["src/auth.py", "tests/test_auth.py"],
      "context_files": ["src/token.py"],
      "categories": ["requirements", "correctness", "security", "tests"]
    }
  ],
  "cross_cutting": {
    "enabled": true,
    "focus": ["API compatibility", "integration coverage"]
  },
  "max_review_concurrency": 2,
  "max_audit_concurrency": 2,
  "max_rounds": 2
}
```

## Phase 1: Parallel Evidence-Backed Review

### 1.1 Determine review range

在启动本轮 reviewer 前记录当前快照：

```bash
git rev-parse HEAD
```

将结果写入 `context.round_review_head_sha`。所有本轮 review tasks 的 range 必须以这个固定 SHA 结尾，避免 reviewer 运行期间 HEAD 变化造成输入不一致。

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
2. 上轮 accepted finding 是否关闭
3. 修复触及的直接依赖面
4. 新增或改变的需求覆盖状态

不得重新逐行审查未变化的 units。

### 1.2 Create review tasks

为每个需要执行的 lane 写独立任务文件：

```text
round-{N}/tasks/review-{task-id}.json
```

Schema：

```json
{
  "session_id": "...",
  "round": 1,
  "task_id": "auth-api",
  "task_type": "unit",
  "profile": "medium",
  "review_range": "<base_sha>...<round_review_head_sha>",
  "changed_files": ["src/auth.py", "tests/test_auth.py"],
  "context_files": ["src/token.py"],
  "categories": ["requirements", "correctness", "security", "tests"],
  "requirements": [],
  "prior_findings": [],
  "allowed_commands": ["pytest tests/test_auth.py"],
  "environment": {
    "parallel_safe": true,
    "notes": "read-only isolated unit test; no shared database or fixed port"
  },
  "output_path": ".../round-1/reviews/auth-api.md"
}
```

Cross-cutting task 使用 `task_type: "cross_cutting"`，只读取接口、调用关系和必要 diff，不重复完整的逐文件审查。

Reviewer 的 Bash 安全契约与 auditor 相同：

- `allowed_commands` 只列可执行的测试/复现命令；Git 的只读 diff/show/log 命令可按 task scope 使用
- `environment.parallel_safe: true` 仅用于只读、隔离且不会争用数据库、端口、snapshot、Docker 服务或工作区文件的命令
- `parallel_safe: false` 的 reviewer task 必须串行运行，或只做静态 review 并把运行验证留给 audit
- reviewer 禁止修改源码、snapshot、数据库基线和 lockfile
- 不确定是否安全时按 `false` 处理

`prior_findings` 使用以下记录，只传与当前 unit 或直接依赖面相关的条目：

```json
{
  "fingerprint_key": "contract|src/token.py|refresh_token|expired-token-accepted",
  "status": "open | fixed | verified | rejected | needs_human",
  "first_seen_round": 1,
  "last_seen_round": 2,
  "evidence_digest": "sha256-or-short-stable-summary"
}
```

### 1.3 Launch concurrently

在同一条响应中发出本批所有独立 `Agent` tool calls，受 `max_review_concurrency` 限制。每个调用使用 `subagent_type: code-quality:edd-reviewer`，prompt 只需给出 task 文件路径：

```text
Execute review task:
.claude-plugins-data/code-quality/review-loop/<session-id>/round-<round>/tasks/review-<task-id>.json
```

一批完成后再发下一批。不要串行等待本可并行的 lanes。

Reviewer 必须将报告写到 task 中指定的唯一 `output_path`。

## Phase 2: Merge and Deduplicate Findings

读取本轮 `reviews/*.md`，生成 `merged-review.md`。

每个 finding 必须包含稳定 fingerprint：

```yaml
fingerprint:
  category: contract_violation
  primary_path: src/token.py
  symbol: refresh_token
  behavior: expired-token-accepted
```

合并规则：

1. fingerprint 相同视为同一 finding
2. 保留证据最强、复现最具体的版本
3. 合并互补证据与 affected files
4. severity 由证据支持程度决定，不取最高喊价
5. 已 rejected fingerprint 只有在出现新证据时才能重新打开
6. nit 不进入 audit
7. 未绑定当前 diff、需求或直接依赖面的 finding 丢弃

`merged-review.md` 记录来源 task IDs，便于追踪，但每个 finding 只进入一次 audit。

Fingerprint lifecycle 存在 `context.finding_history`：

- `open`：auditor 已采纳，等待修复
- `fixed`：developer 已修改且 verification to close 通过，等待下一轮 delta review
- `verified`：后续 reviewer 确认修复关闭且没有同 fingerprint 回归
- `rejected`：证据不成立；仅当新 finding 的 `evidence_digest` 变化时允许重新打开
- `needs_human`：需要外部环境或人类决策，不自动修复

每轮 merge 按 `fingerprint_key` upsert，不追加重复记录。`first_seen_round` 保持不变，`last_seen_round` 更新。Reviewer 对 `fixed` finding 只做 closure check；对 `verified`/`rejected` finding 默认跳过，除非有新证据。

如果没有 blocking，也没有 `audit_candidate: true` 的 risk：

- 不调用 auditor
- 进入测试/终止判断

## Phase 3: Parallel Evidence Audit

### 3.1 Group findings

按共享上下文和验证方式分组：

- 同一模块
- 同一测试命令
- 同一根因
- 同一 evidence environment

不要机械地一 finding 启动一个 agent。

为每组写：

```text
round-{N}/tasks/audit-{group-id}.json
```

Schema：

```json
{
  "session_id": "...",
  "round": 1,
  "group_id": "auth",
  "finding_ids": ["R1", "R3"],
  "merged_review_path": ".../round-1/merged-review.md",
  "context_path": ".../context.json",
  "allowed_commands": ["pytest tests/test_auth.py"],
  "environment": {
    "parallel_safe": true,
    "notes": "read-only tests; no shared database"
  },
  "output_path": ".../round-1/audits/auth.md"
}
```

### 3.2 Concurrency safety

可并行：

- static proof
- read-only checks
- 隔离良好的单元测试

需要串行或隔离 worktree/namespace：

- 共享数据库
- 固定端口
- snapshot 更新
- Docker Compose 共享服务
- 会写工作区的命令
- 全量 build/test gate

不确定时标记 `parallel_safe: false` 并串行执行。

### 3.3 Launch auditors

在同一条响应中发出安全的独立 `Agent` tool calls，受 `max_audit_concurrency` 限制。每个调用使用 `subagent_type: code-quality:edd-auditor`：

```text
Execute audit task:
.claude-plugins-data/code-quality/review-loop/<session-id>/round-<round>/tasks/audit-<group-id>.json
```

每个 auditor 只处理任务文件列出的 findings，写入唯一 `output_path`。

### 3.4 Merge verdicts

合并 `audits/*.md` 为 `merged-verdict.md`：

- `accepted`：证据成立，进入 Developer Action List；finding status 设为 `open`
- `downgraded`：证据不足以维持原级别；只有明确 worth fixing 的 risk 进入，进入时 status 设为 `open`
- `rejected`：不修复，status 设为 `rejected`，记录 evidence digest
- `needs_human`：不自动修复，status 设为 `needs_human`，写入 `context.needs_human_findings`，并触发人工决策终止条件

同一 finding 不得因多个 audit 文件重复进入 action list。

## Phase 4: Fix and Verify

只修复：

- accepted blocking
- auditor 明确标记 `worth_fixing: true` 的 downgraded risk

修复规则：

- 小而精确
- 不顺手重构
- 不处理 nit
- 每项修复执行原始 `verification_to_close`
- 不覆盖 `reviewed_head_sha` 或 `round_review_head_sha`；它们代表 reviewer 实际看过的快照

测试分两层：

1. finding-specific verification
2. profile 要求的 affected/full gate

全量测试、共享环境测试和最终 gate 串行执行。

测试失败时先判断是否由当前修复引入。修复后重测；无法安全修复则停止并报告证据，不伪造通过结果。

提交信息描述实际代码变化，不使用 `review round` 作为 scope：

```text
fix(auth): reject expired refresh tokens
```

### 4.1 Fix commit gate

完成 finding-specific verification 和 profile test gate 后，修复必须进入一个干净、范围明确的 commit，SHA 增量协议才可以继续：

1. 用 `git status --short` 和 `git diff` 确认只有本轮 accepted action list 对应改动
2. 提交本轮修复；不要夹带审查 artifacts 或用户原有改动
3. 将 `git rev-parse HEAD` 写入 `context.last_fix_commit_sha`
4. 再次执行 `git status --short`
5. tracked worktree 仍有改动时 fail closed，最终状态为 `BLOCKED_DIRTY_WORKTREE`；不得进入 Phase 5 或声称审查完成

允许存在已忽略的 review artifacts。修复 commit 之后的 HEAD 必须与 `last_fix_commit_sha` 一致。下一轮 reviewer 或 final delta task 从上一份 `reviewed_head_sha` 审到这个 fix commit。

## Phase 5: Advance or Stop

一轮成功结束后：

1. 将 `context.reviewed_head_sha` 更新为本轮保存的 `context.round_review_head_sha`，不是修复后的当前 HEAD
2. 清空 `context.round_review_head_sha`
3. 按 fingerprint lifecycle 更新 `finding_history`；已修复且 verification 通过的 `open` finding 设为 `fixed`
4. 更新 `needs_human_findings` 和 requirements 状态
5. `rounds_completed += 1`

如果本轮产生修复 commit，修复后的 HEAD 尚未被 reviewer 审查；下一轮 range 因此是 `reviewed_head_sha...新的 round_review_head_sha`。

继续下一轮仅当：

- 有实际修复产生新 diff
- 仍有 missing requirement
- auditor 要求补充验证

终止条件：

- 无 accepted blocking、无 worth-fixing risk、需求无 missing
- 达到 profile 的 max rounds
- 连续两轮 blocking 全部因弱证据被降级或拒绝
- `context.needs_human_findings` 非空：停止自动修复，最终状态为 `NEEDS_HUMAN`，列出所需环境或决策

终止前比较 `reviewed_head_sha` 与当前 HEAD。若两者不同，说明最后一批 fix commit 尚未被审查。创建一个普通 review task 文件，使用：

```json
{
  "task_id": "final-delta",
  "task_type": "final_delta",
  "profile": "low",
  "review_range": "<reviewed_head_sha>...<last_fix_commit_sha>",
  "changed_files": ["<files changed by final fix commit>"],
  "context_files": ["<direct callers or contracts>"],
  "categories": ["correctness", "security", "contract"],
  "prior_findings": ["<all finding_history records with status fixed>"],
  "allowed_commands": ["<safe targeted verification commands>"],
  "environment": {"parallel_safe": false, "notes": "final safety pass runs alone"},
  "output_path": "<round-dir>/reviews/final-delta.md"
}
```

使用 `code-quality:edd-reviewer` 串行执行：

1. 检查 fix commit 新引入的 correctness、security、contract regression
2. 对所有仍为 `fixed` 的 finding 执行 closure check，确认后更新为 `verified`
3. 不重新打开完整循环，不检查 nit/maintainability
4. 若发现 blocking 或仍有无法关闭的 fixed finding，最终状态必须是 `BLOCKED` 并报告证据；不得声称 review loop clean
5. 若通过，将 `reviewed_head_sha` 更新为 `last_fix_commit_sha`；此时必须等于当前 HEAD

High profile 结束前执行一次轻量 final integration pass，仅检查跨 unit 契约和最终 requirements，不重新逐行审查完整 diff。

## Reviewer and Auditor Contracts

Reviewer：

- blocking 必须有 failing test、repro command、requirement mismatch、static proof、security exploit path 或 contract violation
- risk 默认不 audit，除非 `audit_candidate: true`
- finding 必须有 fingerprint
- 只审 task 指定范围
- 不为显得有用而制造 finding

Auditor：

- 只验证任务列出的 finding
- 不做新的泛化 review
- 运行命令必须记录真实结果
- 不扩大修复范围
- 无法验证时 downgraded/rejected/needs_human，不猜测

## Final Report

输出：

```markdown
## EDD Review Loop 完成

- Profile: medium
- Rounds: 2
- Review lanes: 3
- Findings: blocking 2 / risk 1 / nit 2
- Audit: accepted 1 / downgraded 1 / rejected 1
- Fixed: 1
- Incremental re-review: yes
- Tests: <真实命令和结果>
- Remaining risks: <没有则 none>
- Artifacts: .claude-plugins-data/code-quality/review-loop/<session-id>/
```

不要用冗长逐行 diff 代替结论。

## Quality Check

- [ ] profile 由风险而非单纯 LOC 决定
- [ ] change units 按行为/模块边界切分
- [ ] 并行 agent 没有写同一文件
- [ ] reviewer 没有重复读取无关完整 diff
- [ ] findings 已按 fingerprint 去重
- [ ] auditor 只处理 blocking 和 audit-candidate risks
- [ ] 会争用共享环境的 audit/test 已串行或隔离
- [ ] 后续 round 使用增量 range
- [ ] 每个修复都有 verification to close
- [ ] 最终测试结果来自真实执行
