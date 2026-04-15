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
- Hamming Code
- 汉明码
relates_to:
- target: '[[理查德·哈明]]'
  type: caused
  confidence: 0.95
- target: '[[Hamming距离]]'
  type: depends_on
  confidence: 0.95
- target: '[[信息论]]'
  type: part_of
  confidence: 0.9
- target: '[[信道编码定理]]'
  type: implements
  confidence: 0.85
- target: '[[Hamming界]]'
  type: related_to
  confidence: 0.9
supersedes: null
---

# Hamming码

## 概述

Hamming 码是 Richard Hamming (1950) 发明的第一个实用[[纠错编码]]方案，用 7 位传输 4 位信息（码率 4/7 ≈ 57%），能自动检测并纠正单个比特错误。

## 关键内容

### Hamming(7,4) 码的构造

数据位 d₁, d₂, d₃, d₄ 放在位置 3, 5, 6, 7。
校验位 p₁, p₂, p₃ 放在位置 1, 2, 4（2 的幂次位置）。

```
位置:  1   2   3   4   5   6   7
内容:  p₁  p₂  d₁  p₃  d₂  d₃  d₄
```

### 校验方程

- p₁ ⊕ d₁ ⊕ d₂ ⊕ d₄ = 0
- p₂ ⊕ d₁ ⊕ d₃ ⊕ d₄ = 0
- p₃ ⊕ d₂ ⊕ d₃ ⊕ d₄ = 0

### 纠错过程

接收后计算三个伴随式（syndrome）s₁, s₂, s₃。如果全为 0，无错误。否则 (s₃s₂s₁)₂ 的二进制值直接给出**出错的位置**！

例如 s₃=1, s₂=0, s₁=1 → 出错位置 = (101)₂ = 5，翻转第 5 位即可纠正。

### 精妙之处

校验位放在 2 的幂次位置，使得伴随式的二进制值直接指向出错位置——这是一个极其优雅的构造。

### SECDED 扩展

增加一个全局奇偶校验位，将 (7,4) 码扩展为 (8,4) 码，实现**单纠错双检错**（SECDED: Single Error Correction, Double Error Detection）。这一扩展几乎不增加开销却显著提高可靠性。

### 工业应用

- **[[纠错编码|ECC]] 内存**：服务器和关键系统的内存使用 SECDED Hamming 码保护
- **闪存/SSD**：使用 Hamming 码或更强的 BCH 码纠正存储错误
- **通信协议**：许多基础通信协议使用 Hamming 原理进行错误检测

## 来源

- [[raw/books/信息论/04_hamming_1950_error_correcting_codes.md]] — Hamming (1950) 深度解析

## 相关

- [[理查德·哈明]] — 发明者
- [[Hamming距离]] — 纠错能力的度量基础
- [[信息论]] — 所属学科
- [[信道编码定理]] — Shannon 证明了可能性，Hamming 给出了构造
- [[Hamming界]] — Hamming 码恰好达到此界（完美码）
