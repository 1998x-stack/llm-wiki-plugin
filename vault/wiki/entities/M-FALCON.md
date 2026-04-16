---
type: entity
entity_type: tool
status: active
confidence: 0.92
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 2
tags: [推荐系统, 推理优化, Meta, KV Cache, HSTU]
aliases: [M-FALCON, Microbatched-Fast Attention Leveraging Cacheable OperatioNs]
relates_to:
  - {target: HSTU, type: uses}
  - {target: 生成式推荐, type: implements}
  - {target: 两阶段推荐架构, type: compares_to}
supersedes: null
---

# M-FALCON

## 概述
M-FALCON（Micro[[bat]]ched-Fast Attention Leveraging Cacheable OperatioNs），[[Meta]] 提出的高效推理算法，使万亿参数[[生成式推荐]]模型在毫秒级延迟和相同推理预算下运行。

## 关键内容

1. **核心问题**：1.5 万亿参数的 [[HSTU]] 模型如何在生产环境中以毫秒级延迟运行？[[Meta]] 推荐系统每天处理数百亿次用户交互，推理延迟要求在毫秒级别。

2. **KV 缓存复用**：用户历史序列的 KV 缓存可在编码阶段完成后缓存下来，对所有候选物品共享复用。避免为每个候选重复计算历史序列的注意力。

3. **微批处理（Micro-[[bat]]ching）**：将候选物品分成小批次，通过修改注意力掩码防止候选之间信息泄露，同时共享历史序列的计算。推理成本随候选数量线性增长而非二次增长。

4. **计算摊销**：通过 KV 缓存 + 微批处理，历史序列的计算被所有候选摊销。最终实现 **285 倍复杂度的模型在相同推理预算下运行**，同时获得 1.5x-2.99x 吞吐量提升。

5. **工程意义**：M-FALCON 是[[生成式推荐]]从理论走向工业部署的关键工程创新。没有它，万亿参数模型的推理成本在经济上不可行。

6. **与 [[两阶段推荐架构]] 的关系**：传统架构中召回层用 [[近似最近邻检索|ANN]] 快速筛选候选，排序层用复杂模型精细排序。M-FALCON 使单一生成式模型能以可接受成本直接处理大量候选，模糊了召回和排序的边界。

## 来源
- [Actions Speak Louder than Words (ArXiv)](https://arxiv.org/abs/2402.17152)
- [ICML 2024 Proceedings](https://proceedings.mlr.press/v235/zhai24a.html)

## 相关
- [[HSTU]] — M-FALCON 服务的目标架构
- [[生成式推荐]] — M-FALCON 支撑的推荐范式
- [[两阶段推荐架构]] — M-FALCON 试图弥合的召回-排序边界
- [[近似最近邻检索]] — 传统召回层的核心技术，M-FALCON 部分替代其作用
