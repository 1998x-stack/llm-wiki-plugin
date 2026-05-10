---
type: concept
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: ["机器学习", "深度学习", "正则化", "最佳实践", "算法变体"]
aliases: ["Dropout 最佳实践", "Dropout 变体", "Dropout 应用指南"]
relates_to:
  - target: "[[Dropout]]"
    type: "elaborates"
  - target: "[[Dropout: A Simple Way to Prevent Neural Networks from Overfitting (2014 论文)]]"
    type: "elaborates"
  - target: "[[PyTorch]]"
    type: "applied_in"
  - target: "[[TensorFlow]]"
    type: "applied_in"
  - target: "[[共适应]]"
    type: "addresses"
supersedes: null
---

# Dropout 最佳实践与变体

## 概述 (50-200字符)
介绍 [[Dropout]] 的最佳实践原则、常见误区以及重要的[[算法]]变体。涵盖了丢弃率选择、使用场景、实现注意事项和衍生技术。

## 关键内容 (≥300字符, 用[[双链]])
1. **丢弃率选择最佳实践**：全连接层通常使用 0.5 的丢弃率（参数多易[[过拟合（Overfitting）|过拟合]]），卷积层使用 0.1-0.3 的较低丢弃率（权重共享已有正则效果），LSTM/RNN 中用于非循环连接使用 0.2-0.5，[[Transformer 架构|Transformer]] 中通常使用 0.1，输出层通常不用 [[Dropout]]。小数据集上过高的丢弃率可能导致欠拟合。
2. **实现注意事项**：关键是在训练和推理时正确切换模式（`model.train()` vs `model.eval()`），否则会导致推理结果随机波动且准确率下降。避免在 [[Batch Normalization]] 后使用 [[Dropout]]，两者训练/测试行为不一致会产生冲突。
3. **重要变体**：[[Spatial Dropout]] 按通道单位丢弃整个特征图，适用于 CNN；[[DropConnect]] [[Dropout（随机失活）|随机丢弃]]权重而非激活值；[[Stochastic Depth]] 随机跳过整个残差层；[[DropPath]] [[Dropout（随机失活）|随机丢弃]]路径（用于 NAS 网络）；[[MC Dropout]] 推理时也开启 [[Dropout]] 以估计预测不确定性。
4. **理论解释与应用场景**：[[Dropout]] 通过三种机制生效：隐式[[集成学习（Ensemble Learning）]]（训练 2^N 个子网络）、打破[[共适应]]（强迫神经元独立学习特征）、[[托马斯·贝叶斯|贝叶斯]]近似（变分推断）。在各类深度学习任务中都有广泛应用，是防止[[过拟合（Overfitting）|过拟合]]的基本工具。

## 来源
- [raw/articles/ai-papers/foundations/paper_10_dropout.md] — 精读源文件

## 相关
- [[Dropout]] — elaborates
- [[MC Dropout]] — variant
- [[Inverted Dropout]] — variant
- [[DropConnect]] — variant
- [[Spatial Dropout]] — variant
- [[Stochastic Depth]] — variant
- [[DropPath]] — variant
- [[共适应]] — addresses
- [[过拟合]] — prevents
- [[PyTorch]] — applied_in
- [[TensorFlow]] — applied_in