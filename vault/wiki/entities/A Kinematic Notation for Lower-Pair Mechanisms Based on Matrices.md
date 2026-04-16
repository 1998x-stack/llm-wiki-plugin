---
type: entity
title: "A Kinematic Notation for Lower-Pair Mechanisms Based on Matrices"
status: active
confidence: 1.0
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags:
  - 机器人学
  - 研究
  - 方法论
aliases:
  - Denavit-Hartenberg 1955 Paper
  - DH Original Paper
relates_to:
  - target: "[[Denavit-Hartenberg 参数]]"
    type: caused
    confidence: 1.0
  - target: "[[Jacques Denavit]]"
    type: caused
    confidence: 1.0
  - target: "[[Richard S. Hartenberg]]"
    type: caused
    confidence: 1.0
  - target: "[[ASME Journal of Applied Mechanics]]"
    type: depends_on
    confidence: 1.0
supersedes: null
---

# A Kinematic Notation for Lower-Pair Mechanisms Based on Matrices

## 概述
《A Kinematic Notation for Lower-Pair Mechanisms Based on Matrices》是由 [[Jacques Denavit]] 和 [[Richard S. Hartenberg]] 于 1955 年 6 月发表在《ASME Journal of Applied Mechanics》上的里程碑式论文。该文首次提出了利用四个参数和[[齐次变换矩阵]]来系统化描述任意低副机构（Lower-Pair Mechanisms）运动学关系的方法。这篇论文不仅解决了当时机构学领域描述方法混乱的问题，更为后来诞生的机器人学提供了核心的数学工具——**Denavit-Hartenbe[[ripgrep|rg]] (DH) 参数**，被公认为机器人运动学理论的奠基之作。

## 关键内容

### 1. 发表背景与动机
在 1955 年之前，机构学领域缺乏统一的运动学描述标准。德国工程师 Franz Reuleaux 的符号系统虽具开创性，但无法定量描述空间运动所需的变量数量。随着航空航天和自动化技术的发展，**空间机构**（三维运动）的分析需求激增，传统的几何直觉方法显得笨拙且难以计算机化。同时，[[矩阵]]代数在工程中的应用正在兴起，但缺乏将其应用于机构几何关系的系统方法。本论文旨在回答：**能否找到一种最小化、系统化的符号体系，用方程和[[矩阵]]无歧义地描述任意空间机构？**

### 2. 核心理论与方法
论文提出了革命性的解决方案：
*   **四参数充分性证明**：作者证明了两个相邻连杆间的相对位姿仅需四个参数（$\theta, d, a, \alpha$）即可完整描述。这是[[信息论]]意义上的最小表示，利用了相邻关节轴之间的几何约束，将刚体变换的 6 个自由度压缩至 4 个。
*   **坐标系建立规则**：定义了严格的坐标系附着规则（$z$ 轴沿关节轴，$x$ 轴沿公垂线），消除了人为定义的歧义。
*   **[[矩阵]]变换公式**：推导了标准的 4×4 [[齐次变换矩阵]]形式，将旋转和平移操作统一表达。
*   **链式乘法原理**：展示了如何通过[[矩阵]]连乘（$T_{0n} = T_{01} \cdot T_{12} \cdots$）求解多连杆系统的末端位姿，实现了运动学分析的算法化。

### 3. 验证与实例
作为一篇理论方法论文，作者通过两个具体的空间机构实例验证了方法的可行性：
1.  **空间四杆机构**的运动学分析。
2.  **空间曲柄滑块机构**的运动学分析。
结果显示，DH 方法能够系统地处理三维复杂运动链，得出的结果与传统几何方法一致，但过程更加规范且易于推广。

### 4. 历史地位与局限性
*   **历史地位**：该论文是机器人学的“语法”起源。尽管发表时现代工业机器人尚未问世，但它为 1960 年代以后的机器人技术发展提供了现成的数学语言。[[Richard P. Paul|Richard Paul]] (1981) 和 John Craig (1986) 等后续学者将其系统化并推广至整个机器人社区。
*   **局限性**：论文也指出了方法的一些固有局限，如在处理平行关节轴时的奇异性问题（公垂线不唯一），以及主要针对开链机构的设计。这些局限在后来的研究中催生了“改进的 [[Denavit-Hartenberg 参数|DH 约定]]”和旋量理论等补充方法。

### 5. 引用信息
*   **期刊**: ASME Journal of Applied Mechanics, Vol. 22, Issue 2, pp. 215–221
*   **DOI**: 10.1115/1.4011045
*   **单位**: Northwestern University, USA

## 来源
- [[raw/books/机器人学/01-denavit-hartenberg-kinematic-notation.md]]

## 相关
- [[Denavit-Hartenberg 参数]]
- [[Jacques Denavit]]
- [[Richard S. Hartenberg]]
- [[ASME Journal of Applied Mechanics]]
- [[齐次变换矩阵]]