---
type: concept
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags:
- 技术
- 研究
- 数学
- 信息论
aliases:
- Kullback-Leibler Divergence
- KL Divergence
- Relative Entropy
- 相对熵
- 库尔巴克-莱布勒散度
relates_to:
- target: '[[所罗门·库尔巴克]]'
  type: caused
  confidence: 0.95
- target: '[[理查德·莱布勒]]'
  type: caused
  confidence: 0.95
- target: '[[信息熵]]'
  type: related_to
  confidence: 0.95
- target: '[[互信息]]'
  type: related_to
  confidence: 0.95
- target: '[[信息论]]'
  type: part_of
  confidence: 0.9
- target: '[[交叉熵]]'
  type: related_to
  confidence: 0.95
supersedes: null
---

# KL散度

## 概述

KL 散度（Kullback-Leibler Dive[[ripgrep|rg]]ence）度量两个概率分布之间的差异：D_KL(P||Q) = Σ P(x) log(P(x)/Q(x))，是[[信息论]]、统计学和机器学习中最核心的分布差异度量。

## 关键内容

### 定义

**离散情形**：
$$D_{\text{KL}}(P \| Q) = \sum_{x} P(x) \ln \frac{P(x)}{Q(x)}$$

**连续情形**：
$$D_{\text{KL}}(P \| Q) = \int p(x) \ln \frac{p(x)}{q(x)} \, dx$$

### 基本性质

1. **非负性**（Gibbs 不等式）：D_KL(P||Q) ≥ 0，等号当且仅当 P = Q
2. **不对称性**：D_KL(P||Q) ≠ D_KL(Q||P)（一般地）
3. **不满足三角不等式**：KL 散度不是度量（metric）

不对称性不是缺陷，而是反映了 P 和 Q 在统计推断中扮演的不同角色：P 通常是"真实分布"，Q 是"模型分布"。

### 三种直觉解释

1. **惊讶度之差**：如果现实是 P，但你以为是 Q，你会比已知 P 时平均多惊讶多少
2. **编码效率损失**：如果真实数据来自 P，但你用基于 Q 设计的编码来压缩，每个符号平均多花 D_KL(P||Q) bit
3. **假设检验**：D_KL(P||Q) 越大，越容易用数据区分 P 和 Q

### 与互信息的关系

$$I(X;Y) = D_{\text{KL}}(P_{XY} \| P_X \otimes P_Y)$$

[[互信息]]等于联合分布与边际分布之积之间的 KL 散度——衡量 X 和 Y 的联合分布"偏离独立"的程度。

### 与交叉熵的关系

$$H(P, Q) = H(P) + D_{\text{KL}}(P \| Q)$$

[[交叉熵]] = 真实熵 + 模型偏差。最小化[[交叉熵]]等价于最小化 KL 散度。

### 在机器学习中的应用

- **[[交叉熵]]损失**：深度学习分类任务的标准损失函数
- **变分自编码器(VAE)**：ELBO 中的 KL 正则化项
- **知识蒸馏**：学生网络最小化与教师网络输出的 KL 散度
- **[[强化学习]]**：[[PPO]]/[[TRPO]] 用 KL 散度约束策略更新幅度
- **GAN**：原始 GAN 目标函数与 Jensen-Shannon 散度（KL 的对称化版本）密切相关

## 来源

- [[raw/books/信息论/05_kullback_leibler_1951_information_and_sufficiency.md]] — Kullback & Leibler (1951) 深度解析

## 相关

- [[所罗门·库尔巴克]] — 提出者之一
- [[理查德·莱布勒]] — 提出者之一
- [[信息熵]] — 密切相关
- [[互信息]] — 可用 KL 散度表达
- [[信息论]] — 所属学科
- [[交叉熵]] — 与 KL 散度直接相关
