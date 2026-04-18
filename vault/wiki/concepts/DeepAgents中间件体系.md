---
type: concept
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 9
tags: [AI, Agent, 中间件, LangChain, 架构, Agent系统]
aliases: [AgentMiddleware, DeepAgents middleware]
relates_to:
  - target: "[[DeepAgents]]"
    type: part_of
    confidence: 0.95
  - target: "[[Agent Harness模式]]"
    type: implements
    confidence: 0.9
  - target: "[[DeepAgents后端协议]]"
    type: related_to
    note: FilesystemMiddleware 依赖 BackendProtocol
    confidence: 0.9
supersedes: null
---

# DeepAgents 中间件体系

## 概述

[[DeepAgents]] [[ROS (Robot Operating System)|中间件]]（`libs/deepagents/deepagents/middleware/`）是 [[Agent Harness模式]] 的核心扩展点：每个[[ROS (Robot Operating System)|中间件]]继承 `AgentMiddleware`，重写 `wrap_model_call()` 在**每次 LLM 调用前**拦截请求，改写系统提示、工具列表或消息，实现横切能力（规划、文件系统、子代理、[[上下文压缩]]、记忆、人机协同等）。

## 关键内容

### 中间件机制

- 通过 `wrap_model_call(handler, request)` 拦截每次发往 LLM 的 `ModelRequest`
- 可修改：系统消息、工具列表、消息序列
- 可维护跨轮状态（配合 LangGraph state schema 的 reducer）
- **与普通工具的本质区别**：普通工具只在模型选中后执行；[[ROS (Robot Operating System)|中间件]]在每次 LLM 调用前统一预处理

### 各中间件详解

#### FilesystemMiddleware
注册文件操作工具（`ls`、`read_file`、`write_file`、`edit_file`、`glob`、`grep`），与 [[DeepAgents后端协议|BackendProtocol]] 绑定。当 backend 未实现 `SandboxBackendProtocol` 时，动态移除 `execute` 工具（防止误暴露执行面）。大文件策略：分页读取（`offset`/`limit`），结果驱逐（超限自动截断）。

#### SubAgentMiddleware
提供 `task` 工具，支持三种子代理规格：
- `SubAgent`（声明式，内联执行）
- `CompiledSubAgent`（已编译的 LangGraph 图）
- `AsyncSubAgent`（带 `graph_id` 的异步远程任务）

自动为子代理注入与主代理对齐的能力（Todo + Filesystem + Summarization + Patch + 可选 [[Agent Skills|Skills]] + 缓存），保证子调用"能力模型对齐"。

#### AsyncSubAgentMiddleware
处理异步/远程子代理（`AsyncSubAgent` 含 `graph_id`），提供生命周期工具：启动任务、查询状态、等待完成。仅在存在异步子代理时启用。

#### SummarizationMiddleware（工厂模式）
由 `create_summarization_middleware(model, backend)` 创建。两种触发模式：
- **自动**：token 计数超阈值时自动触发，用摘要替换旧消息历史
- **手动**：提供工具让模型主动压缩上下文
大型工具输出落盘（写入 backend 文件），减少上下文占用。

#### MemoryMiddleware
在 `memory=` 参数有值时启用。将指定记忆文件（如 `AGENTS.md`）内容注入系统提示，使 Agent 持有持久化指令/偏好知识。**放在[[ROS (Robot Operating System)|中间件]]栈尾部**（缓存之后），避免记忆更新破坏 [[Anthropic]] prompt cache 前缀。

#### SkillsMiddleware
在 `skills=` 参数有值时启用。从 backend 路径加载技能描述，注入系统提示，实现技能的**渐进式披露**（按需暴露，控制上下文长度）。

#### PatchToolCallsMiddleware
修正/规范化模型输出中格式异常的工具调用（悬空工具调用修复），提升与不同模型输出格式的兼容性。

#### AnthropicPromptCachingMiddleware
为 [[Anthropic]] 模型注入 prompt cache 头；非 [[Anthropic]] 模型时 `unsupported_model_behavior="ignore"` 静默跳过。**放在尾部靠前**，记忆/人机协同之前。

#### HumanInTheLoopMiddleware
在 `interrupt_on=` 参数有值时启用。配置哪些条件下暂停执行等待人工审批。放在栈最末尾。

#### TodoListMiddleware（来自 LangChain）
始终启用，提供 `write_todos` 工具，让 Agent 维护结构化待办列表，支持规划能力。

### 公共 API（`middleware/__init__.py` `__all__`）

```python
AsyncSubAgent, AsyncSubAgentMiddleware, CompiledSubAgent,
FilesystemMiddleware, MemoryMiddleware, SkillsMiddleware,
SubAgent, SubAgentMiddleware, SummarizationMiddleware,
SummarizationToolMiddleware, create_summarization_tool_middleware
```

### REPL 中间件（`libs/repl/`）

独立包 `langchain-repl`，提供 `ReplMiddleware`，支持在 REPL 场景中运行代码解释器，与 CLI/SDK 形成不同入口形态。

## 来源
- [[raw/books/deepagents-book-main/02-核心设计哲学与架构总览.md]]
- [[raw/books/deepagents-book-main/06-中间件体系总论.md]]
- [[raw/books/deepagents-book-main/07-FilesystemMiddleware-文件系统中间件.md]]
- [[raw/books/deepagents-book-main/08-SubAgentMiddleware-子代理中间件.md]]
- [[raw/books/deepagents-book-main/09-AsyncSubAgentMiddleware-异步子代理.md]]
- [[raw/books/deepagents-book-main/10-SummarizationMiddleware-上下文压缩.md]]
- [[raw/books/deepagents-book-main/11-MemoryMiddleware与SkillsMiddleware.md]]
- [[raw/books/deepagents-book-main/12-PatchToolCallsMiddleware与工具修复.md]]
- [[raw/books/deepagents-book-main/26-REPL中间件.md]]

## 相关
- [[DeepAgents]]
- [[Agent Harness模式]]
- [[DeepAgents后端协议]]
