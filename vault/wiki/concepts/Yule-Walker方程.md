---
type: concept
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [时间序列分析, 参数估计, 数学方法, 时间序列]
aliases: ["Yule-Walker Equations", "尤尔-沃克方程", "Yule-Walker方程"]
relates_to:
  - target: "[[George Udny Yule]]"
    type: implements
    confidence: 0.9
  - target: "[[自回归模型]]"
    type: extends
    confidence: 0.9
  - target: "[[时间序列分析]]"
    type: part_of
    confidence: 0.9
  - target: "[[Gilbert Walker]]"
    type: collaborates_with
    confidence: 0.9
  - target: "[[语音编码]]"
    type: relates_to
    confidence: 0.8
  - target: "[[yule-1927-ar-model]]"
    type: implements
    confidence: 1.0
supersedes: null
---

# Yule-Walker方程

## 概述
Yule-Walker方程是将[[Time Series Analysis|时间序列]]的自相关系数与[[自回归模型]]参数联系起来的一组方程，用于从观测数据中估计[[自回归模型|AR模型]]的参数。

## 关键内容

1. **基本功能**：
   - 提供系统化方法，从观测数据中自动估计[[自回归模型]]的参数
   - 将[[Time Series Analysis|时间序列]]的自相关系数与[[自回归模型|AR模型]]的参数建立数学联系
   - 方程组的系数[[矩阵]]是Toeplitz[[矩阵]]，可用Levinson-Durbin递推等高效[[算法]]求解

2. **历史背景**：
   - 由George Yule推导，后与气象学家[[Gilbert Walker]]共同命名
   - Yule在1927年研究[[太阳黑子|太阳黑子数]]据时提出[[自回归模型]]及相应参数估计方法
   - Walker是一位传奇人物，原本是剑桥的数学家，后来远赴印度担任气象局长，试图用统计方法预测季风
   - 在研究季风预测过程中，Walker独立发展了类似的数学工具，并最终发现了著名的"[[南方涛动]]"（[[南方涛动|Southern Oscillation]]），即厄尔尼诺现象的大气部分
   - 两人的工作形成了完美的互补，共同推动了[[时间序列分析]]的发展

3. **数学特性**：
   - 具有优美的数学结构——系数[[矩阵]]是Toeplitz[[矩阵]]（对角线上的元素相等）
   - 可以用高效的[[算法]]（如Levinson-Durbin递推）快速求解

4. **现代应用**：
   - 语音编码技术中，用于线性预测编码（LPC）参数估计
   - 信号处理专家Thierry Dutoit有句著名的话："每一次手机通话，都在每10微秒求解一次Yule-Walker方程。"
   - 金融预测、气象预报、地震学、脑科学（脑电图信号分析）、自然语言处理等领域广泛应用

## 来源
- [[yule-1927-ar-model]] — 定义与历史
- [[Gilbert Walker]] — 共同贡献

## 相关
- [[George Udny Yule]] — implements
- [[自回归模型]] — extends
- [[时间序列分析]] — part_of
- [[Gilbert Walker]] — collaborates_with
- [[语音编码]] — relates_to
- [[南方涛动]] — relates_to