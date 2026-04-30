# GitHub Actions CI/CD 参考

## ci.yml — PR 检查

CI 直接调用 `make check` / `make ui-check`，不在 workflow 里重复写 lint/test 步骤。

```yaml
name: Development

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
    paths-ignore:
      - 'docs/**'
      - '.gitignore'
      - 'README.md'
```

### Python 后端（uv）

```yaml
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - run: uv sync
      - run: make check
```

### Go 后端

```yaml
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'
          cache: true
      - run: make check
```

### Node.js 前端（pnpm）

```yaml
  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: 10
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
          cache-dependency-path: frontend/pnpm-lock.yaml
      - run: pnpm install --frozen-lockfile
        working-directory: frontend
      - run: make ui-check
```

### 系统依赖（按需）

```yaml
      - name: Install system dependencies
        run: |
          sudo apt-get update && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
            portaudio19-dev
```

### 私有 Go 模块（按需）

```yaml
      - name: Configure git for private modules
        run: |
          git config --global url."https://${{ secrets.GH_ACCESS_TOKEN }}@github.com".insteadOf "https://github.com"
```

## release.yml — 发布流程

触发：push tag `v*.*.*` 或 workflow_dispatch 手动触发。

```yaml
name: Release
run-name: Publish artifacts by @${{ github.actor }}

on:
  push:
    tags:
      - "v*.*.*"
  workflow_dispatch:
    inputs:
      only_build_image:
        description: "Only build image, default is true"
        required: true
        type: boolean
        default: true
      commit:
        description: "Commit sha to build from"
        required: false
        type: string
      image_tag:
        description: "Docker image tag (e.g. v1.2.3)"
        required: false
        type: string

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}
```

### 流程

```
resolve-image-tag → build-amd64 ─┐
                  → build-arm64 ─┤→ merge-manifest → publish-release
```

### resolve-image-tag

```yaml
  resolve-image-tag:
    runs-on: ubuntu-latest
    outputs:
      image_tag: ${{ steps.resolve.outputs.image_tag }}
      source_ref: ${{ steps.resolve.outputs.source_ref }}
      only_build_image: ${{ steps.resolve.outputs.only_build_image }}
      push_latest: ${{ steps.resolve.outputs.push_latest }}
      publish_release: ${{ steps.resolve.outputs.publish_release }}
    steps:
      - name: Resolve release inputs
        id: resolve
        run: |
          if [ "${{ github.event_name }}" = "workflow_dispatch" ]; then
            TAG="${{ github.event.inputs.image_tag }}"
            SOURCE_REF="${{ github.event.inputs.commit }}"
            ONLY_BUILD_IMAGE="${{ github.event.inputs.only_build_image }}"
            if [ -z "$SOURCE_REF" ]; then
              SOURCE_REF="${{ github.sha }}"
            fi
            if [ -z "$TAG" ] && [ "$ONLY_BUILD_IMAGE" = "true" ]; then
              SHORT_SHA="${SOURCE_REF:0:7}"
              TIMESTAMP="$(date -u +'%Y%m%d%H%M%S')"
              TAG="${SHORT_SHA}-${TIMESTAMP}"
            fi
            if [ "$ONLY_BUILD_IMAGE" = "true" ]; then
              PUSH_LATEST="false"
              PUBLISH_RELEASE="false"
            else
              PUSH_LATEST="true"
              PUBLISH_RELEASE="true"
            fi
          else
            TAG="${{ github.ref_name }}"
            SOURCE_REF="${{ github.sha }}"
            ONLY_BUILD_IMAGE="false"
            PUSH_LATEST="true"
            PUBLISH_RELEASE="true"
          fi
          echo "image_tag=$TAG" >> "$GITHUB_OUTPUT"
          echo "source_ref=$SOURCE_REF" >> "$GITHUB_OUTPUT"
          echo "only_build_image=$ONLY_BUILD_IMAGE" >> "$GITHUB_OUTPUT"
          echo "push_latest=$PUSH_LATEST" >> "$GITHUB_OUTPUT"
          echo "publish_release=$PUBLISH_RELEASE" >> "$GITHUB_OUTPUT"
```

逻辑：
- tag push: image_tag = tag 名，推 latest，发布 Release
- workflow_dispatch + only_build_image: image_tag = `{sha}-{timestamp}`，不推 latest
- workflow_dispatch + 完整发布: 同 tag push

### 多架构构建

amd64 和 arm64 分别在不同 runner 上并行构建：

```yaml
  build-amd64:
    runs-on: ubuntu-latest
    needs: [resolve-image-tag]
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ needs.resolve-image-tag.outputs.source_ref }}

      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/setup-buildx-action@v3

      - uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          platforms: linux/amd64
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ needs.resolve-image-tag.outputs.image_tag }}-amd64
```

ARM64 runner（`ubuntu-24.04-arm`）可能没有预装 Docker，需要检测并安装：

```yaml
  build-arm64:
    runs-on: ubuntu-24.04-arm
    needs: [resolve-image-tag]
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ needs.resolve-image-tag.outputs.source_ref }}

      - name: Ensure Docker is available
        run: |
          if ! command -v docker >/dev/null 2>&1; then
            sudo apt-get update
            sudo apt-get install -y docker.io
          fi
          sudo systemctl start docker || sudo service docker start || true
          sudo chgrp docker /var/run/docker.sock || true
          sudo chmod 660 /var/run/docker.sock || true
          if ! docker info >/dev/null 2>&1; then
            sudo chmod 666 /var/run/docker.sock || true
          fi
          docker info >/dev/null

      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/setup-buildx-action@v3

      - uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          platforms: linux/arm64
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ needs.resolve-image-tag.outputs.image_tag }}-arm64
```

### merge-manifest

合并 amd64 和 arm64 为多架构 manifest：

```yaml
  merge-manifest:
    runs-on: ubuntu-latest
    needs: [resolve-image-tag, build-amd64, build-arm64]
    permissions:
      contents: read
      packages: write
    steps:
      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/setup-buildx-action@v3

      - name: Create and push multi-arch manifest
        run: |
          TAG="${{ needs.resolve-image-tag.outputs.image_tag }}"
          IMAGE="${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}"
          if [ "${{ needs.resolve-image-tag.outputs.push_latest }}" = "true" ]; then
            docker buildx imagetools create \
              -t ${IMAGE}:${TAG} \
              -t ${IMAGE}:latest \
              ${IMAGE}:${TAG}-amd64 \
              ${IMAGE}:${TAG}-arm64
          else
            docker buildx imagetools create \
              -t ${IMAGE}:${TAG} \
              ${IMAGE}:${TAG}-amd64 \
              ${IMAGE}:${TAG}-arm64
          fi

      - name: Print image summary
        run: |
          IMAGE="${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ needs.resolve-image-tag.outputs.image_tag }}"
          {
            echo "## Image Summary"
            echo ""
            echo "- Image: \`${IMAGE}\`"
            if [ "${{ needs.resolve-image-tag.outputs.push_latest }}" = "true" ]; then
              echo "- Also pushed: \`:latest\`"
            fi
            echo "- Source commit: \`${{ needs.resolve-image-tag.outputs.source_ref }}\`"
          } >> "${GITHUB_STEP_SUMMARY}"
```

### publish-release

```yaml
  publish-release:
    runs-on: ubuntu-latest
    needs: [resolve-image-tag, merge-manifest]
    if: needs.resolve-image-tag.outputs.publish_release == 'true'
    permissions:
      contents: write
    steps:
      - uses: softprops/action-gh-release@v2
        with:
          tag_name: ${{ needs.resolve-image-tag.outputs.image_tag }}
          name: Release ${{ needs.resolve-image-tag.outputs.image_tag }}
          target_commitish: ${{ needs.resolve-image-tag.outputs.source_ref }}
          generate_release_notes: true
          body: |
            ## Container Image
            ```bash
            docker pull ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ needs.resolve-image-tag.outputs.image_tag }}
            ```
```
