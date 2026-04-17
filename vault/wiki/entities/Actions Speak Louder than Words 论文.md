---
type: entity
entity_type: paper
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 4
tags: [推荐系统, 生成式推荐, Meta, ICML 2024, Scaling Laws]
aliases: [Actions Speak Louder than Words, Trillion-Parameter Sequential Transducers for Generative Recommendations]
relates_to:
  - {target: HSTU, type: implements}
  - {target: 生成式推荐, type: implements}
  - {target: M-FALCON, type: implements}
  - {target: 推荐系统 Scaling Laws, type: implements}
supersedes: null
---

# Actions Speak Louder than Words 论文

## 概述
ICML 2024 论文，Meta 团队提出 1.5 万亿参数[[生成式推荐]]模型 HSTU，首次在工业级推荐系统中验证 Scaling Laws，在线 A/B 测试提升 12.4%，部署于数十亿用户平台。

## 关键内容

1. **论文信息**：*Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations*，作者 Jiaqi Zhai, Lucy Liao, Xing Liu, Yueming Wang, Rui Li, Xuan Cao, Leon Gao, Zhaojie Gong, Fangda Gu, Michael He, Yinghai Lu, Yu Shi。机构：Meta（横跨 MRS、PyTorch、AI Infra、Discovery、Instagram 团队）。发表于 ICML 2024（PMLR 235:58484-58509）。

2. **标题含义**："Actions Speak Louder than Words"有双重含义——用户行为（actions）比文本描述（words）更能反映真实偏好；模型应直接从行为学习而非依赖物品描述。[[Ablation Study|消融实验]]验证：仅用内容特征下降 25.3%，仅用行为特征仅下降 2.6%。

3. **核心贡献**：
   - 提出 HSTU 架构，针对推荐场景改造 [[Transformer架构|Transformer]]（SiLU 注意力、相对偏置、U [[矩阵]]门控）。
   - 提出 [[生成式推荐]] 范式，将召回和排序统一为"预测下一个 token"的序列生成任务。
   - 提出 [[M-FALCON]] 高效推理算法，使 285 倍复杂度模型在相同推理预算下运行。
   - 首次验证 [[推荐系统 Scaling Laws]]，模型质量随计算量呈幂律增长，跨越三个数量级。

4. **部署规模**：1.5 万亿参数，1000 亿训练样本，256 块 H100 GPU 训练，Meta 旗下多产品线部署，日均数百亿次交互。

5. **实验结果**：离线 NDCG 提升 65.8%；在线 A/B 测试主要指标提升 12.4%（工业级极为罕见）；HR@100 从 29.0% 到 36.9%。

6. **历史影响**：被广泛认为是推荐系统的"GPT 时刻"，推动 [[Google]]、快手、美团、阿里、[[Netflix]]、字节等向[[生成式推荐]]迁移。Meta 开源完整代码，NVIDIA 提供工业级实现。

## 来源
- [论文原文 (ArXiv)](https://arxiv.org/abs/2402.17152)
- [ICML 2024 Proceedings](https://proceedings.mlr.press/v235/zhai24a.html)
- [官方开源代码 (GitHub)](https://github.com/meta-recsys/generative-recommenders)
- [Is this the ChatGPT moment for recommendation systems? (Shaped.ai)](https://www.shaped.ai/blog/is-this-the-chatgpt-moment-for-recommendation-systems)

## 相关
- HSTU — 论文提出的核心架构
- [[生成式推荐]] — 论文提出的推荐范式
- [[M-FALCON]] — 论文提出的高效推理算法
- [[推荐系统 Scaling Laws]] — 论文首次验证的核心发现
- [[SASRec]] — HSTU 的概念先驱
- Meta — 论文所属机构
