---
type: entity
title: "Lydia Kavraki"
status: active
confidence: 1.0
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [AI, 研究, 工具, 机器人学]
aliases:
  - Lydia E. Kavraki
relates_to:
  - target: "[[概率路线图 (PRM)]]"
    type: caused
    confidence: 1.0
  - target: "[[Jean-Claude Latombe]]"
    type: depends_on
    confidence: 0.9
  - target: "[[Rice University]]"
    type: uses
    confidence: 0.8
  - target: "[[Stanford University]]"
    type: uses
    confidence: 0.8
supersedes: null
---

# Lydia Kavraki

## 概述
Lydia E. Kavraki 是计算机科学和机器人学领域的杰出学者，现任莱斯大学（Rice University）教授。她最著名的贡献是与 [[Jean-Claude Latombe]] 等人共同提出了**概率路线图（PRM）**算法，该工作开创了采样规划（Sampling-based Planning）这一主导现代[[运动规划]]的方法论范式。Kavraki 的研究跨越了机器人[[运动规划]]、计算几何和计算生物学，她将 PRM 的思想成功应用于蛋白质折叠和药物设计等高维构型空间问题。因其开创性工作，她当选为 ACM Fellow 和 IEEE Fellow，并获得 IEEE RAS 先驱奖等多项荣誉。

## 关键内容

### 学术背景与合作网络
Kavraki 的学术生涯始于斯坦福大学（Stanford University），她在[[运动规划]]奠基人 [[Jean-Claude Latombe]] 的指导下攻读博士学位。她的博士研究聚焦于随机化[[运动规划]]，其核心成果即为 1996 年发表的里程碑式论文《[[概率路线图 (PRM)|Probabilistic Roadmaps for Path Planning]] in High-Dimensional Configuration Spaces》。这项研究体现了跨大西洋的学术合作，她与来自乌得勒支大学（Utrecht University）的 [[Mark Overmars]] 和 [[Petr Švestka]] 紧密合作，融合了斯坦福团队在实际机器人规划问题的深刻理解与乌得勒支团队在计算几何算法理论上的严谨分析。这种互补性使得 PRM 兼具实用性与理论深度。

### 核心贡献：概率路线图 (PRM)
Kavraki 在 PRM 工作中的核心洞察是提出了一种全新的解决高维[[运动规划]]问题的思路：不再试图精确计算复杂的构型空间障碍物几何形状，而是通过随机采样构建一个稀疏的图（路线图）来近似自由空间的连通性。这一方法突破了困扰学界多年的“维数灾难”，使得 6 自由度甚至更高自由度的机器人路径规划在计算上变得可行。PRM 的“学习 - 查询”两阶段架构不仅解决了当时的工业痛点，更定义了过去三十年[[运动规划]]研究的主旋律。

### 跨学科影响：从机器人到生物学
Kavraki 并未将 PRM 局限于传统机器人领域。在加入莱斯大学后，她极具远见地将这一算法思想拓展至计算生物学领域。她指出蛋白质分子可以被视为具有高自由度的“机器人”，其折叠过程等同于在高维构型空间中寻找低能量路径。利用 PRM 的采样策略，她的团队在蛋白质折叠预测、药物分子对接等方面取得了突破性进展，展示了随机采样方法在探索复杂生物大分子构象空间中的强大能力。

### 荣誉与遗产
鉴于其在算法创新和跨学科应用上的卓越贡献，Kavraki 获得了学术界的高度认可：
*   **ACM Fellow (2010)** 与 **IEEE Fellow (2010)**：表彰其在计算几何和机器人学领域的杰出贡献。
*   **IEEE RAS 先驱奖**：肯定其作为采样规划领域开创者的地位。
*   **OMPL 与 MoveIt!**：她创立并领导的 Rice University Kavraki Lab 维护着 Open [[运动规划|Motion Planning]] Library (OMPL)，该库被集成在 ROS 的 MoveIt! 框架中，成为全球机器人开发者最常用的[[运动规划]]工具包。

## 来源
- [[raw/books/机器人学/10-kavraki-probabilistic-roadmaps.md]]

## 相关
- [[概率路线图 (PRM)]]
- [[Jean-Claude Latombe]]
- [[Rice University]]
- [[Stanford University]]
- [[Mark Overmars]]
- [[Petr Švestka]]
- [[运动规划]]