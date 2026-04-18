---
type: concept
status: active
confidence: 0.85
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [gsd, workflow, parallelization, project-management]
aliases: ["Wave Execution", "波次执行", "波次并行执行"]
relates_to:
  - target: "[[GSD]]"
    type: part_of
---

# Wave Execution

## 概述
GSD 系统的并行执行机制，通过 DAG 依赖分析将可并行的任务分组到同一"波次"，实现高效的并行处理。

## 关键内容

1. **核心思想**：
   - 分析 PLAN 文件间的依赖关系
   - 构建 DAG（有向无环图）
   - 将可并行的计划放入同一"波次"

2. **示例**：
   ```
   WAVE 1（并行）              WAVE 2（并行）          WAVE 3
   ┌──────────┐ ┌──────────┐  ┌──────────┐ ┌──────┐  ┌──────────┐
   │ Plan 01  │ │ Plan 02  │→ │ Plan 03  │ │ P04  │→ │ Plan 05  │
   │User Model│ │Prod Model│  │Orders API│ │CartAPI│  │ Checkout │
   └──────────┘ └──────────┘  └──────────┘ └──────┘  └──────────┘
   ```

3. **关键原则**：
   > **垂直切片比水平切片并行度高得多**
   
   - 按功能端到端切分的计划，各模块之间相互独立，可以完全并行
   - 按技术层次切分的计划，必须严格顺序执行

4. **优势**：
   - 最大化并行执行效率
   - 减少总体执行时间
   - 保持任务依赖关系清晰

## 来源
- [[01-overview-context-rot]] — Context Rot 与上下文工程

## 相关
- [[GSD]] — part_of
- [[DAG]] — uses
- [[Parallel Execution]] — implements
