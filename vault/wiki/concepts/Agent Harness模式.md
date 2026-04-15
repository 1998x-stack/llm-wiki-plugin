---
type: concept
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 3
tags: [AI, Agent, 架构, 设计模式, LLM]
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
supersedes: null
---

# Agent Harness 模式

## 概述

**Agent Harness**（"马具"）是一种 AI Agent 工程架构模式：**不**从零实现 Agent 运行时，而是在现有 LLM 框架（如 LangGraph 的 `create_agent`）之上，通过**[[ROS (Robot Operating System)|中间件]]**、**后端协议**和**默认系统提示**，以可组合的方式叠加"规划、文件系统、子代理、上下文压缩"等通用能力，让用户开箱即用。代表实现：[[DeepAgents]]。

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

[[Pi-Agent]] 代表了 Harness 设计谱系的另一端——**极简主义**。相比 [[DeepAgents]] 的 batteries-included 方式（11 个[[ROS (Robot Operating System)|中间件]]、多后端协议），[[Pi-Agent|Pi]] 只有 4 个工具、< 1000 token 系统提示，却在 Terminal-Bench 基准测试中击败了工具集更丰富的 Agent。

这证明了 Harness 模式的关键变体：
- **[[DeepAgents]] 路线**：组合丰富的[[ROS (Robot Operating System)|中间件]]栈 → 适合企业级多场景
- **[[Pi-Agent|Pi]] 路线**：极简工具 + 精确上下文控制 → 适合高级用户精确编程

两者的共同点：都将 Model 与 Harness 清晰分离，都强调 [[Context-Engineering]] 的重要性。

## 来源
- [[raw/books/deepagents-book-main/01-项目概览与仓库结构.md]]
- [[raw/books/deepagents-book-main/02-核心设计哲学与架构总览.md]]
- [[raw/articles/ai-tools/pi-agent/01-overview-philosophy.md]]

## 相关
- [[DeepAgents]] — batteries-included 代表
- [[Pi-Agent]] — 极简代表
- [[DeepAgents中间件体系]]
- [[DeepAgents后端协议]]
- [[Context-Engineering]]
