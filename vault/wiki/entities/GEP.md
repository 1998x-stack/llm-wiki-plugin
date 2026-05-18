---
type: entity
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-agent, protocol, evolution, AI工程]
aliases: ["GEP", "Gene Evolution Protocol", "Gene Evolution Protocol"]
entity_type: tool
relates_to:
  - target: "[[Evolver]]"
    type: implemented_by
  - target: "[[自我进化型 AI Agent 协议]]"
    type: part_of
supersedes: null
---

# GEP

## 概述
GEP（Gene Evolution Protocol）是 [[Evolver]] 项目中的基因进化协议，用于指导 AI Agent 的自进化过程。

## 关键内容

1. **协议作用**：
   - 指导 AI Agent 的进化过程
   - 约束和规范进化行为，确保可审计性
   - 生成进化提示（Prompt）以引导 Agent 改进

2. **核心组件**：
   - Gene 策略资产库：存储可复用的改进策略
   - Capsule 解决方案库：存储问题解决方案
   - EvolutionEvent 审计日志：记录进化事件的不可变链

3. **工作流程**：
   - 在 [[Evolver]] 的三阶段进化循环中发挥核心作用
   - 在执行阶段用于构建 [[Mutation]] 和生成 GEP Prompt
   - 通过协议确保所有变更都经过审计

## 来源
- [[Evolver/01_overview_architecture]] — 项目总览与整体架构中提及

## 相关
- [[Evolver]] — 实现 GEP 的核心项目
- [[AI Agent]] — 应用领域
- [[Self-Evolving Agent Protocol]] — 相关协议概念