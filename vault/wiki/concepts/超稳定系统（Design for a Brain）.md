---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["概率论", 控制论]
aliases: ["超稳定系统", "Ultrastable System", "同态器", "Homeostat"]
relates_to:
  - target: "[[控制论（Cybernetics）]]"
    type: part_of
    confidence: 0.9
  - target: "[[马尔可夫体制转换模型]]"
    type: relates_to
    confidence: 0.7
  - target: "[[强化学习]]"
    type: extends
    confidence: 0.75
supersedes: null
---

# 超稳定系统（Design for a Brain）

## 概述
W. Ross Ashby 于 1952 年出版的《大脑的设计》提出"超稳定系统"概念，证明适应性行为可完全由机械过程产生——无需预见、无需智慧，仅靠随机参数切换与环境选择性保留即可实现。

## 关键内容

1. **核心问题**：适应性行为能否完全由确定性机械过程产生，而无需诉诸任何形式的"预见"、"目的"或"智慧"？Ashby 将问题归结为：设计一个能自适应的"大脑"，其最小必要结构是什么？

2. **超稳定系统**：当系统偏离"本质变量"的可接受范围时，会触发参数切换机制，随机尝试新参数[[Configuration|配置]]，直到找到使系统恢复稳定的[[Configuration|配置]]。这是"试错学习"的机械实现。

3. **同态器（Homeostat）**：Ashby 构建的物理实验装置，由四个相互耦合的单元组成，每个单元可通过随机切换参数来响应环境变化。演示了纯机械系统如何展现"适应性"行为。

4. **哲学意义**：与达尔文用自然选择消解"生物设计"背后的设计者需求遥相呼应——Ashby 用超稳定系统消解了"适应行为"背后对预见能力的需求。目的性只是机械过程的表象。

5. **影响**：对人工智能、自适应控制、复杂系统理论产生深远影响，是[[强化学习]]的理论先驱之一。

## 来源
- [[06-ashby-design-for-brain]] — Design for a Brain

## 相关
- [[控制论（Cybernetics）]] — part_of
- [[马尔可夫体制转换模型]] — relates_to
- [[强化学习]] — extends
