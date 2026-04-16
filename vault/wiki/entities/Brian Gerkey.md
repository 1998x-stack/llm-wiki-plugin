---
type: entity
title: "Brian Gerkey"
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [AI, 工具，研究]
aliases: ["B. Gerkey"]
relates_to:
  - target: "[[ROS (Robot Operating System)]]"
    type: caused
    confidence: 1.0
  - target: "[[Player/Stage]]"
    type: caused
    confidence: 1.0
  - target: "[[Willow Garage]]"
    type: depends_on
    confidence: 1.0
  - target: "[[Open Source Robotics Foundation]]"
    type: caused
    confidence: 1.0
  - target: "[[Intrinsic]]"
    type: depends_on
    confidence: 0.9
supersedes: null
---

# Brian Gerkey

## 概述
Brian Gerkey 是著名的机器人学家和开源软件倡导者，**ROS **([[ROS (Robot Operating System)|Robot Operating System]]) 的关键架构师之一，也是 **Player/Stage** 项目的创始人。他曾担任 [[Willow Garage]] 的核心工程师，后将 ROS 项目带入 **Open Source Robotics Foundation **(OSRF) 并担任 CEO。2022 年，随着 OSRF 的营利性部门被 Alphabet 旗下 Intrinsic 收购，Gerkey 加入 Intrinsic 继续领导 ROS 2 及相关开源机器人技术的发展。他在机器人[[ROS (Robot Operating System)|中间件]]、开源社区治理以及机器人标准化方面做出了卓越贡献。

## 关键内容

### Player/Stage 的先驱工作
在 ROS 出现之前，Brian Gerkey 与 Richard Vaughan、Kasper Stoy 于 2000 年在南加州大学创建了 **Player/Stage** 项目。Player 提供了一种网络透明的机器人设备接口，允许程序通过 TCP/IP 统一访问传感器和执行器；Stage 则是一个轻量级的二维多机器人模拟器。Player/Stage 是当时最成功的开源机器人软件框架，被十几个研究机构采用。然而，其客户端 - 服务器架构在处理复杂系统和分布式计算时存在局限，这促使 Gerkey 思考下一代架构的可能性，并为后来 ROS 的点对点设计提供了宝贵的经验教训。

### 打造 ROS 生态系统
加入 [[Willow Garage]] 后，Gerkey 将 Player/Stage 的设计经验注入 ROS 架构中。他不仅参与了核心技术决策，更在社区建设上发挥了关键作用。他推动了 BSD 许可证的选择，降低了商业应用门槛；建立了 ROS Wiki 和 ROS Answers，促进了知识共享；并主导了 [[PR2 机器人|PR2]] Beta Program，通过向全球顶尖高校赠送机器人，成功构建了 ROS 的早期用户网络。Gerkey 深知，一个成功的开源项目不仅需要优秀的技术，更需要活跃的社区和可持续的治理结构。

### 领导 OSRF 与 ROS 2 时代
[[Willow Garage]] 关闭后，Gerkey 联合创立了非营利组织 **Open Source Robotics Foundation **(OSRF)，确保了 ROS 项目的独立性和连续性。在他的领导下，OSRF 启动了 **ROS 2** 的开发，引入 DDS [[ROS (Robot Operating System)|中间件]]以解决实时性、安全性和去中心化问题，使 ROS 能够进入工业和自动驾驶领域。2022 年，Alphabet 旗下的 Intrinsic 收购了 OSRF 的营利性部门，Gerkey 及其团队加入 [[Google]] 母公司，获得了更稳定的资源支持，继续推动开源机器人软件在工业场景的落地。他的职业生涯贯穿了机器人软件从学术原型到工业标准的整个过程。

## 来源
- [[raw/books/机器人学/13-quigley-ros-robot-operating-system.md]]

## 相关
- [[ROS (Robot Operating System)]]
- [[Player/Stage]]
- [[Willow Garage]]
- [[Open Source Robotics Foundation]]
- [[PR2 机器人]]