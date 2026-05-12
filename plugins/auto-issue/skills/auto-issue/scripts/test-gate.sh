#!/usr/bin/env bash
# test-gate.sh — Auto-Issue 测试门脚本
# 由 autoissue-developer 的 SubagentStop hook 自动调用
# 读取 .claude-plugins-data/auto-issue/.test-env 获取项目配置，或自动检测

set -euo pipefail

cd "${CLAUDE_PROJECT_DIR:-.}"

# ── 加载配置 ──
TEST_ENV=".claude-plugins-data/auto-issue/.test-env"
if [[ -f "$TEST_ENV" ]]; then
  # shellcheck source=/dev/null
  source "$TEST_ENV"
fi

# ── 颜色 ──
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

fail=0

run_test() {
  local name="$1"
  local cmd="$2"

  if [[ -z "$cmd" || "$cmd" == "N/A" ]]; then
    echo -e "${YELLOW}⊘ ${name}: 未配置，跳过${NC}"
    return 0
  fi

  echo -e "\n${YELLOW}▶ ${name}: ${cmd}${NC}"
  if eval "$cmd"; then
    echo -e "${GREEN}✓ ${name}: 通过${NC}"
  else
    echo -e "${RED}✗ ${name}: 失败${NC}"
    fail=1
  fi
}

# ── 如果有配置文件，按配置执行 ──
if [[ -n "${UNIT_TEST_CMD:-}" ]]; then
  run_test "单元测试" "$UNIT_TEST_CMD"
  run_test "集成测试" "${INTEGRATION_TEST_CMD:-}"
  run_test "E2E 测试" "${E2E_TEST_CMD:-}"
else
  # ── 自动检测项目类型 ──
  echo -e "${YELLOW}⚠ 未找到 .claude-plugins-data/auto-issue/.test-env，自动检测项目类型${NC}\n"

  if [[ -f "pyproject.toml" ]] || [[ -f "setup.py" ]]; then
    # Python 项目
    if command -v uv &>/dev/null; then
      run_test "单元测试" "uv run pytest tests/ -q --tb=line 2>/dev/null || uv run pytest -q --tb=line"
    elif command -v pytest &>/dev/null; then
      run_test "单元测试" "pytest tests/ -q --tb=line 2>/dev/null || pytest -q --tb=line"
    else
      echo -e "${RED}✗ Python 项目但未找到 pytest/uv${NC}"
      fail=1
    fi

  elif [[ -f "package.json" ]]; then
    # JS/TS 项目
    if grep -q '"test"' package.json; then
      run_test "单元测试" "npm test"
    fi
    if grep -q '"test:e2e"' package.json; then
      run_test "E2E 测试" "npm run test:e2e"
    fi

  elif [[ -f "Cargo.toml" ]]; then
    run_test "单元测试" "cargo test"

  elif [[ -f "go.mod" ]]; then
    run_test "单元测试" "go test ./..."

  else
    echo -e "${RED}✗ 无法识别项目类型，请创建 .claude-plugins-data/auto-issue/.test-env 配置测试命令${NC}"
    fail=1
  fi
fi

# ── 结果 ──
echo ""
if [[ $fail -eq 0 ]]; then
  echo -e "${GREEN}🎉 所有测试通过${NC}"
  exit 0
else
  echo -e "${RED}💥 存在测试失败，请修复后重试${NC}"
  exit 1
fi
