---
name: write-tests
description: |
  编写高质量测试——覆盖后端 API、Service、前端组件。涵盖 pytest + FastAPI、Vitest + RTL、Go testing。
  触发时机：实现新功能、修复 bug、测试失败、用户要求写测试。
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# 测试编写原则

测试是代码的"保险单"——好的测试让重构无畏，坏的测试是脱不掉的枷锁。

## 测试优先级的艺术

不是所有代码都值得同等测试投入。优先测试：

1. **契约边界**（API endpoints、public interfaces）— 改这里影响所有人
2. **业务逻辑核心**（计算、转换、策略选择）— bug 代价最高
3. **集成路径**（模块间交互、数据流）— 单元全绿但集成崩盘最常见
4. **边缘情况**（空输入、并发、异常路径）— 容易漏掉

不要为琐碎的工具函数、简单的 getter/setter、或者几乎不会改动的配置代码写详细测试。

## 好的测试的三条标准

**确定性** — 每次运行结果相同，不依赖时间、网络、随机数。 flaky test 比没测试更糟糕。

**独立性** — 每个测试自己 setup/teardown，不依赖其他测试的运行顺序或遗留状态。

**可读性** — 测试即文档。看测试名就知道测什么，看 setup 就知道 given，看断言就知道 then。

## 核心模式：Arrange - Act - Assert

```python
def test_transfer_funds_deducts_from_sender():
    # Arrange
    sender = create_account(balance=1000)
    recipient = create_account(balance=0)

    # Act
    transfer(sender, recipient, amount=300)

    # Assert
    assert sender.balance == 700
    assert recipient.balance == 300
```

```typescript
it('deducts amount from sender balance', async () => {
  // Arrange
  const sender = createAccount({ balance: 1000 })
  const recipient = createAccount({ balance: 0 })

  // Act
  await transfer(sender, recipient, { amount: 300 })

  // Assert
  expect(sender.balance).toBe(700)
  expect(recipient.balance).toBe(300)
})
```

每个测试只验证一个行为。多个断言可以，但必须围绕同一个概念。

---

## 何时写测试

### TDD（测试驱动开发）— 适合复杂逻辑

```
红 → 写一个跑不通的测试
绿 → 最快速度让测试通过
重构 → 清理代码，保持测试绿色
```

对于计算逻辑、状态机、策略选择，TDD 效果最好。先写测试迫使你思考接口设计。

### 伴随实现 — 适合大多数功能

写完功能顺手动笔，不需要完美，但至少覆盖：
- happy path（正常输入 → 正常输出）
- 主要错误路径（无效输入 → 合适错误）
- 边界情况（空值、最大值、特殊字符）

### 回归测试 — 适合 bugfix

修 bug 时写一个测试复现那个 bug，确保它不再回来。如果修复后发现没有现有测试覆盖这个场景，先补测试。

---

## Mock 和 Stub 的分寸

**需要 mock 的**：
- 外部服务（数据库、HTTP API、文件系统）
- 非确定性来源（时间、随机数）
- 复杂子系统的细节（不想测的实现细节）

**不要 mock 的**：
- 被测代码本身
- 值对象（简单的 data class、dict）
- 边界内的简单逻辑

Mock 的层次：
- **Stub** — 返回固定值，用于控制输入
- **Spy** — 记录调用，用于验证交互
- **Mock** — 预设期望，用于验证行为

过多 mock 是测试过度耦合实现的信号。如果换个实现测试就全挂了，说明在测"实现"而不是"行为"。

### 常见浏览器 API Mock

jsdom/happy-dom 环境下，以下 API 需要显式 mock 以避免警告或错误：

```typescript
// src/test/setup.ts - 测试环境统一配置

// Mock localStorage（避免 happy-dom 警告：--localstorage-file was provided without a valid path）
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
  length: 0,
  key: vi.fn(),
}
globalThis.localStorage = localStorageMock as Storage

// Mock IntersectionObserver（常用于懒加载组件）
globalThis.IntersectionObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}))

// Mock ResizeObserver（常用于自适应布局）
globalThis.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}))

// Mock window.matchMedia（常用于响应式/暗色模式检测）
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
})
```

**原则**：在测试 setup 中集中 mock，避免在每个测试文件中重复。测试不需要持久化功能，mock 版本足够。

---

## 测试命名

好的测试名 = 活着的文档。不需要冗余的前缀（`test_` 后缀之类），让名字本身有意义。

```
✅ 清晰：
   test_transfer_funds_deducts_sender_balance
   test_transfer_funds_credits_recipient_balance
   test_transfer_with_insufficient_balance_raises_error

❌ 模糊：
   test_transfer_1
   test_transfer_funds
   test_error_case
```

对于 API 测试，可以带上 HTTP 方法和路径：

```
test_POST_/api/v1/tasks_creates_task
test_GET_/api/v1/tasks/:id_returns_404_for_missing
```

---

## 边缘情况的思维框架

写测试时强迫自己想三个问题：

1. **空和零** — 空字符串、空列表、零、null、None
2. **边界** — 最大值、最小值、第一个、最后一个
3. **错误** — 无效类型、超大输入、格式错误的 payload

常见的边缘场景：

| 类型 | 示例 |
|------|------|
| 空输入 | `[]`、`{}`、`""`、`null` |
| 单元素 | `[1]`、`{"a": 1}` |
| 重复值 | `[1, 1, 1]` |
| 极端值 | `MAX_INT`、`"" * 10000` |
| 错误格式 | 非 JSON、错误的枚举值 |
| 并发 | 同一资源同时读写 |
| 权限 | 未认证、错误角色 |

---

## 测试结构参考

### API Endpoint 测试

```
tests/
└── api/
    └── test_<router>.py    # 按 router 分组
```

每个 endpoint 测四个问题：
1. 未授权？（401/403）
2. 正常请求成功？（200/201）
3. 参数错误？（422 validation error）
4. 资源不存在？（404）

### Service/Unit 测试

```
tests/
└── services/
    └── test_<service>.py   # 按 service 分组
```

测行为，不是测实现：
- 给定输入 X，输出 Y 吗？
- 给定错误条件 Z，抛出预期的异常吗？
- 状态变迁正确吗？

### 集成测试

```
tests/
└── integration/
    └── test_<workflow>.py  # 按用户流程分组
```

测端到端场景，不 mock 数据库或核心服务。保留外部 HTTP 调用但用 recorded responses 或 test doubles。

---

## 常见错误

**1. 断言不足** — 只测返回码，不测响应体
```python
# ❌ 弱
assert response.status_code == 200
# ✅ 强
assert response.status_code == 200
assert response.json()["id"] == expected_id
assert response.json()["status"] == "pending"
```

**2. 重复造 mock** — 每个测试文件都写一遍 `MockRedis`
→ 提取到 `tests/fixtures/` 或测试工具模块

**3. 共享可变状态** — 测试间不隔离
→ 每个测试自己 setup，用 fresh fixtures

**4. 测实现细节** — 过度 mock 内部方法
→ 改实现方式测试就挂。测 public contract。

**5. 测试不清理** — 留下文件、数据库记录、内存状态
→ teardown 在 finally/afterEach 里

**6. 随机失败不处理** —  flaky test 是技术债
→ 先标记 `@pytest.mark.flaky(reruns=3)`，然后修复

---

## 运行和验证

```bash
# 快速反馈：只跑改过的文件相关测试
pytest tests/ -k "test_name_contains"

# 覆盖率报告（找出未覆盖的分支）
pytest tests/ --cov=src --cov-report=html
pytest tests/ --cov=src --cov-report=term-missing

# 前端测试
vitest run                    # 单次
vitest run --coverage         # 覆盖率
vitest --watch                # watch 模式

# CI 模式：不能 interactive
CI=true npm test
```

---

## 框架速查

### pytest（Python）

```python
import pytest

# 异步测试
@pytest.mark.anyio
async def test_async():
    result = await my_function()
    assert result == expected

# 参数化：同一个测试多个输入
@pytest.mark.parametrize("input,expected", [
    ([1, 2], 3),
    ([], 0),
    ([-1], -1),
])
def test_sum(input, expected):
    assert sum(input) == expected

# fixture（setup/teardown）
@pytest.fixture
def fresh_db():
    db = create_test_db()
    yield db
    db.cleanup()
```

### Vitest + React Testing Library（JavaScript/TypeScript）

```typescript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

// 组件测试
describe('<LoginForm />', () => {
  it('submits credentials on button click', async () => {
    const user = userEvent.setup()
    const onSubmit = vi.fn()
    render(<LoginForm onSubmit={onSubmit} />)

    await user.type(screen.getByLabelText(/username/i), 'admin')
    await user.type(screen.getByLabelText(/password/i), '123')
    await user.click(screen.getByRole('button', { name: /submit/i }))

    expect(onSubmit).toHaveBeenCalledWith({
      username: 'admin',
      password: '123',
    })
  })
})
```

### Go（testing 标准库）

```go
func TestAdd(t *testing.T) {
    got := Add(2, 3)
    if got != 5 {
        t.Errorf("Add(2, 3) = %d; want 5", got)
    }
}
```
