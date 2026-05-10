---
type: entity
title: "PUMA 机器人"
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [工具，研究, 机器人学]
aliases: ["PUMA 560", "Programmable Universal Machine for Assembly", "Unimation PUMA"]
relates_to:
  - target: "[[Robot Manipulators: Mathematics, Programming, and Control]]"
    type: uses
    confidence: 1.0
  - target: "[[Unimation]]"
    type: caused
    confidence: 0.9
  - target: "[[Stanford Arm]]"
    type: contradicts
    confidence: 0.5
supersedes: null
---

# PUMA 机器人

## 概述
PUMA（Programmable Universal Machine for Assembly）系列机器人是由 [[Unimate|Unimation]] 公司在 1970 年代末推出的一款标志性工业机器人，其中 PUMA 560 型号最为著名。它是第一台由小型[[计算]]机控制的多用途装配机器人，迅速成为工业自动化的标杆产品。在 [[Richard P. Paul]] 的经典著作《[[Robot Manipulators: Mathematics, Programming, and Control|Robot Manipulators]]》中，PUMA 560 被选作核心教学案例，全书的理论推导（从 DH 参数建模到逆运动学解析解）均围绕该机器人展开。PUMA 机器人的广泛应用和 Paul 的深入分析，使其成为机器人学教育和研究中最具代表性的实体模型之一。

## 关键内容
### 历史背景与技术特征
PUMA 系列诞生于工业机器人商业爆发的初期。不同于早期的专用自动化设备，PUMA 旨在提供通用的装配解决方案。PUMA 560 拥有六个旋转自由度，采用典型的“球形手腕”构型（后三轴相交于一点），这种设计极大地简化了逆运动学的求解过程。它由小型[[计算]]机（如 LSI-11）控制，支持更复杂的编程和传感器集成，代表了当时机器人技术的最高水平。其市场成功证明了基于数学模型的通用机器人在汽车制造（点焊、喷涂）等领域的巨大价值。

### 在机器人学理论中的特殊地位
PUMA 560 之所以在学术界享有盛誉，很大程度上归功于 [[Richard P. Paul]] 的专著。Paul 选择 PUMA 560 作为贯穿全书的工程实例，完成了从物理实体到数学模型的完整映射：
1.  **DH 参数标定**：书中给出了 PUMA 560 精确的 DH 参数表，成为后世验证运动学[[算法]]的标准数据集。
2.  **逆运动学解析解**：Paul 利用 PUMA 的球形手腕特性，详细推导了其逆运动学的 16 组封闭解（对应肘上/肘下、肩左/肩右、腕翻转/不翻转等不同构型）。这一推导过程不仅展示了代数求解技巧，更揭示了机器人几何结构与解析可解性之间的深刻联系。
3.  **轨迹规划与控制**：书中的轨迹规划[[算法]]和力控制策略也均以 PUMA 为对象进行了数值验证。

### 教育与研究的基准
由于 Paul 著作的广泛影响，PUMA 560 成为了全球机器人学课程的“标准实验台”。即使在没有实物机器人的情况下，学生和研究者也使用其数学模型进行[[算法]]开发和仿真测试。许多经典的机器人学[[算法]]（如逆运动学求解器、奇异点回避策略、动力学参数辨识）都在 PUMA 模型上进行了首次验证或基准测试。可以说，PUMA 560 不仅是工业史上的里程碑，也是机器人学理论发展史上的重要载体。

### 遗产与影响
虽然 PUMA 系列机器人已逐渐退出工业生产一线，但其设计理念（特别是球形手腕）和数学模型依然活跃在现代机器人技术中。它的 DH 参数和运动学方程被内置于无数仿真软件（如 MATLAB Robotics Toolbox, Gazebo, V-REP）和教育代码库中。每当新一代机器人工程师学习逆运动学时，他们大概率仍在求解那个四十多年前由 Paul 定义的 PUMA 方程。PUMA 因此超越了其作为单一产品的生命周期，成为了机器人学知识体系中一个永恒的象征。

## 来源
- [[raw/books/机器人学/05-paul-robot-manipulators-mathematics.md]]

## 相关
- [[Robot Manipulators: Mathematics, Programming, and Control]]
- [[Unimation]]
- [[Stanford Arm]]