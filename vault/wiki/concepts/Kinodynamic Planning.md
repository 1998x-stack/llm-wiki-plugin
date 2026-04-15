---
type: concept
title: "Kinodynamic Planning"
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [AI, 研究，方法论]
aliases: ["Kinodynamic Motion Planning", "动力学运动规划"]
relates_to:
  - target: "[[快速扩展随机树 (RRT)]]"
    type: implements
    confidence: 0.95
  - target: "[[运动规划]]"
    type: extends
    confidence: 1.0
supersedes: null
---

# Kinodynamic Planning

## 概述
Kinodynamic Planning（动力学运动规划）是一类同时考虑运动学约束（如非完整约束）和动力学约束（如速度、加速度、力矩限制）的运动规划问题。与传统仅关注几何路径的运动规划不同，Kinodynamic Planning 要求在状态空间（包括位置和速度）中寻找一条满足系统微分方程约束的可行轨迹。该概念由 Bruce Donald、Patrick Xavier、John Canny 和 John Reif 于 1993 年系统化提出，是高维复杂机器人系统规划的核心挑战。

## 关键内容

### 问题定义与挑战
Kinodynamic Planning 的核心难点在于状态空间的维度加倍（位置 + 速度）以及可达区域的复杂性。对于一个 $n$ 自由度的机械臂，其状态空间维度为 $2n$。在此空间中，任意两个状态之间不能简单地通过直线连接，因为系统必须遵循动力学方程 $\dot{x} = f(x, u)$，其中 $u$ 是控制输入。这意味着从一个状态到另一个状态的转移必须是通过合法的控制输入演化而来的轨迹，而非几何上的捷径。传统基于网格的方法因维数灾难在此类问题中失效，而基于势场的方法容易陷入局部极小值。

### RRT 的解决方案
**[[快速扩展随机树 (RRT)]]** 的出现为 Kinodynamic Planning 提供了革命性的解决方案。RRT 的扩展步骤天然支持前向模拟：算法不需要解决困难的两点边值问题（即如何从状态 A 精确移动到状态 B），只需从当前状态 $x_{near}$ 选择一个随机控制输入 $u$，对动力学方程进行短时间积分得到新状态 $x_{new}$。只要模拟器是物理正确的，生成的每一步运动自动满足所有的运动和动力学约束。这种“构建即可行”的特性使得 RRT 成为该领域事实上的标准方法。

### 应用领域
Kinodynamic Planning 在许多实际场景中至关重要，包括：
*   **自动驾驶**：车辆不仅有转向角限制（非完整），还有加速度和加加速度（jerk）限制，以确保乘客舒适和车辆稳定。
*   **航空航天**：飞行器和卫星的姿态控制受到推力大小和方向的严格限制。
*   **高速机械臂**：高速运动的机械臂必须考虑惯性力和力矩限制，以避免结构损坏或失控。
RRT 及其变体（如 Kinodynamic RRT*）在这些领域中成功实现了复杂动态系统的实时轨迹规划。

## 来源
- [[raw/books/机器人学/11-lavalle-rapidly-exploring-random-trees.md]]

## 相关
- [[快速扩展随机树 (RRT)]]
- [[运动规划]]
- [[非完整约束]]