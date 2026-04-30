# Makefile 参考

## 结构

```makefile
.PHONY: help install run dev clean lint format type-check test check \
       docker-up docker-down docker-local-up docker-local-down

.DEFAULT_GOAL := help

help: ## 显示所有可用命令
	@printf "\n\033[1m项目名称\033[0m\n\n"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
```

每个 target 加 `## 描述`，自动出现在 help 中。

## 后端 targets

lint/format/type-check/test 各自独立，`check` 聚合。CI 直接调用 `make check`。

### Python（uv + ruff + mypy）

```makefile
lint: ## 代码检查
	uv run ruff check backend/ tests/ --fix

format: ## 代码格式化
	uv run ruff format backend/ tests/

type-check: ## 类型检查
	uv run mypy backend/ tests/

test: ## 运行测试
	uv run pytest tests/ -v

check: lint format type-check test ## 全部检查
```

### Go

```makefile
lint: ## 代码检查
	golangci-lint run ./...

format: ## 代码格式化
	gofmt -w .

test: ## 运行测试
	go test ./... -v -race

check: lint format test ## 全部检查
```

## 前端 targets（pnpm）

```makefile
ui-lint: ## 前端代码检查
	cd frontend && pnpm lint

ui-format: ## 前端格式化
	cd frontend && pnpm format

ui-type-check: ## 前端类型检查
	cd frontend && pnpm type-check

ui-test: ## 前端测试
	cd frontend && pnpm test

ui-check: ui-lint ui-format ui-type-check ui-test ## 前端全部检查
```

**package.json 脚本配置**（精简 CI 输出）：

```json
{
  "scripts": {
    "lint": "eslint . --quiet",
    "format": "prettier --write 'src/**/*.{ts,tsx,css}' --log-level warn",
    "format:check": "prettier --check 'src/**/*.{ts,tsx,css}' --log-level warn",
    "type-check": "tsc --noEmit",
    "test": "vitest --run --reporter dot"
  }
}
```

**关键点**：
- `eslint --quiet`：只显示错误，不显示警告
- `prettier --log-level warn`：只显示警告和错误，不列出每个文件（`--silent` 不存在）
- `tsc --noEmit`：tsc 默认就是安静模式，`--silent` 标志不存在
- `vitest --reporter dot`：点阵输出，替代默认的详细列表

**测试环境警告抑制**：

若测试中出现 `--localstorage-file was provided without a valid path` 警告（来自 happy-dom/Zustand persist），在 `src/test/setup.ts` 中 mock localStorage：

```typescript
// src/test/setup.ts
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
  length: 0,
  key: vi.fn(),
}
globalThis.localStorage = localStorageMock as Storage
```

## Docker targets

```makefile
docker-up: ## Docker 部署（拉取镜像）
	docker compose up -d

docker-down: ## Docker 停止
	docker compose down

docker-local-up: ## Docker 部署（本地构建）
	cd docker && docker compose -f docker-compose.local.yml up -d --build

docker-local-down: ## Docker 停止（本地）
	cd docker && docker compose -f docker-compose.local.yml down
```
