---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 2
tags: [推荐系统, 评估指标, 召回率, 排序质量, AI记忆, RAG]
aliases: [Recall@K, Recall at K, 召回率@K, R@K, R@5, R@10]
relates_to:
  - {target: NDCG, type: compares_to}
  - {target: MRR, type: compares_to}
  - {target: 序列推荐, type: part_of}
  - {target: 两阶段推荐架构, type: part_of}
  - {target: LongMemEval, type: used_by}
  - {target: 混合搜索, type: optimized_by}
  - {target: MemPalace, type: used_by}
  - {target: 近似最近邻检索, type: relates_to}
supersedes: null
---

# Recall@K

## 概述
推荐系统核心评估指标，衡量在推荐列表前 K 个物品中是否包含用户实际交互的物品，反映模型的召回能力而非排序精细度。

## 关键内容

1. **定义**：[[候选生成|Recall]]@K = $\frac{1}{|U|} \sum_{u \in U} \mathbb{I}(\text{hit}_u@K)$，其中 $\text{hit}_u@K$ 表示用户 $u$ 的真实交互物品是否出现在推荐列表的前 K 个中。取值范围 [0, 1]，越高越好。

2. **与 MRR 的区别**：[[候选生成|Recall]]@K 只关心"是否召回"，不关心召回物品在列表中的具体位置（只要在前 K 内即可）；MRR 衡量正确物品排名的倒数，对排序位置更敏感。两者结合使用可全面评估推荐质量。

3. **与 NDCG 的区别**：NDCG 同时考虑召回和排序位置的质量（通过折扣因子），是更细粒度的指标；[[候选生成|Recall]]@K 更粗粒度但更直观，是推荐系统论文中最常用的主指标之一。

4. **在[[序列推荐]]中的应用**：[[GRU4Rec]] 使用 [[候选生成|Recall]]@20 作为主要评估指标，在 RSC15 数据集上达到 0.5196。后续研究通常报告 [[候选生成|Recall]]@5、[[候选生成|Recall]]@10、[[候选生成|Recall]]@20 多个 K 值。

5. **在两阶段架构中的意义**：在[[两阶段推荐架构]]的[[候选生成]]阶段，[[候选生成|Recall]]@K 是核心评估指标，衡量候选集是否覆盖了用户可能感兴趣的物品；在[[检索重排序|精排]]阶段则更关注 NDCG 等排序质量指标。

6. **K 值选择**：K 的选择取决于业务场景。电商推荐通常 K=20~50，信息流推荐 K=10~20，搜索推荐 K=5~10。K 越大 [[候选生成|Recall]] 越高，但用户体验可能因推荐列表过长而下降。

### AI 记忆系统中的 Recall@K

在 AI 长期记忆系统中，[[候选生成|Recall]]@K 衡量记忆检索的可靠性——前 K 个候选记忆中包含正确答案的比例。

- **[[候选生成|Recall]]@5 含义**：返回 5 个候选 Drawer，正确答案在其中的概率
- **[[MemPalace]] 成绩**：[[LongMemEval]] R@5 = 96.6%（原文模式），对比 Mem0/Zep 的 ~85%
- **[[LoCoMo]] 成绩**：[[MemPalace]] R@10 = 88.9%，超过 [[Memori]] 的 81.95%（+7pp）
- **架构迭代对比**：
  - 朴素向量搜索：R@5 = 60.9%
  - [[LLM 路由]] v1：R@5 = 34.2%（灾难性失败，比基线低 26pp）
  - 关键词路由 v2：R@5 = 75.6%
  - 宫殿结构 + [[混合搜索]] v3：R@10 = 88.9%
  - 最终 Hybrid v5：R@5 = 96.6%

## 来源
- [GRU4Rec 原始论文 (arXiv)](https://arxiv.org/abs/1511.06939)
- [[raw/articles/ai-tools/mempalace/mempalace_07_benchmarks.md]] — MemPalace 深度解析第七篇：Benchmark 深度解析

## 相关
- MRR — 互补的排序质量指标
- NDCG — 更细粒度的排序指标
- [[序列推荐]] — 主要应用场景
- [[两阶段推荐架构]] — 候选生成阶段的核心指标
- [[LongMemEval]] — used_by
- [[混合搜索]] — optimized_by
- [[MemPalace]] — used_by
- [[近似最近邻检索]] — relates_to
