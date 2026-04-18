---
type: entity
entity_type: paper
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 8
tags: [推荐系统, 生成式推荐, LLM, Meta, Self-Attention, Scaling Laws, ICML 2024]
aliases: [HSTU, Hierarchical Sequential Transduction Units, Hierarchical Sequential Transduction Unit]
relates_to:
  - {target: SASRec, type: extends}
  - {target: 序列推荐, type: implements}
  - {target: 自注意力机制, type: uses}
  - {target: 生成式推荐, type: implements}
  - {target: M-FALCON, type: uses}
  - {target: 推荐系统 Scaling Laws, type: implements}
  - {target: 级联推荐管道, type: supersedes}
  - {target: 因果掩码, type: uses}
  - {target: 缩放点积注意力, type: extends}
  - {target: DLRM, type: supersedes}
supersedes: null
---

# HSTU

## 概述
HSTU（Hierarchical Sequential Transduction Unit），Meta 在 ICML 2024 发表的万亿参数[[生成式推荐]]架构，针对推荐场景改造 [[Transformer架构|Transformer]]，首次在工业级推荐系统中验证 Scaling Laws，在线 A/B 测试提升 12.4%。

## 关键内容

1. **论文信息**：*[[Actions Speak Louder than Words 论文|Actions Speak Louder than Words]]: [[Actions Speak Louder than Words 论文|Trillion-Parameter Sequential Transducers for Generative Recommendations]]*，作者 Jiaqi Zhai 等（Meta MRS/PyTorch/AI Infra/Instagram 团队），ICML 2024（PMLR 235:58484-58509），ArXiv: [2402.17152](https://arxiv.org/abs/2402.17152)，代码开源: [github.com/meta-recsys/generative-recommenders](https://github.com/meta-recsys/generative-recommenders)。

2. **核心方法**：将[[序列推荐]]从判别式模型转向生成式模型。用户行为序列被表示为时间序列 $\{(c_1, a_1), (c_2, a_2), \ldots, (c_t, a_t)\}$，其中 $c_i$ 为内容 token，$a_i$ 为动作 token（点击、停留、购买等）。**召回**建模为预测下一个内容 token $c_{t+1}$，**排序**建模为预测下一个动作 token $a_{t+1}$，两者统一到单一模型中。

3. **HSTU 架构改造**（与标准 [[Transformer架构|Transformer]] 的关键区别）：
   - **SiLU 注意力替代 Softmax**：注意力分数计算使用 $\phi_2(QK^\top + \text{relative\_attention\_bias}) \cdot V$，其中 $\phi_2$ 为 SiLU 激活而非 Softmax。保留偏好强度信息，适应非平稳分布。[[Ablation Study|消融实验]]证实 Softmax 替换导致性能下降。
   - **相对注意力偏置替代[[绝对位置编码]]**：将位置信息和时间间隔作为相对偏置直接注入注意力分数，同时编码序列顺序和交互时间距离。
   - **[[门控机制（Gating Mechanism）|门控]]机制（U [[矩阵]]）**：在 QKV 之外引入 U [[矩阵]]作为[[门控机制（Gating Mechanism）|门控]]信号，通过 Hadamard 乘积控制[[特征交叉|特征交互]]贡献，类似 LSTM [[门控机制（Gating Mechanism）|门控]]。
   - **精简架构**：注意力外线性层从 6 个减少到 2 个，激进融合计算操作，降低激活内存。
   - **[[因果掩码]]**：单向注意力，确保[[AR 模型（自回归模型）|自回归]]生成合法性。

4. **与 [[SASRec]] 的关系**：HSTU 的[[AR 模型（自回归模型）|自回归]]生成式思路可以追溯到 [[SASRec]] 建立的[[因果掩码]] + [[Self-Attention机制|自注意力]]框架。[[SASRec]] 为今天的[[生成式推荐]]奠定了概念基础。

5. **部署规模**：1.5 万亿参数，1000 亿训练样本，256 块 H100 GPU 训练，部署于 Meta 数十亿用户平台，日均处理数百亿次用户交互。

6. **实验结果**：
   - 离线 NDCG 提升高达 65.8%；8192 长度序列上比 FlashAttention2 [[Transformer架构|Transformer]] 快 5.3x-15.2x。
   - 在线 A/B 测试主要参与指标提升 **12.4%**（工业级极为罕见），HR@100 从 29.0% 提升到 36.9%。
   - [[Ablation Study|消融实验]]：仅用交互特征下降 2.6%，仅用内容特征下降 25.3%，验证"[[Actions Speak Louder than Words 论文|Actions Speak Louder than Words]]"。

7. **局限性**：训练成本极高（仅科技巨头可复制）；序列长度翻倍致 FLOPs 四倍增长；[[冷启动问题]]未专门讨论；万亿参数黑盒可解释性差；外部复现困难。

8. **历史地位**：被广泛认为是推荐系统的"GPT 时刻"，推动了 [[Google]]、快手、美团、阿里、[[Netflix]]、字节等向[[生成式推荐]][[规范化理论|范式]]迁移。MLCommons DLRMv3 基准直接受其启发。

## 来源
- [论文原文 (ArXiv)](https://arxiv.org/abs/2402.17152)
- [ICML 2024 Proceedings](https://proceedings.mlr.press/v235/zhai24a.html)
- [官方开源代码 (GitHub)](https://github.com/meta-recsys/generative-recommenders)
- [NVIDIA HSTU 实现](https://github.com/NVIDIA/recsys-examples/blob/main/examples/hstu/README.md)
- [Is this the ChatGPT moment for recommendation systems? (Shaped.ai)](https://www.shaped.ai/blog/is-this-the-chatgpt-moment-for-recommendation-systems)
- [The Rise of Generative Recommenders (ML Frontiers)](https://mlfrontiers.substack.com/p/the-rise-of-generative-recommenders)
- [BaseModel vs HSTU (Synerise)](https://sair.synerise.com/basemodel-vs-meta-ais-hstu-for-sequential-recommendations/)
- [DLRMv3 Benchmark (MLCommons)](https://mlcommons.org/2026/02/dlrmv3-inference-meta/)

## 相关
- [[SASRec]] — HSTU 的概念先驱，自回归框架的奠基者
- [[序列推荐]] — HSTU 解决的核心场景
- [[自注意力机制]] — HSTU 的核心计算机制
- [[生成式推荐]] — HSTU 实现的推荐范式
- [[M-FALCON]] — HSTU 的高效推理算法
- [[推荐系统 Scaling Laws]] — HSTU 首次验证的核心发现
- [[级联推荐管道]] — HSTU 试图替代的传统架构
- [[因果掩码]] — HSTU 使用的注意力约束机制
- Meta — HSTU 的研发机构
