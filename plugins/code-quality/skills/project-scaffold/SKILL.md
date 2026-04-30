---
name: project-scaffold
description: |
  为项目生成生产级 Makefile、Docker 部署配置和 GitHub Actions CI/CD 工作流。
  当用户提到 Makefile、Docker、CI/CD、GitHub Actions、项目脚手架、部署配置时触发。
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Project Scaffold — Makefile / Docker / CI

为项目生成生产级的 Makefile、Docker 部署和 GitHub Actions CI/CD 配置。

## 核心原则

1. 先读懂项目再动手 — 技术栈、入口、端口、部署架构决定一切配置。
2. Makefile 是统一入口 — CI 直接调用 `make check`，不重复写步骤。
3. 配置贴合实际 — 不照搬模板，不添加项目未使用的服务和挂载。

## 工作流程

### Step 1: 项目分析

生成前必须确认：语言/框架、包管理器、入口文件、端口、前端是否内嵌于后端、是否需要额外服务、项目名称和 GitHub 路径。

关键决策 — 单体 vs 前后端分离：如果后端已 serve 前端静态文件（`StaticFiles`、SPA fallback 路由、缓存头中间件），用单镜像方案，不需要 Nginx 容器。

### Step 2: 生成文件

参考 `references/makefile.md`、`references/docker.md`、`references/ci.md`。

生成后运行 `make check`（含前端则加 `make ui-check`）验证通过。lint/type-check 错误正面修掉，不放宽配置。

## 工具链偏好

无特殊约束时优先使用：

| 领域 | 推荐 | 替代 |
|------|------|------|
| Python 包管理 | uv | pip |
| Python lint + format | ruff | black + flake8 |
| Python 类型检查 | mypy | pyright |
| Node.js 包管理 | pnpm | npm |
| Node.js format | prettier | — |
