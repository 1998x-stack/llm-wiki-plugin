---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [统计学, 因果推断, 缺失数据, 推荐系统]
aliases: [Missing Not At Random, MNAR]
relates_to:
  - {target: MCAR, type: compares_to}
  - {target: 选择偏差, type: part_of}
  - {target: 逆倾向评分, type: compares_to}
  - {target: 倾向性评分, type: uses}
  - {target: 隐式反馈, type: uses}
supersedes: null
---

# MNAR (非随机缺失)

## 概述
非随机缺失（Missing Not At Random）指数据的缺失机制与缺失值本身相关，即某个值是否被观测到取决于该值的大小，导致观测数据有偏。

## 关键内容

1. **定义**：在 MNAR 机制下，**某个评分是否被观测到，与该评分的值本身高度相关**。这与 MCAR（完全随机缺失）形成鲜明对比——MCAR 下缺失是完全随机的，观测数据是全量数据的无偏子集。

2. **在推荐系统中的表现**：
   - 用户更倾向于评价自己喜欢的物品（观测到的评分偏高）
   - 推荐系统更倾向于曝光热门物品（热门物品评分样本远大于冷门物品）
   - 排在前列的物品更容易被点击（位置靠前的物品获得更多反馈信号）

3. **与[[选择偏差]]的关系**：MNAR 是 [[选择偏差]]、[[流行度偏差]]、[[位置偏差]] 的统计学本质。所有这些偏差都可以归结为"数据缺失不是随机的"。

4. **对传统方法的影响**：大量 [[矩阵分解]] 方法（如经典 [[SVD++]]、ALS 等）直接在观测到的评分上最小化误差，隐式假设缺失数据是 MCAR 的。在 MNAR 数据上，这种做法在理论上是有偏的。

5. **与 MAR 的区别**：MAR（Missing At Random）指缺失机制与观测到的变量相关，但不与缺失值本身相关。MNAR 是最困难的缺失机制，因为缺失机制本身无法从观测数据中完全推断。

6. **处理方法**：
   - IPS：通过逆倾向加权校正 MNAR 偏差，当[[倾向性评分]]已知时，IPS 是真实风险的无偏估计
   - [[SNIPS]]：IPS 的自归一化版本，降低方差
   - 联合似然推断：同时建模评分值和观测概率（如 Marlin & Zemel 2009），但计算复杂度高

7. **鸡生蛋问题**：[[倾向性评分]] 本身需要从有偏的 MNAR 数据中估计，形成循环依赖。[[Tobias Schnabel]] 等人提出的朴素[[托马斯·贝叶斯|贝叶斯]]和逻辑回归方法做出了较强的参数化假设。

## 来源
- [Recommendations as Treatments (Schnabel et al., ICML 2016)](https://arxiv.org/abs/1602.05352)

## 相关
- MCAR — 完全随机缺失，MNAR 的对照
- [[选择偏差]] — MNAR 在推荐系统中的具体表现
- [[逆倾向评分]] — 处理 MNAR 的核心方法
- [[倾向性评分]] — MNAR 校正的关键输入
- [[隐式反馈]] — 隐式反馈中的 MNAR 模式更加复杂
