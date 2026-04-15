---
type: concept
title: "Denavit-Hartenberg 参数"
status: active
confidence: 1.0
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags:
  - 机器人学
  - 矩阵理论
  - 方法论
  - 工具
aliases:
  - DH 参数
  - DH Convention
  - D-H Notation
relates_to:
  - target: "[[Jacques Denavit]]"
    type: caused
    confidence: 1.0
  - target: "[[Richard S. Hartenberg]]"
    type: caused
    confidence: 1.0
  - target: "[[齐次变换矩阵]]"
    type: uses
    confidence: 1.0
  - target: "[[旋量理论]]"
    type: contradicts
    confidence: 0.8
  - target: "[[改进的 DH 约定]]"
    type: extends
    confidence: 0.9
supersedes: null
---

# Denavit-Hartenberg 参数

## 概述
Denavit-Hartenberg（DH）参数是一种用于描述串联机器人机械臂及低副机构运动学关系的标准化符号系统。该方法由 Jacques Denavit 和 Richard S. Hartenberg 于 1955 年提出，核心思想是通过四个几何参数（关节角 $\theta$、连杆偏距 $d$、连杆长度 $a$、连杆扭角 $\alpha$）完整定义相邻连杆坐标系之间的相对位姿。通过将这种关系转化为 4×4 齐次变换矩阵并进行链式乘法，DH 参数为计算机辅助运动学分析提供了统一且高效的数学框架，被誉为机器人运动学的“通用语言”。

## 关键内容

### 1. 核心参数定义
DH 方法证明了描述两个相邻连杆间相对位置和方向所需的最小参数数量为四个。对于旋转关节，$\theta$ 为变量；对于移动关节，$d$ 为变量。具体定义如下：
*   **关节角 ($\theta$)**：绕 $z_{i-1}$ 轴旋转，使 $x_{i-1}$ 轴与 $x_i$ 轴平行或重合的角度。
*   **连杆偏距 ($d$)**：沿 $z_{i-1}$ 轴测量，从 $x_{i-1}$ 轴到 $x_i$ 轴的距离。
*   **连杆长度 ($a$)**：沿 $x_i$ 轴测量，从 $z_{i-1}$ 轴到 $z_i$ 轴的距离（即公垂线长度）。
*   **连杆扭角 ($\alpha$)**：绕 $x_i$ 轴旋转，使 $z_{i-1}$ 轴与 $z_i$ 轴平行或重合的角度。

### 2. 坐标系建立规则
为了消除歧义，DH 方法规定了严格的坐标系附着规则：
1.  **$z$ 轴**：始终沿第 $i$ 个关节的运动轴方向。
2.  **$x$ 轴**：沿相邻两个 $z$ 轴（$z_{i-1}$ 和 $z_i$）的公垂线方向，指向从 $i-1$ 到 $i$。
3.  **$y$ 轴**：根据右手定则确定，补全直角坐标系。
这一规则确保了任意开链机构的几何结构都能被唯一地参数化（除平行轴奇异性外）。

### 3. 齐次变换矩阵与链式法则
相邻坐标系 $i-1$ 到 $i$ 的变换矩阵 $T_{i-1}^i$ 由四个基本变换组合而成：
$$ T_{i-1}^i = \text{Rot}(z, \theta_i) \cdot \text{Trans}(z, d_i) \cdot \text{Trans}(x, a_i) \cdot \text{Rot}(x, \alpha_i) $$
展开后的矩阵形式为标准 4×4 矩阵。对于包含 $n$ 个关节的机械臂，末端执行器相对于基座的位姿 $T_0^n$ 可通过矩阵连乘获得：
$$ T_0^n = T_0^1 \cdot T_1^2 \cdot \dots \cdot T_{n-1}^n $$
这种链式组合特性使得复杂的空间运动学问题转化为标准的线性代数运算，极大地简化了计算机求解过程。

### 4. 局限性与现代视角
尽管 DH 参数是行业标准，但其存在局限性：
*   **奇异性问题**：当相邻关节轴平行时，公垂线不唯一，导致坐标系定义不确定。为此，John Craig 提出了“改进的 DH 约定”（Modified DH）。
*   **适用范围**：主要适用于开链机构，处理并联机构（闭环）时需额外引入约束方程。
*   **替代方案**：现代理论中，基于李群和李代数的**旋量理论（Screw Theory）**提供了更优雅的数学描述，避免了部分奇异性，但在工程实践和教学中，DH 参数因其直观性仍占据主导地位。

## 来源
- [[raw/books/机器人学/01-denavit-hartenberg-kinematic-notation.md]]

## 相关
- [[Jacques Denavit]]
- [[Richard S. Hartenberg]]
- [[齐次变换矩阵]]
- [[旋量理论]]
- [[改进的 DH 约定]]