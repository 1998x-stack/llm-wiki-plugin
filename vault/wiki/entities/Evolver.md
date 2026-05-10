---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [ai-agent, self-evolving, protocol-engine, javascript]
aliases: ["Evolver", "Self-Evolving Agent Protocol", "PCEC", "Protocol-Constrained Evolution Core"]
entity_type: project
relates_to:
  - target: "[[GEP]]"
    type: implements
  - target: "[[EvoMap]]"
    type: part_of
  - target: "[[A2A 协议]]"
    type: uses
  - target: "[[Mutation]]"
    type: part_of
supersedes: null
---

# Evolver

## 概述
Evolver 是一个[[自我进化型 AI Agent 协议]]引擎（[[自我进化型 AI Agent 协议|Self-Evolving Agent Protocol]], PCEC），作为 AI Agent 的"细胞核"，提供协议约束的自进化能力。

## 关键内容

1. **核心定位**：
   - 一个协议约束的 AI Agent 自进化引擎（GEP 驱动）
   - 将临时 Prompt 调整变成可审计、可复用的进化资产
   - 通过协议约束实现可审计、资产化的进化过程

2. **关键特性**：
   - **Gene/Capsule 策略资产库**：将 Bug 修复等改进固化为可复用资产
   - **不可变进化事件审计链**：记录完整的 EvolutionEvent 审计日志
   - **[[A2A 协议]]广播**：实现 Agent 间（Agent-to-Agent）的资产共享
   - **安全边界控制**：通过 [[Blast Radius 控制|Blast Radius]] 和校验命令白名单[[门控机制（Gating Mechanism）|门控]]保障安全
   - **记忆图防重复修复循环**：避免无限修复循环

3. **架构组成**：
   - 三阶段进化循环：分析（Analysis）、选择（Selection）、执行（Execution）
   - Gene/Capsule 资产管理系统
   - A2A（Agent-to-Agent）协议实现
   - 因果记忆图（信号-基因-结果链路追踪）
   - 进程生命周期管理和自修复机制

## 来源
- [[Evolver/01_overview_architecture]] — 项目总览与整体架构

## 相关
- [[GEP]] — Gene Evolution Protocol，Evolver 的核心协议
- [[EvoMap]] — Evolver 所属的生态体系
- [[AI Agent]] — 相关技术领域