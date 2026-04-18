---
type: concept
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["机器学习", "深度学习", "序列建模", "时间序列"]
aliases: ["Long Short-Term Memory", "长短期记忆网络", "LSTM 细胞", "LSTM Cell"]
relates_to:
  - target: "[[循环神经网络（RNN）]]"
    type: extends
    confidence: 0.95
  - target: "[[梯度消失]]"
    type: caused
    confidence: 0.9
  - target: "[[门控机制（Gating Mechanism）]]"
    type: implements
    confidence: 0.95
  - target: "[[细胞状态（Cell State）]]"
    type: implements
    confidence: 0.95
  - target: "[[Transformer架构]]"
    type: compares_to
    confidence: 0.85
  - target: "[[双向 LSTM（Bi-LSTM）]]"
    type: extends
    confidence: 0.9
supersedes: null
---

# LSTM（长短期记忆网络）

## 概述 (50-200字符)
由 [[Sepp Hochreiter]] 和 [[Jürgen Schmidhuber]] 于 1997 年提出，通过[[细胞状态（Cell State）|细胞状态]]和[[门控机制（Gating Mechanism）|门控]]机制（[[遗忘门（Forget Gate）|遗忘门]]、[[输入门（Input Gate）|输入门]]、[[输出门（Output Gate）|输出门]]）解决 RNN [[梯度消失]]问题，使神经网络能够学习跨越数百时间步的长期依赖，是序列建模的里程碑。

## 关键内容 (≥300字符, 用[[双链]])
1. **历史背景**：[[Sepp Hochreiter]] 在 1991 年硕士论文中首次从数学上证明标准 [[循环神经网络（RNN）]] 在 BPTT 训练时，梯度因连乘权重[[矩阵]]和 tanh'（∈(0,1)）而指数级衰减，网络无法记住 10 步以前的信息。1997 年与导师 [[Jürgen Schmidhuber]] 在 *Neural Computation* 发表划时代论文《[[Long Short-Term Memory (1997 论文)|Long Short-Term Memory]]》。

2. **[[细胞状态（Cell State）|细胞状态]]与[[门控机制（Gating Mechanism）|门控]]**：LSTM 引入一条贯穿序列的"信息高速公路"——[[细胞状态（Cell State）]] Cₜ，通过三个门精确控制信息流动：[[遗忘门（Forget Gate）]]（fₜ = σ(Wf·[hₜ₋₁, xₜ] + bf)，决定丢弃什么）、[[输入门（Input Gate）]]（iₜ 控制更新量，C̃ₜ = tanh(Wc·[hₜ₋₁, xₜ] + bc) 为候选值）、[[输出门（Output Gate）]]（oₜ = σ(Wo·[hₜ₋₁, xₜ] + bo)，决定输出什么）。[[细胞状态（Cell State）|细胞状态]]更新：Cₜ = fₜ ⊙ Cₜ₋₁ + iₜ ⊙ C̃ₜ。

3. **解决[[梯度消失]]的数学本质**：[[细胞状态（Cell State）|细胞状态]]的梯度 ∂Cₜ/∂Cₜ₋₁ = fₜ，当[[遗忘门（Forget Gate）|遗忘门]]接近 1 时，梯度通过加法直接传递而不衰减。对比 RNN：∂hₜ/∂hₜ₋₁ = Wₕᵀ · diag(tanh'(·))，需要乘以小于 1 的数，连乘后指数衰减。类比：RNN 像用粉笔写黑板（每次覆盖），LSTM [[细胞状态（Cell State）|细胞状态]]像一本可精确"写入"、"擦除"、"读取"的日记本。

4. **实际应用与退出**：LSTM 统治序列学习领域近 20 年，在语音识别（[[Google]] Voice 2015）、机器翻译（[[Google]] 翻译 2016）、文本生成、时间序列预测等领域大规模部署。2017 年 [[Transformer架构]] 问世后逐步退场，但在时间序列、嵌入式/边缘设备、[[强化学习]]等场景仍广泛使用（2024 年仍活跃）。

5. **代码实现**：PyTorch 中通过 `nn.LSTM(input_size, hidden_size, num_layers, bidirectional=True)` 实现。支持多层堆叠、双向处理、dropout 正则化。权重绑定（embedding 与输出层共享权重）可节省参数。

## 来源
- [[Long Short-Term Memory (1997 论文)]] — Hochreiter, S., & Schmidhuber, J. (1997). Neural Computation, 9(8), 1735–1780
- [[raw/articles/ai-papers/machine-learning/04_lstm_1997.md]] — LSTM 核心原理、数学推导与 PyTorch 代码实现

## 相关
- [[循环神经网络（RNN）]] — extends（解决 RNN 梯度消失）
- [[梯度消失]] — caused（LSTM 解决的核心问题）
- [[门控机制（Gating Mechanism）]] — implements（核心设计模式）
- [[细胞状态（Cell State）]] — implements（核心创新）
- [[遗忘门（Forget Gate）]] — implements（门控组件）
- [[输入门（Input Gate）]] — implements（门控组件）
- [[输出门（Output Gate）]] — implements（门控组件）
- [[Transformer架构]] — compares_to（后续替代方案）
- [[双向 LSTM（Bi-LSTM）]] — extends（双向扩展）
- [[Sepp Hochreiter]] — relates_to（共同发明人）
- [[Jürgen Schmidhuber]] — relates_to（共同发明人）
