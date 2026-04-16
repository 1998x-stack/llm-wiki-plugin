---
type: entity
title: "Richard S. Hartenberg"
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
  - R. S. Hartenberg
  - Richard Hartenberg
relates_to:
  - target: "[[Denavit-Hartenberg 参数]]"
    type: caused
    confidence: 1.0
  - target: "[[Jacques Denavit]]"
    type: caused
    confidence: 1.0
  - target: "[[Northwestern University]]"
    type: depends_on
    confidence: 0.9
supersedes: null
---

# Richard S. Hartenberg

## 概述
Richard S. Hartenbe[[ripgrep|rg]] 是 20 世纪中期著名的机构学专家，以其在运动学符号系统化方面的杰出贡献而闻名。他与 [[Jacques Denavit]] 共同撰写的 1955 年论文《[[A Kinematic Notation for Lower-Pair Mechanisms Based on Matrices]]》是机器人学历史上引用率最高的文献之一。在这篇论文中，Hartenbe[[ripgrep|rg]] 与 Denavit 共同发明了**Denavit-Hartenbe[[ripgrep|rg]] (DH) 参数**，这套方法至今仍是描述机器人机械臂运动学的国际标准。他在推动[[矩阵]]方法在机械工程中的应用方面发挥了关键作用。

## 关键内容

### 1. 学术生涯与背景
Richard S. Hartenbe[[ripgrep|rg]] 在 1950 年代任职于**Northwestern University**，与 [[Jacques Denavit]] 同为该校的研究人员。当时的工程界正经历从图解法向解析法转变的过程，计算机的出现使得[[矩阵]]运算成为可能，但缺乏统一的几何建模标准。Hartenbe[[ripgrep|rg]] 意识到，若要实现机构分析的自动化，必须建立一套无歧义的数学描述体系。

### 2. 开创性工作：统一运动学语言
Hartenbe[[ripgrep|rg]] 与 Denavit 的合作成果解决了当时机构学领域的混乱局面。在此之前，如 Franz Reuleaux 等前辈的符号系统仅能定性描述拓扑结构，无法进行定量的空间计算。Hartenbe[[ripgrep|rg]] 参与构建的 DH 方法具有以下突破性：
*   **完备性**：证明了四个参数即可完整描述低副机构中相邻构件的相对运动。
*   **规范性**：制定了明确的坐标系附着规则，使得不同研究者对同一机构的建模结果一致。
*   **可扩展性**：通过[[齐次变换矩阵]]的连乘，轻松处理任意长度的运动链。

### 3. 对机器人学的深远影响
尽管 Hartenbe[[ripgrep|rg]] 发表论文时，现代意义上的“机器人”概念尚未完全形成，但他的工作意外地成为了机器人学的基石。随着 1960 年代工业机器人的兴起，工程师们发现 DH 参数完美契合了串联机械臂的建模需求。
*   **教材标准化**：从 [[Richard P. Paul|Richard Paul]] 到 John Craig，再到现代的 Siciliano 和 Lynch & Park，所有主流机器人学教材均以 Hartenbe[[ripgrep|rg]] 和 Denavit 的方法作为运动学章节的核心。
*   **工业应用**：几乎所有工业机器人的控制器底层算法、仿真软件（如 ROS, Gazebo, MATLAB Robotics Toolbox）都依赖 DH 参数进行正向运动学解算。

### 4. 遗产
Richard S. Hartenbe[[ripgrep|rg]] 的名字永远与"DH 参数”联系在一起。他的工作展示了如何通过精妙的数学抽象将复杂的物理几何问题简化为标准的代数运算。这种方法论不仅影响了机器人学，也对计算机图形学、动画骨骼绑定等领域产生了间接影响。他是将经典机构学带入数字化时代的先驱之一。

## 来源
- [[raw/books/机器人学/01-denavit-hartenberg-kinematic-notation.md]]

## 相关
- [[Denavit-Hartenberg 参数]]
- [[Jacques Denavit]]
- [[Northwestern University]]
- [[A Kinematic Notation for Lower-Pair Mechanisms Based on Matrices]]