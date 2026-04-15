---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags:
- 技术
- 研究
- 数学
aliases:
- Hamming Distance
- 汉明距离
relates_to:
- target: '[[理查德·哈明]]'
  type: caused
  confidence: 0.95
- target: '[[Hamming码]]'
  type: part_of
  confidence: 0.95
- target: '[[Hamming界]]'
  type: part_of
  confidence: 0.9
- target: '[[信息论]]'
  type: part_of
  confidence: 0.85
supersedes: null
---

# Hamming距离

## 概述

Hamming 距离是两个等长字符串在相同位置上不同字符（或比特）的数目，是编码理论、生物信息学和机器学习中的基本度量。

## 关键内容

### 定义

$$d(x, y) = |\{i : x_i \neq y_i\}|$$

例如：
- d(10**1**1**0**01, 10**0**1**1**01) = 2（第 3 位和第 5 位不同）
- d(000, 111) = 3（所有位都不同）

### 与纠错能力的关系

一个编码方案的纠错能力完全由其码字之间的**最小 Hamming 距离** d_min 决定：

- **检错能力**：可以检测到最多 d_min - 1 个错误
- **纠错能力**：可以纠正最多 ⌊(d_min - 1) / 2⌋ 个错误

### 直觉

把每个码字想象成 n 维空间中的一个点。如果所有码字之间的最小距离至少为 d_min，那么一个码字发生 t < d_min/2 个错误后，它仍然比任何其他码字更"近"，因此解码器可以正确识别原始码字。

### 跨领域应用

- **生物信息学**：DNA 序列比较
- **密码学**：密钥距离分析
- **机器学习**：最近邻分类中的距离度量
- **哈希算法**：Simhash 等局部敏感哈希基于 Hamming 距离

## 来源

- [[raw/books/信息论/04_hamming_1950_error_correcting_codes.md]] — Hamming (1950) 深度解析

## 相关

- [[理查德·哈明]] — 提出者
- [[Hamming码]] — 基于 Hamming 距离的纠错码
- [[Hamming界]] — 基于 Hamming 距离的理论上界
- [[信息论]] — 所属学科
