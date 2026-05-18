---
type: concept
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [control-theory, time-series-analysis, mathematical-modeling, dynamical-systems, 工具与框架]
aliases: ["状态空间模型", "状态空间表示"]
relates_to: []
supersedes: null
---

# State-Space Model

## 概述
一种用于描述动态系统的数学建模框架，通过状态变量来描述系统的内部状态和外部观测之间的关系。

## 关键内容

1. **基本组成**：
   - **状态转移方程**：描述系统的内在演化规律，表达为"下一时刻的状态 = 当前状态经过某种变换 + 过程噪声"
   - **观测方程**：描述传感器如何观测系统，表达为"测量值 = 状态经过某种映射 + 测量噪声"

2. **建模优势**：
   - 提供了统一的数学语言来描述各种不同类型的系统
   - 将系统的内在动态与观测过程清晰地分离开来
   - 支持多输入多输出系统的建模
   - 能够处理不可直接观测的隐含状态变量

3. **应用领域**：
   - 控制理论：描述受控系统的动态行为
   - 信号处理：滤波和预测问题
   - [[时间序列分析]]：[[ARIMA]]、[[指数平滑]]等方法的状态空间表示
   - 经济学：宏观经济学模型和计量经济模型
   - 生物学：生态系统和生理系统建模

4. **与[[卡尔曼滤波]]的关系**：
   - [[卡尔曼滤波]]是在状态空间模型框架下的最优估[[计算]]法
   - 状态空间模型为[[卡尔曼滤波]]提供了建模基础
   - 许多[[Time Series Analysis|时间序列]]方法（如[[ARIMA]]、[[指数平滑]]）都可以等价地表示为状态空间模型

5. **重要发展**：
   - 由[[Rudolf Emil Kalman|Rudolf Kalman]]在1960年引入控制理论
   - 成为了现代控制理论和[[时间序列分析]]的通用语言
   - 后续发展出线性、非线性、时变等多种形式

## 来源
- [[/raw/books/时间序列分析/04-kalman-1960-filter.md]] — 介绍建模框架与应用
- [[Forecasting, Structural Time Series Models and the Kalman Filter]] — 详细阐述与时间序列分析的联系

## 相关
- [[Kalman Filter]] — 在该框架下的最优估计算法
- [[Rudolf Emil Kalman]] — 框架的引入者
- [[ARIMA Models]] — 可以表示为状态空间模型
- [[Time Series Analysis]] — 应用领域之一
- [[Structural Time Series Models]] — 特定类型的状态空间模型