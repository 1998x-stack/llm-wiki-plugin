---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags:
- 技术
- 研究
- 数学
aliases:
- Hamming Bound
- Sphere Packing Bound
- 汉明界
- 球填充界
relates_to:
- target: '[[理查德·哈明]]'
  type: caused
  confidence: 0.9
- target: '[[Hamming码]]'
  type: related_to
  confidence: 0.9
- target: '[[球填充问题]]'
  type: related_to
  confidence: 0.9
- target: '[[信息论]]'
  type: part_of
  confidence: 0.85
supersedes: null
---

# Hamming界

## 概述

Hamming 界（也称球填充界）是纠错码的理论上界：在 n 位空间中，码字数 2ᵏ 与纠错能力 t 满足 2ᵏ · Σ C(n,i) ≤ 2ⁿ，达到此界的编码称为"完美码"。

## 关键内容

### 公式

$$2^k \cdot \sum_{i=0}^{t} \binom{n}{i} \leq 2^n$$

其中 t = ⌊(d_min - 1)/2⌋ 是纠错能力。

### 直觉

每个码字"覆盖"了所有与它距离不超过 t 的 n 位字符串（共 Σ C(n,i) 个），这些"球"不能重叠。所有码字的球加起来不能超过 n 维空间的总大小 2ⁿ，因此码字数 2ᵏ 有上界。

就像在一个房间里放球——球不能重叠，球越大（纠错能力越强），能放的球就越少。

### 完美码

Hamming(7,4) 码恰好达到了 Hamming 界——是"完美码"（perfect code）：球填充无缝隙。其他已知的完美码包括 (23,12) Golay 码。

### 与 Shannon 球填充的关系

Shannon (1949) 在连续信道中使用球填充推导了 Shannon-Hartley 公式。Hamming (1950) 在离散空间中使用了相同的几何直觉推导了 Hamming 界。两者从不同角度揭示了信息传输的几何本质。

## 来源

- [[raw/books/信息论/04_hamming_1950_error_correcting_codes.md]] — Hamming (1950) 深度解析

## 相关

- [[理查德·哈明]] — 提出者
- [[Hamming码]] — 达到此界的完美码
- [[球填充问题]] — 连续信道中的对应概念
- [[信息论]] — 所属学科
