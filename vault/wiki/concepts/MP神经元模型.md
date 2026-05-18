---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [神经网络, AI历史, 计算模型, 脑科学]
aliases: [MP神经元模型, McCulloch-Pitts neuron, MP neuron, McCulloch-Pitts神经元]
relates_to:
  - "[[感知机（Perceptron）]] — extends"
  - "[[Warren McCulloch]] — created_by"
  - "[[Walter Pitts]] — created_by"
  - "[[The Perceptron (1958 论文)]] — precursor_to"
supersedes: null
---

# MP神经元模型

## 概述
1943年由[[Warren McCulloch]]和[[Walter Pitts]]提出的首个神经元数学模型，将生物神经元抽象为带阈值的二值逻辑单元，证明神经网络可执行任意逻辑运算。

## 关键内容

1. **数学抽象**：MP模型将生物神经元简化为一个二值阈值单元——接收多个输入信号，进行加权求和，当总和超过预设阈值时输出1（"放电"），否则输出0（"静默"）。这是对生物神经元工作原理的首次数学形式化。
2. **核心局限——权重不可学习**：MP模型中所有权重必须由人工预先设定，机器自身不具备从数据中学习权重的能力。这一缺陷在1958年被[[Frank Rosenblatt]]的[[感知机（Perceptron）]]所解决——[[感知机]]引入了[[感知机学习规则]]，实现了权重的自动调整。
3. **[[计算]]能力**：McCulloch和Pitts证明了由MP神经元组成的网络在理论上可以[[计算]]任何布尔逻辑函数，这为后来的[[多层感知机]]和深度学习奠定了概念基础。
4. **历史地位**：MP模型是现代神经网络的最早理论前身。尽管它本身不具备学习能力，但确立了"神经元 = 加权求和 + 阈值"这一基本[[计算]][[规范化理论|范式]]，至今仍是所有神经网络的核心结构。[[感知机（Perceptron）]]在此基础上增加了自动学习机制。

## 来源
- [[paper_01_perceptron.md]] — 时代背景：1950年代的AI梦想章节

## 相关
- [[感知机（Perceptron）]] — extends with automatic learning
- [[Warren McCulloch]] — created_by
- [[Walter Pitts]] — created_by
- [[The Perceptron (1958 论文)]] — precursor_to
- [[多层感知机]] — evolved_from
