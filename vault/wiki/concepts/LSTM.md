---
type: concept
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [神经网络, 深度学习, 序列建模, 记忆机制, 脑科学]
aliases: ["Long Short-Term Memory", "LSTM", "长短期记忆网络"]
relates_to:
  - target: "[[Sepp Hochreiter]]"
    type: created_by
    confidence: 0.95
  - target: "[[Jurgen Schmidhuber]]"
    type: created_by
    confidence: 0.95
  - target: "[[循环神经网络（RNN）]]"
    type: extends
    confidence: 0.9
  - target: "[[梯度消失]]"
    type: solves
    confidence: 0.95
  - target: "[[门控机制]]"
    type: implements
    confidence: 0.95
  - target: "[[常误差流（Constant Error Carousel）]]"
    type: implements
    confidence: 0.95
  - target: "[[GRU]]"
    type: predecessor_to
    confidence: 0.85
  - target: "[[Transformer]]"
    type: predecessor_to
    confidence: 0.85
  - target: "[[遗忘门]]"
    type: implements
    confidence: 0.95
  - target: "[[输入门]]"
    type: implements
    confidence: 0.95
  - target: "[[输出门]]"
    type: implements
    confidence: 0.95
supersedes: null
---

# LSTM

## 概述
长短期记忆（[[LSTM（长短期记忆网络）|Long Short-Term Memory]]）是一种特殊的循环神经网络，通过[[记忆细胞]]和[[门控机制]]解决传统RNN的[[梯度消失]]问题，能够学习长期依赖关系。由Hochreiter和Schmidhuber于1997年提出，是深度学习序列建模的里程碑式创新。

## 关键内容
1. **核心创新**：
   - [[记忆细胞]]（[[记忆细胞|Memory Cell]]）：提供专门的通道让信息可以无损地流过任意长的时间跨度
   - [[门控机制]]：包含[[输入门]]、[[遗忘门]]和[[输出门]]，控制信息的流入、保存和流出
   - [[常误差流（Constant Error Carousel）|常误差流]]（CEC）：通过自连接权重恒为1，确保误差信号在[[反向传播]]时不被缩放

2. **工作原理**：
   - [[输入门]]控制当前时刻有多少新信息可以流入[[记忆细胞]]
   - [[遗忘门]]控制[[记忆细胞]]中有多少旧信息需要被丢弃
   - [[输出门]]控制[[记忆细胞]]中的信息有多少可以输出到网络的其他部分
   - 每个时刻都进行"信息审计"——决定保留什么、丢弃什么、输出什么

3. **历史背景**：
   - 1990年代初期，RNN无法学习超过10-20个时间步的依赖关系
   - 1991年Hochreiter在本科毕业论文中首次系统分析RNN[[梯度消失]]问题
   - 1994年Bengio等人进一步确认该问题
   - 1997年Hochreiter和Schmidhuber发表划时代论文，提出LSTM解决方案

4. **应用领域**：
   - 语音识别：[[Google]]在2015年前后引入LSTM，使错误率下降近49%
   - 机器翻译：[[Google]]翻译在2016年全面切换到基于LSTM的系统，翻译质量出现质的飞跃
   - 金融预测：在捕捉股票价格、汇率等[[Time Series Analysis|时间序列]]的长周期模式方面表现优越
   - 手写识别、音乐生成、文本生成、医疗时序[[数据分析]]等众多领域

5. **序列建模演化**：
   - 2014年：GRU（[[GRU|门控循环单元]]）简化LSTM为两个门，参数更少，训练更快
   - 2014-2015年：[[注意力机制]]增强长距离依赖捕捉能力
   - 2017年：[[Transformer]]完全抛弃循环结构，采用[[自注意力机制]]
   - LSTM为[[Transformer]]的发展奠定了[[门控机制（Gating Mechanism）|门控]]和选择性记忆的思想基础

6. **历史意义**：
   - 解决了困扰RNN研究界近十年的[[梯度消失]]问题
   - 开创了[[门控机制（Gating Mechanism）|门控]]网络的范式，影响了后续所有序列建模架构
   - 推动了深度学习的复兴，在深度学习低谷期产生实际成果
   - 论文被引用超过98,000次，是[[计算]]机科学领域被引用最多的论文之一
   - 在1997-2017年间成为序列建模的标准架构，驱动了无数AI产品的核心技术

## 来源
- [[12-hochreiter-1997-lstm.md]] — LSTM历史、核心原理和应用详解
- [[Long Short-Term Memory (1997 论文)]] — 原始论文

## 相关
- [[Sepp Hochreiter]] — created_by
- [[Jurgen Schmidhuber]] — created_by
- [[循环神经网络（RNN）]] — extends
- [[梯度消失]] — solves
- [[门控机制]] — implements
- [[常误差流（Constant Error Carousel）]] — implements
- [[遗忘门]] — implements
- [[输入门]] — implements
- [[输出门]] — implements
- [[GRU]] — predecessor_to
- [[Transformer]] — predecessor_to
- [[注意力机制]] — predecessor_to