---
type: entity
title: "Willow Garage"
status: inactive
confidence: 1.0
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [AI, 工具，研究, 机器人学]
aliases: ["WG", "Willow Garage Inc."]
relates_to:
  - target: "[[ROS (Robot Operating System)]]"
    type: caused
    confidence: 1.0
  - target: "[[PR2 机器人]]"
    type: caused
    confidence: 1.0
  - target: "[[Open Source Robotics Foundation]]"
    type: caused
    confidence: 1.0
  - target: "[[Scott Hassan]]"
    type: depends_on
    confidence: 1.0
  - target: "[[Brian Gerkey]]"
    type: depends_on
    confidence: 1.0
supersedes: null
---

# Willow Garage

## 概述
Willow Garage 是一家成立于 2006 年的美国机器人技术孵化器，由硅谷企业家 Scott Hassan 创立。该机构致力于个人机器人技术的研发，其最著名的成就是开发了 **ROS **([[ROS (Robot Operating System)|Robot Operating System]]) 开源软件框架和 **PR2** 个人机器人平台。Willow Garage 以坚定的开源承诺著称，不仅将所有软件代码开源，还曾免费向全球顶尖研究机构赠送多台昂贵的 [[PR2 机器人]]，以此培育社区生态。虽然公司于 2014 年关闭，但其遗产通过 Open Source Robotics Foundation (OSRF) 得以延续，深刻塑造了现代机器人学的软件格局。

## 关键内容

### 成立背景与愿景
Willow Garage 的诞生源于创始人 Scott Hassan（[[Google]] 搜索引擎原型技术的共同开发者）对"机器人界 Linux"的愿景。2000 年代中期，机器人软件开发处于碎片化状态，各实验室重复造轮子。Hassan 受到[[斯坦福大学]]博士生 Eric Berger 和 Keenan Wyrobek 关于理想机器人软件框架设计的启发，结合 [[Morgan Quigley]] 在 STAIR 项目中开发的 Switchyard 框架经验，决定成立一家专门机构来解决这一痛点。其目标是打造一个开源的、社区驱动的软件平台，使机器人开发像 Web 开发一样高效协作。

### 核心贡献：ROS 与 PR2
Willow Garage 的核心产出是 **ROS** 和 **[[PR2 机器人]]**。
*   **ROS 的工程化**：虽然 ROS 的概念源自学术界，但 Willow Garage 投入了大量工程资源将其从一个研究原型转化为稳健的工业级框架。公司雇佣了包括 Ken Conley, Josh Faust, Tully Foote 等在内的核心工程师团队，开发了 rviz, rosbag, TF 等关键工具链，并建立了 Wiki 文档和 ROS Answers 社区平台。
*   **PR2 Beta Program**：2010 年，Willow Garage 启动了 PR2 Beta Program，将价值数十万美元的 11 台 [[PR2 机器人]]免费赠送给 MIT、UC Berkeley、[[斯坦福大学|斯坦福]]等全球顶尖高校。这一策略极具远见，迅速在全球范围内培养了一批精通 ROS 的"种子用户"，形成了强大的网络效应，使 ROS 迅速成为事实标准。

### 开源哲学与商业模式
在当时以专有软件为主导的机器人行业，Willow Garage 采取了激进的开源策略。它选择 BSD 许可证以降低商业使用门槛，鼓励企业基于 ROS 开发产品。这种"先投入、后收获"的模式虽然在短期内难以看到直接商业回报，但成功构建了庞大的生态系统。众多机器人创业公司（如 Fetch Robotics, Locus Robotics）和工业巨头（如 ABB, Kuka）随后基于 ROS 构建了自己的产品栈。

### 遗产与转型
2014 年，Willow Garage 正式关闭，但这并未终结其项目。其维护的开源项目（ROS, Gazebo 等）移交给了非营利组织 **Open Source Robotics Foundation **(OSRF)。OSRF 后来成立了营利性子公司 OSRC，并于 2022 年被 Alphabet 旗下的 Intrinsic 收购，原核心团队加入 Intrinsic 继续推动 ROS 2 的发展。Willow Garage 的故事展示了开源模式在硬科技领域的可持续性路径：通过建立公共基础设施（Commons），推动整个行业的进步，最终通过生态系统的繁荣反哺核心技术团队。

## 来源
- [[raw/books/机器人学/13-quigley-ros-robot-operating-system.md]]

## 相关
- [[ROS (Robot Operating System)]]
- [[PR2 机器人]]
- [[Open Source Robotics Foundation]]
- [[Scott Hassan]]
- [[Brian Gerkey]]
- [[Morgan Quigley]]