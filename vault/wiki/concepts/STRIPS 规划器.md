---
type: concept
title: "STRIPS 规划器"
status: active
confidence: 1.0
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [AI, 方法论，研究]
aliases: ["STanford Research Institute Problem Solver", "STRIPS"]
relates_to:
  - target: "[[Shakey 机器人]]"
    type: uses
    confidence: 1.0
  - target: "[[Richard E. Fikes]]"
    type: caused
    confidence: 1.0
  - target: "[[Nils J. Nilsson]]"
    type: caused
    confidence: 1.0
  - target: "[[PDDL]]"
    type: extends
    confidence: 0.9
  - target: "[[A*搜索算法]]"
    type: depends_on
    confidence: 0.8
supersedes: null
---

# STRIPS 规划器

## 概述
STRIPS（STanford Research Institute Problem Solver）是人工智能历史上最具影响力的自动规划系统之一，由 Richard E. Fikes 和 Nils J. Nilsson 于 1971 年提出。它首创了使用“前提条件（Preconditions）、添加列表（Add List）和删除列表（Delete List）”三元组来形式化描述动作效果的框架，成功将规划问题从通用的定理证明中分离出来，转化为状态空间搜索问题。作为 Shakey 机器人的核心决策引擎，STRIPS 奠定了此后半个世纪自动规划领域的理论基础，其表示法直接演化为现代标准语言 PDDL。

## 关键内容

### 核心表示法：STRIPS 操作符
STRIPS 最核心的贡献在于定义了一种简洁而强大的动作描述格式，即 STRIPS 操作符。每个操作符包含三个部分：
1.  **前提条件（Preconditions）**：一组逻辑谓词的合取，规定了执行该动作前世界必须满足的状态。只有当前状态蕴含所有前提条件时，动作才可执行。
2.  **添加列表（Add List）**：动作执行后新增到世界状态中的谓词集合，代表动作产生的“正效果”。
3.  **删除列表（Delete List）**：动作执行后从世界状态中移除的谓词集合，代表被动作推翻的旧事实。

这种表示法巧妙地通过显式声明变化（添加/删除）而隐式假设不变（未提及即保持），有效缓解了著名的“框架问题”（Frame Problem），避免了在每一步推理中显式列举所有未改变事物的组合爆炸。

### 规划过程与搜索策略
STRIPS 将规划问题形式化为在状态空间中寻找从初始状态到目标状态的路径。其搜索策略结合了前向搜索与手段 - 目的分析（Means-Ends Analysis）：
*   **目标驱动**：若当前状态不满足目标，系统选择一个未满足的子目标。
*   **操作符选择**：寻找一个其“添加列表”包含该子目标的操作符。
*   **递归求解**：检查该操作符的前提条件。若满足则执行；若不满足，则将未满足的前提条件作为新的子目标递归处理。
*   **定理证明辅助**：在检查前提条件是否满足时，STRIPS 调用 QA3 定理证明器进行逻辑推导，但仅限于当前固定状态，从而大幅提高了效率。

### 历史地位与现代演进
STRIPS 不仅是一个理论框架，更在 Shakey 机器人上得到了实际验证，实现了感知、推理与行动的统一。它确立了“规划即搜索”的范式，直接催生了后续的非线性规划、偏序规划以及 GRAPHPLAN 等高效算法。1998 年诞生的 PDDL（规划领域定义语言）本质上是 STRIPS 表示法的标准化扩展，至今仍是国际规划竞赛（IPC）的标准输入格式。在大语言模型（LLM）时代，STRIPS 的逻辑严谨性被视为弥补 LLM“幻觉”、确保多步推理正确性的关键组件，形成了"LLM 翻译 + STRIPS 求解”的新架构。

## 来源
- [[raw/books/机器人学/04-fikes-nilsson-strips-planner.md]]

## 相关
- [[Shakey 机器人]]
- [[Richard E. Fikes]]
- [[Nils J. Nilsson]]
- [[PDDL]]
- [[A*搜索算法]]