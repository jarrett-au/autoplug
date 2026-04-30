# Docker 配置参考

## 文件布局

```
根目录/
├── Dockerfile
├── docker-compose.yml         # 生产部署 — 放根目录，服务器只需复制少量文件
├── .dockerignore
├── .env.example
└── docker/
    └── docker-compose.local.yml   # 本地构建 — 需要 context: .. 引用上级
```

## Dockerfile — 多阶段构建

### Python + 前端（uv + pnpm，单体模式）

```dockerfile
# --- Stage 1: Python 依赖 ---
FROM python:3.13-slim AS python-deps
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# --- Stage 2: 前端构建 ---
FROM node:20-alpine AS frontend-build
RUN corepack enable && corepack prepare pnpm@latest --activate
WORKDIR /app/frontend
COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY frontend/ ./
RUN pnpm build

# --- Stage 3: 运行时 ---
FROM python:3.13-slim AS runtime
WORKDIR /app
COPY --from=python-deps /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY backend/ ./backend/
COPY main.py ./
COPY --from=frontend-build /app/frontend/dist ./frontend/dist
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Go

```dockerfile
FROM golang:1.22-alpine AS build
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /app/bin/server ./cmd/server

FROM alpine:3.19 AS runtime
COPY --from=build /app/bin/server /usr/local/bin/server
EXPOSE 8080
CMD ["server"]
```

## docker-compose.yml（根目录，生产）

```yaml
name: my-project

services:
  app:
    image: ${APP_IMAGE:-ghcr.io/org/repo:latest}
    container_name: my-project
    pull_policy: ${PULL_POLICY:-always}
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./config:/app/config:ro
    ports:
      - "${SERVER_PORT:-8080}:8080"
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8080/health || exit 1"]
      interval: 10s
      timeout: 3s
      retries: 5
      start_period: 10s
```

`name:` 必须设置，否则 Docker Desktop 用文件夹名显示。

### Healthcheck 选择

```yaml
# 有 curl
test: ["CMD-SHELL", "curl -f http://localhost:8080/health || exit 1"]
# 有 wget（alpine）
test: ["CMD-SHELL", "wget --spider -q http://localhost:8080/health || exit 1"]
# 纯 Python（无 curl/wget）
test: ["CMD-SHELL", "python3 -c \"import urllib.request; urllib.request.urlopen('http://localhost:8080/health', timeout=2)\""]
```

## docker/docker-compose.local.yml（子目录，本地构建）

```yaml
name: my-project

services:
  app:
    build:
      context: ..
      dockerfile: Dockerfile
    container_name: my-project-local
    restart: unless-stopped
    volumes:
      - ../config:/app/config:ro
    ports:
      - "${SERVER_PORT:-8080}:8080"
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8080/health || exit 1"]
      interval: 5s
      timeout: 5s
      retries: 10
      start_period: 5s
```
