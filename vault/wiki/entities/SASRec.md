---
type: entity
entity_type: paper
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 3
tags: [推荐系统, 序列推荐, Transformer, Self-Attention, ICDM]
aliases: [SASRec, Self-Attentive Sequential Recommendation]
relates_to:
  - {target: Wang-Cheng Kang, type: part_of}
  - {target: Julian McAuley, type: part_of}
  - {target: 序列推荐, type: implements}
  - {target: GRU4Rec, type: supersedes}
  - {target: Caser, type: supersedes}
  - {target: FPMC, type: supersedes}
  - {target: BERT4Rec, type: compares_to}
  - {target: 自注意力机制, type: uses}
  - {target: 位置编码, type: uses}
  - {target: 因果掩码, type: uses}
  - {target: 缩放点积注意力, type: uses}
  - {target: 二元交叉熵, type: uses}
  - {target: NDCG, type: uses}
  - {target: 马尔可夫链, type: extends}
  - {target: TiSASRec, type: caused}
  - {target: BST, type: caused}
  - {target: S3-Rec, type: caused}
  - {target: SSE-PT, type: caused}
  - {target: LightSANs, type: caused}
  - {target: DuoRec, type: caused}
  - {target: SASRec+, type: caused}
  - {target: HSTU, type: caused}
  - {target: ICDM, type: published_at}
supersedes: null
---

# SASRec

## 概述 (50-200字符)
[[Wang-Cheng Kang]] 与 [[Julian McAuley]] 于 ICDM 2018 发表的里程碑论文，首次将 [[Self-Attention机制|Self-Attention]] 机制引入[[序列推荐]]，构建统一框架兼具[[马尔可夫链]]的稀疏聚焦与 RNN 的长程语义捕获能力。

## 关键内容 (≥300字符，分条目，用[[双链]])

1. **论文信息**：标题 "Self-Attentive [[序列推荐|Sequential Recommendation]]"，作者 [[Wang-Cheng Kang]] 与 [[Julian McAuley]]，机构 UCSD，发表于 IEEE ICDM 2018（Pages 197-206），arXiv: 1808.09781，累计引用 3000+（截至2026年），是[[序列推荐]]领域引用量最高的论文之一。开源代码: https://github.com/kang205/SASRec。

2. **核心问题**：给定用户历史行为序列 $S^u = (s_1^u, s_2^u, ..., s_{|S^u|}^u)$，设计基于 [[Self-Attention机制|Self-Attention]] 的模型，自适应捕获不同时间跨度的依赖关系（短期局部模式 + 长期全局偏好），准确预测下一个交互物品。

3. **架构设计**（四组件）：
   - **[[嵌入表示|嵌入层]]**：物品 ID 通过嵌入[[矩阵]]映射为 d 维稠密向量 + [[可学习位置嵌入|Learnable Positional Embedding]]（不同于 [[Transformer架构|Transformer]] 的正弦/余弦固定编码）
   - **[[Self-Attention机制|自注意力]]块**：核心[[计算]]模块，通过 Q/K/V 三[[矩阵]]进行 [[缩放点积注意力]]，默认堆叠 2 层
   - **逐点前馈网络**：两层 FFN，权重在所有位置间共享（类似 1x1 卷积）
   - **预测层**：序列最后位置输出与候选物品嵌入做点积，嵌入[[矩阵]]与输入层共享

4. **[[因果掩码]]（[[因果掩码|Causal Masking]]）**：SASRec 与标准 [[Transformer架构|Transformer]] Encoder 的关键区别。施加下三角掩码[[矩阵]]，第 i 位置只能看到自己及之前的位置，无法获取未来信息。这使得 SASRec 本质上等价于 [[Transformer架构|Transformer]] Decoder（[[AR 模型（自回归模型）|自回归]]模式），而非 Encoder 的双向模式。

5. **自适应依赖距离**：最优雅的特性——在稀疏数据集（如 [[Amazon]] Beauty）上注意力集中于最近 1-2 个物品（行为类似一阶[[马尔可夫链]]）；在密集数据集（如 [[MovieLens]]-1M）上[[Attention Dilution|注意力分散]]到更远历史（行为类似 RNN）。模型自动根据数据特征调整建模策略，无需人工选择 MC 或 RNN。

6. **正则化**：[[残差连接]] + [[Layer Normalization|层归一化]]（Post-norm）+ [[Dropout]]（密集数据集 0.2，稀疏数据集 0.5）。

7. **训练目标**：[[二元交叉熵]]损失，每个位置采样一正一负（真实下一个物品 + 随机负样本），远优于全物品 softmax 的[[计算]]效率。

8. **实验结果**：在四个数据集（[[Amazon]] Beauty/Games, Steam, [[MovieLens]]-1M）上均取得最优表现，Hit Rate 提升 6.9%，NDCG 提升 9.6%（相对最强基线）。训练速度比 [[Caser]] 快约 11 倍，比 [[GRU4Rec]]+ 快约 17 倍（[[MovieLens]]-1M 上 ~350 秒收敛）。

9. **理论退化分析**：当[[Self-Attention机制|自注意力]]块退化为恒等映射、使用非共享物品嵌入、移除[[位置编码]]时，SASRec 退化为 [[FPMC|分解马尔可夫链]]，证明 SASRec 是经典[[协同过滤]]模型的广义化。

10. **历史地位**：[[Transformer架构|Transformer]] 架构进入推荐系统领域的标志性里程碑，开创了推荐系统的 [[Transformer架构|Transformer]] 时代。催生了 [[BERT4Rec]]（2019）、[[TiSASRec]]（2020）、[[SSE-PT]]（2020）、BST（2019）、[[S3-Rec]]（2020）、[[LightSANs]]（2021）、[[DuoRec]]（2022）、[[SASRec+]]（2023）等一系列后续工作。阿里巴巴的 BST 直接受其启发应用于[[淘宝]][[CTR 预估|点击率预估]]系统。

11. **局限性**：固定最大序列长度（默认 50-200），$O(n^2 d)$ 复杂度限制进一步增大；单向注意力在训练阶段信息利用不充分（后续 [[BERT4Rec]] 试图解决）；仅依赖物品 ID，无物品属性/用户画像；缺少时间间隔建模（后续 [[TiSASRec]] 弥补）；"一正一负"训练目标非最优（后续 [[SASRec+]] 证明替换为全物品 softmax 可显著提升）。

## 来源
- [SASRec 原始论文 (ICDM 2018)](https://ieeexplore.ieee.org/document/8594844)
- [arXiv: 1808.09781](https://arxiv.org/abs/1808.09781)
- [官方代码 (GitHub)](https://github.com/kang205/SASRec)

## 相关
- [[Wang-Cheng Kang]] — 第一作者
- [[Julian McAuley]] — 通讯作者
- [[序列推荐]] — SASRec 解决的核心场景
- [[GRU4Rec]] — SASRec 超越的 RNN 基线
- [[Caser]] — SASRec 超越的 CNN 基线
- FPMC — SASRec 超越的 MC 基线，SASRec 可退化为其特例
- [[BERT4Rec]] — 双向 Transformer 后续工作，与 SASRec 持续竞争
- [[自注意力机制]] — SASRec 的核心计算机制
- [[位置编码]] — SASRec 使用可学习位置嵌入
- [[因果掩码]] — SASRec 的关键设计，实现自回归预测
- [[缩放点积注意力]] — SASRec 的注意力计算方式
- [[二元交叉熵]] — SASRec 的训练损失函数
- [[马尔可夫链]] — SASRec 在稀疏数据上退化的行为模式
- [[TiSASRec]] — 引入时间间隔感知的 SASRec 后续
- BST — 阿里巴巴受 SASRec 启发的工业级 CTR 模型
- [[S3-Rec]] — 引入自监督预训练的 SASRec 后续
- [[SSE-PT]] — 加入个性化嵌入的 SASRec 后续
- [[LightSANs]] — 轻量级自注意力网络的 SASRec 后续
- [[DuoRec]] — 对比学习增强的 SASRec 后续
- [[SASRec+]] — 优化损失函数后反超 BERT4Rec 的 SASRec 后续
- HSTU — Meta 的生成式推荐工作，概念上追溯到 SASRec 的自回归框架
