---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["机器学习", "深度学习", "模型评估"]
aliases: ["Overfitting", "过拟合", "过拟合现象", "Overfitting Phenomenon"]
relates_to: ["Dropout（随机失活）", "正则化（Regularization）", "偏差-方差分解", "Early Stopping", "L2 正则化", "L1 正则化", "泛化误差（Generalization Error）", "欠拟合（Underfitting）"]
supersedes: null
---

# 过拟合（Overfitting）

## 概述 (50-200字符)
过拟合指模型在训练集上表现极佳但在测试集上显著退化，本质是模型"死记硬背"了训练数据中的噪声和特定模式，丧失了对未见数据的泛化能力。是机器学习中最核心的挑战之一。

## 关键内容 (≥300字符, 用[[双链]])
1. **定义与表现**：过拟合的典型信号是训练集与测试集性能出现巨大差距。例如深度神经网络可能达到训练集 99% 准确率，但测试集仅 65%。模型参数越多、训练时间越长、数据量越小，过拟合风险越高。与之相对的是[[欠拟合（Underfitting）]]——模型连训练数据都无法拟合。
2. **[[偏差-方差分解]]视角**：[[偏差-方差分解]]将泛化误差分解为偏差（模型系统性偏离真实函数）和方差（模型对训练数据扰动的敏感度）。过拟合对应高方差：模型过于复杂，对训练集中的随机噪声产生过度响应。正则化的核心目标就是降低方差，即使可能略微增加偏差。
3. **传统正则化方法**：**[[L2 正则化]]** 惩罚大权重 `L + λ‖w‖²`，使权重分布更平滑；**[[L1 正则化]]** 产生稀疏权重 `L + λ‖w‖₁`，兼具特征选择功能；**[[Early Stopping]]** 在验证集误差不再下降时停止训练，防止模型过度拟合训练数据。这些方法对浅层网络有效，但对数百万参数的深度网络效果有限。
4. **深度学习的过拟合应对**：深度神经网络因参数量巨大（数百万至数十亿），过拟合风险极高。**[[Dropout（随机失活）]]**（[[Geoffrey E. Hinton|Hinton]] 2014）通过随机置零神经元，等价于指数级子网络集成，是最有效的深度正则化方法之一。[[Batch Normalization]] 也有轻微正则化效果。[[数据增强（Data Augmentation）]]通过人工扩展训练分布，从根本上减少过拟合空间。

## 来源
- [Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., & Salakhutdinov, R. (2014). Dropout: a simple way to prevent neural networks from overfitting. JMLR, 15(1), 1929–1958.] — Dropout 论文中的过拟合分析
- [raw/articles/ai-papers/machine-learning/09_dropout_2014.md] — 源文件

## 相关
- [[Dropout（随机失活）]] — prevents
- [[正则化（Regularization）]] — addressed_by
- [[偏差-方差分解]] — explained_by
- [[L2 正则化]] — mitigation_method
- [[L1 正则化]] — mitigation_method
- [[Early Stopping]] — mitigation_method
- [[欠拟合（Underfitting）]] — contrasts_with
- [[泛化误差（Generalization Error）]] — measures
