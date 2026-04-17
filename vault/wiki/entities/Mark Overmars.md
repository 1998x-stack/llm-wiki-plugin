---
type: entity
title: "Mark Overmars"
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [研究, 数学, 机器人学]
aliases:
  - Mark H. Overmars
relates_to:
  - target: "[[概率路线图 (PRM)]]"
    type: caused
    confidence: 1.0
  - target: "[[Petr Švestka]]"
    type: caused
    confidence: 0.9
  - target: "[[Utrecht University]]"
    type: uses
    confidence: 0.8
  - target: "[[计算几何]]"
    type: implements
    confidence: 0.8
supersedes: null
---

# Mark Overmars

## 概述
Mark H. Overmars 是荷兰乌得勒支大学（Utrecht University）的杰出教授，主要研究领域为计算几何（Computational Geometry）及其在[[运动规划]]中的应用。他是概率路线图（[[概率路线图 (PRM)|PRM]]）算法的共同提出者之一，代表了 [[概率路线图 (PRM)|PRM]] 研发团队中负责算法理论严谨性的一方。Overmars 长期致力于将计算几何的高效数据结构（如 KD-tree、可见性图变种）引入机器人学，解决了高维空间中的邻域搜索和路径连接等关键问题。

## 关键内容

### 计算几何与运动规划的交叉
Overmars 的学术特色在于擅长运用计算几何的理论工具解决实际的规划问题。在 [[概率路线图 (PRM)|PRM]] 的研发中，他及其团队（包括博士生 [[Petr Švestka]]）贡献了关于随机采样分布、近邻查找效率以及路线图连通性分析的深刻见解。不同于纯工程导向的方法，Overmars 团队注重算法的时间复杂度分析和概率完备性的数学证明，这使得 [[概率路线图 (PRM)|PRM]] 不仅仅是一个启发式工具，更成为一个有坚实理论支撑的算法框架。

### 跨大西洋合作的关键角色
1990 年代，Overmars 与斯坦福大学的 [[Jean-Claude Latombe]] 建立了紧密的合作关系。这种跨大陆的合作模式在当时并不多见，它成功结合了斯坦福团队对机器人物理约束和工业需求的理解，以及乌得勒支团队在离散几何和随机算法方面的专长。Overmars 在合作中确保了 [[概率路线图 (PRM)|PRM]] 算法在处理高维数据时的可扩展性，特别是利用[[Octree八叉树|空间索引]]结构加速了近邻搜索过程，这是 [[概率路线图 (PRM)|PRM]] 能够在高维空间中高效运行的关键技术细节。

### 多机器人协同规划
除了 [[概率路线图 (PRM)|PRM]]，Overmars 还在多机器人协同[[运动规划]]方面做出了重要贡献。他指导的 [[Petr Švestka]] 在多机器人系统的联合构型空间规划上进行了深入研究，进一步扩展了采样方法的应用边界。Overmars 的工作表明，通过合理的几何抽象和随机化策略，即使是维度极高的多智能体系统，也能找到可行的协调路径。

## 来源
- [[raw/books/机器人学/10-kavraki-probabilistic-roadmaps.md]]

## 相关
- [[概率路线图 (PRM)]]
- [[Petr Švestka]]
- [[Utrecht University]]
- [[计算几何]]
- [[Jean-Claude Latombe]]
- [[Lydia Kavraki]]