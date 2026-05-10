---
type: entity
status: active
confidence: 0.7
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [推荐系统, CTR预估, 深度学习]
aliases: [NFM, Neural Factorization Machines]
relates_to: 
  - target: "[[Factorization Machines]]"
    type: extends
    confidence: 0.8
  - target: "[[DNN]]"
    type: hybrid_with
    confidence: 0.8
  - target: "[[特征交叉]]"
    type: implements
    confidence: 0.8
supersedes: null
entity_type: paper
---

# NFM

## 概述
2017年提出的神经因子分解机模型，在FM的二阶交互层上叠加DNN，是FM与深度学习结合的另一种架构设计。

## 关键内容

1. **神经网络扩展**：
   在FM的二阶交互层之上添加深度神经网络，将FM的交互结果作为DNN的输入。

2. **层次化特征交互**：
   先通过FM建模二阶交互，再通过DNN捕获更高阶的非线性交互。

3. **架构创新**：
   与DeepFM的并行架构不同，NFM采用串联架构，FM的结果作为DNN的输入进行进一步处理。

## 来源
- [[推荐系统/06-factorization-machines.md]] — 9.2 后续工作的起点

## 相关
- [[Factorization Machines]] — extends
- [[DNN]] — hybrid_with
- [[特征交叉]] — implements