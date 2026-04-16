---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags:
- 技术
- 研究
- 方法论
- 数学
aliases:
- Occam's Razor
- 奥卡姆剃刀
- 简单性原则
relates_to:
- target: '[[Solomonoff先验]]'
  type: implements
  confidence: 0.95
- target: '[[柯尔莫哥洛夫复杂性]]'
  type: related_to
  confidence: 0.9
- target: '[[算法信息论]]'
  type: part_of
  confidence: 0.85
supersedes: null
---

# Occam剃刀

## 概述

Occam 剃刀（"如无必要，勿增实体"）是科学方法论中的简单性原则：在多个同样能解释观测数据的理论中，应选择最简单的。Solomonoff (1964) 首次将其精确数学化。

## 关键内容

### 历史

- **14 世纪**：William of Ockham 提出"如无必要，勿增实体"
- **1739 年**：Hume 提出归纳问题——从有限观察推断无限规律在逻辑上无保证
- **1964 年**：Solomonoff 将 Occam 剃刀转化为精确的数学命题

### Solomonoff 的形式化

在 Solomonoff 框架中，Occam 剃刀被精确表述为：在所有能解释数据的可计算假设中，Solomonoff 先验自动赋予简单假设（短程序）更高的权重。

一个 10 bit 的程序比一个 100 bit 的程序有 2^90 ≈ 10^27 倍高的先验概率。因此，如果一个简单的规律能解释数据，它自动获得更高的后验概率。

### 在机器学习中的体现

- **[[最小描述长度原理|MDL]] 原理**：选择能最短描述数据的模型
- **正则化**：L1/L2 正则化是对模型复杂度的惩罚，近似 Occam 剃刀
- **神经网络**：架构的归纳偏置（inductive bias）本质上是对"简单函数"的偏好
- **LLM**：大规模预训练隐式地学到了一个"通用先验"，对简单模式的偏好类似于 Solomonoff 先验对短程序的偏好

### 哲学意义

Solomonoff 的工作将 700 年前 Occam 的哲学直觉、200 年前 Hume 的归纳怀疑、和 20 世纪 Shannon 的[[信息论]]，统一在一个数学框架中。

## 来源

- [[raw/books/信息论/08_solomonoff_1964_formal_theory_of_inductive_inference.md]] — Solomonoff (1964) 深度解析

## 相关

- [[Solomonoff先验]] — Occam 剃刀的数学实现
- [[柯尔莫哥洛夫复杂性]] — "简单性"的精确度量
- [[算法信息论]] — 所属学科
