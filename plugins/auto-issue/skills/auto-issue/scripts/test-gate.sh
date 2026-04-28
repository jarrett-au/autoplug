#!/usr/bin/env bash
# test-gate.sh — Auto-Issue 测试门脚本
# 由 autoissue-developer 的 SubagentStop hook 自动调用
# 优先级: Makefile → .claude/.test-env → 自动检测

set -euo pipefail

cd "${CLAUDE_PROJECT_DIR:-.}"

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

# ── 检查 Makefile 中是否包含指定 target ──
makefile_has_target() {
  local target="$1"
  [[ -f "Makefile" ]] && grep -qE "^[[:space:]]*${target}[[:space:]]*:" Makefile
}

# ── 优先级 1: Makefile ──
if [[ -f "Makefile" ]]; then
  make_cmd=""
  make_name=""

  # 优先级: check > ui-check > test (check 通常整合了 lint+format+test)
  if makefile_has_target "check"; then
    make_cmd="make check"
    make_name="make check"
  elif makefile_has_target "ui-check"; then
    make_cmd="make ui-check"
    make_name="make ui-check"
  elif makefile_has_target "test"; then
    make_cmd="make test"
    make_name="make test"
  fi

  if [[ -n "$make_cmd" ]]; then
    echo -e "${YELLOW}⚠ 检测到 Makefile，优先使用 ${make_name}${NC}"
    run_test "${make_name}" "$make_cmd"
  fi
fi

# ── 优先级 2: .claude/.test-env 配置 ──
TEST_ENV=".claude/.test-env"
if [[ -f "$TEST_ENV" ]]; then
  # shellcheck source=/dev/null
  source "$TEST_ENV"

  # 如果 Makefile 已有覆盖命令，跳过 test-env（避免重复）
  if [[ -n "${make_cmd:-}" ]]; then
    echo -e "${YELLOW}ℹ Makefile 已覆盖测试执行，跳过 .test-env 配置${NC}"
  elif [[ -n "${UNIT_TEST_CMD:-}" ]]; then
    echo -e "${YELLOW}ℹ 使用 .claude/.test-env 配置${NC}"
    run_test "单元测试" "$UNIT_TEST_CMD"
    run_test "集成测试" "${INTEGRATION_TEST_CMD:-}"
    run_test "E2E 测试" "${E2E_TEST_CMD:-}"
  fi
fi

# ── 优先级 3: 自动检测（仅当上面两级都没命中时） ──
if [[ -z "${make_cmd:-}" && ! -f "$TEST_ENV" ]]; then
  echo -e "${YELLOW}⚠ 未找到 Makefile target 和 .claude/.test-env，自动检测项目类型${NC}\n"

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
    echo -e "${RED}✗ 无法识别项目类型，请创建 .claude/.test-env 或在 Makefile 中添加 test target${NC}"
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
