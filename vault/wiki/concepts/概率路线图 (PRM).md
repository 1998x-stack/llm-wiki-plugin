---
type: concept
title: "概率路线图 (PRM)"
status: active
confidence: 1.0
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [AI, 方法论, 数值分析, 工具, 机器人学]
aliases:
  - Probabilistic Roadmap
  - PRM
  - Probabilistic Roadmaps for Path Planning
relates_to:
  - target: "[[构型空间]]"
    type: uses
    confidence: 1.0
  - target: "[[维数灾难]]"
    type: contradicts
    confidence: 0.95
  - target: "[[快速随机搜索树]]"
    type: extends
    confidence: 0.9
  - target: "[[Lydia Kavraki]]"
    type: caused
    confidence: 1.0
  - target: "[[Jean-Claude Latombe]]"
    type: caused
    confidence: 1.0
  - target: "[[Mark Overmars]]"
    type: caused
    confidence: 1.0
  - target: "[[Petr Švestka]]"
    type: caused
    confidence: 1.0
  - target: "[[运动规划]]"
    type: implements
    confidence: 1.0
supersedes: null
---

# 概率路线图 (PRM)

## 概述
概率路线图（Probabilistic Roadmap, PRM）是一种用于高维构型空间中机器人[[运动规划]]的采样算法，由 [[Lydia Kavraki]] 等人于 1996 年提出。该方法通过将连续的[[运动规划]]问题转化为离散的图搜索问题，成功克服了传统精确方法面临的“维数灾难”。PRM 采用“两阶段”策略：首先在学习阶段通过随机采样构建表示自由空间连通性的路线图，随后在查询阶段利用图搜索算法快速找到具体路径。作为采样规划（Sampling-based Planning）[[规范化理论|范式]]的奠基者，PRM 极大地推动了机器人学从理论走向工业实用。

## 关键内容

### 核心思想与架构
PRM 的核心洞察在于放弃对构型空间障碍物（C-obstacle）进行精确的几何建模，转而通过随机采样来隐式地探索自由构型空间（C-free）的拓扑结构。算法分为两个截然不同的阶段：
1.  **学习阶段（Learning Phase）**：在构型空间中均匀随机生成大量采样点，剔除碰撞点后保留为顶点。对于每个顶点，查找其邻近点并尝试用局部规划器（通常检查直线插值路径）连接它们，若连接无碰撞则形成边。最终构建出一个无向图 $G=(V, E)$，即“路线图”。这一阶段计算量大但只需执行一次，且独立于具体的起止点。
2.  **查询阶段（Query Phase）**：给定起始构型 $q_{init}$ 和目标构型 $q_{goal}$，尝试将它们连接到已构建的路线图上。一旦连接成功，即可利用 [[Edsger Dijkstra|Dijkstra]] 或 A* 等标准图搜索算法在图中寻找路径。由于图搜索效率极高，此阶段可实现毫秒级响应。

### 理论特性：概率完备性
与传统元胞分解法或可视图法的“确定性完备性”不同，PRM 具有**概率完备性（Probabilistic Completeness）**。这意味着如果自由空间中存在可行路径，随着采样点数量 $n$ 趋向无穷大，PRM 找到该路径的概率趋向于 1。虽然对于有限的采样数无法保证一定找到路径（特别是在狭窄通道场景下），但这种以极小的不确定性换取计算效率巨大提升的策略，被证明在处理 6 自由度及以上的高维问题时极具价值。

### 局限性与改进
PRM 的主要局限性包括：
*   **狭窄通道问题**：在连接两个大区域的狭窄通道中，均匀随机采样命中的概率极低，可能导致路线图不连通。后续研究提出了高斯采样、桥接采样等自适应策略来缓解此问题。
*   **非最优性**：原始 PRM 不保证找到最短或最优路径。2011 年提出的 **PRM*** 算法通过动态调整连接半径，证明了渐近最优性。
*   **动态环境适应性差**：由于路线图是预构建的，环境变化需重建图。这使得 PRM 更适合静态环境下的多查询场景，而单查询或动态场景常选用 RRT（快速随机搜索树）。

### 历史地位与应用
PRM 的提出标志着[[运动规划]]领域从“精确几何计算”向“随机采样统计”的[[规范化理论|范式]]转变。它与后来提出的 RRT 共同构成了现代采样规划的双子星。PRM 及其变体（如 Lazy PRM, PRM*）已成为开源[[运动规划]]库 OMPL 和 ROS MoveIt! 的核心算法，广泛应用于工业机器人自动编程、虚拟装配验证、蛋白质折叠模拟及自动驾驶等领域。

## 来源
- [[raw/books/机器人学/10-kavraki-probabilistic-roadmaps.md]]

## 相关
- [[构型空间]]
- [[维数灾难]]
- [[快速随机搜索树]]
- [[Lydia Kavraki]]
- [[Jean-Claude Latombe]]
- [[Mark Overmars]]
- [[Petr Švestka]]
- [[运动规划]]