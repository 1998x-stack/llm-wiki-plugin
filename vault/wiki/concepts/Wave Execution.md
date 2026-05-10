---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [gsd, workflow, parallelization, project-management, orchestration, parallel-execution, scheduling]
aliases: ["Wave Execution", "波次执行", "波次并行执行", "Wave Scheduling", "批次调度"]
relates_to:
  - target: "[[GSD]]"
    type: part_of
  - target: "[[GSD 多智能体编排架构]]"
    type: implements
    confidence: 0.9
  - target: "[[Multi-Agent Orchestration]]"
    type: relates_to
    confidence: 0.8
  - target: "[[Dependency Graph]]"
    type: builds_on
    confidence: 0.8
---

# Wave Execution

## 概述
一种并行任务调度模式，将具有依赖关系的任务按照拓扑顺序分组成波次，同波次内的任务可并行执行，不同波次按序等待执行完成，以最大化并行度同时保证依赖约束。GSD系统利用此机制通过DAG依赖分析将可并行的任务分组到同一"波次"，实现高效的并行处理。

## 关键内容

1. **核心原理**：
   - 将任务的依赖关系图进行拓扑排序
   - 将无相互依赖的任务归类到同一波次
   - 同波次内的任务可以并行执行
   - 等待整个波次完成后再开始下一波次

2. **[[算法]]实现**：
   - 解析所有任务的依赖关系
   - 构建依赖关系图
   - 找出所有依赖已完成的可立即执行任务
   - 将这些任务组成一个波次
   - 重复直到所有任务都被调度

3. **GSD中的应用示例**：
   ```
   WAVE 1（并行）              WAVE 2（并行）          WAVE 3
   ┌──────────┐ ┌──────────┐  ┌──────────┐ ┌──────┐  ┌──────────┐
   │ Plan 01  │ │ Plan 02  │→ │ Plan 03  │ │ P04  │→ │ Plan 05  │
   │User Model│ │Prod Model│  │Orders API│ │CartAPI│  │ Checkout │
   └──────────┘ └──────────┘  └──────────┘ └──────┘  └──────────┘
   ```

4. **冲突检测与解决**：
   - 检测同一波次内的任务是否会产生资源冲突（如修改同一文件）
   - 如检测到冲突，则将冲突任务推迟到下一波次
   - 或将冲突任务合并为同一计划

5. **关键原则**：
   > **垂直切片比水平切片并行度高得多**
   
   - 按功能端到端切分的计划，各模块之间相互独立，可以完全并行
   - 按技术层次切分的计划，必须严格顺序执行

6. **优势**：
   - 最大化并行执行效率
   - 减少总体执行时间
   - 保持任务依赖关系清晰
   - 避免资源竞争和冲突
   - 提供清晰的执行进度感知

## 来源
- [[01-overview-context-rot]] — Context Rot 与上下文工程
- [[raw/articles/ai-tools/claude-skills/04-multi-agent-orchestration.md]] — GSD多智能体编排架构详解

## 相关
- [[GSD]] — part_of
- [[GSD 多智能体编排架构]] — implements
- [[Multi-Agent Orchestration]] — relates_to
- [[DAG]] — uses
- [[Parallel Execution]] — implements
- [[Dependency Graph]] — depends_on
