---
type: concept
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 6
tags: [AI, Agent, 架构, 设计模式, LLM, Agent系统]
aliases: [Harness模式, Agent Harness, batteries-included agent harness]
relates_to:
  - target: "[[DeepAgents]]"
    type: implemented_by
    confidence: 0.95
  - target: "[[DeepAgents中间件体系]]"
    type: related_to
    confidence: 0.9
  - target: "[[DeepAgents后端协议]]"
    type: related_to
    confidence: 0.9
  - target: "[[Pi-Agent]]"
    type: implemented_by
    confidence: 0.9
  - target: "[[生成器-评估器架构]]"
    type: related_to
    confidence: 0.92
  - target: "[[上下文焦虑]]"
    type: related_to
    confidence: 0.85
  - target: "[[元控制框架]]"
    type: extends
    confidence: 0.9
  - target: "[[脑手分离架构]]"
    type: related_to
    confidence: 0.85
supersedes: null
---

# Agent Harness 模式

## 概述

**Agent Harness**（"马具"）是一种 AI Agent 工程架构模式：**不**从零实现 Agent 运行时，而是在现有 LLM 框架（如 LangGraph 的 `create_agent`）之上，通过**[[ROS (Robot Operating System)|中间件]]**、**后端协议**和**默认系统提示**，以可组合的方式叠加"规划、文件系统、子代理、[[上下文压缩]]"等通用能力，让用户开箱即用。代表实现：[[DeepAgents]]。

## 关键内容

### 核心哲学

- **组合优于继承**：能力通过工厂函数参数（`tools`、`middleware`、`backend`、`subagents` 等）声明，而非深继承树
- **在已有框架之上叠加**，而非另起炉灶——保留原框架（LangGraph）的流式、checkpoint、Studio 等完整生态
- **边界清晰**：
  - 存储与执行 → **Backend 协议**层
  - 工具注入与提示增强 → **Middleware** 层
  - 最终执行图 → **图编排层**（LangGraph `CompiledStateGraph`）

### 三层架构

```
后端层（Backend）    — 存储（状态/磁盘/远程）+ 执行（沙箱 shell）
中间件层（Middleware）— 工具注入 + 提示/消息改写 + 跨轮状态
图编排层（LangGraph）— create_agent → CompiledStateGraph
```

关键设计：**后端换皮、工具不变**——文件类工具语义固定，数据落点（内存状态/本地盘/远程沙箱）可切换，上层 API 不变。

### 中间件与普通工具的本质区别

| | 中间件（Middleware） | 普通工具（Tool） |
|--|--|--|
| 执行时机 | 每次 LLM 调用**前**拦截请求 | 模型选中后才执行 |
| 能力 | 修改系统提示/工具列表/消息；跨轮状态 | 无状态的业务动作执行 |
| 适用 | 全 SDK 消费者默认可用的横切能力 | 特定集成方的轻量定制 |

### 默认中间件栈顺序（DeepAgents 实现）

1. TodoListMiddleware（始终）
2. SkillsMiddleware（`skills` 参数有值时）
3. FilesystemMiddleware（始终）
4. SubAgentMiddleware（始终）
5. SummarizationMiddleware（始终）
6. PatchToolCallsMiddleware（始终）
7. AsyncSubAgentMiddleware（有异步子代理时）
8. 用户自定义 middleware（`middleware=` 参数）
9. AnthropicPromptCachingMiddleware（始终；非 Anthropic 模型静默忽略）
10. MemoryMiddleware（`memory=` 参数有值时）
11. HumanInTheLoopMiddleware（`interrupt_on=` 参数有值时）

**顺序设计决策**：缓存[[ROS (Robot Operating System)|中间件]]（9）在记忆[[ROS (Robot Operating System)|中间件]]（10）之前，避免记忆更新破坏 Anthropic prompt cache 前缀稳定性。

### Harness 模式的工程收益

- 用户无需了解 LangGraph 内部即可得到可用 Agent
- 同一 SDK 可在内存、本地盘、远程沙箱之间切换运行环境
- 能力通过参数渐进启用，零配置即可运行，按需扩展
- 图仍是 LangGraph 原生产物，与 checkpoint、流式、可观测性方案直接对接

### Pi Agent：极简 Harness 的反面验证

[[Pi-Agent]] 代表了 Harness 设计谱系的另一端——**极简主义**。相比 [[DeepAgents]] 的 batteries-included 方式（11 个[[ROS (Robot Operating System)|中间件]]、多后端协议），Pi 只有 4 个工具、< 1000 token 系统提示，却在 Terminal-Bench 基准测试中击败了工具集更丰富的 Agent。

这证明了 Harness 模式的关键变体：
- **[[DeepAgents]] 路线**：组合丰富的[[ROS (Robot Operating System)|中间件]]栈 → 适合企业级多场景
- **Pi 路线**：极简工具 + 精确上下文控制 → 适合高级用户精确编程

两者的共同点：都将 Model 与 Harness 清晰分离，都强调 [[Context-Engineering]] 的重要性。

### Anthropic 长时自主编码 Harness（三 Agent 系统）

[[Prithvi-Rajasekaran]] 在 Anthropic 构建的长时自主编码 Harness 代表了另一类 Harness 设计哲学——**面向任务能力边界的动态调整**：

```
Planner（1-4句 prompt → 完整产品规格 + 设计语言）
   ↓
Generator（按规格逐 Sprint 构建，Sprint 前先谈合约）← [[Sprint合约制]]
   ↓
Evaluator（Playwright MCP，点击测试运行中的应用 + 对照准则打分）
   ↓
Generator（修复 + 迭代，循环直到所有准则通过）
```

核心设计原则：**每个 Harness 组件都在弥补模型当前的某个不足——当模型能力提升时，这些组件就该被移除。** Opus 4.5 需要 Sprint 分解 + [[上下文重置]] 才能完成长时任务；Opus 4.6 发布后，这两个组件被移除，Harness 大幅简化而性能不降。

这与 [[DeepAgents]] 的"batteries-included"路线形成对比：
- **[[DeepAgents]] 路线**：预设丰富[[ROS (Robot Operating System)|中间件]]，适合企业多场景
- **[[Anthropic]] 任务 Harness 路线**：从最小 Harness 出发，随模型能力迭代减复杂度

### Harness 假设的过时风险

Harness 编码了关于"模型不能独立做什么"的假设，但这些假设会随模型进步而**过时**。[[Anthropic]] 发现：

- [[Claude-Sonnet-4-5|Claude Sonnet 4.5]] 会在接近上下文限制时过早结束任务（[[上下文焦虑]]），因此在 harness 中加入[[上下文重置]]
- 但同样的 harness 用于 Claude Opus 4.5 时，该行为消失了——重置变成了死重

这引出了 [[元控制框架]] 的设计哲学：不对具体 harness 有主见，而是对**围绕 Claude 的接口**有主见，使 harness 实现可随模型能力自由替换。

### 从 Harness 到 Meta-harness

[[Managed-Agents]] 代表了 Harness 模式的下一个演进阶段——**[[元控制框架]]**（[[元控制框架]]）：
- 定义通用接口（会话、harness、沙箱）而非具体实现
- 每个组件可独立失败和替换
- 通过 [[脑手分离架构]] 实现弹性：大脑（Claude + harness）与手（沙箱）和会话（事件日志）解耦
- 性能收益：p50 TTFT 下降 60%，p95 TTFT 下降 90%+

## 来源
- [[raw/books/deepagents-book-main/01-项目概览与仓库结构.md]]
- [[raw/books/deepagents-book-main/02-核心设计哲学与架构总览.md]]
- [[raw/articles/ai-tools/pi-agent/01-overview-philosophy.md]]
- [[raw/articles/ai-engineering/anthropic-engineering/Harness design for long-running application development.md]]
- [[raw/articles/ai-engineering/anthropic-engineering/Scaling Managed Agents_ Decoupling the brain from the hands.md]] — Meta-harness 与脑手分离
- [[raw/articles/ai-tools/ralph-loop/testing-patterns.md]] — Testing Patterns（外部验证原则、四种验证模式、验证失败处理树）

## 相关
- [[DeepAgents]] — batteries-included 代表
- [[Pi-Agent]] — 极简代表
- [[生成器-评估器架构]] — 三 Agent Harness 的核心架构模式
- [[Sprint合约制]] — 三 Agent Harness 的 Sprint 前谈判机制
- [[上下文焦虑]] — 驱动 Harness 中上下文重置设计的现象
- [[DeepAgents中间件体系]]
- [[DeepAgents后端协议]]
- [[Context-Engineering]]
- [[元控制框架]] — extends（Harness 模式的抽象演进）
- [[脑手分离架构]] — related_to（Harness 组件的解耦模式）
- [[Managed-Agents]] — implemented_by（Harness 模式的托管服务实现）
- [[Ralph Loop]] — implemented_by（面向自主编码的迭代循环 Harness 变体）
- [[Initializer Agent]] — related_to（Harness 的准备阶段模式）
- [[E2E 验证模式]] — related_to（Harness 的验证层设计模式）
