---
type: concept
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [不确定性估计, 贝叶斯深度学习, 推理, Dropout, 机器学习]
aliases: ["Monte Carlo Dropout", "MC Dropout", "Bayesian Dropout"]
relates_to: [{"target": "[[Dropout（随机失活）]]", "type": "extends", "confidence": 0.9}, {"target": "[[Inverted Dropout]]", "type": "compares_to", "confidence": 0.8}, {"target": "[[过拟合（Overfitting）]]", "type": "relates_to", "confidence": 0.7}, {"target": "[[托马斯·贝叶斯]]", "type": "relates_to", "confidence": 0.8}, {"target": "[[变分贝叶斯近似]]", "type": "based_on", "confidence": 0.9}]
supersedes: null
---

# MC Dropout

## 概述
Monte Carlo [[Dropout]]，在推理时保持 [[Dropout]] 激活，通过多次前向传播估计模型预测的不确定性。这种技术允许我们获得模型预测的概率分布，而不只是点估计，从而提供预测不确定性的量化。

## 关键内容

1. **[[托马斯·贝叶斯|贝叶斯]]近似**：Gal 和 Ghahramani（2016）证明，在推理时启用 [[Dropout]] 等价于对深度高斯过程进行变分推断，为模型不确定性估计提供了[[计算]]高效的近似方法。这使 [[Dropout]] 不仅是正则化工具，也是[[托马斯·贝叶斯|贝叶斯]]深度学习的桥梁。

2. **不确定性量化**：对同一输入进行 T 次带 [[Dropout]] 的前向传播，得到 T 个预测结果。预测的均值作为最终输出，方差作为不确定性估计。这在医疗诊断、自动驾驶等安全关键场景中至关重要。

3. **与 [[Inverted Dropout]] 的对比**：[[Inverted Dropout]] 在推理时关闭 [[Dropout]] 以获得确定性输出；MC [[Dropout]] 则在推理时保持 [[Dropout]] 以获取预测分布。两者[[服务]]于不同目的：前者用于标准推理，后者用于不确定性估计。

4. **实现代码示例**：
```python
def predict_with_uncertainty(model, x, n_samples=100):
    """MC Dropout 预测函数"""
    model.train()  # 保持 Dropout 开启
    predictions = []
    for _ in range(n_samples):
        with torch.no_grad():
            pred = torch.softmax(model(x), dim=-1)
            predictions.append(pred)
    
    predictions = torch.stack(predictions)
    mean = predictions.mean(0)     # 预测均值
    std = predictions.std(0)       # 预测不确定性（标准差）
    return mean, std
```

MC [[Dropout]] 是一种无需修改网络架构即可获取不确定性估计的实用技术，是[[托马斯·贝叶斯|贝叶斯]]深度学习的重要实践方法。

## 来源
- [Gal, Y., & Ghahramani, Z. (2016). Dropout as a bayesian approximation: Representing model uncertainty in deep learning. ICML, 48, 1050-1059.] — 理论基础
- [[raw/articles/ai-papers/foundations/paper_10_dropout.md]] — 详细介绍

## 相关
- [[Dropout（随机失活）]] — extends
- [[Inverted Dropout]] — compares_to
- [[托马斯·贝叶斯]] — theoretical_basis
- [[变分贝叶斯近似]] — theoretical_basis
- [[过拟合（Overfitting）]] — relates_to
