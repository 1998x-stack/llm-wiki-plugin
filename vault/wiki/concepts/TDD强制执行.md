---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [software-engineering, development-methodology, quality-assurance]
aliases: [Test-Driven Development, TDD强制执行, Test Driven Development]
relates_to: 
  - target: "[[Superpowers]]"
    type: implemented_by
  - target: "[[Software Engineering]]"
    type: methodology
  - target: "[[Quality Assurance]]"
    type: assurance_method
  - target: "[[Testing]]"
    type: approach
  - target: "[[Development Discipline]]"
    type: core_principle
supersedes: null
---

# TDD强制执行

## 概述
TDD强制执行是一种在软件开发过程中通过技术手段确保[[测试驱动开发]]方法论得到严格执行的实践。

## 关键内容
1. **核心理念**：通过系统级约束而非仅靠开发者自觉来确保TDD流程的执行，防止跳过测试环节。

2. **[[Superpowers]]中的实现**：
   - 检测到代码写在测试前→删除代码，重新开始
   - 这不是建议，而是系统级约束
   - 在AI编码工具中，这是最强硬的质量[[门控机制（Gating Mechanism）|门控]]

3. **实施方式**：
   - 写测试→确认测试失败→写实现（不可跳过）
   - 微任务分解到2-5分钟颗粒度
   - 每个任务有明确的完成标准和验证步骤

4. **价值**：
   - 解决AI"有能力但无纪律"的问题
   - 提升代码质量和可靠性
   - 防止AI在复杂任务中迷失方向

5. **应用场景**：特别适用于[[AI辅助开发]]环境中，确保AI代理遵循严格的开发流程和质量标准。

## 来源
- [[claude-code-tools-comparison]] — TDD强制执行在Superpowers中的应用分析

## 相关
- [[Superpowers]] — implemented_by
- [[Software Engineering]] — methodology
- [[Quality Assurance]] — assurance_method
- [[Testing]] — approach
- [[Development Discipline]] — core_principle