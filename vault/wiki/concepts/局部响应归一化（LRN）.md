---
type: concept
status: active
confidence: 0.8
created: 2026-04-18
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 2
tags: ["机器学习", "深度学习", "归一化", "神经网络"]
aliases: ["LRN", "Local Response Normalization", "局部响应归一化"]
relates_to: ["AlexNet", "Batch Normalization", "侧抑制", "深度学习"]
supersedes: null
---

# 局部响应归一化（LRN）

## 概述 (50-200字符)
LRN 是一种受神经科学"[[侧抑制]]"启发的归一化技术，对相邻通道的激活值做局部归一化。[[AlexNet]] 使用 LRN 提升泛化能力，后被 [[Batch Normalization]] 取代。

## 关键内容 (≥300字符, 用[[双链]])
1. **生物学灵感**：LRN 受神经科学中"[[侧抑制]]"（lateral inhibition）现象启发——相邻神经元之间相互竞争抑制，使响应更强的神经元更加突出。在 CNN 中，LRN 对同一空间位置、相邻通道的激活值做归一化，抑制过大的响应、增强相对较大的激活。
2. **数学形式**：对于位置 (x,y) 处第 i 个通道的激活值 aᵢ，LRN 输出为 aᵢ / (k + α·Σⱼ aⱼ²)^β，其中求和跨越相邻通道（窗口大小 n），k、α、β、n 为超参数。[[AlexNet]]使用 k=2, α=1e-4, β=0.75, n=5。
3. **在 [[AlexNet]] 中的应用**：LRN 应用于 Conv1 和 Conv2 的 ReLU 激活之后、MaxPool 之前。原论文报告 LRN 带来约 1-2% 的 Top-1/[[Top-5 错误率]]下降。然而 LRN [[计算]]开销较大，且效果不如后续技术显著。
4. **被 [[Batch Normalization]] 取代**：2015 年[[Batch Normalization]]提出后，LRN 基本被淘汰。BN 对整个 mini-batch 做归一化（而非局部通道窗口），效果更强、训练更快、对初始化更不敏感。现代架构中 LRN 已极少使用，但作为 CNN 演化史上的一个节点仍有历史意义。

## 来源
- [Krizhevsky, A., Sutskever, I., & Hinton, G. E. (2012). ImageNet classification with deep convolutional neural networks. NeurIPS, 25.] — AlexNet 论文
- [raw/articles/ai-papers/machine-learning/07_alexnet_2012.md] — 源文件
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读

## 相关
- [[AlexNet]] — used_in
- [[Batch Normalization]] — supersedes
- [[ReLU激活函数]] — applied_after
- [[深度学习]] — historical_technique
