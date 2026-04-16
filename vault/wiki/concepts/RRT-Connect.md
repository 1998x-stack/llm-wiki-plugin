---
type: concept
title: "RRT-Connect"
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [AI, 方法论，工具, 机器人学]
aliases: ["RRT-Connect Algorithm", "Bidirectional RRT"]
relates_to:
  - target: "[[快速扩展随机树 (RRT)]]"
    type: extends
    confidence: 1.0
  - target: "[[Steven M. LaValle]]"
    type: caused
    confidence: 1.0
  - target: "[[James J. Kuffner Jr.]]"
    type: caused
    confidence: 1.0
supersedes: null
---

# RRT-Connect

## 概述
[[快速扩展随机树 (RRT)|RRT]]-Connect 是快速扩展随机树（[[快速扩展随机树 (RRT)|RRT]]）算法的重要变体，由 [[Steven M. LaValle]] 和 James J. Kuffner Jr. 于 2000 年提出。该算法通过同时从起始构型和目标构型生长两棵树，并尝试在每一步迭代中连接这两棵树，从而显著提高了路径规划的效率。[[快速扩展随机树 (RRT)|RRT]]-Connect 引入了贪心延伸策略，使其在开阔空间中的收敛速度通常比基本 [[快速扩展随机树 (RRT)|RRT]] 快一个数量级，特别适用于单查询[[运动规划]]问题。

## 关键内容

### 双向生长机制
与基本 [[快速扩展随机树 (RRT)|RRT]] 仅从起点单向生长不同，[[快速扩展随机树 (RRT)|RRT]]-Connect 维护两棵树：$T_{init}$（ rooted at $q_{init}$）和 $T_{goal}$（rooted at $q_{goal}$）。算法在每一步迭代中交替扩展这两棵树。扩展一棵树后，算法立即尝试将新生成的节点与另一棵树中的最近节点进行连接。如果连接路径无碰撞，则两棵树成功合并，形成从起点到终点的完整路径。这种双向搜索策略大幅减少了搜索空间的覆盖时间，因为两棵树从两端相向而行，更容易在中间相遇。

### 贪心延伸策略
[[快速扩展随机树 (RRT)|RRT]]-Connect 的一个关键创新是**贪心延伸（Greedy Extension）**。在标准 [[快速扩展随机树 (RRT)|RRT]] 中，每次扩展只向前移动一个固定步长 $\epsilon$。而在 [[快速扩展随机树 (RRT)|RRT]]-Connect 中，当试图向另一棵树的方向延伸时，算法会连续执行延伸操作，直到遇到障碍物或到达目标树的连接范围。这种策略在无障碍或开阔区域能迅速拉长树枝，极大地减少了所需的迭代次数。贪心延伸充分利用了局部空间的连通性，避免了单步探索的低效。

### 性能优势与应用
实验表明，[[快速扩展随机树 (RRT)|RRT]]-Connect 在多种基准测试中表现出比基本 [[快速扩展随机树 (RRT)|RRT]] 快 5 到 10 倍的速度提升，尤其在中等难度的规划问题中效果显著。由于其高效性和鲁棒性，[[快速扩展随机树 (RRT)|RRT]]-Connect 成为了开源[[运动规划]]库 **[[OMPL]]** 中的默认推荐算法之一，并被广泛应用于工业机器人、类人机器人（如 H7 机器人手臂规划）以及自动驾驶领域。它是解决单查询、高维、非完整约束规划问题的强有力工具。

## 来源
- [[raw/books/机器人学/11-lavalle-rapidly-exploring-random-trees.md]]

## 相关
- [[快速扩展随机树 (RRT)]]
- [[Steven M. LaValle]]
- [[James J. Kuffner Jr.]]
- [[运动规划]]