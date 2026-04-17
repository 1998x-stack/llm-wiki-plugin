---
type: entity
title: "Morgan Quigley"
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [AI, 工具，研究, 机器人学]
aliases: ["M. Quigley"]
relates_to:
  - target: "[[ROS (Robot Operating System)]]"
    type: caused
    confidence: 1.0
  - target: "[[Switchyard]]"
    type: caused
    confidence: 1.0
  - target: "[[Andrew Y. Ng]]"
    type: depends_on
    confidence: 0.9
  - target: "[[Willow Garage]]"
    type: depends_on
    confidence: 0.9
  - target: "[[Stanford University]]"
    type: depends_on
    confidence: 0.9
supersedes: null
---

# Morgan Quigley

## 概述
Morgan Quigley 是美国计算机科学家和机器人学家，**ROS **([[ROS (Robot Operating System)|Robot Operating System]]) 的主要创始人之一。他在斯坦福大学攻读博士学位期间，师从 Andrew Y. Ng，参与了 STAIR（STanford Artificial Intelligence Robot）项目。在该项目中，他开发了名为 **Switchyard** 的软件框架，这是 ROS 的直接前身。Quigley 随后加入 [[Willow Garage]]，成为核心工程师，领导了 ROS 的早期架构设计和实现。他是 2009 年发表的经典论文《ROS: an open-source [[ROS (Robot Operating System)|Robot Operating System]]》的第一作者，该论文已成为机器人学领域被引用次数最高的文献之一。

## 关键内容

### 学术背景与 Switchyard 的诞生
Morgan Quigley 在斯坦福大学人工智能实验室（SAIL）攻读博士期间，深入参与了 Andrew Y. Ng 发起的 STAIR 项目。该项目旨在将视觉、语音、操作、导航等多个 AI 子领域统一集成到一台机器人上。面对不同研究生开发的模块之间语言不通、数据格式各异、难以集成的挑战，Quigley 设计了 **Switchyard** 框架。Switchyard 引入了模块化、松耦合的架构理念，允许各子系统独立迭代并通过版本管理保持整体稳定。这一实践验证了分布式通信架构在大型机器人项目中的可行性，为 ROS 的核心理念奠定了坚实基础。

### 在 Willow Garage 的角色
毕业后，Quigley 加入了新成立的 [[Willow Garage]]，担任核心工程师。在这里，他将 Switchyard 的概念进一步工程化，演变为 ROS。他主导了 ROS 计算图模型（节点、话题、服务）的设计，确立了发布 - 订阅通信机制和语言无关的消息序列化方案。作为第一作者，他与 Ken Conley, [[Brian Gerkey]] 等人共同撰写了 2009 年 ICRA Workshop 论文，正式向世界介绍了 ROS。这篇论文虽然篇幅短小，却开启了一场机器人软件的运动。

### 技术影响
Quigley 的贡献不仅在于代码实现，更在于他对机器人软件[[规范化理论|范式]]的重新定义。他主张机器人软件不应是 monolithic（单体）的，而应是由可复用组件构成的生态系统。他的设计理念使得 ROS 能够跨越硬件差异，支持从低成本教育机器人到复杂人形机器人的广泛应用。尽管后来 ROS 演进为 ROS 2，但其核心的通信抽象和哲学依然深深烙印着 Quigley 早期的设计思想。他的工作极大地降低了机器人研究的门槛，加速了全球机器人技术的创新节奏。

## 来源
- [[raw/books/机器人学/13-quigley-ros-robot-operating-system.md]]

## 相关
- [[ROS (Robot Operating System)]]
- [[Switchyard]]
- [[Andrew Y. Ng]]
- [[Willow Garage]]
- [[Brian Gerkey]]