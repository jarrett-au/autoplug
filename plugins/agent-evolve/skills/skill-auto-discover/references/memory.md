# 存储指令和记忆（CLAUDE.md 与自动记忆）

> 来源：<https://code.claude.com/docs/zh-CN/memory>

## 两种记忆系统

| 方面 | CLAUDE.md | 自动记忆 |
|------|-----------|---------|
| 谁编写 | 你 | Claude |
| 内容 | 指令和规则 | 学习和模式 |
| 范围 | 项目/用户/组织 | 每个 worktree |
| 加载 | 每个会话（完整） | 每个会话（前 200 行或 25KB） |
| 用途 | 编码标准、工作流、架构 | 构建命令、调试见解、偏好 |

## CLAUDE.md 文件位置与优先级

| 范围 | 位置 | 共享对象 |
|------|------|---------|
| **托管策略**（最高优先级） | `/Library/Application Support/ClaudeCode/CLAUDE.md`（macOS）/ `/etc/claude-code/CLAUDE.md`（Linux） | 组织所有用户 |
| **项目指令** | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 团队成员 |
| **用户指令** | `~/.claude/CLAUDE.md` | 仅自己（所有项目） |
| **本地指令** | `./CLAUDE.local.md`（加 .gitignore） | 仅自己（当前项目） |

> 更具体位置优先于更广位置。目录树向上遍历拼接所有 CLAUDE.md。

## CLAUDE.md 编写规则

- **大小**：每个文件 ≤200 行，否则消耗更多 context 并降低遵守度
- **结构**：Markdown 标题+项目符号分组
- **具体性**：可验证的指令（"2空格缩进" > "正确格式化"）
- **一致性**：矛盾规则会导致 Claude 任意选择

### 导入语法

```markdown
@README.md                           # 项目概述
@docs/git-instructions.md            # Git 工作流
@~/.claude/my-project-instructions.md # 个人偏好（跨 worktree）
```

- 相对路径相对于包含导入的文件解析
- 递归导入最大 5 跳
- 块级 HTML 注释 `<!-- -->` 在注入 context 前剥离（代码块内保留）

### AGENTS.md 兼容

已有 AGENTS.md 的项目可创建导入它的 CLAUDE.md：
```markdown
@AGENTS.md

## Claude Code 特有指令
对 src/billing/ 的更改使用 Plan Mode。
```

## .claude/rules/ 路径范围规则

规则可用 `paths` frontmatter 限定到特定文件：

```yaml
---
paths:
  - "src/api/**/*.ts"
  - "src/**/*.{ts,tsx}"
---
# API 开发规则
- 所有端点必须包括输入验证
```

- 无 `paths` 字段 → 启动时无条件加载
- 有 `paths` → 仅在 Claude 处理匹配文件时加载
- 支持 glob 模式：`**/*.ts`、`src/**/*`、`*.md`
- 支持符号链接（循环链接自动检测）

### 用户级规则

`~/.claude/rules/` 中的规则适用于所有项目，在项目规则**之前**加载（项目规则优先级更高）。

## 自动记忆

### 存储位置

```
~/.claude/projects/<project>/memory/
├── MEMORY.md          # 索引（前 200 行/25KB 加载到每个会话）
├── debugging.md       # 主题文件（按需读取）
├── api-conventions.md
└── ...
```

- 按项目隔离（同一 git 仓库的 worktree 共享）
- 机器本地，不跨机器/云共享

### 配置

```json
{ "autoMemoryEnabled": true }  // 默认开启
// 或环境变量：CLAUDE_CODE_DISABLE_AUTO_MEMORY=1
```

### 管理与调试

- `/memory` 命令：查看加载的文件、切换自动记忆、编辑文件
- 文件为纯 markdown，可直接编辑或删除
- 自定义存储位置：`{ "autoMemoryDirectory": "~/my-custom-memory-dir" }`

## 排除 CLAUDE.md（Monorepo）

```json
// .claude/settings.local.json
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

- 托管策略 CLAUDE.md **不可排除**
- 模式用 glob 与绝对路径匹配

## /compact 后的行为

- 项目根 CLAUDE.md：**自动重新注入**
- 子目录嵌套 CLAUDE.md：**不自动重新注入**，下次读取该目录时重新加载
- 仅对话中给出的指令：**不保留**（需写入 CLAUDE.md）

## 托管设置 vs 托管 CLAUDE.md

| 关注点 | 配置位置 |
|--------|---------|
| 阻止工具/命令/路径 | `permissions.deny` |
| 沙箱隔离 | `sandbox.enabled` |
| 环境变量/API 路由 | `env` |
| 认证/组织锁定 | `forceLoginMethod` |
| 代码样式/质量 | 托管 CLAUDE.md |
| 数据处理/合规 | 托管 CLAUDE.md |
| 行为指令 | 托管 CLAUDE.md |

> 设置 = 客户端强制；CLAUDE.md = 行为塑造（非硬强制）。

## 从其他目录加载

```bash
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config
```
