---
type: concept
title: "SLAM"
status: active
confidence: 0.97
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [机器人学, 定位, 建图, 概率推理, SLAM]
aliases:
  - 同时定位与建图
  - Simultaneous Localization and Mapping
  - 机器人SLAM
relates_to:
  - target: "[[卡尔曼滤波]]"
    type: uses
    confidence: 0.9
  - target: "[[贝叶斯推理]]"
    type: uses
    confidence: 0.95
  - target: "[[运动规划]]"
    type: related_to
    confidence: 0.8
  - target: "[[概率路线图 (PRM)]]"
    type: related_to
    confidence: 0.7
supersedes: null
---

# SLAM

## 概述

SLAM（Simultaneous Localization and Mapping，同时定位与建图）是移动机器人学的核心问题：在地图和自身位置均未知的条件下，机器人如何边走边建图、边建图边定位——打破"需要地图才能定位、需要定位才能建图"的循环依赖。

## 关键内容

### 问题定义

已知观测序列 z₁:t 和[[优化控制序|控制序]]列 u₁:t，同时估计：
- 机器人位姿序列 x₁:t（定位）
- 环境地图 m（建图）
- 即求后验 P(x₁:t, m | z₁:t, u₁:t)

**核心困难**：定位需要地图，建图需要精确位置——形成循环依赖（"鸡生蛋"问题）。

### 三大算法范式

| 范式 | 核心方法 | 复杂度 | 特点 |
|------|---------|--------|------|
| **E[[卡尔曼滤波|KF]]-SLAM** | 扩展[[卡尔曼滤波]]，联合估计所有地标 | O(n²) | 理论清晰，不可扩展 |
| **FastSLAM** | Rao-Blackwellized 粒子滤波，轨迹-地标分解 | O(n log n) | 复杂度突破，可扩展到数万地标 |
| **GraphSLAM** | 图优化，位姿/地标为节点，约束为边 | 稀疏[[矩阵]]求解 | 全局一致性，适合离线大图 |

**FastSLAM 核心洞察**：已知机器人轨迹后，各地标的位置估计相互独立，可用独立的[[卡尔曼滤波]]处理，将复杂度从 O(n²) 降至 O(n log n)。

**GraphSLAM 贡献**：将 SLAM 建模为约束满足问题，利用稀疏结构实现高效全局优化，催生了 g2o、iSAM、GTSAM 等框架。

### 地图表示形式

- **占据栅格地图**（Occupancy Grid）：将环境离散为网格，每格标注占据概率。直观完整，适合激光雷达。
- **特征地图**（Feature-based）：用角点、线段等几何特征表示环境。存储高效，依赖特征提取。
- **拓扑地图**（Topological）：用图结构表示连接关系。抽象度高，适合大尺度导航。

### 历史演进

- 1986年：R.C. Smith & P. Cheeseman 提出雏形
- 1990年代：Hugh Durrant-Whyte & John Leonard 正式化
- 2000年代：[[Sebastian Thrun]] 等在《[[Probabilistic Robotics]]》中系统化，成为"机器人学圣杯"
- 2007年后：视觉 SLAM（PTAM, ORB-SLAM）崛起，RGB-D SLAM 普及
- 2010年代：图优化成为主流后端（g2o, GTSAM）

### 现代发展

- **视觉 SLAM**：用摄像头替代激光雷达，ORB-SLAM3、LIO-SAM 等方案广泛使用
- **深度学习 SLAM**：SuperPoint/SuperGlue 替代手工特征，神经网络估计深度
- **语义 SLAM**：在几何地图上叠加物体类别信息（"桌子在 A 处，椅子在 B 处"）
- **神经场景表示**：NeRF、3D Gaussian Splatting 作为新型地图形式

## 来源

- [[raw/books/机器人学/12-thrun-probabilistic-robotics.md]]

## 相关

- [[卡尔曼滤波]] — EKF-SLAM 的基础算法
- [[贝叶斯推理]] — SLAM 的统一理论框架
- [[运动规划]] — SLAM 提供地图，运动规划在地图上规划路径
- [[Sebastian Thrun]] — FastSLAM、GraphSLAM 的主要贡献者
