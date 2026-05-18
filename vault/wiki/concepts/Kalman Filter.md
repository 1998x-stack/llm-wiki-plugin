---
type: concept
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [control-theory, signal-processing, filtering, prediction, time-series-analysis, 计算理论]
aliases: ["卡尔曼滤波", "卡尔曼过滤器"]
relates_to: []
supersedes: null
---

# Kalman Filter

## 概述
一种用于从含噪声的测量数据中估计动态系统状态的递归[[算法]]，由[[Rudolf Emil Kalman]]在1960年提出。

## 关键内容

1. **核心思想**：
   - 通过结合系统模型预测和传感器测量值来估计系统状态
   - 采用预测-更新的递归循环机制
   - 在预测值和测量值之间进行最优加权平均

2. **[[算法]]原理**：
   - **预测步骤**：根据动力学模型预测下一时刻的状态和不确定性
   - **更新步骤**：利用新获取的传感器测量值更新状态估计
   - **卡尔曼增益**：决定预测值和测量值的权重分配

3. **优势特点**：
   - 无需存储全部历史数据，只需维护当前最佳估计和不确定性
   - 支持多输入多输出系统
   - 能够处理非平稳信号
   - [[算法]]简洁，易于编程实现

4. **历史意义**：
   - 1960年在ASME Journal of Basic Engineering发表
   - 解决了冷战时期太空竞赛中的导航定位难题
   - 在阿波罗登月计划中发挥了关键作用

5. **现代应用**：
   - GPS导航系统中的定位融合
   - 自动驾驶汽车的传感器融合
   - 机器人定位与轨迹跟踪
   - 金融工程中的动态状态估计
   - 气象预报中的数据同化

## 来源
- [[/raw/books/时间序列分析/04-kalman-1960-filter.md]] — 详细介绍算法原理与应用
- [[A New Approach to Linear Filtering and Prediction Problems]] — 原始论文

## 相关
- [[Rudolf Emil Kalman]] — 发明者
- [[State-Space Model]] — 依托的建模框架
- [[Wiener Filter]] — 前身方法
- [[Extended Kalman Filter]] — 扩展版本
- [[Unscented Kalman Filter]] — 无迹卡尔曼滤波