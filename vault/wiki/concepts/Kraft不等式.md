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
- 信息论
aliases:
- Kraft Inequality
- Kraft-McMillan 不等式
relates_to:
- target: '[[前缀码]]'
  type: part_of
  confidence: 0.95
- target: '[[Huffman编码]]'
  type: related_to
  confidence: 0.9
- target: '[[信息论]]'
  type: part_of
  confidence: 0.85
supersedes: null
---

# Kraft不等式

## 概述

Kraft 不等式指出[[前缀码]]的码字长度 l₁, ..., lₙ 必须满足 Σ 2^(-lᵢ) ≤ 1，McMillan (1956) 将其推广到所有唯一可译码，确定了[[前缀码]]码长的可行空间。

## 关键内容

### 表述

$$\sum_{i=1}^{n} 2^{-l_i} \leq 1$$

### 含义

- **必要性**：任何[[前缀码]]的码长必须满足此不等式
- **充分性**：任何满足此不等式的正整数序列 l₁, ..., lₙ 都可以构造出一个[[前缀码]]

### McMillan 推广

McMillan (1956) 证明：Kraft 不等式对所有**唯一可译码**（uniquely decodable codes），而不仅仅是[[前缀码]]，都成立。这意味着在寻找最优唯一可译码时，只需搜索[[前缀码]]就够了——Huffman 编码因此是所有唯一可译码中最优的。

### 直觉

把每个码字想象成二叉树中的一条路径。2^(-lᵢ) 是深度为 lᵢ 的节点占整棵二叉树"空间"的比例。所有码字占的空间之和不能超过 1（整棵树）。

## 来源

- [[raw/books/信息论/06_huffman_1952_minimum_redundancy_codes.md]] — Huffman (1952) 深度解析

## 相关

- [[前缀码]] — 不等式的适用对象
- [[Huffman编码]] — 在 Kraft 约束下的最优构造
- [[信息论]] — 所属学科
