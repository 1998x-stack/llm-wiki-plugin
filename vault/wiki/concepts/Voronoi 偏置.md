---
type: concept
title: "Voronoi 偏置"
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [数学，AI, 方法论, 机器人学]
aliases: ["Voronoi Bias", "Voronoi Region Bias"]
relates_to:
  - target: "[[快速扩展随机树 (RRT)]]"
    type: uses
    confidence: 1.0
  - target: "[[Voronoi 图]]"
    type: depends_on
    confidence: 0.9
supersedes: null
---

# Voronoi 偏置

## 概述
Voronoi 偏置（Voronoi Bias）是快速扩展随机树（RRT）算法能够高效探索高维空间的核心数学机制。该现象指出，在均匀随机采样空间中，RRT 树中位于边缘、周围未被探索区域较大的节点，因其 Voronoi 区域体积更大，被选为扩展起点的概率更高。这种隐式的探索策略使得算法无需复杂的启发式函数，便能自然地倾向于向未探索区域生长，从而避免了在已充分探索区域的无效计算。

## 关键内容

### 数学原理
Voronoi 偏置基于 Voronoi 图的几何性质。对于树 $T$ 中的每一个节点 $q_i$，其 Voronoi 区域 $V(q_i)$ 定义为构型空间中所有距离 $q_i$ 比距离其他任何树节点更近的点的集合。当算法在空间中均匀随机采样点 $q_{rand}$ 时，$q_{rand}$ 落入某个节点 $q_i$ 的 Voronoi 区域 $V(q_i)$ 的概率正比于该区域的体积（或测度）。即：
$$ P(\text{select } q_i) = \frac{\text{Vol}(V(q_i))}{\text{Vol}(C_{free})} $$
在 RRT 的生长过程中，位于树内部或被密集包围的节点，其 Voronoi 区域较小；而位于树前沿、面向大片空白区域的节点，其 Voronoi 区域显著较大。因此，随机采样点更有可能落在这些边缘节点的 Voronoi 区域内，导致这些节点被频繁选为 $q_{near}$ 进行扩展。

### 在 RRT 中的作用
Voronoi 偏置赋予了 RRT 一种“免费”的探索策略。传统的搜索算法（如 A*）需要精心设计启发式函数来指导搜索方向，而 RRT 仅通过简单的“随机采样 + 最近邻选择”组合，就自动涌现出向未知空间探索的行为。这种特性使得 RRT 在高维空间中表现优异，因为它不需要显式地建模空间的拓扑结构或障碍物的分布，完全依靠[[概率论]]性质驱动搜索过程。

### 局限性与影响
虽然 Voronoi 偏置在开阔空间中非常有效，但在**窄通道**问题上表现受限。如果可行路径必须通过一个极窄的瓶颈，该区域对应的 Voronoi 区域体积极小，随机采样点落入其中的概率极低，导致树难以生长进入通道。尽管如此，Voronoi 偏置仍然是理解基于采样规划算法行为的关键概念，也是后续改进算法（如加权采样、自适应采样）的理论基础。

## 来源
- [[raw/books/机器人学/11-lavalle-rapidly-exploring-random-trees.md]]

## 相关
- [[快速扩展随机树 (RRT)]]
- [[Voronoi 图]]
- [[运动规划]]