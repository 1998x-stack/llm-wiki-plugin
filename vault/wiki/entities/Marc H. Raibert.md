---
type: entity
title: "Marc H. Raibert"
status: active
confidence: 1.0
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [AI, 工具，方法论，研究, 机器人学]
aliases: ["Raibert", "马克·雷伯特"]
relates_to:
  - target: "[[Legged Robots That Balance]]"
    type: implements
    confidence: 1.0
  - target: "[[Boston Dynamics]]"
    type: caused
    confidence: 1.0
  - target: "[[动态平衡]]"
    type: implements
    confidence: 1.0
  - target: "[[弹簧 - 质量模型]]"
    type: uses
    confidence: 0.9
supersedes: null
---

# Marc H. Raibert

## 概述
Marc H. Raibert 是美国著名的计算机科学家和机器人学家，被誉为现代动态腿式机器人之父。他于 1977 年在麻省理工学院（MIT）获得博士学位，随后在卡内基梅隆大学（CMU）任教并创建了 Leg Laboratory（腿实验室）。1986 年，他将实验室迁回 MIT 并出版了开创性专著《[[Legged Robots That Balance]]》。Raibert 最核心的贡献是提出了[[动态平衡]]控制框架，证明了机器人可以通过主动控制实现类似动物的奔跑和跳跃。1992 年，他创办了 [[Boston Dynamics]] 公司，将学术理论转化为 BigDog、Atlas 和 Spot 等震惊世界的机器人产品。

## 关键内容
### 学术生涯与 Leg Laboratory
Raibert 的学术生涯始于对动态系统的深刻洞察。在 CMU 期间，他拒绝了当时主流的静态步行研究[[规范化理论|范式]]，转而探索如何让机器人在非稳定状态下运动。他创建的 Leg Laboratory 成为了全球动态腿式运动研究的中心。他的研究哲学强调"构建即理解"（understanding through building），坚持通过构建物理原型来验证理论，这一方法深刻影响了后来的机器人学研究文化。

### 三分解控制框架的提出
Raibert 最伟大的科学成就是提出了"[[三分解控制框架]]"（[[三分解控制框架|Three-Part Decomposition]]）。他发现复杂的动态腿式运动可以优雅地分解为三个相对独立的子问题：弹跳高度控制（通过能量注入）、前进速度控制（通过落脚点规划）和身体姿态控制（通过髋关节力矩）。这一发现不仅解决了高维非线性系统的控制难题，还揭示了不同腿数动物运动背后的统一原理。

### 从单腿到多腿的扩展
Raibert 展示了其控制框架惊人的可扩展性。他从最简单的单腿弹跳机器人入手，成功将控制逻辑推广到双足跑步机器人和四足多步态机器人。通过引入"虚拟腿"（virtual leg）的概念，他证明了四足动物的 trot（小跑）、pace（同侧步）和 bound（跳跃）等步态本质上都是单腿控制策略的时序编排。这一成果打破了以往每种腿数需要独立设计控制器的局限。

### 创办 Boston Dynamics
1992 年，Raibert 离开学术界创办了 [[Boston Dynamics]]，将[[动态平衡]]理论工程化。在他的领导下，公司开发了 BigDog（2005），这是第一台能在崎岖地形自主运行的液压驱动四足机器人；Atlas（2013），具备后空翻和跑酷能力的人形机器人；以及 Spot（2019），首款商业化的四足机器人。这些产品不仅验证了 Raibert 三十年前提出的理论，更推动了整个机器人行业的进步。

### 荣誉与影响
Raibert 的工作完成了腿式机器人从"静态稳定"到"动态稳定"的[[规范化理论|范式]]转移。他的专著《[[Legged Robots That Balance]]》被引用数千次，成为该领域被引频率最高的文献之一。他与生物力学领域的交叉研究（如与 Robert Full 和 Reinhard Blickhan 的合作）进一步验证了[[弹簧 - 质量模型]]在描述动物运动时的普适性。Raibert 的研究方法论和控制思想至今仍是理解动态腿式运动的基石。

## 来源
- [[raw/books/机器人学/09-raibert-legged-robots-balance.md]]

## 相关
- [[Legged Robots That Balance]]
- [[Boston Dynamics]]
- [[动态平衡]]
- [[弹簧 - 质量模型]]