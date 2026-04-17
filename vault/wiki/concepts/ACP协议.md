---
type: concept
status: active
confidence: 0.85
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [AI, Agent, 协议, 网络, LangChain, Agent系统]
aliases: [Agent Client Protocol, ACP, deepagents-acp]
relates_to:
  - target: "[[DeepAgents]]"
    type: part_of
    confidence: 0.9
supersedes: null
---

# ACP 协议（Agent Client Protocol）

## 概述

**Agent Client Protocol（ACP）** 是一种标准化的"客户端—智能体"通信协议，定义客户端如何与 AI Agent 进行会话、工具调用和消息流交互。[[DeepAgents]] 通过独立子包 `deepagents-acp`（`libs/acp/`）提供 ACP 服务端集成，将 Deep Agent 能力暴露给遵循 ACP 的客户端。

## 关键内容

### 包结构

| 模块 | 职责 |
|------|------|
| `deepagents_acp/__init__.py` | 包级说明与对外符号 |
| `deepagents_acp/__main__.py` | CLI 入口，`python -m deepagents_acp` 启动测试服务端 |
| `deepagents_acp/server.py` | ACP 服务端核心：对接 `acp` 库的会话/工具协议，调用 `create_deep_agent` 组装 Agent |
| `deepagents_acp/utils.py` | 服务端辅助逻辑 |

### 设计决策

- **独立子包**：ACP 与核心 SDK 解耦，独立版本化，通过 `[tool.uv.sources]` 指向可编辑本地路径桥接
- **协议优先**：服务端逻辑与 `acp` 库 schema 和会话生命周期 API 对齐，减少自研分叉
- **构建后端**：Hatchling；Python 3.14（其余子包用 3.12）

### 与 DeepAgents 的集成

`server.py` 调用 `deepagents.create_deep_agent` 和 `deepagents.backends`（`CompositeBackend`、`FilesystemBackend`、`StateBackend`），将 Deep Agent 编译结果接入 ACP 消息协议，客户端按协议连接即获得统一 Agent 会话体验。

### 测试覆盖

- `test_main.py`、`test_agent.py`：主流程
- `test_model_switching.py`：运行时模型切换
- 命令白名单检测、危险模式检测

## 来源
- [[raw/books/deepagents-book-main/25-ACP-Agent-Client-Protocol.md]]

## 相关
- [[DeepAgents]]
