---
type: concept
title: "Probabilistic Robotics"
status: active
confidence: 1.0
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [AI, 方法论，研究，工具]
aliases: ["概率机器人学", "PR"]
relates_to:
  - target: "[[Sebastian Thrun]]"
    type: uses
    confidence: 1.0
  - target: "[[Wolfram Burgard]]"
    type: uses
    confidence: 1.0
  - target: "[[Dieter Fox]]"
    type: uses
    confidence: 1.0
  - target: "[[贝叶斯滤波]]"
    type: implements
    confidence: 1.0
  - target: "[[SLAM]]"
    type: implements
    confidence: 1.0
  - target: "[[蒙特卡罗定位]]"
    type: implements
    confidence: 1.0
  - target: "[[FastSLAM]]"
    type: implements
    confidence: 1.0
  - target: "[[GraphSLAM]]"
    type: implements
    confidence: 1.0
  - target: "[[POMDP]]"
    type: extends
    confidence: 0.9
supersedes: null
---

# Probabilistic Robotics

## 概述
《Probabilistic Robotics》是由 [[Sebastian Thrun]]、[[Wolfram Burgard]] 和 [[Dieter Fox]] 于 2005 年出版的学术专著，被公认为概率机器人学领域的奠基之作。本书系统性地将[[托马斯·贝叶斯|贝叶斯]]概率框架应用于机器人学的核心问题，包括定位（Localization）、建图（Mapping）和[[SLAM|同时定位与建图]]（[[SLAM]]）。它提出将不确定性视为需要管理的信息而非单纯噪声，统一了[[卡尔曼滤波]]、粒子滤波等多种算法，并介绍了 [[蒙特卡罗定位|MCL]]、Fast[[SLAM]] 和 Graph[[SLAM]] 等开创性方法。该书不仅是全球数百所大学的标准教材，其算法实现（如 ROS 中的 [[蒙特卡罗定位|amcl]]）也广泛应用于工业界和自动驾驶领域。

## 关键内容

### 理论框架与核心哲学
本书的核心贡献在于建立了一个统一的**[[托马斯·贝叶斯|贝叶斯]]滤波**理论框架，用于处理机器人感知和行动中的不确定性。传统方法往往试图消除传感器噪声或依赖硬性规则，而本书主张通过概率分布来量化和管理不确定性。其基本递归公式为：$\text{bel}(x_t) = \eta \cdot P(z_t | x_t) \cdot \int P(x_t | u_t, x_{t-1}) \cdot \text{bel}(x_{t-1}) \, dx_{t-1}$。这一框架将看似不同的算法（如[[卡尔曼滤波]]、粒子滤波、信息滤波）统一为同一方程在不同假设下的实例化，极大地简化了算法的选择和理解。

### 三大核心问题的系统化
本书详细定义了机器人学的三个子问题：
1.  **定位（Localization）**：在已知地图下估计机器人状态的后验分布。书中重点介绍了**[[蒙特卡罗定位]]（[[蒙特卡罗定位|MCL]]）**，利用粒子滤波解决全局定位和“绑架机器人”问题，成为行业标准。
2.  **建图（Mapping）**：在已知轨迹下构建环境模型，涵盖了占据栅格地图、特征地图和拓扑地图等多种表示方法。
3.  **[[SLAM]]（[[SLAM|Simultaneous Localization and Mapping]]）**：解决定位与建图的循环依赖问题。书中提出了**Fast[[SLAM]]**（利用 Rao-Blackwellized 粒子滤波将复杂度降至 $O(n \log n)$）和**Graph[[SLAM]]**（将 [[SLAM]] 转化为图优化问题），突破了传统 E[[卡尔曼滤波|KF]]-[[SLAM]] 的规模限制。

### 决策与规划
除了状态估计，本书还将讨论延伸至不确定性条件下的决策，引入了**部分可观测[[马尔可夫]]决策过程（POMDP）**框架。该框架将机器人的任务建模为信念空间中的策略搜索，统一了“探索”与“利用”的权衡，为主动感知和鲁棒规划提供了理论基础。

### 实践验证与影响
书中的理论经过了严格的现实世界验证，包括史密森尼博物馆的 Minerva 导游机器人和赢得 2005 年 DARPA Grand Challenge 的 Stanley 自动驾驶汽车。这些案例证明了概率方法在动态、非结构化环境中的鲁棒性。此外，本书深刻影响了 ROS（[[ROS (Robot Operating System)|Robot Operating System]]）生态系统的设计，其算法构成了现代移动机器人导航栈的核心。

## 来源
- [[raw/books/机器人学/12-thrun-probabilistic-robotics.md]]

## 相关
- [[Sebastian Thrun]]
- [[Wolfram Burgard]]
- [[Dieter Fox]]
- [[贝叶斯滤波]]
- [[SLAM]]
- [[蒙特卡罗定位]]
- [[FastSLAM]]
- [[GraphSLAM]]
- [[POMDP]]