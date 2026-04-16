---
type: concept
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags: [技术, 研究, 数学, 信息论]
aliases:
- Huffman Coding
- 哈夫曼编码
- 霍夫曼编码
relates_to:
- target: '[[大卫·哈夫曼]]'
  type: caused
  confidence: 0.95
- target: '[[信源编码定理]]'
  type: implements
  confidence: 0.95
- target: '[[信息熵]]'
  type: depends_on
  confidence: 0.9
- target: '[[信息论]]'
  type: part_of
  confidence: 0.9
- target: '[[前缀码]]'
  type: implements
  confidence: 0.95
supersedes: null
---

# Huffman编码

## 概述

Huffman 编码是 David Huffman (1952) 发明的最优[[前缀码]]构造算法，通过自底向上的贪心策略，为给定概率分布的信源符号构造平均码长最短的变长编码。

## 关键内容

### 算法

1. 将每个符号作为叶子节点，权重等于其概率
2. 选择权重最小的两个节点，创建新内部节点作为父节点，权重为两者之和
3. 将新节点放回集合，移除被合并的两个节点
4. 重复步骤 2-3，直到只剩一个节点（根节点）
5. 从根到每个叶子的路径（左=0，右=1）即为该符号的编码

### 示例

符号 A(0.4), B(0.3), C(0.15), D(0.10), E(0.05)：
- A → 0 (1 bit)
- B → 10 (2 bit)
- C → 110 (3 bit)
- D → 1110 (4 bit)
- E → 1111 (4 bit)
- 平均码长 = 2.05 bit/符号，信源熵 ≈ 2.03 bit/符号，效率 ≈ 99.0%

### 最优性

Huffman 编码是最优[[前缀码]]——没有其他[[前缀码]]能实现更短的平均码长。

**关键引理**：
1. 概率较大的符号码字长度不超过概率较小的符号
2. 概率最小的两个符号是兄弟叶子节点（码长相同，仅最后一位不同）

### 与 Shannon 熵的关系

$$H(X) \leq L_{\text{Huffman}} < H(X) + 1$$

当符号概率都是 2 的负整数幂时，Huffman 编码恰好达到 Shannon 熵。

### 工业应用

| 标准/格式 | 年份 | Huffman 编码的角色 |
|----------|------|------------------|
| JPEG | 1992 | 对 DCT 系数进行 Huffman 编码 |
| MPEG/MP3 | 1993 | 对频谱系数进行 Huffman 编码 |
| DEFLATE (ZIP, gzip) | 1993 | LZ77 + Huffman 的组合 |
| PNG | 1996 | 使用 DEFLATE（包含 Huffman） |
| HTTP/2 | 2015 | HPACK 头部压缩使用静态 Huffman 表 |

## 来源

- [[raw/books/信息论/06_huffman_1952_minimum_redundancy_codes.md]] — Huffman (1952) 深度解析

## 相关

- [[大卫·哈夫曼]] — 发明者
- [[信源编码定理]] — 理论下界
- [[信息熵]] — 压缩极限
- [[信息论]] — 所属学科
- [[前缀码]] — 编码类型
