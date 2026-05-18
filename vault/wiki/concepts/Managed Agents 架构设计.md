---
type: concept
title: "Managed Agents 架构设计"
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["AI", "方法论", "工具", "研究", "Agent系统"]
aliases: ["托管式智能体架构", "Agent Runtime Design", "Anthropic Managed Agents Architecture"]
relates_to:
  - target: "[[事件驱动 Agent 架构]]"
    type: implements
    confidence: 1.0
  - target: "[[Agent Harness 模式]]"
    type: uses
    confidence: 1.0
  - target: "[[脑手分离架构]]"
    type: extends
    confidence: 0.9
  - target: "[[长时任务 Agent 设计]]"
    type: supports
    confidence: 0.9
  - target: "[[恢复机制]]"
    type: depends_on
    confidence: 0.8
supersedes: null
---

# Managed Agents 架构设计

## 概述
[[Managed-Agents|Managed Agents]] 架构是一种专为长时运行、高可靠性[[Agent Systems|智能体系统]]设计的工程[[规范化理论|范式]]，核心思想是将"大脑"（决策逻辑）与"双手"（执行环境）解耦。该架构基于事件驱动模型，通过不可变的 Session Event Log 作为唯一事实来源，实现状态的持久化与故障恢复。

## 关键内容

### 核心设计原则
1. **状态外置**：状态存储在 Session 和 Event Log 中，[[计算]]节点可随时替换。
2. **Harness 无状态**：工作器可随时崩溃或重新调度，不影响任务连续性。
3. **Sandbox 隔离**：[[Claude Code 沙箱机制|沙箱]]仅作为执行器，失败仅表现为 Tool Failure 事件。
4. **凭证隔离**：Secrets 对模型不可达，通过 Vault 引用绑定。
5. **全事件流**：工具执行、人工审批均通过事件流处理。
6. **资源复用**：Agent 和 Environment 是可复用的版本化资源。

### 系统分层架构
- **控制面**：管理 Agent、Environment、Policy、Vault 等可复用资源。
- **运行时面**：处理 Session 实例，进入事件驱动循环。
- **工程组件**：Harness（读取状态、组装上下文、调用 LLM）、Sandbox（隔离执行）、Approval Service（人工干预）。

### 数据模型与版本控制
- **Agent Versioning**：更新生成新快照，不覆盖原记录。
- **Environment Revisions**：自建 revision 表记录 packages、networking 策略快照。
- **Append-Only Event Log**：session_events 表以追加方式写入，禁止更新旧事件。

### 运行时主流程
1. 资源定义 → 2. Session 启动 → 3. 事件触发 → 4. 决策循环 → 5. 执行与阻塞 → 6. 状态恢复

## 来源
- [[raw/ChatGPT-Chat/ChatGPT-文章解读 Anthropic Agent/03-从0到1设计ManagedAgents的系统架构图.md]]

## 相关
- [[事件驱动 Agent 架构]]
- [[Agent Harness 模式]]
- [[脑手分离架构]]
- [[长时任务 Agent 设计]]
- [[恢复机制]]
