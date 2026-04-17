---
type: entity
title: "Tomas Lozano-Perez"
status: active
confidence: 1.0
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags:
  - AI
  - 机器人学
  - 计算几何
  - 方法论
aliases:
  - Tomas Lozano-Pérez
  - T. Lozano-Perez
relates_to:
  - target: "[[构型空间方法]]"
    type: caused
    confidence: 1.0
  - target: "[[运动规划]]"
    type: extends
    confidence: 1.0
  - target: "[[麻省理工学院人工智能实验室]]"
    type: depends_on
    confidence: 0.9
supersedes: null
---

# Tomas Lozano-Perez

## 概述
Tomas Lozano-Perez 是麻省理工学院（MIT）的终身教授，机器人学与人工智能领域的杰出科学家。他于 1983 年发表的论文《Spatial Planning: A [[构型空间方法|Configuration Space Approach]]》系统地提出了**构型空间（Configuration Space, C-space）**概念，将复杂的机器人[[运动规划]]问题转化为高维空间中的路径搜索问题，奠定了现代[[运动规划]]领域的理论基石。除了[[构型空间方法]]，他在计算机视觉、机器学习和计算化学等领域也有重要贡献。他是 IEEE、ACM 和 AAAI 的 Fellow，美国国家工程院院士，曾获得 IEEE Robotics Pioneer Award (2011) 和 IEEE Robotics and Automation Award (2021)。

## 关键内容

### 学术背景与职业生涯
Tomas Lozano-Perez 的学术生涯几乎全部在 MIT 度过。他于 1973 年获得 MIT 学士学位（SB '73），1976 年获硕士学位（SM '76），并于 1980 年在 MIT 获得博士学位（PhD '80）。他的博士论文及随后的研究工作直接催生了[[构型空间方法]]。他曾担任 MIT 人工智能实验室副主任以及电气工程与计算机科学系计算机科学副系主任。他的研究风格以深厚的数学基础和对实际算法可行性的关注著称，成功地将抽象的计算几何理论应用于具体的机器人控制问题。

### 核心贡献：构型空间方法
Lozano-Perez 最具影响力的工作是将“机器人如何在有障碍物的环境中移动”这一问题进行了概念上的重构。在他之前，避障算法通常直接在工作空间（Work Space）中处理复杂的几何碰撞检测，这种方法难以推广到不同形状的机器人。Lozano-Perez 提出将所有描述机器人位姿的自由度作为坐标轴，构建一个高维的**构型空间**。在这个空间中，机器人被简化为一个点，而障碍物则被映射为“构型空间障碍物”（C-obstacle）。这一转换使得[[运动规划]]问题从“复杂形状物体的穿行”变成了“点在自由空间中的寻路”，极大地统一了该领域的理论框架。

### 其他研究领域
除了[[运动规划]]，Lozano-Perez 的研究兴趣广泛：
*   **计算机视觉**：早期提出了“解释树”（Interpretation Tree）方法，用于从传感器数据中识别物体位姿。
*   **机器学习**：在多实例学习（Multiple Instance Learning）领域有开创性工作，特别是在医学影像分析中的应用。
*   **计算化学**：利用[[运动规划]]算法解决蛋白质折叠和分子对接问题，展示了 C-space 方法在生物学领域的跨学科潜力。

### 荣誉与奖项
鉴于其对机器人学的奠基性贡献，Lozano-Perez 获得了多项顶级荣誉。他是 IEEE、ACM 和 AAAI 三个主要专业协会的 Fellow。2011 年，他因在[[运动规划]]领域的开创性工作获得 IEEE Robotics Pioneer Award；2021 年，他又获得了 IEEE Robotics and Automation Award。他的 1983 年论文被引用超过 3700 次，是机器人学历史上被引用最多的论文之一，其提出的概念已成为现代机器人[[操作系统]]（如 ROS/MoveIt!）和规划库（如 OMPL）的核心基础。

## 来源
- [[raw/books/机器人学/06-lozano-perez-configuration-space.md]]

## 相关
- [[构型空间方法]]
- [[运动规划]]
- [[麻省理工学院人工智能实验室]]