---
type: concept
status: active
confidence: 0.5
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 损失函数, 对比学习]
aliases: [InfoNCE Loss, Noise Contrastive Estimation 信息]
relates_to:
  - {target: 对比学习, type: implements}
  - {target: BPR, type: compares_to}
  - {target: 负采样, type: uses}
supersedes: null
---

# InfoNCE

## 概述
[[对比学习]]中的核心损失函数，通过最大化正样本对[[互信息]]下界来学习高质量表征，在单负样本设定下退化为 BPR Loss。

## 关键内容

1. **定义**：InfoNCE = -E[log exp(sim(q, k⁺)/τ) / (exp(sim(q, k⁺)/τ) + Σ_i exp(sim(q, k_i⁻)/τ))]，其中 q 为查询向量，k⁺ 为正样本，k_i⁻ 为负样本，τ 为温度参数。

2. **与 BPR Loss 的关系**：当 InfoNCE 中只使用一个负样本时，退化为 BPR Loss 的形式。这意味着 BPR 可被理解为单负样本版本的[[对比学习]]，两者在数学结构上高度一致。

3. **在推荐系统中的应用**：现代图[[对比学习]]推荐模型（SGL、SimGCL、LightGCL）通常组合 L = L_BPR + λ · L_CL，其中 L_CL 常采用 InfoNCE 或其变体，用于学习更鲁棒的用户和物品表征。

4. **温度参数 τ 的作用**：控制模型对难负样本的关注程度。较小的 τ 使模型更关注难负样本，较大的 τ 使梯度分布更均匀。τ 的选择对[[对比学习]]效果至关重要。

5. **负样本数量的影响**：InfoNCE 的理论下界随负样本数量增加而提高。但在实践中，过多负样本增加[[计算]]开销，需要在质量和效率之间权衡。

## 来源
- [[BPR 论文]] — Rendle et al. (2009) UAI 2009, 现代视角审视：与对比学习损失函数的形式化联系

## 相关
- [[对比学习]] — implements
- BPR — compares_to
- [[负采样]] — uses
