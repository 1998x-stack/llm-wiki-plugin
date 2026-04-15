# Skill 08：test-driven-development — AI 编程 Agent 的 TDD 铁律

> **系列位置**：Superpowers 深度解析 · 第 8 篇  
> **SKILL.md 位置**：`skills/test-driven-development/SKILL.md`（357+ 行）  
> **Companion 文件**：`skills/test-driven-development/testing-anti-patterns.md`  
> **触发描述**：`Use when implementing any feature or bugfix, before writing implementation code`  
> **技能类型**：刚性（Rigid）——必须严格按流程执行，不允许适配

---

## 一句话定位

`test-driven-development` 是 Superpowers 最严苛的刚性技能。它以一条铁律为核心——**NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST**——并围绕这条铁律构建了一个有强制验证门（Mandatory Verification Gate）的 5 阶段循环，以及一张完备的合理化借口拦截表。

---

## 铁律（The Iron Law）

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

这条规则没有例外。如果生产代码在对应的测试失败被观察到之前就被写了，**这些代码必须被删除**。

具体规定（来自 SKILL.md 第 31-45 行）：
- ❌ 不能以"留作参考"的名义保留
- ❌ 不能"在写测试的同时适配已有代码"
- ❌ 不能在写测试时偷看已有实现
- ✅ **Delete means delete.** 删除后从测试开始重新实现

---

## TDD 适用范围

| 场景 | 要求 |
|------|------|
| 新功能实现 | **Always** |
| Bug 修复 | **Always** |
| 重构 | **Always** |
| 行为变更 | **Always** |
| 一次性原型 | 询问人类伙伴 |
| 代码生成（非业务逻辑） | 询问人类伙伴 |
| 配置文件 | 询问人类伙伴 |

> "想跳过 TDD 的冲动是合理化信号，不是合法的例外。"

---

## 5 阶段循环：带强制验证门的 RED-GREEN-REFACTOR

### Phase 1 — RED：写一个失败的测试

**写测试的要求**：

| 要求 | 正确做法 | 错误做法 |
|------|---------|---------|
| 每个测试只测一个行为 | 单一 `expect`，单一结果 | 一个测试验证邮件 AND 域名 AND 空格 |
| 清晰的测试名称 | `'retries failed operations 3 times'` | `'retry works'` 或 `'test1'` |
| 测试真实代码 | 调用真实函数 | 只断言 mock 被调用了 N 次 |
| 测试名描述行为 | `'rejects empty email'` | `'test email validation'` |

**测试是最好的使用示例**：写测试时，想象自己在写这个 API 的使用文档。

```typescript
// ✅ 好的 RED 测试——清晰描述行为
test('retries failed operations 3 times', async () => {
    let attempts = 0;
    const flaky = () => {
        attempts++;
        if (attempts < 3) throw new Error('temporary failure');
        return 'success';
    };
    
    const result = await withRetry(flaky);
    
    expect(result).toBe('success');
    expect(attempts).toBe(3);
});

// ❌ 坏的 RED 测试——测试 mock 行为
test('retry logic', async () => {
    const mockFn = jest.fn().mockResolvedValue('ok');
    await withRetry(mockFn);
    expect(mockFn).toHaveBeenCalled();  // 这测的是什么？
});
```

---

### Phase 2 — 验证 RED（强制验证门）

**不运行测试就不能进入 GREEN 阶段。**

运行测试后，必须确认 3 件事：

```
✅ 测试失败了（而不是因为语法错误"崩溃"了）
✅ 失败信息是预期的那条（function not defined / assertion failed / ...）
✅ 失败的原因是"功能缺失"，而不是"测试本身有 bug"
```

| 运行结果 | 处理方式 |
|---------|---------|
| 测试立刻通过 | 你在测试已有行为，修正测试，不能进入 GREEN |
| 测试因语法/导入错误崩溃 | 修正错误，重新运行，确认是正确的失败 |
| 测试以预期方式失败 | ✅ 进入 GREEN |

> 如果测试一写就通过了，要么是实现已经存在（测试不必要），要么是测试写错了（测试无效）。两种情况都要修正。

---

### Phase 3 — GREEN：写最少的实现代码

**"最少"不是"最简单"，而是"严格满足当前测试，不多一个功能"**。

```typescript
// ✅ 好的 GREEN 实现——严格最少
async function withRetry(operation: () => Promise<any>, maxRetries = 3) {
    let lastError: Error;
    for (let i = 0; i < maxRetries; i++) {
        try {
            return await operation();
        } catch (err) {
            lastError = err as Error;
        }
    }
    throw lastError!;
}
```

**明确禁止在 GREEN 阶段做的事**：
- ❌ 加可选参数（测试没有要求的）
- ❌ 加配置项
- ❌ 重构其他代码
- ❌ 实现测试还没覆盖的功能（YAGNI）

---

### Phase 4 — 验证 GREEN（强制验证门）

**运行完整测试套件**（不是只运行新测试）。

```
✅ 新测试通过
✅ 所有之前通过的测试仍然通过（无回归）
✅ 输出干净：无错误、无警告
```

| 结果 | 处理方式 |
|------|---------|
| 新测试失败 | 修改代码（不是测试） |
| 其他测试失败 | 先修复回归，再继续 |
| 全绿 + 输出干净 | ✅ 进入 REFACTOR |

---

### Phase 5 — REFACTOR：清理，但不添加行为

重构的目标：提升内部质量，不改变外部行为。

```
✅ 可以做：
  - 删除重复代码
  - 改善命名
  - 提取 helper 函数
  - 优化数据结构

❌ 不能做：
  - 加新功能
  - 改变接口
  - "顺手"修复其他地方
```

每次重构后立刻运行完整测试套件，确认仍然全绿。重构期间任何让测试变红的改动必须立刻撤销或修正。

---

## 合理化借口拦截表（Rationalization Table）

技能维护了一张完备的借口拦截表（来自 SKILL.md 第 257-270 行）：

| Agent 的借口 | 现实是什么 |
|------------|----------|
| "这太简单了，不需要测试" | 简单代码一样会坏。写测试只需要 30 秒。 |
| "我先实现，测试立刻就能通过，证明我写得好" | 测试立刻通过证明什么都没被检验。 |
| "测试后补达到同样的目标" | 测试先写 = "它应该做什么？"；测试后补 = "它做了什么？"——根本不同。 |
| "我已经手动测试过了" | 临时验证不是系统性验证，没有记录，无法重复运行。 |
| "删掉 X 小时的工作是浪费" | 沉没成本谬误。保留未验证的代码是技术债。 |

---

## 红旗：必须删代码、重新来的信号

出现以下任何一条，必须删除代码，重新从测试开始（来自 SKILL.md 第 272-288 行）：

```
🚩 代码在测试前写了
🚩 测试在实现后才写
🚩 测试一写就通过，没有代码变化
🚩 无法解释测试为什么失败
🚩 自己在合理化"就这一次"
🚩 "这只是精神，不是仪式"的想法出现了
🚩 "保留作参考"或"适配已有代码"
```

---

## Testing Anti-Patterns（测试反模式）

技能配套了 `testing-anti-patterns.md`，它在以下场景会被自动加载：
- 写或修改测试时
- 添加 mock 时
- 考虑在生产类上加测试专用方法时

### 三条铁律（Iron Laws of Testing）

```
1. 永远不要测试 mock 的行为
2. 永远不要在生产类上加测试专用方法
3. 永远不要在不理解依赖的情况下 mock
```

### 主要反模式汇总

| 反模式 | 违反示例 | 正确做法 |
|-------|---------|---------|
| **测试 Mock 行为** | `expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument()` | 测试真实组件，或不 mock 它 |
| **生产类上的测试方法** | `class Session { async destroy() {...} }` — destroy 只为测试存在 | 把清理逻辑移到 `test-utils/` |
| **不理解依赖就 Mock** | Mock 一个其实有必要副作用的方法 | 在正确的层级 mock（如慢的外部调用） |
| **不完整的 Mock** | `const mockResponse = { status: 'success' }` — 缺少真实 API 的其他字段 | 镜像真实 API 的完整响应 schema |

---

## 完成前验证清单

标记任何任务完成之前，必须检查：

```
□ 每个新函数/方法都有测试
□ 观察到了每个测试在实现前失败
□ 每个测试失败的原因是"功能缺失"而不是"测试 bug"
□ 写了最少的代码让每个测试通过
□ 所有测试通过
□ 输出干净（无错误、无警告）
□ 测试使用真实代码（mock 只在不可避免时使用）
□ 边界条件和错误路径有覆盖
```

任何一项没有打勾 = TDD 被跳过了 = 必须重来。

---

## Bug 修复的 TDD 完整流程

```
发现 Bug
  ↓
1. 写一个能复现 Bug 的失败测试
   test('rejects empty email', async () => {
     const result = await submitForm({ email: '' });
     expect(result.error).toBe('Email required');
   });
  ↓
2. 运行，确认测试失败（复现了 Bug）
  ↓
3. 写最少的修复代码
  ↓
4. 运行，确认测试通过（Bug 已修复）
  ↓
5. 运行完整测试套件（无回归）
  ↓
6. Commit（包含复现测试 + 修复代码）
```

**关键**：复现测试是修复的一部分，不能省略。它不仅验证修复，还防止 Bug 在未来回归。

---

## 与其他技能的关系

```
writing-plans → 每个 Task 都内置 RED/GREEN/REFACTOR 步骤
                Plan 已经把 TDD 步骤写好了，子 Agent 只需执行

subagent-driven-development → 派遣的实现子 Agent 被要求遵循 TDD
                               spec-reviewer 会检查测试是否到位

systematic-debugging → 找到根因后，Phase 4 修复使用 TDD 技能
                        先写复现测试，再写修复代码
```

---

*上一篇：[Skill 07：dispatching-parallel-agents] | 下一篇：[Skill 09：systematic-debugging]*
