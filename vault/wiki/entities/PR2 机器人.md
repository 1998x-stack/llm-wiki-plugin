---
type: entity
title: "PR2 机器人"
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [AI, 工具，研究, 机器人学]
aliases: ["Personal Robot 2", "PR2"]
relates_to:
  - target: "[[ROS (Robot Operating System)]]"
    type: implements
    confidence: 1.0
  - target: "[[Willow Garage]]"
    type: depends_on
    confidence: 1.0
  - target: "[[PR1 机器人]]"
    type: extends
    confidence: 0.9
supersedes: null
---

# PR2 机器人

## 概述
**[[Probabilistic Robotics|PR]]2 **(Personal Robot 2) 是由 **[[Willow Garage]]** 开发的一款全尺寸移动操作机器人平台，被视为 [[ROS (Robot Operating System)]] 的旗舰硬件载体。[[Probabilistic Robotics|PR]]2 造价高昂（约 40 万美元），配备两条 7 自由度手臂、可倾斜激光雷达、多个摄像头及全向移动底座。它不仅是 [[Willow Garage]] 技术实力的展示，更是 ROS 生态系统的"杀手级应用"。通过 2010 年启动的 [[Probabilistic Robotics|PR]]2 Beta Program，[[Willow Garage]] 免费向全球 11 所顶尖研究机构赠送了该机器人，极大地加速了 ROS 的普及和机器人学研究的发展。

## 关键内容

### 硬件规格与设计理念
[[Probabilistic Robotics|PR]]2 是一款高度集成的研究型机器人，设计目标是支持复杂的日常操作任务。其主要特征包括：
*   **双机械臂**：两条 7 自由度手臂，具备力控能力，可执行抓取、折叠衣物、操作门把手等精细动作。
*   **感知系统**：头部装有可俯仰的 Hokuyo 激光雷达用于建图和定位，胸部和手臂配备多个 RGB 摄像头用于视觉识别，全身覆盖触觉传感器。
*   **移动底盘**：采用全向轮设计，可在狭窄空间灵活移动。
*   **计算平台**：板载多台高性能计算机，运行 Ubuntu Linux 和 ROS 系统，处理海量的传感器数据和复杂的规划算法。

### 与 ROS 的共生关系
[[Probabilistic Robotics|PR]]2 与 ROS 是相辅相成的关系。[[Probabilistic Robotics|PR]]2 的所有软件栈——从底层电机驱动、传感器融合到高层的任务规划、人机交互——完全构建在 ROS 之上。[[Willow Garage]] 利用 [[Probabilistic Robotics|PR]]2 完成了一系列里程碑式的演示，如自主导航、开门、叠毛巾、从冰箱取啤酒等，这些演示有力地证明了 ROS 支撑复杂多模态系统的能力。反过来，[[Probabilistic Robotics|PR]]2 的复杂性也推动了 ROS 工具链（如 [[TensorFlow|TF]] 坐标变换、MoveIt! [[运动规划]]）的成熟和完善。

### PR2 Beta Program 的历史意义
2010 年，[[Willow Garage]] 实施了著名的 **[[Probabilistic Robotics|PR]]2 Beta Program**，将 11 台 [[Probabilistic Robotics|PR]]2 机器人免费赠送给 MIT、UC Berkeley、斯坦福、佐治亚理工、弗莱堡大学等机构。这一举措在机器人学界引起了轰动。获得 [[Probabilistic Robotics|PR]]2 的实验室迅速成为了 ROS 创新的中心，产出了大量高影响力的研究成果，并反向为 ROS 贡献了数千个功能包。这种"种子投放"策略成功地在全球范围内建立了一个紧密协作的研究者网络，确立了 ROS 作为机器人软件事实标准的地位。尽管 [[Probabilistic Robotics|PR]]2 本身因成本过高未能量产商业化，但它作为研究平台的价值不可估量，被誉为机器人学界的"Model T"。

## 来源
- [[raw/books/机器人学/13-quigley-ros-robot-operating-system.md]]

## 相关
- [[ROS (Robot Operating System)]]
- [[Willow Garage]]
- [[PR1 机器人]]
- [[TurtleBot]]