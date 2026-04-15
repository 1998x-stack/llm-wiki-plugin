# Skill 09：systematic-debugging — 4 阶段根因调试法

> **系列位置**：Superpowers 深度解析 · 第 9 篇  
> **SKILL.md 位置**：`skills/systematic-debugging/SKILL.md`  
> **Companion 文件**：`root-cause-tracing.md`、`defense-in-depth.md`、`condition-based-waiting.md`、`find-polluter.sh`  
> **触发描述**：`Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes`  
> **技能类型**：刚性（Rigid）——不允许在没有完成根因调查的情况下提出修复方案

---

## 一句话定位

`systematic-debugging` 用一条铁律——**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST**——以及 4 个必须按顺序完成的阶段，将"猜测式调试"替换为"证据驱动的根因调查"，再配合 3 个配套的专业技术参考文件，处理从简单 Bug 到测试污染的各种调试场景。

---

## 铁律（The Iron Law）

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

Phase 1（根因调查）是一个硬门（Hard Gate）。Agent 在没有完成 Phase 1 之前，不能提出任何修复方案。

> "违反流程的字面要求就是违反流程的精神。"

---

## 适用场景

技能适用于**任何**技术问题：

```
✅ 测试失败
✅ 生产 Bug
✅ 性能问题（意料之外的慢）
✅ 构建失败
✅ 任何"不按预期工作"的行为
```

---

## 高压场景下也不能跳过

技能明确列出了"最想跳过"的场景，并一一驳斥：

| 高压情境 | 为什么想跳过 | 为什么必须不跳过 |
|---------|-----------|--------------|
| 时间压力 / 紧急生产故障 | 猜测感觉更快 | 系统性方法比反复折腾（thrashing）快得多 |
| "只是一个小修复" | 问题看起来很明显 | 简单 Bug 也有根因 |
| 已经尝试了多次修复 | 筋疲力尽 / 沉没成本 | 这是架构问题的信号，需要重新审视 |
| 上次修复无效 | 沮丧 | 新信息需要重新分析，不是继续猜测 |
| 不完全理解问题 | 不确定 | 急于修复保证了返工 |

---

## 四个必须按顺序完成的阶段

```
Phase 1：根因调查（Root Cause Investigation）
         ↓
Phase 2：模式分析（Pattern Analysis）
         ↓
Phase 3：假设与验证（Hypothesis and Testing）
         ↓
Phase 4：实现修复（Implementation）
```

### Phase 1：根因调查

**目标：在触碰代码之前理解故障。**

**Step 1.1：仔细阅读错误信息**

```bash
# 不要只看最后一行！完整读 stack trace
# 记录：行号、文件路径、调用链

# ❌ 错误做法：看到 "TypeError: cannot read property of undefined" 就开始改代码
# ✅ 正确做法：读完整 stack trace，找到调用链的起点
```

**Step 1.2：稳定复现**

```
能稳定复现？
  是 → 记录精确的复现步骤
  否 → 收集更多数据（日志、环境变量、时序），先不要动代码
```

**在不能稳定复现之前，不要开始调查代码。** 不能复现的 Bug 无法被验证修复。

**Step 1.3：检查最近的变更**

```bash
# 看看最近改了什么
git diff HEAD~5..HEAD
git log --oneline -20

# 检查：
# - 代码变更
# - 依赖版本变更（package.json、requirements.txt）
# - 配置变更
```

**Step 1.4：诊断性插桩（Diagnostic Instrumentation）**

对于多组件系统，在**每个组件边界**处添加日志：

```python
# API 层
logger.debug(f"[API] Request received: {request.data}")

# Service 层
logger.debug(f"[Service] Processing: {data}")
logger.debug(f"[Service] Result: {result}")

# Database 层
logger.debug(f"[DB] Query: {sql}")
logger.debug(f"[DB] Response rows: {len(rows)}")
```

一次性添加完所有日志，然后运行，分析所有输出，找到**数据从哪个边界开始出错**。

不要边加日志边分析，先全量收集，再整体分析。

**Step 1.5：向后追踪数据流**

从错误发生处开始，逆着调用链向上追踪：

```
Error at: module_c.process() — 这里看到了异常
  ↑ Called by: module_b.transform() — 这里数据已经错了
  ↑ Called by: module_a.load() — 这里数据还是对的
  ↑ Root cause: module_a.load() 没有验证输入，接受了空值
```

这个"向后追踪"技术有专门的参考文件 `root-cause-tracing.md`。

---

### Phase 2：模式分析

**目标：找到工作状态和故障状态之间的差异。**

**Step 2.1：找到能正常工作的类似代码**

```python
# 如果用户登录在某些情况下有效，找到那个有效的情况
# 对比两者：有效路径 vs 失败路径
# 这是找到"差异点"最有效的方法
```

**Step 2.2：完整阅读参考实现**

不要浏览（skim），完整阅读。细节差异往往就藏在被跳过的部分。

**Step 2.3：列出所有差异**

无论多小，全部列出来：
- 参数名不同？
- 异步/同步不一致？
- 错误处理方式不同？
- 数据类型假设不同？

---

### Phase 3：假设与验证

**目标：用最小干预验证理论。**

**Step 3.1：形成单一假设**

```
"我认为根因是 X，因为 Y。"

例：
"我认为根因是 module_a.load() 传入了 None，因为 Phase 2 发现
 工作路径在调用 load() 前做了 None 检查，而失败路径没有。"
```

**Step 3.2：最小化测试**

```
一次只改一个变量。

❌ 同时修改 A 和 B，然后看是否修复
✅ 只修改 A，看结果；如果无效，撤销 A，再试 B
```

**Step 3.3：根据结果更新假设**

```
测试后：
  假设验证 → 进入 Phase 4
  假设证伪 → 形成新假设，重复 Step 3.1
```

---

### Phase 4：实现修复

**目标：针对根因的永久性修复。**

```
Step 4.1: 使用 TDD 技能写复现测试
           test('module_a rejects None input', ...)
           
Step 4.2: 实现最少的修复代码（只修根因，不"顺手"重构）

Step 4.3: 运行完整测试套件（确认修复有效，无回归）

Step 4.4: 写代码注释，解释为什么这样修复
          # None check required: upstream callers may pass None when...

Step 4.5: Commit（包含复现测试 + 修复代码）
```

---

## 3-Fix 规则：架构升级触发器

如果三次或更多次的修复尝试都失败了，**必须停止**，质疑基础架构：

**架构问题的信号**：
```
🔴 每次修复都暴露新的共享状态或耦合问题
🔴 修复需要大规模重构才能应用
🔴 每次修复都在其他地方创造新症状
```

**处理方式**：在尝试更多修复之前，先与人类合作伙伴讨论是否需要重新设计架构。这不是失败，是正确的工程判断。

---

## 高级技术参考文件

技能目录包含了 4 个配套的技术参考：

### root-cause-tracing.md — 根因追踪技术

**场景**：错误出现在深层调用栈，需要逆向追踪到触发点。

```python
# 在每个层级添加追踪日志
def process_data(data):
    logger.debug(f"[process_data] ENTER: {data}")
    result = transform(data)
    logger.debug(f"[process_data] EXIT: {result}")
    return result
    
# 追踪模式：
# ✅ 正确输入 → ✅ 正确输出    (这层没问题)
# ✅ 正确输入 → ❌ 错误输出    (根因就在这层)
```

### defense-in-depth.md — 多层防御

**场景**：修复了根因后，在多个层次加入验证，防止同类问题从其他入口进入。

```
Layer 1: API/Entry Point  →  验证外部输入
Layer 2: Business Logic   →  验证业务规则
Layer 3: Data Layer       →  验证数据完整性
Layer 4: Debug Guards     →  环境隔离（防止测试运行危险操作）
```

### condition-based-waiting.md — 条件等待替代硬超时

**场景**：测试中有异步等待，硬超时会导致测试不稳定（flaky tests）。

```typescript
// ❌ 硬超时（任意猜测 5 秒够不够）
await new Promise(resolve => setTimeout(resolve, 5000));

// ✅ 条件等待（等到状态满足，最多等 30 秒）
await waitFor(
    () => service.isReady(),
    { timeout: 30000, interval: 100 }
);
```

### find-polluter.sh — 测试污染排查工具

**场景**：某个测试在单独运行时通过，但在完整套件中运行时失败。这是测试污染（Test Pollution）——某个先前运行的测试改变了全局状态。

```bash
# find-polluter.sh 通过二分搜索找到污染源
./skills/systematic-debugging/find-polluter.sh

# 工作原理：
# 1. 确认失败测试在全套件中失败
# 2. 对测试列表做二分搜索
# 3. 找到最小的导致失败的测试组合
# 4. 确定污染源（那个影响了全局状态的测试）
```

---

## 红旗：必须停止并回到 Phase 1 的信号

```
🚩 "先快速修一下，之后再调查"
🚩 "就改一下 X 看看会不会好"
🚩 "我不完全理解，但这个可能有用"
🚩 在追踪数据流之前就提出解决方案
🚩 连续修复失败超过 3 次（架构问题信号）
```

---

## 与 TDD 技能的结合

```
systematic-debugging 找到根因
        ↓
Phase 4 开始
        ↓
激活 test-driven-development 技能
        ↓
先写复现测试（RED）
        ↓
写最少修复代码（GREEN）
        ↓
重构（REFACTOR）
        ↓
运行完整套件验证无回归
```

systematic-debugging 负责"找到问题在哪里"，TDD 负责"用正确的方式修复"。两者是天然的配对。

---

*上一篇：[Skill 08：test-driven-development] | 下一篇：[Skill 10：verification-before-completion]*
