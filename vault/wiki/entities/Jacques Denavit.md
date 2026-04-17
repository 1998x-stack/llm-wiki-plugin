---
type: entity
title: "Jacques Denavit"
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags:
  - 机器人学
  - 研究
  - 方法论
aliases:
  - J. Denavit
relates_to:
  - target: "[[Denavit-Hartenberg 参数]]"
    type: caused
    confidence: 1.0
  - target: "[[Richard S. Hartenberg]]"
    type: caused
    confidence: 1.0
  - target: "[[Northwestern University]]"
    type: depends_on
    confidence: 0.9
supersedes: null
---

# Jacques Denavit

## 概述
Jacques Denavit 是一位在机构学和机器人学领域具有开创性贡献的学者。他最著名的成就是与 [[Richard S. Hartenberg]] 合作，于 1955 年发表了里程碑式的论文《[[A Kinematic Notation for Lower-Pair Mechanisms Based on Matrices]]》。在这项工作中，他们共同提出了后来被称为"Denavit-Hartenberg (DH) 参数”的运动学描述方法。这一方法彻底改变了多连杆机构和机器人机械臂的建模方式，将复杂的几何关系转化为系统的[[矩阵]]运算，成为现代机器人学事实上的标准语言。

## 关键内容

### 1. 学术背景与合作
1955 年，Jacques Denavit 任职于美国**Northwestern University**（西北大学）。当时，机构学领域缺乏统一的运动学描述符号，不同的研究者使用各异的坐标约定，导致成果难以比较和复用。Denavit 敏锐地捕捉到了[[矩阵]]代数在工程计算中的潜力，并与同事 [[Richard S. Hartenberg]] 展开了深入合作。

### 2. 核心贡献：DH 参数的提出
Denavit 与 Hartenberg 的核心洞见在于证明了**四个参数足以完整描述任意两个相邻连杆间的空间关系**。他们不仅定义了这四个参数（$\theta, d, a, \alpha$），还制定了一套严格的坐标系建立规则（$z$ 轴沿关节轴，$x$ 轴沿公垂线）。
这项工作解决了当时空间机构分析的几个关键痛点：
*   **最小化参数**：确定了描述相邻连杆关系的最少变量数。
*   **系统化表示**：消除了人为定义坐标系时的随意性和歧义。
*   **计算友好**：将运动学问题转化为适合计算机处理的[[矩阵]]连乘形式。

### 3. 历史影响
虽然论文发表时现代工业机器人尚未诞生（[[Unimate]] 于 1961 年问世），但 Denavit 的工作为即将到来的机器人革命奠定了理论基础。他的方法被后来的机器人学先驱如 [[Richard P. Paul|Richard Paul]] 和 John Craig 广泛采纳并写入经典教材。直到今天，全球绝大多数机器人学课程的第一课仍是学习 Denavit 建立的这套符号系统。他的工作被视为连接经典机构学与现代计算机辅助机器人学的桥梁。

### 4. 研究领域
Denavit 的研究主要集中在**机构学（Mechanism Theory）**和**运动学（Kinematics）**。他致力于寻找描述机械系统运动的通用数学语言，其工作不仅限于理论推导，更注重方法的实用性和系统性，为后续的动力学分析和控制算法提供了必要的几何基础。

## 来源
- [[raw/books/机器人学/01-denavit-hartenberg-kinematic-notation.md]]

## 相关
- [[Denavit-Hartenberg 参数]]
- [[Richard S. Hartenberg]]
- [[Northwestern University]]
- [[A Kinematic Notation for Lower-Pair Mechanisms Based on Matrices]]