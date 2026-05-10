---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [AI Engineering, Multi-Agent Systems, LLM]
aliases: ["智能体系统", "Agent Systems", "AI Agent Systems"]
relates_to:
  - {target: Context Engineering, type: supports, confidence: 0.8}
  - {target: LLM, type: application_of, confidence: 0.8}
  - {target: Tool Calling, type: uses, confidence: 0.8}
  - {target: Memory Systems, type: requires, confidence: 0.9}
  - {target: MCP, type: uses, confidence: 0.7}
supersedes: null
---

# Agent Systems

## 概述
基于大[[Language-Model|语言模型]]构建的自主智能体系统，能够感知环境、做出决策、执行任务并与外部工具和[[服务]]交互，代表了人工智能从被动响应到主动执行的[[规范化理论|范式]]转变。

## 关键内容

1. **核心组件**：
   - 规划（Planning）：将复杂任务分解为可执行的子任务
   - 记忆（Memory）：短期记忆存储当前上下文，长期记忆存储知识和经验
   - 工具使用（Tool Usage）：调用外部工具和[[服务]]扩展能力
   - 感知（Perception）：理解和处理来自环境的信息输入

2. **架构模式**：
   - 单智能体系统：单个LLM驱动的智能体，执行特定任务
   - 多智能体系统：多个智能体协作完成复杂任务
   - 分层智能体：不同层级智能体负责不同粒度的任务规划和执行

3. **关键技术**：
   - 工具调用（Function [[天职|Calling]]）：标准化的API调用机制
   - [[Memory-Management|记忆管理]]系统：[[分层记忆架构]]（[[工作记忆]]、[[情节记忆]]、[[语义记忆]]）
   - [[Context Management|上下文管理]]：维护长时间对话和任务执行的上下文一致性
   - 状态管理：跟踪任务进度和执行状态

4. **应用场景**：
   - 个人助理：日程管理、信息检索、文档处理
   - 业务自动化：客户[[服务]]、流程执行、[[数据分析]]
   - 研究辅助：文献调研、实验设计、报告生成

## 来源
- AI-Agent--02_context_engineering — Context Engineering的应用场景中提及

## 相关
- [[Context Engineering]] — supports
- [[LLM]] — application_of
- [[Tool Calling]] — uses
- [[Memory Systems]] — requires
- [[MCP]] — uses