---
type: concept
status: active
confidence: 0.75
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [signal-processing, filtering, prediction, stationary-process]
aliases: ["维纳滤波", "维纳过滤器"]
relates_to: []
supersedes: null
---

# Wiener Filter

## 概述
由[[Norbert Wiener]]在1940年代提出的经典信号处理方法，用于从含噪信号中提取有用信息。

## 关键内容

1. **基本原理**：
   - 旨在最小化估计误差的均方值
   - 基于信号和噪声的统计特性设计滤波器
   - 适用于平稳随机过程（统计特性不随时间变化）

2. **技术特点**：
   - 要求信号是平稳的（统计特性不随时间变化）
   - 需要对整段信号历史做频域分析
   - 在频域中工作，求解[[Norbert Wiener|维纳]]-霍普夫方程
   - 难以处理多变量系统
   - 工程实现较为复杂

3. **与[[卡尔曼滤波]]的对比**：
   - [[Norbert Wiener|维纳]]滤波：要求信号平稳，需整段信号历史，频域操作，难以处理多变量
   - [[卡尔曼滤波]]：可处理非平稳信号，时域递归[[计算]]，天然支持多输入多输出，易于编程

4. **历史地位**：
   - 在[[卡尔曼滤波]]出现前是信号处理领域的统治性方法
   - 为后续滤波理论的发展奠定了基础
   - 在某些特定场景下仍有应用价值

5. **局限性**：
   - 无法处理非平稳信号
   - [[计算]]复杂度高，不适合实时处理
   - 多变量系统处理困难
   - 频域方法不易于工程实现

## 来源
- [[/raw/books/时间序列分析/04-kalman-1960-filter.md]] — 介绍其原理与与卡尔曼滤波的对比
- [[Norbert Wiener]] — 原始提出者

## 相关
- [[Norbert Wiener]] — 提出者
- [[Kalman Filter]] — 后续发展的改进方法
- [[Signal Processing]] — 应用领域
- [[Stationary Process]] — 适用的前提条件