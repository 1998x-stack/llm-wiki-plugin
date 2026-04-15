# GSD 深度解析 · 第四篇
# 多智能体编排架构：11 个专家协作完成一个阶段

> **上一篇**：[第三篇——核心工作流五步法](./03-core-workflow.md)

---

## 一、为什么需要多智能体，而不是一个强大的主智能体？

直觉上，让一个智能体完成所有工作似乎更简单：给它所有信息，让它研究、规划、执行、验证。这不是更直接吗？

这个直觉在小规模任务中是对的。但在中大型项目中，它面临三个根本性限制：

**限制一：上下文污染的累积效应**

一个负责所有工作的主智能体，随着任务推进，它的上下文窗口会被研究报告、计划讨论、执行记录、错误诊断等各类信息填满。到第五个任务时，它的"注意力带宽"已经严重碎片化。

**限制二：角色冲突导致质量降级**

规划者和执行者需要不同的思维模式。规划者应该站在高处思考"整体需要什么"，执行者应该深入细节思考"这行代码怎么写"。让同一个智能体在两种模式间不断切换，两者都会做得更差。

**限制三：串行执行是性能瓶颈**

如果研究、规划、执行都在一个智能体的同一个上下文中串行进行，你会发现执行一个中等复杂度的阶段需要数小时——完全受限于单一的上下文窗口大小和推理速度。

**GSD 的答案：专家分工 + 并行编排**

> *"Every stage uses the same pattern: a thin orchestrator spawns specialized agents, collects results, and routes to the next step."*
> *"The orchestrator never does heavy lifting."*

---

## 二、GSD 的 11 个专家子智能体

### 2.1 子智能体全谱

| 智能体 ID | 职责 | 工作阶段 | 并发度 |
|-----------|------|----------|--------|
| `gsd-planner` | 基于研究生成 XML 结构化计划 | plan-phase | 串行 |
| `gsd-roadmapper` | 将需求分解为路线图阶段 | new-project | 串行 |
| `gsd-executor` | 执行单个 PLAN.md 中的任务 | execute-phase | **并行** |
| `gsd-phase-researcher` | 阶段专属领域研究 | plan-phase | **×4 并行** |
| `gsd-project-researcher` | 项目级领域研究 | new-project | **×4 并行** |
| `gsd-research-synthesizer` | 合并多份研究报告 | plan-phase | 串行 |
| `gsd-debugger` | 诊断失败根因，生成修复计划 | verify-work | 按需 |
| `gsd-codebase-mapper` | 棕地代码库分析 | map-codebase | **×4 并行** |
| `gsd-verifier` | 验证代码库是否达成阶段目标 | execute-phase | 串行 |
| `gsd-plan-checker` | 8 维度计划质量验证 | plan-phase | 串行 |
| `gsd-integration-checker` | 跨模块集成一致性检查 | execute-phase | 串行 |

### 2.2 每个子智能体详解

#### `gsd-phase-researcher`（×4 并行）

这是 GSD 中最常被调用的子智能体，每次 `plan-phase` 都会并行 spawn 4 个：

```
gsd-phase-researcher [stack]
职责：研究本阶段涉及的技术栈
输入：PROJECT.md（技术约束）+ CONTEXT.md（实现偏好）+ 阶段描述
典型输出：
  - Next.js App Router 中使用 WebSocket 的限制与替代方案
  - jose 和 jsonwebtoken 的 CommonJS/ESM 兼容性对比
  - Prisma ORM 在 Serverless 环境中的连接池配置

gsd-phase-researcher [features]
职责：研究功能实现的最佳方案
输入：CONTEXT.md（用户偏好）+ 阶段功能描述
典型输出：
  - 无限滚动的三种实现方案（Intersection Observer vs React Virtual vs 库）
  - 分页与游标分页的适用场景对比
  - 拖拽排序的 dnd-kit vs @dnd-kit/sortable 选型建议

gsd-phase-researcher [architecture]
职责：研究架构模式，确保与现有代码一致
输入：codebase/ARCHITECTURE.md + PROJECT.md + 阶段需求
典型输出：
  - 新功能如何融入现有的 Feature-Sliced Design 架构
  - 状态管理：全局 Zustand store 还是本地 useState
  - API 错误处理：统一在 middleware 还是各个端点

gsd-phase-researcher [pitfalls]
职责：研究已知问题、性能陷阱、版本兼容
输入：技术栈版本信息 + 功能描述
典型输出：
  - Vercel 边缘函数 CPU 时间限制（50ms），bcrypt 在边缘不可用
  - Next.js 14 App Router 中 cookies() 只能在 Server Component 中调用
  - Safari 不支持 EventSource 的 withCredentials
```

**为什么是 4 个维度而不是 1 个综合研究者？**

每个维度需要不同的搜索策略和关注点。技术栈研究者关注 API 文档和版本说明；陷阱研究者关注 GitHub Issues 和 Stack Overflow 的错误报告。如果合并成一个，它会在四个方向之间分散注意力，每个维度的深度都会降低。

#### `gsd-planner`

```
输入：
  - PROJECT.md（技术约束和禁令）
  - REQUIREMENTS.md（本阶段必须实现的 v1 需求）
  - CONTEXT.md（用户的实现偏好决策）
  - RESEARCH.md（四维研究结论）

职责：
  1. 综合所有输入，理解"需要做什么"和"如何做"
  2. 将工作分解为 2-3 个原子 XML 计划
  3. 每个计划控制在单个 200k 上下文可完成的规模内
  4. 分析计划间依赖关系，标记 <depends_on> 标签
  5. 确保垂直切片（每个计划是功能完整的端到端切片）

输出：N-01-PLAN.md, N-02-PLAN.md（等）
```

#### `gsd-plan-checker`

```
输入：gsd-planner 生成的所有 PLAN 文件

验证 8 个维度（详见第五篇）：
  1. 需求覆盖完整性
  2. 技术一致性（与 PROJECT.md 约定）
  3. 计划原子性（单上下文可完成）
  4. 依赖关系正确性
  5. 并行安全性（同波次无文件冲突）
  6. 可验证性（<verify> 包含可执行命令）
  7. 上下文一致性（与 CONTEXT.md 决策）
  8. Nyquist 验证覆盖（测试合约）

结果：
  PASS → 计划批准，流程推进到 execute-phase
  FAIL → 生成修订意见，返回 gsd-planner 修订
  最多循环 3 次，3 次后仍失败则上报给用户判断
```

#### `gsd-executor`

```
输入（最小化！）：
  - PROJECT.md（项目约束）
  - 当前 N-M-PLAN.md（XML 结构任务列表）

关键特性：
  - 拥有独立的干净 200k 上下文（不受其他执行者影响）
  - 逐任务执行，每任务完成立即 git commit --no-verify
  - <verify> 标签中的命令会被真正执行（curl, pnpm test 等）
  - 执行完成后退出，不保留历史状态

输出：N-M-SUMMARY.md（执行存档）+ git commits
```

#### `gsd-verifier`

```
输入：
  - PROJECT.md
  - REQUIREMENTS.md（本阶段 v1 需求）
  - 所有 N-M-SUMMARY.md（执行存档）

职责：
  - 不仅检查"代码是否存在"，而是检查"代码是否实现了需求"
  - 读取 git diff，检查 SUMMARY 中声明的工作是否反映在代码中
  - 运行关键测试命令，验证功能是否可用

结果：
  PASS → 生成 VERIFICATION.md（成功），告知用户可以进行 verify-work
  FAIL → 生成 VERIFICATION.md（失败 + 诊断），问题记录供 verify-work 处理
```

#### `gsd-debugger`

```
触发条件：verify-work 中用户报告某项验收失败

输入：
  - 用户描述的失败现象
  - 相关源代码文件
  - 对应的 PLAN.md（原始意图）
  - git diff（实际实现与原始意图的偏差）

职责：
  1. 复现分析：根据用户描述和代码推断失败路径
  2. 根因定位：找到最可能的失败原因（不是简单的"代码有 bug"）
  3. 修复规划：生成具体的修复计划（XML 格式，可直接被 execute-phase 执行）

输出：修复计划 PLAN 文件
```

#### `gsd-codebase-mapper`（×4 并行）

```
触发：/gsd:map-codebase（棕地项目使用）

gsd-stack-mapper     → STACK.md
  分析：package.json, Dockerfile, 配置文件
  输出：技术栈清单（语言版本、框架版本、主要依赖）

gsd-arch-mapper      → ARCHITECTURE.md
  分析：目录结构、模块划分、设计模式
  输出：架构描述（是否 monorepo、分层方式、关键抽象）

gsd-convention-mapper → CONVENTIONS.md
  分析：现有代码的命名规范、文件组织、注释风格
  输出：约定清单（供 gsd-planner 在生成新代码时遵守）

gsd-concern-mapper   → CONCERNS.md
  分析：已知 TODO、deprecated 代码、性能问题、安全风险
  输出：技术债务列表（供规划时避开或处理）
```

---

## 三、编排模式详解

### 3.1 编排者设计原则

GSD 的编排者（主会话中的 Claude）遵循一个铁律：**编排者永远不执行重型任务**。

```
编排者做的事（轻量）：
  ✅ 读取状态文件，判断当前阶段
  ✅ 构建子智能体的上下文（选择要加载哪些文件）
  ✅ spawn 子智能体（实际上是创建新的子会话）
  ✅ 等待子智能体完成，收集返回结果
  ✅ 解析结果，决定下一步路由
  ✅ 向用户呈现摘要，请求审批

编排者不做的事（重型）：
  ❌ 自己进行领域研究
  ❌ 自己生成代码
  ❌ 自己分析大量代码文件
  ❌ 自己运行调试诊断
```

**结果**：主会话的上下文窗口始终保持在 30-40% 使用率，整个开发过程中保持稳定的响应速度和质量。

### 3.2 波次并行执行的调度算法

当执行阶段开始，编排者：

```python
# 伪代码描述 GSD 的波次调度逻辑

def schedule_waves(plan_files):
    # 1. 解析所有计划的依赖关系
    dependency_graph = {}
    for plan in plan_files:
        deps = parse_depends_on(plan)
        dependency_graph[plan.id] = deps
    
    # 2. 拓扑排序，构建执行波次
    waves = []
    remaining = set(plan_files)
    completed = set()
    
    while remaining:
        # 找出所有依赖已完成的计划（可以立即执行）
        ready = {
            plan for plan in remaining 
            if all(dep in completed for dep in dependency_graph[plan.id])
        }
        waves.append(list(ready))
        completed |= ready
        remaining -= ready
    
    return waves

# 3. 按波次执行
for wave in waves:
    # 同波次的计划并行执行
    results = parallel_execute(wave)
    # 等待整个波次完成
    wait_for_all(results)
    # 才开始下一波次
```

**文件冲突检测**：如果同波次的两个计划都要修改同一个文件，plan-checker 会在验证阶段检测到这个冲突，要求将其中一个移到下一波次，或合并为同一个计划。

### 3.3 子智能体上下文构建策略

每个子智能体的上下文是精心构建的，不是无差别地传入所有信息：

```
gsd-executor 上下文构建：
  必须包含：
    - PROJECT.md（技术约束，防止错误选型）
    - 当前 PLAN.md（要执行的任务）
  
  不包含：
    - 其他阶段的 PLAN 文件
    - REQUIREMENTS.md（需求已在 PLAN 中蒸馏）
    - RESEARCH.md（研究结论已在 PLAN 中蒸馏）
    - 历史 SUMMARY.md（通过 git 历史访问）
    - CONTEXT.md（偏好已在 PLAN 中体现）

gsd-planner 上下文构建：
  必须包含：
    - PROJECT.md + REQUIREMENTS.md + CONTEXT.md
    - 所有 4 份研究报告（核心输入）
  
  不包含：
    - 其他阶段的计划或执行记录
    - 历史会话内容
```

这种精确的上下文构建确保每个子智能体的信号噪声比保持在最优状态。

---

## 四、模型分配策略

GSD 允许为不同智能体分配不同的模型，通过 `model_profile` 配置：

### 4.1 四种预设 Profile

| 智能体 | quality | balanced（默认） | budget | inherit |
|--------|---------|-----------|--------|---------|
| gsd-planner | Opus | **Opus** | Sonnet | 继承 |
| gsd-roadmapper | Opus | Sonnet | Sonnet | 继承 |
| gsd-executor | Opus | Sonnet | Sonnet | 继承 |
| gsd-phase-researcher | Opus | Sonnet | **Haiku** | 继承 |
| gsd-project-researcher | Opus | Sonnet | **Haiku** | 继承 |
| gsd-research-synthesizer | Sonnet | Sonnet | **Haiku** | 继承 |
| gsd-debugger | Opus | Sonnet | Sonnet | 继承 |
| gsd-codebase-mapper | Sonnet | **Haiku** | Haiku | 继承 |
| gsd-verifier | Sonnet | Sonnet | **Haiku** | 继承 |
| gsd-plan-checker | Sonnet | Sonnet | **Haiku** | 继承 |
| gsd-integration-checker | Sonnet | Sonnet | **Haiku** | 继承 |

### 4.2 模型分配哲学

**为什么 gsd-planner 在 balanced 模式下用 Opus？**

计划阶段是整个工作流中最关键的架构决策时刻：
- 如何将需求分解为原子任务？
- 哪些任务应该并行，哪些应该串行？
- 每个任务的边界在哪里？
- 技术选型是否与 PROJECT.md 约束一致？

这些决策的质量直接决定后续所有执行步骤的成败。用 Opus 在这里投资是值得的。

**为什么 gsd-codebase-mapper 在 balanced 模式下用 Haiku？**

代码库分析是信息提取任务，不需要复杂推理：
- 读取 package.json，列出技术栈（Haiku 完全胜任）
- 分析目录结构，描述架构（Haiku 胜任）
- 查找 TODO 注释（Haiku 胜任）

用 Haiku 分析代码库，节省大量 token 成本。

**为什么 gsd-phase-researcher 在 budget 模式下用 Haiku？**

研究任务虽然需要一定推理能力，但主要是信息检索和整理。在 budget 模式下（通常是成本敏感场景），Haiku 能提供足够质量的研究报告，节省更多 token 留给执行阶段。

### 4.3 自定义模型分配

如果预设 profile 不满足需求，可以在 `config.json` 中自定义：

```json
{
  "model_profile": "inherit",
  "model_overrides": {
    "gsd-planner": "o3",
    "gsd-executor": "o4-mini",
    "gsd-debugger": "o3",
    "gsd-phase-researcher": "gpt-4o-mini"
  }
}
```

这在使用 OpenRouter 或本地模型时特别有用——可以精确控制哪些智能体使用哪个模型，平衡性能和成本。

### 4.4 `inherit` 模式的使用场景

`inherit` 模式让所有子智能体继承主会话的当前模型。适合：

- **非 Anthropic 提供商**（OpenRouter, LM Studio）：避免 GSD 试图指定 Anthropic 模型 ID 导致 API 错误
- **非 Claude 运行时**（Gemini CLI, OpenCode, Codex）：各运行时有自己的模型选择机制
- **动态模型切换**：在 OpenCode 中用 `/model` 切换后，所有子智能体自动跟随

---

## 五、主会话上下文保持低占用的机制

GSD 声称主会话上下文始终保持在 30-40% 使用率。这是如何做到的？

**机制一：结果只接收摘要，不接收原始输出**

子智能体执行完成后，将完整结果写入文件（RESEARCH.md, PLAN.md, SUMMARY.md 等），编排者只接收"执行完成 + 文件路径"的简短通知，不接收完整的研究报告原文或完整代码。

**机制二：`/clear` 配合文件系统**

GSD 的官方使用指南中强调：

```bash
/gsd:new-project
/clear                   # ← 关键步骤
/gsd:discuss-phase 1
/clear
/gsd:plan-phase 1
# 不需要 /clear（plan-phase 主要工作在子智能体中）
/gsd:execute-phase 1
/clear
/gsd:verify-work 1
```

每个主要命令之间清空主会话，通过文件系统（而非上下文历史）传递信息。

**机制三：`/gsd:resume-work` 快速恢复**

清空上下文后，通过 STATE.md 和 ROADMAP.md 快速恢复项目状态，而不是重新阅读所有历史对话。

---

## 六、当多智能体协作失败时：`/gsd:forensics`

当工作流出现异常（子智能体失败、文件缺失、状态不一致）：

```bash
/gsd:forensics
```

`forensics` 智能体会检查：

```
1. Git 历史异常
   - 孤儿 commit（没有父提交的 commit）
   - 意外的分支状态
   - rebase 产生的历史重写痕迹

2. 规划产物完整性
   - 缺失的 PLAN/SUMMARY/VERIFICATION 文件
   - 文件间的交叉引用断裂
   - ROADMAP 状态与实际文件不匹配

3. 状态不一致
   - config.json 配置漂移
   - ROADMAP 显示完成但 SUMMARY 不存在

输出：诊断报告写入 .planning/forensics/
     包含：发现的问题 + 推荐修复步骤
```

---

## 小结

GSD 的多智能体架构体现了一个软件工程的经典原则：**单一职责原则（SRP）在 AI 系统层面的应用**。

每个子智能体有明确的职责边界，接收精确裁剪的上下文，产出结构化的输出，通过文件系统（而非共享内存）与其他智能体通信。

这种设计让 GSD 能够：
- **扩展**：增加新的专家子智能体不影响现有流程
- **调试**：任何一个子智能体的失败都有明确的隔离边界
- **优化**：为不同智能体配置不同模型，精确控制成本/质量比

下一篇，我们深入 GSD 的计划系统——XML schema 的设计细节和 8 维 plan-checker 的验证逻辑。

---

*参考：[GSD GitHub](https://github.com/gsd-build/get-shit-done) · [USER-GUIDE.md](https://github.com/gsd-build/get-shit-done/blob/main/docs/USER-GUIDE.md)*
