---
type: concept
status: active
confidence: 0.95
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [深度学习, 网络架构, 优化, 机器学习]
aliases: ["Skip Connection", "跳跃连接", "Shortcut Connection", "捷径连接", "恒等捷径"]
relates_to: ["残差网络（ResNet）", "残差连接（Residual Connection）", "恒等映射（Identity Mapping）", "梯度消失", "退化问题（Degradation Problem）"]
supersedes: null
---

# 跳跃连接（Skip Connection）

## 概述
一种神经网络架构设计模式，将某一层的输入直接跨层加到更深层的输出上，形成"捷径"通路，使梯度能够无障碍地流向浅层。

## 关键内容
1. **基本结构**：跳跃连接将输入 x 绕过中间的权重层，直接与这些层的输出 F(x) 相加，得到 H(x) = F(x) + x。这种设计最早在[[残差网络（ResNet）]]中系统化应用，但类似思想此前已在 Highway Network 中出现。
2. **梯度高速公路效应**：[[反向传播]]时，梯度通过跳跃连接获得一条直通车道：∂L/∂x = ∂L/∂H · (∂F/∂x + 1)。其中的 "+1" 项保证了梯度信号永远不会完全消失，从根本上缓解了[[梯度消失]]问题。
3. **维度匹配处理**：当跳跃连接两端的通道数或空间尺寸不一致时，有两种处理策略——(A) 补零（Zero Padding），不增加参数；(B) 1×1 投影卷积，增加参数但效果更好。[[残差网络（ResNet）|ResNet]]的瓶颈块中采用 1×1 卷积处理降采样场景。
4. **跨领域迁移**：跳跃连接的思想已超越[[计算]]机视觉，成为深度学习的基础构件。[[Transformer]]中的每个 Attention 和 FFN 块后都有[[残差连接]]；[[U-Net]]的跳跃连接用于图像分割中的多尺度特征融合；神经ODE将跳跃连接解释为微分方程的离散化形式。
5. **与[[恒等映射（Identity Mapping）]]的关系**：跳跃连接使得网络在极端情况下可以退化为恒等映射——只需将权重层的输出推向零即可。这解决了深层网络难以学习恒等映射的[[退化问题（Degradation Problem）]]。

## 来源
- [[Deep Residual Learning for Image Recognition (2016 论文)]] — 第3节"Deep Residual Learning"，残差块设计与跳跃连接公式

## 相关
- [[残差网络（ResNet）]] — implements
- [[残差连接（Residual Connection）]] — relates_to（同义概念的不同表述）
- [[梯度消失]] — caused（缓解）
- [[退化问题（Degradation Problem）]] — caused（解决）
- [[恒等映射（Identity Mapping）]] — relates_to
- [[瓶颈结构（Bottleneck）]] — uses
