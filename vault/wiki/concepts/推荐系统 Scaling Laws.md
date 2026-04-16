---
type: concept
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 3
tags: [推荐系统, Scaling Laws, HSTU, Meta, 基础模型]
aliases: [Recommendation System Scaling Laws, 推荐系统规模定律]
relates_to:
  - {target: HSTU, type: implements}
  - {target: 生成式推荐, type: enables}
  - {target: DLRM, type: contradicts}
  - {target: 矩阵分解, type: compares_to}
supersedes: null
---

# 推荐系统 Scaling Laws

## 概述
推荐系统模型质量随训练计算量呈幂律增长的规律，由 Meta [[HSTU]] 论文首次在工业级推荐系统中验证，为推荐领域"基础模型"路线提供实证基础。

## 关键内容

1. **发现背景**：OpenAI 2020 年发现 LLM 的 Scaling Laws——模型质量随计算量呈幂律增长，直接催生 GPT-3/4。推荐系统领域此前一直未找到类似规律。传统 [[DLRM]] 在约 200B 参数量级出现性能饱和，无论加深网络、增加[[特征交叉]]还是扩大 embedding 表，收益都趋于平坦。

2. **核心发现**：[[HSTU]] 架构下，[[生成式推荐]] 模型质量（以 [[NDCG]] 等指标衡量）随训练 FLOPs 呈**幂律关系增长**，跨越三个数量级，从小型模型一直扩展到 GPT-3/LLaMA-2 规模。

3. **实践意义**：
   - **可预测性**：模型效果可提前预测，不需要每次都训练完整规模模型来评估。
   - **基础模型可行性**：训练通用[[推荐系统基础模型|推荐基础模型]]、然后针对不同业务场景微调成为可能。
   - **资源分配**：有更多 GPU 就能训练更好的推荐模型，为算力投资提供理论依据。
   - **碳足迹优化**：可通过小规模实验预测大规模表现，减少盲目训练大模型的浪费。

4. **与 LLM Scaling Laws 的对比**：
   - 相似性：都通过自回归序列建模捕捉复杂模式，都展现幂律增长，都用统一框架替代碎片化方案。
   - 差异性：推荐处理的是用户行为——噪声更大、非平稳性更强的信号。物品词汇表持续变化（新物品上线、旧物品下架），与 NLP 的固定词汇表不同。

5. **行业影响**：直接启发了 MLCommons DLRMv3 基准测试，将模型规模从 50GB 提升到 1TB（20 倍），每候选计算量从 40M FLOPs 提升到 260G FLOPs（6500 倍）。推动了整个行业向更大规模模型迁移。

6. **隐忧**：如果推荐系统进步越来越依赖计算规模，只有资源最丰富的公司能保持竞争力，加剧行业马太效应。1.5 万亿参数模型训练需 256 块 H100 GPU 和 1000 亿样本，中小企业几乎无法企及。

## 来源
- [Actions Speak Louder than Words (ArXiv)](https://arxiv.org/abs/2402.17152)
- [The Rise of Generative Recommenders (ML Frontiers)](https://mlfrontiers.substack.com/p/the-rise-of-generative-recommenders)
- [DLRMv3 Benchmark (MLCommons)](https://mlcommons.org/2026/02/dlrmv3-inference-meta/)

## 相关
- [[HSTU]] — 首次验证推荐系统 Scaling Laws 的架构
- [[生成式推荐]] — Scaling Laws 适用的推荐范式
- [[DLRM]] — 不展现 Scaling Laws 的传统推荐模型
- [[矩阵分解]] — 更早期的推荐方法，同样不展现 Scaling Laws
- [[NDCG]] — 验证 Scaling Laws 使用的核心评估指标
