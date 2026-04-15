---
type: concept
title: "快速扩展随机树 (RRT)"
status: active
confidence: 1.0
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [AI, 方法论，研究，工具]
aliases: ["RRT", "Rapidly-Exploring Random Trees"]
relates_to:
  - target: "[[概率路线图方法]]"
    type: contradicts
    confidence: 0.9
  - target: "[[Steven M. LaValle]]"
    type: caused
    confidence: 1.0
  - target: "[[RRT-Connect]]"
    type: extends
    confidence: 1.0
  - target: "[[RRT*]]"
    type: extends
    confidence: 1.0
  - target: "[[运动规划]]"
    type: implements
    confidence: 1.0
  - target: "[[Kinodynamic Planning]]"
    type: implements
    confidence: 0.95
supersedes: null
---

# 快速扩展随机树 (RRT)

## 概述
快速扩展随机树（Rapidly-Exploring Random Trees, RRT）是一种用于高维空间路径规划的采样算法，由 Steven M. LaValle 于 1998 年提出。该算法通过构建一棵以起始点为根的树，利用随机采样引导树向未探索区域生长，从而高效地解决单查询运动规划问题。RRT 的核心优势在于其极致的简洁性、对非完整约束和动力学约束的天然适应性，以及增量式构建带来的实时响应能力。作为基于采样的运动规划两大支柱之一（另一为 PRM），RRT 已广泛应用于机器人学、自动驾驶及手术导航等领域。

## 关键内容

### 核心算法循环
RRT 算法维护一棵树 $T$，初始仅包含起始构型 $q_{init}$。算法反复执行以下循环直至找到目标或达到迭代上限：
1.  **随机采样**：在构型空间中均匀随机生成一点 $q_{rand}$。
2.  **最近邻搜索**：在树 $T$ 中寻找距离 $q_{rand}$ 最近的节点 $q_{near}$。
3.  **延伸**：从 $q_{near}$ 向 $q_{rand}$ 方向延伸固定步长 $\epsilon$，得到新节点 $q_{new}$。
4.  **碰撞检测**：检查边 $(q_{near}, q_{new})$ 是否无碰撞。若无碰撞，将 $q_{new}$ 加入树中；否则丢弃。
5.  **目标检查**：若 $q_{new}$ 足够接近目标 $q_{goal}$，则回溯路径并终止。

### Voronoi 偏置机制
RRT 高效性的数学基础是**Voronoi 偏置（Voronoi Bias）**。当进行均匀随机采样时，树中每个节点被选为 $q_{near}$ 的概率正比于其 Voronoi 区域的体积。位于树边缘、周围大片空间尚未被探索的节点拥有更大的 Voronoi 区域，因此更大概率被选中进行扩展。这种机制使 RRT 无需显式启发式函数，即可自然地倾向于向未探索区域生长，避免了在已充分探索区域的冗余计算。

### 处理非完整与动力学约束
与传统方法不同，RRT 的延伸步骤天然支持前向模拟：算法不需要解决困难的两点边值问题（即如何从状态 A 精确移动到状态 B），只需从当前状态 $x_{near}$ 选择一个随机控制输入 $u$，对动力学方程进行短时间积分得到新状态 $x_{new}$。只要模拟器是物理正确的，生成的每一步运动自动满足所有的运动和动力学约束。这种“构建即可行”的特性使得 RRT 成为该领域事实上的标准方法。

### 局限性与改进
基本 RRT 存在路径质量差（锯齿状）和不保证最优性的缺陷。为解决这些问题，后续提出了 **[[RRT*]]** 算法，通过重新选择父节点和重布线（rewiring）实现了渐近最优性。此外，针对窄通道问题，研究者开发了多种自适应采样策略。尽管存在局限，RRT 及其变体因其模块化和易实现性，已成为 **[[OMPL]]** 等标准库的核心组件。

## 来源
- [[raw/books/机器人学/11-lavalle-rapidly-exploring-random-trees.md]]

## 相关
- [[概率路线图方法]]
- [[Steven M. LaValle]]
- [[RRT-Connect]]
- [[RRT*]]
- [[运动规划]]
- [[Kinodynamic Planning]]