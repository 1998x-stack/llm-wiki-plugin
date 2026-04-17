---
type: entity
title: "Boston Dynamics"
status: active
confidence: 1.0
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [AI, 工具，研究, 机器人学]
aliases: ["BD", "波士顿动力"]
relates_to:
  - target: "[[Marc H. Raibert]]"
    type: implements
    confidence: 1.0
  - target: "[[Legged Robots That Balance]]"
    type: implements
    confidence: 1.0
  - target: "[[动态平衡]]"
    type: implements
    confidence: 1.0
  - target: "[[三分解控制框架]]"
    type: implements
    confidence: 0.9
supersedes: null
---

# Boston Dynamics

## 概述
Boston Dynamics 是一家世界领先的机器人工程公司，成立于 1992 年，由著名机器人学家 [[Marc H. Raibert]] 从麻省理工学院（MIT）离职后创办。公司总部位于美国马萨诸塞州，以其开发的具有高度[[动态平衡]]能力和卓越运动性能的腿式机器人而闻名于世。Boston Dynamics 的产品线涵盖了从四足机器人（如 BigDog, Spot）到人形机器人（如 Atlas）等多种形态，广泛应用于军事、工业巡检、救援搜救及科研领域。公司的核心技术根源可追溯至 [[Marc H. Raibert|Raibert]] 在 MIT Leg Laboratory 期间提出的[[动态平衡]]理论和[[三分解控制框架]]，代表了学术界理论向工业界应用转化的典范。

## 关键内容
### 创立背景与技术渊源
Boston Dynamics 的成立直接源于 [[Marc H. Raibert]] 在 MIT 出版的专著《[[Legged Robots That Balance]]》中提出的理论突破。在 1980 年代，[[Marc H. Raibert|Raibert]] 证明了动态腿式运动的可行性，并构建了单腿、双足和四足的原型机。然而，受限于当时的硬件条件（如液压系统的体积和能源非自主性），这些原型机主要停留在实验室阶段。[[Marc H. Raibert|Raibert]] 创办 Boston Dynamics 的愿景是将这些理论转化为真正实用、自主且强大的机器人系统。公司继承了 MIT Leg Lab"构建即理解"的工程文化，坚持通过物理原型迭代来推动技术进步。

### 代表性产品演进
**BigDog (2005)**：由公司早期研发的四足军用机器人，由 DARPA 资助。BigDog 采用液压驱动，搭载内燃机作为动力源，实现了完全的能源自主。它能够在雪地、碎石路等极端崎岖地形上稳定行走，并展示了惊人的抗扰动能力（如在视频中被踢后恢复平衡）。BigDog 的成功验证了 [[Marc H. Raibert|Raibert]] [[动态平衡]]理论在复杂真实环境中的有效性。

**Atlas (2013-至今)**：一款全尺寸人形机器人，最初为液压驱动，后升级为全电驱动。Atlas 以其惊人的运动能力著称，能够执行后空翻、跑酷、跳跃台阶以及在狭窄空间内灵活移动。Atlas 的控制系统在 [[Marc H. Raibert|Raibert]] 三分解框架的基础上，融合了模型预测控制（MPC）、全身优化（WBC）等现代算法，代表了当前人形机器人技术的最高水平。

**Spot (2019-至今)**：Boston Dynamics 首款商业化成功的四足机器人。Spot 采用全电驱动，噪音低、维护简便，广泛应用于工业巡检、公共安全数据采集和科研教育领域。Spot 的控制系统高度成熟，能够自主导航、避障并适应各种地形，标志着动态腿式机器人正式进入大规模商用阶段。

### 核心技术特点
Boston Dynamics 机器人的核心竞争力在于其先进的[[动态平衡]]控制算法。与传统工业机器人不同，BD 的机器人不依赖预编程的固定轨迹，而是通过实时感知自身状态和环境，利用主动控制力矩来维持平衡。其控制架构深受 [[Marc H. Raibert|Raibert]]"[[三分解控制框架]]"的影响，将运动分解为高度、速度和姿态控制，并通过精确的落脚点规划实现敏捷机动。此外，公司在液压传动、高扭矩密度电机设计及传感器融合方面也拥有深厚的技术积累。

### 行业影响与未来展望
Boston Dynamics 的出现彻底改变了公众和业界对机器人运动能力的认知。其展示的视频在全球范围内 viral 传播，激发了人们对腿式机器人的巨大兴趣和投资热情。公司的成功证明了[[动态平衡]]理论不仅具有学术价值，更能创造巨大的商业和社会价值。随着人工智能和深度[[强化学习]]技术的融入，Boston Dynamics 正在进一步提升机器人的自主决策能力和环境适应性，推动腿式机器人在更多复杂场景中的应用。

### 所有权变迁
自成立以来，Boston Dynamics 经历了多次所有权变更，先后隶属于 Alphabet ([[Google]])、SoftBank 集团，并于 2020 年被现代汽车集团（Hyundai Motor Group）收购。尽管所有者更迭，但公司始终坚持其核心技术路线和工程愿景，持续推出创新的机器人产品。

## 来源
- [[raw/books/机器人学/09-raibert-legged-robots-balance.md]]

## 相关
- [[Marc H. Raibert]]
- [[Legged Robots That Balance]]
- [[动态平衡]]
- [[三分解控制框架]]