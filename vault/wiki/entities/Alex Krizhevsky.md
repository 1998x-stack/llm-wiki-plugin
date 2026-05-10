---
type: person
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 3
tags: ["人物", "人工智能", "深度学习", "计算机视觉"]
aliases: ["Alex Krizhevsky", "亚历克斯·克里热夫斯基", "Krizhevsky"]
relates_to: ["AlexNet", "ImageNet", "Geoffrey E. Hinton", "Ilya Sutskever", "ImageNet Classification with Deep Convolutional Neural Networks (2012 论文)", "Dropout: A Simple Way to Prevent Neural Networks from Overfitting (2014 论文)", "Dropout（随机失活）", "Nitish Srivastava", "Ruslan Salakhutdinov"]
supersedes: null
---

# Alex Krizhevsky

## 概述 (50-200字符)
Alex Krizhevsky 是加拿大[[计算]]机科学家，2012 年提出 [[AlexNet]]——在 [[ImageNet]] 竞赛中以压倒性优势夺冠的深度[[卷积神经网络（CNN）|卷积神经网络]]，开启了深度学习革命。

## 关键内容 (≥300字符, 用[[双链]])
1. **[[AlexNet]] 的诞生**：2012 年，Krizhevsky 作为[[Geoffrey E. Hinton]]的博士生，设计了 [[AlexNet]] 参加 [[ImageNet|ImageNet 大规模视觉识别挑战赛]]（[[ImageNet|ILSVRC]]）。该网络包含 5 层卷积和 3 层全连接，总参数量约 6200 万，使用[[ReLU激活函数]]、[[Dropout]]、[[数据增强（Data Augmentation）]]和双 [[GPU训练|GPU 并行训练]]，将 [[Top-5 错误率]]从 25.8% 降至 15.3%，领先第二名 10 个百分点。
2. **技术创新**：Krizhevsky 的关键贡献在于将多项技术有效整合：首次在大规模视觉任务中系统使用 ReLU（比 Sigmoid 快 6 倍）、引入 [[Dropout]] 防止[[过拟合（Overfitting）|过拟合]]、设计数据增强策略（随机裁剪、翻转、PCA 色彩扰动）、以及创造性地将网络分布在两块 GTX 580 GPU 上并行训练（将训练时间从数月缩短至 5-6 天）。[[AlexNet]] 的具体架构为：输入(224×224×3) → Conv1(96个11×11卷积核,stride=4) → ReLU → LRN → MaxPool → Conv2(256个5×5卷积核) → ReLU → LRN → MaxPool → Conv3/4/5(384/384/256个[[3×3卷积核]]) → FC1/FC2/FC3(4096/4096/1000神经元) → [[Softmax]]。
3. **历史影响**：[[AlexNet]] 被广泛认为是深度学习革命的起点。它证明了深度[[卷积神经网络（CNN）|卷积神经网络]]在大规模视觉任务中的压倒性优势，直接推动了 AI 产业的投资浪潮——[[NVIDIA]] GPU 从游戏显卡变为 AI 芯片，[[Google]]/[[DeepMind]] 等公司大举投入深度学习研究。
4. **[[Dropout]] 共同作者**：2014 年，Krizhevsky 作为共同作者参与了 [[Dropout|Dropout 正则化]]论文的发表。他在 [[AlexNet]] 中率先使用 [[Dropout]]（全连接层 p=0.5），是这一技术最早的实践验证者之一。
5. **后续发展**：[[AlexNet]] 之后，Krizhevsky 继续在深度学习领域工作，但相对低调。他与[[Ilya Sutskever]]（同为 [[Geoffrey E. Hinton|Hinton]] 学生）后来共同创立了 [[OpenAI]]（2015 年），推动了 [[GPT 系列]][[Language-Model|语言模型]]的发展。

## 来源
- [Krizhevsky, A., Sutskever, I., & Hinton, G. E. (2012). ImageNet classification with deep convolutional neural networks. NeurIPS, 25.] — 原始论文
- [Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., & Salakhutdinov, R. (2014). JMLR, 15(1), 1929–1958.] — Dropout 论文
- [raw/articles/ai-papers/machine-learning/07_alexnet_2012.md] — 源文件
- [raw/articles/ai-papers/machine-learning/09_dropout_2014.md] — 源文件
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读

## 相关
- [[Geoffrey E. Hinton]] — advised_by
- [[Ilya Sutskever]] — collaborated_with
- [[AlexNet]] — created
- [[ImageNet Classification with Deep Convolutional Neural Networks (2012 论文)]] — authored
- [[ImageNet]] — competed_in
- [[Dropout: A Simple Way to Prevent Neural Networks from Overfitting (2014 论文)]] — co_author
- [[Dropout（随机失活）]] — early_adopter
- [[Nitish Srivastava]] — collaborated_with
- [[Ruslan Salakhutdinov]] — collaborated_with
