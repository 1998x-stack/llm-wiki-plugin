---
type: concept
status: active
confidence: 0.95
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["深度学习", "优化方法", "网络架构"]
aliases: ["Residual Learning", "残差学习", "残差表示学习"]
relates_to: ["残差网络（ResNet）", "残差连接（Residual Connection）", "跳跃连接（Skip Connection）", "退化问题（Degradation Problem）", "恒等映射（Identity Mapping）"]
supersedes: null
---

# 残差学习（Residual Learning）

## 概述
一种神经网络学习[[规范化理论|范式]]，将目标映射[[重构]]为输入与残差函数之和，使网络只需学习输入与目标之间的差异部分，而非完整映射。

## 关键内容
1. **核心公式**：传统网络直接学习目标映射 H(x)，而残差学习将目标[[重构]]为 H(x) = F(x) + x，网络只需学习残差函数 F(x) = H(x) - x。这一[[重构]]使得当最优解接近[[恒等映射（Identity Mapping）]]时，网络只需将权重推向零，远比学习精确的恒等变换容易。
2. **直觉类比**：与其从零开始画一幅画（学习完整映射），不如在草稿上修改（学习残差）——后者容易得多。实验验证了这一点：训练后残差函数 F(x) 的响应普遍比非残差函数小，说明网络确实"接近恒等映射"，权重[[矩阵]]大多学到的是小扰动。
3. **两种学习情景**：(a) 当某层不需要做任何变换时，残差学习只需 F(x) = 0（将权重推向零）；(b) 当某层需要做小修改时，残差学习只需学习与输入的差值，而差值通常远小于完整输出。这两种情景都比传统映射学习更简单。
4. **与[[跳跃连接（Skip Connection）]]的关系**：残差学习是学习[[规范化理论|范式]]，[[跳跃连接（Skip Connection）|跳跃连接]]是实现机制。残差学习定义了"学什么"（残差而非完整映射），[[跳跃连接（Skip Connection）|跳跃连接]]定义了"怎么实现"（将输入加到输出上）。两者共同构成了[[残差网络（ResNet）]]的核心。
5. **理论解释**：从损失曲面视角看，残差学习将原本崎岖、充满尖锐局部极小值的优化空间平滑化，使优化器更容易找到好的路径。从[[隐式集成]]视角看，残差学习等价于对指数级数量的浅层路径进行集成。

## 来源
- [[Deep Residual Learning for Image Recognition (2016 论文)]] — 第3节"Deep Residual Learning"，残差学习公式与动机分析

## 相关
- [[残差网络（ResNet）]] — implements
- [[残差连接（Residual Connection）]] — implements
- [[跳跃连接（Skip Connection）]] — relates_to（实现机制）
- [[退化问题（Degradation Problem）]] — caused（解决）
- [[恒等映射（Identity Mapping）]] — relates_to
- [[损失曲面（Loss Landscape）]] — relates_to（平滑化效应）
