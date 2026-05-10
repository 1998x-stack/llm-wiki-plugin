---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 5
tags: ["机器学习", "深度学习", "正则化"]
aliases: ["Dropout", "随机失活", "随机丢弃", "Dropout Regularization"]
relates_to: [{"target": "[[过拟合（Overfitting）]]", "type": "prevents", "confidence": 0.95}, {"target": "[[集成学习（Ensemble Learning）]]", "type": "interpreted_as", "confidence": 0.9}, {"target": "[[正则化（Regularization）]]", "type": "category", "confidence": 0.95}, {"target": "[[Dropout: A Simple Way to Prevent Neural Networks from Overfitting (2014 论文)]]", "type": "described_in", "confidence": 1.0}, {"target": "[[Geoffrey E. Hinton]]", "type": "invented_by", "confidence": 0.95}, {"target": "[[Nitish Srivastava]]", "type": "first_author", "confidence": 0.9}, {"target": "[[AlexNet]]", "type": "used_in", "confidence": 0.9}, {"target": "[[MC Dropout（蒙特卡洛 Dropout）]]", "type": "extends_to", "confidence": 0.85}, {"target": "[[Inverted Dropout]]", "type": "has_variant", "confidence": 0.9}, {"target": "[[DropConnect]]", "type": "related_method", "confidence": 0.8}, {"target": "[[Spatial Dropout]]", "type": "related_method", "confidence": 0.8}, {"target": "[[DropPath（Stochastic Depth）]]", "type": "related_method", "confidence": 0.8}, {"target": "[[Alex Krizhevsky]]", "type": "co_developer", "confidence": 0.85}, {"target": "[[Ilya Sutskever]]", "type": "co_developer", "confidence": 0.85}, {"target": "[[Ruslan Salakhutdinov]]", "type": "co_developer", "confidence": 0.85}]
supersedes: null
---

# Dropout（随机失活）

## 概述 (50-200字符)
[[Dropout]] 是一种神经网络正则化技术，训练时以概率 p 随机将神经元输出置零，迫使每个神经元学习更鲁棒、独立的特征表示，有效防止[[过拟合（Overfitting）]]，由[[Geoffrey E. Hinton]]团队于 2014 年正式提出。

## 关键内容 (≥300字符, 用[[双链]])
1. **核心机制与数学形式化**：训练时每个神经元以概率 p（通常 0.5）被随机置零，即 `ỹ^(l) = r^(l) ⊙ y^(l)`，其中 `r_j^(l) ~ Bernoulli(1-p)`。测试时所有神经元开启，权重乘以保留概率 (1-p) 以保证[[期望值]]不变。现代实现采用 **[[Inverted Dropout]]**：训练时直接除以 (1-p)，测试时无需任何调整，只需切换 `model.eval()` 即可。
2. **数学公式**：
   - **训练时**：`ỹ^(l) = r^(l) ⊙ y^(l)`，其中 `r_j^(l) ~ Bernoulli(1-p)`
   - **测试时**：`w_test = w_train × (1 - p)` （或现代版本：训练时 `x = x * mask / (1 - p)`，测试时无缩放）
   - **[[模型融合|集成学习]]视角**：[[Dropout]] 等价于同时训练指数级数量（2^N）的子网络并做集成。每次前向传播随机生成一个"薄"子网络，所有子网络共享参数但只有参与的子集被更新。测试时的权重缩放近似于对所有子网络取几何平均，这是 [[Dropout]] 强大泛化能力的理论基础。
3. **代码实现**：
```python
import torch
import torch.nn as nn

class MyDropout(nn.Module):
    def __init__(self, p=0.5):
        """
        p: 丢弃概率（被置零的概率）
        注意：论文中 p 有时指"保留概率"，不同库定义不同！
        PyTorch 的 nn.Dropout(p) 中 p 是丢弃概率
        """
        super().__init__()
        assert 0 <= p < 1
        self.p = p
    
    def forward(self, x):
        if not self.training:          # 推理模式：直接返回
            return x
        
        if self.p == 0:
            return x
        
        # 生成 Bernoulli 掩码（保留概率 = 1-p）
        keep_prob = 1 - self.p
        mask = torch.bernoulli(torch.full_like(x, keep_prob))
        
        # Inverted Dropout：训练时缩放
        return x * mask / keep_prob
```
4. **减少共适应（Co-adaptation）**：没有 [[Dropout]] 时，神经元会相互依赖来修正错误（"共谋"），导致单个神经元无法独立工作。[[Dropout]] 强制每个神经元学习更鲁棒、更独立的特征——"你不能依赖你的邻居，因为它随时可能消失"。[[Geoffrey E. Hinton]]用有性生殖作类比：基因随机混合比完全复制更能防止"寄生基因"传播。
5. **变体与应用场景**：**[[Spatial Dropout]]** 随机置零整个特征图通道（适用于 CNN）；**[[DropConnect]]** 随机置零权重而非神经元；**[[MC Dropout（蒙特卡洛 Dropout）]]** 测试时保持 [[Dropout]] 开启以估计预测不确定性（Gal & Ghahramani 2016 证明等价于[[托马斯·贝叶斯|贝叶斯]]近似推断）；**[[DropPath（Stochastic Depth）]]** 随机跳过整个残差块（[[残差网络（ResNet）|ResNet]]、ViT）；**Attention [[Dropout]]** 对注意力权重做 [[Dropout]]（[[Transformer 架构|Transformer]]）。尽管[[Batch Normalization]]在卷积网络中承担了部分正则化作用，[[Dropout]] 在全连接层、[[Transformer 架构|Transformer]]、[[强化学习]]、[[托马斯·贝叶斯|贝叶斯]]估计和小数据集场景中仍不可替代。
6. **最佳实践**：丢弃率推荐 - 全连接层 0.5，卷积层 0.1-0.3，输出层不用。常见误区包括忘记切换 `model.eval()`、对小数据集用过大丢弃率、在[[Batch Normalization|批归一化]]后加 [[Dropout]] 等。

## 来源
- [Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., & Salakhutdinov, R. (2014). Dropout: a simple way to prevent neural networks from overfitting. JMLR, 15(1), 1929–1958.] — 原始论文
- [raw/articles/ai-papers/machine-learning/09_dropout_2014.md] — 源文件
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读（首次实践验证）
- [[raw/articles/ai-papers/foundations/paper_10_dropout.md]] — 全文精读
- [Gal, Y., & Ghahramani, Z. (2016). Dropout as a bayesian approximation: Representing model uncertainty in deep learning. ICML, 48, 1050-1059.] — MC Dropout 理论基础

## 相关
- [[Dropout: A Simple Way to Prevent Neural Networks from Overfitting (2014 论文)]] — described_in
- [[Geoffrey E. Hinton]] — invented_by
- [[Nitish Srivastava]] — first_author
- [[Alex Krizhevsky]] — co_author
- [[Ilya Sutskever]] — co_author
- [[Ruslan Salakhutdinov]] — co_author
- [[过拟合（Overfitting）]] — prevents
- [[集成学习（Ensemble Learning）]] — interpreted_as
- [[AlexNet]] — used_in
- [[Inverted Dropout]] — variant
- [[MC Dropout（蒙特卡洛 Dropout）]] — variant
- [[DropConnect]] — variant
- [[Spatial Dropout]] — variant
- [[DropPath（Stochastic Depth）]] — variant
- [[Batch Normalization]] — alternative_to
