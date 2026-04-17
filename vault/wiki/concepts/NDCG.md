---
type: concept
status: active
confidence: 0.5
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [评估指标, 排序, 推荐系统]
aliases: [Normalized Discounted Cumulative Gain, 归一化折扣累积增益]
relates_to:
  - {target: AUC, type: compares_to}
  - {target: BPR, type: relates_to}
supersedes: null
---

# NDCG (Normalized Discounted Cumulative Gain)

## 概述
一种考虑推荐列表位置权重的排序质量评估指标，对排名靠前的相关物品赋予更高的权重。

## 关键内容

1. **定义**：NDCG@K = DCG@K / IDCG@K，其中 DCG@K = Σ_(i=1)^K rel_i / log₂(i+1)，IDCG 为理想排序下的 DCG 最大值。rel_i 为位置 i 处物品的相关性得分。

2. **与 AUC 的区别**：AUC 对所有位置一视同仁，只关注全局排序质量；NDCG 对 Top 位置赋予更高权重，更贴近实际推荐场景中用户主要关注前列推荐的行为。

3. **在 BPR 上下文中的意义**：[[BPR 论文]]以 AUC 为主要评价指标，但后续研究指出 BPR 在 NDCG、MRR 等 Top 权重指标上的表现同样重要。Listwise 方法（如 Softmax [[交叉熵]]）在 NDCG 上提供比 BPR 更紧的下界。

4. **适用场景**：电商推荐、搜索引擎结果排序、信息流推荐等场景中，用户注意力集中在前几条结果，NDCG 比 AUC 更能反映实际用户体验。

5. **局限性**：需要已知物品的相关性得分（[[显式反馈]]或人工标注），在纯[[隐式反馈]]场景下难以直接计算，通常用交互行为代理相关性。

## 来源
- [[BPR 论文]] — Rendle et al. (2009) UAI 2009, 与 Listwise 方法比较中提及

## 相关
- AUC — compares_to
- BPR — relates_to
