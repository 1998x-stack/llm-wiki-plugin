---
type: entity
entity_type: paper
status: active
confidence: 0.7
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, CTR预估, 分解模型]
aliases: [FFM, Field-aware Factorization Machines, 场感知分解机]
relates_to:
  - {target: Factorization Machines, type: extends}
  - {target: CTR 预估, type: implements}
  - {target: 特征交叉, type: uses}
supersedes: null
---

# FFM (Field-aware Factorization Machines)

## 概述
Juan 等人于 RecSys 2016 提出的 [[Factorization Machines|FM]] 扩展模型，引入"场"（Field）概念，让不同场之间的[[特征交叉|特征交互]]使用不同的[[嵌入表示|隐向量]]，解决了 [[Factorization Machines|FM]] 对所有交叉等权处理的局限。

## 关键内容

1. **场的概念**：在 [[CTR 预估]]中，特征可归入不同的"场"（Field），如用户性别、年龄、广告类别等。[[Factorization Machines|FM]] 中每个特征只有一个[[嵌入表示|隐向量]]，而 F[[Factorization Machines|FM]] 中每个特征针对不同的交互场使用不同的[[嵌入表示|隐向量]]。例如特征"男性"与"体育广告"交互时用向量 $\mathbf{v}_{男性,广告}$，与"年龄=25"交互时用向量 $\mathbf{v}_{男性,人口统计}$。
2. **参数增加换取表达力**：F[[Factorization Machines|FM]] 的参数量从 [[Factorization Machines|FM]] 的 $O(kn)$ 增至 $O(kn \cdot F)$（$F$ 为场数量），但获得了更精细的[[特征交叉|特征交互]]建模能力。
3. **解决 [[Factorization Machines|FM]] 的等权交叉问题**：[[Factorization Machines|FM]] 对所有 $\binom{n}{2}$ 个特征对一视同仁，无法区分有意义的交叉与噪声。F[[Factorization Machines|FM]] 通过场感知机制，让不同语义类别的[[特征交叉|特征交互]]使用专门的[[嵌入表示|隐向量]]，有效减少了无意义交叉带来的噪声。
4. **[[CTR 预估]]效果**：在 [[CTR 预估]]任务上，F[[Factorization Machines|FM]] 相比 [[Factorization Machines|FM]] 取得了显著的精度提升，成为工业界 [[CTR 预估]]的主流模型之一。
5. **与 [[Factorization Machines|FM]] 的关系**：F[[Factorization Machines|FM]] 是 [[Factorization Machines|FM]] 的直接扩展，继承了 [[Factorization Machines|FM]] 的线性复杂度计算和稀疏数据友好特性，仅在[[嵌入表示|隐向量]]的使用策略上做了场感知的改进。

## 来源
- [Field-aware Factorization Machines (Juan et al. 2016)](https://dl.acm.org/doi/10.1145/2959100.2959134)
- [Factorization Machines (Rendle 2010)](https://arxiv.org/abs/1209.3994)

## 相关
- [[Factorization Machines]] — 基础模型
- [[CTR 预估]] — 主要应用场景
- [[特征交叉]] — 核心建模目标
- [[DeepFM]] — 后续深度模型，共享嵌入思想
