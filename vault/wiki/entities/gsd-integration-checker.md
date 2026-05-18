---
type: entity
status: active
confidence: 0.75
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [gsd-agent, quality-assurance, integration-testing, Agent系统]
aliases: ["gsd-integration-checker", "GSD Integration Checker", "GSD集成检查智能体"]
relates_to: 
  - target: "[[GSD Framework]]"
    type: part_of
    confidence: 0.9
  - target: "[[GSD 多智能体编排架构]]"
    type: implements
    confidence: 0.9
  - target: "[[gsd-executor]]"
    type: validates
    confidence: 0.8
  - target: "[[gsd-verifier]]"
    type: complements
    confidence: 0.7
supersedes: null
---

# gsd-integration-checker

## 概述
GSD框架中的跨模块集成一致性检查智能体，专门负责验证不同模块间的集成是否符合预期，确保整个系统的功能协调性。

## 关键内容

1. **核心职责**：
   - 执行跨模块集成一致性检查
   - 验证不同模块间的接口兼容性
   - 检查模块间的数据流转是否正常
   - 确保集成后的功能表现符合预期

2. **执行时机**：
   - 在execute-phase阶段运行
   - 串行执行（非并行）
   - 通常在[[gsd-executor]]完成执行后进行

3. **检查重点**：
   - 模块间的依赖关系是否正确
   - API调用和数据交换的一致性
   - 跨模块功能的端到端流程
   - 集成点的[[错误处理]]机制

4. **与[[gsd-verifier]]的区别**：
   - [[gsd-verifier]]：验证单个模块或功能是否实现预期
   - gsd-integration-checker：验证跨模块集成是否协调

## 来源
- [[raw/articles/ai-tools/claude-skills/04-multi-agent-orchestration.md]] — GSD多智能体编排架构详解

## 相关
- [[GSD Framework]] — 整体框架
- [[GSD 多智能体编排架构]] — 所属编排系统
- [[gsd-executor]] — 验证其执行结果
- [[gsd-verifier]] — 互补的验证功能