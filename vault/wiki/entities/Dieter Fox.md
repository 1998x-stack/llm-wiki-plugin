---
type: entity
title: "Dieter Fox"
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [AI, 研究，人物, 机器人学]
aliases: ["Dieter Fox", "Fox"]
relates_to:
  - target: "[[Probabilistic Robotics]]"
    type: uses
    confidence: 1.0
  - target: "[[蒙特卡罗定位]]"
    type: uses
    confidence: 1.0
  - target: "[[Sebastian Thrun]]"
    type: uses
    confidence: 1.0
  - target: "[[Wolfram Burgard]]"
    type: uses
    confidence: 1.0
supersedes: null
---

# Dieter Fox

## 概述
Dieter Fox 是美国华盛顿大学（University of Washington）教授，著名的机器人学和人工智能专家。他是[[Probabilistic Robotics|概率机器人学]]领域的先驱之一，以在**[[蒙特卡罗定位]]（[[蒙特卡罗定位|MCL]]）**和粒子滤波方法上的开创性贡献而闻名。作为《[[Probabilistic Robotics]]》的三位合著者之一，Fox 与 [[Sebastian Thrun]] 和 [[Wolfram Burgard]] 共同构建了该领域的理论大厦。他的研究工作集中在如何利用概率方法处理机器人感知中的不确定性，特别是在非线性、非[[正态分布|高斯分布]]环境下的状态估计问题，其成果对现代移动机器人和智能家居系统产生了深远影响。

## 关键内容

### 核心学术贡献
Dieter Fox 最显著的成就之一是参与提出了**[[蒙特卡罗定位]]（[[蒙特卡罗定位|MCL]]）**算法。在 1999 年，他与 [[Sebastian Thrun|Thrun]] 和 [[Wolfram Burgard|Burgard]] 合作，首次将粒子滤波系统地应用于机器人全局定位问题。[[蒙特卡罗定位|MCL]] 算法通过维护一组加权样本（粒子）来表示机器人的信念分布，成功解决了传统[[卡尔曼滤波]]无法处理的多模态分布问题（即机器人可能同时位于多个位置的情况）。这一方法后来成为机器人操作系统（ROS）中标准定位模块 [[蒙特卡罗定位|amcl]] 的基础。

### 在概率机器人学中的角色
在《[[Probabilistic Robotics]]》的撰写过程中，Fox 带来了他在统计推断和信号处理方面的深厚背景。他对粒子滤波理论的深入理解帮助团队厘清了不同滤波方法（如 E[[卡尔曼滤波|KF]]、U[[卡尔曼滤波|KF]]、Particle Filter）之间的关系，并将其统一在[[托马斯·贝叶斯|贝叶斯]]滤波框架下。Fox 的工作特别强调算法在实际应用中的可行性和效率，推动了概率方法从理论研究向工程实践的转化。

### 教育与社区影响
作为华盛顿大学的教授，Fox 培养了大量优秀的机器人学人才。他与 [[Sebastian Thrun|Thrun]]、[[Wolfram Burgard|Burgard]] 合著的教科书已成为全球机器人学教育的标准参考书，塑造了整整一代研究者的思维方式。通过这本书以及相关的学术会议和组织，Fox 积极推广概率思维在机器人学中的应用，使得处理不确定性成为现代机器人系统设计的基本准则。

## 来源
- [[raw/books/机器人学/12-thrun-probabilistic-robotics.md]]

## 相关
- [[Probabilistic Robotics]]
- [[蒙特卡罗定位]]
- [[Sebastian Thrun]]
- [[Wolfram Burgard]]