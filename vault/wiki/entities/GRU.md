---
type: entity
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [深度学习, RNN, 序列建模]
aliases: ["Gated Recurrent Unit", "门控循环单元", "GRU单元"]
entity_type: tool
relates_to:
  - target: "[[GRU4Rec]]"
    type: utilized_by
    confidence: 0.9
  - target: "[[RNN]]"
    type: variant_of
    confidence: 0.8
  - target: "[[LSTM]]"
    type: alternative_to
    confidence: 0.8
  - target: "[[序列推荐]]"
    type: applied_to
    confidence: 0.9
  - target: "[[深度学习]]"
    type: component_of
    confidence: 0.9
supersedes: null
---

# GRU

## 概述
GRU（Gated Recurrent Unit，门控循环单元）是一种改进的循环神经网络单元，由Cho等人于2014年提出，相比LSTM参数更少、训练更快，已成为序列建模任务中的重要组件。

## 关键内容

1. **核心机制**：
   GRU将LSTM的遗忘门和输入门合并为一个更新门，同时引入重置门，参数量减少约25%，训练速度提升10-30%。更新门控制前一时刻隐藏状态的信息保留程度，重置门决定在计算候选隐藏状态时前一时刻状态的遗忘程度。

2. **数学公式**：
   - 更新门：z_t = σ(W_z * x_t + U_z * h_{t-1})
   - 重置门：r_t = σ(W_r * x_t + U_r * h_{t-1})
   - 候选隐藏状态：~h_t = tanh(W * x_t + U(r_t ⊙ h_{t-1}))
   - 最终隐藏状态：h_t = (1 - z_t) ⊙ h_{t-1} + z_t ⊙ ~h_t

3. **在GRU4Rec中的应用**：
   GRU4Rec论文比较了标准RNN、LSTM和GRU三种单元，发现GRU在推荐任务上表现最佳。GRU的参数效率和性能平衡使其成为序列推荐的理想选择，避免了标准RNN的梯度消失问题，同时在相对较短的会话序列上没有LSTM的过拟合倾向。

## 来源
- [[12-gru4rec.md]] — GRU在推荐系统中的应用

## 相关
- [[GRU4Rec]] — utilized_by
- [[RNN]] — variant_of
- [[LSTM]] — alternative_to
- [[序列推荐]] — applied_to
- [[深度学习]] — component_of