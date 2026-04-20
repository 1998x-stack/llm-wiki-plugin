---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["harness-engineering", "agent-infrastructure", "long-running-tasks", "anthropic"]
aliases: ["Harness 框架", "Agent Harness", "长时任务控制框架"]
relates_to:
  - "[[AI Agent 架构模式]] — extends"
  - "[[Agent 架构与设计原则]] — extends"
  - "[[特性追踪器]] — uses"
  - "[[上下文传递协议]] — uses"
  - "[[智能检查点触发]] — uses"
  - "[[三级自主权模型]] — uses"
  - "[[持续验证循环]] — uses"
  - "[[技术债务追踪]] — uses"
supersedes: null
---

# Harness 设计

## 概述
Harness 是为长时运行 AI Agent 设计的控制框架，负责状态管理、验证循环、人机协作协议和上下文持久化，本质上是"为 AI Agent 定制的 CI/CD 系统"。

## 关键内容

1. **核心定位**：Harness 工程专注于长时运行应用开发场景，解决代码库状态积累性、多层次验证需求等挑战。好的 Harness 不只维护"当前状态"，还要维护**决策历史**。

2. **状态的三种形态**：Harness 需管理三类状态——**即时状态**（上下文窗口内的当前代码、测试结果、错误）、**短期状态**（检查点文件中的进行中功能、最近决策、活跃 Bug）、**长期状态**（Git 历史 + 文档中的架构演化、决策原因、完整测试历史）。

3. **与 CI/CD 的类比**：应用开发 Harness 本质上是"为 AI Agent 定制的 CI/CD 系统"——检查点 ≈ CI 构建、[[特性追踪器]] ≈ 项目管理工具、[[持续验证循环]] ≈ 测试流水线、[[三级自主权模型]] ≈ 代码审查流程。理解这个类比有助于借鉴 CI/CD 领域 20 年积累的最佳实践。

4. **核心组件**：完整的 Harness 包含 [[特性追踪器]]（Feature Tracker）、[[上下文传递协议]]（会话交接标准化包）、[[智能检查点触发]]（基于语义事件而非固定间隔）、[[三级自主权模型]]（人机协作协议）、[[持续验证循环]]（代码修改后自动验证）、[[技术债务追踪]]（确保上下文切换时技术债务不丢失）。

5. **实践建议**：设计时考虑会话边界（假设每 2-3 小时需要上下文重置）、让测试充当接口（并行开发前先写测试）、显式追踪技术债务、人工介入点要在 Harness 设计阶段明确决定。

## 来源
- [[14_harness_design_long_running.md]] — 全文，Anthropic Engineering Blog "Harness design for long-running application development"

## 相关
- [[AI Agent 架构模式]] — extends (Harness 是 Agent 架构模式的深化)
- [[Agent 架构与设计原则]] — extends (Harness 是设计原则在长时场景的具体化)
- [[特性追踪器]] — uses (核心组件)
- [[上下文传递协议]] — uses (核心组件)
- [[智能检查点触发]] — uses (核心组件)
- [[三级自主权模型]] — uses (核心组件)
- [[持续验证循环]] — uses (核心组件)
- [[技术债务追踪]] — uses (核心组件)
