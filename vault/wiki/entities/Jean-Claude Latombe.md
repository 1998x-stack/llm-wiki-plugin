---
type: entity
title: "Jean-Claude Latombe"
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [AI, 研究, 机器人学]
aliases:
  - J.C. Latombe
relates_to:
  - target: "[[概率路线图 (PRM)]]"
    type: caused
    confidence: 1.0
  - target: "[[Lydia Kavraki]]"
    type: caused
    confidence: 0.9
  - target: "[[Stanford University]]"
    type: uses
    confidence: 0.8
  - target: "[[构型空间]]"
    type: uses
    confidence: 0.9
supersedes: null
---

# Jean-Claude Latombe

## 概述
Jean-Claude Latombe 是机器人[[运动规划]]领域的奠基人之一，曾任斯坦福大学（Stanford University）教授。他最为人熟知的成就是撰写了该领域的权威专著《Robot [[运动规划|Motion Planning]]》（1991 年），该书系统化了构型空间（Configuration Space）理论，至今仍是该领域的标准参考书。作为 [[Lydia Kavraki]] 的博士导师，他与 Kavraki、[[Mark Overmars]] 等人合作提出了概率路线图（PRM）方法，推动了[[运动规划]]从精确几何方法向随机采样方法的[[规范化理论|范式]]转变。

## 关键内容

### 构型空间理论的集大成者
在 PRM 提出之前，Latombe 的主要贡献在于对构型空间（C-space）理论的梳理和推广。1983 年 Lozano-Perez 提出 C-space 概念后，Latombe 在其 1991 年的专著中将其发展为一套完整的理论框架。他清晰地阐述了如何将机器人的[[运动规划]]问题转化为 C-space 中点的路径搜索问题，并将碰撞检测定义为判断点是否落在 C-obstacle 内。尽管后来的 PRM 方法避开了显式构造 C-obstacle 的计算困难，但 Latombe 建立的这一抽象框架仍然是所有现代[[运动规划]]算法（包括采样方法）的理论基石。

### PRM 的幕后推手
作为斯坦福团队的领军人物，Latombe 在 PRM 的诞生过程中扮演了关键角色。他不仅提供了深厚的理论背景，还带来了丰富的实际机器人规划经验。在与乌得勒支大学（Utrecht University）的 [[Mark Overmars]] 团队合作时，Latombe 确保了算法设计既符合计算几何的严谨性，又能解决实际工业中高自由度机械臂的规划难题。他是连接经典精确规划时代与现代采样规划时代的桥梁人物。

### 学术传承与影响
Latombe 培养了一批杰出的学生，其中最著名的是 [[Lydia Kavraki]]。他在斯坦福指导 Kavraki 完成了关于随机化[[运动规划]]的博士论文，直接催生了 PRM 算法。他的教育理念强调理论与实践的结合，鼓励学生在面对“维数灾难”等看似无解的理论困境时，勇于引入随机性等非传统手段寻找工程上的突破。这种思想深深影响了后续几十年的机器人学研究方向。

## 来源
- [[raw/books/机器人学/10-kavraki-probabilistic-roadmaps.md]]

## 相关
- [[概率路线图 (PRM)]]
- [[Lydia Kavraki]]
- [[Stanford University]]
- [[构型空间]]
- [[Mark Overmars]]
- [[运动规划]]