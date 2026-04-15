# 索引压缩（Index Compression）
> Variable-Byte, PForDelta, Elias Codes — 深度解析系列 第 8 篇

---

## 1. 为什么需要压缩

### 1.1 索引规模估算

```
规模估算（以 1 亿文档的网页搜索引擎为例）:

词典规模: ~1000 万词条
平均 posting list 长度: ~5000 条（doc_id + tf）
原始索引大小:
  100M文档 × 平均文档50词 = 50亿 (term, doc_id) 对
  每对 8 字节（4B docid + 4B tf） = 40 GB 原始大小

压缩后目标: 
  高效压缩可达 5-10 GB（压缩比 4-8x）
  → 完全放入内存（64GB 服务器）
  → 从磁盘检索 → 从内存检索：速度提升 100-1000x
```

### 1.2 压缩的核心原理

**倒排列表的关键特性：**

```
1. DocID 有序（升序）→ 差值编码后，数值变小
2. 差值分布呈幂律（大多数差值很小）→ 变长编码效率高
3. TF 通常很小（大多数文档中词条出现 1-5 次）→ 小数字多

示例:
  原始 DocID 列表: [102, 1005, 1007, 1210, 1212, 1300, 5000]
  
  差值编码: [102, 903, 2, 203, 2, 88, 3700]
              ↑    ↑   ↑   ↑   ↑   ↑    ↑
           首项  差值 小! 中等 小! 中  大（稀有）
  
  数值分布: 大量小数（1-100），少量大数（>1000）
  → 用短码字编码小数，长码字编码大数
```

---

## 2. 变长字节编码（Variable-Byte Encoding / VByte）

### 2.1 基本原理

每个字节的最高位（MSB）作为**延续标志**：
- MSB = 1：这不是最后一个字节（继续读取）
- MSB = 0：这是最后一个字节（停止读取）

剩余 7 位存储数据。

### 2.2 编码规则

```
编码数字 n：

n ∈ [0, 127]（7位可表示）:
  编码为 1 个字节: [0|nnnnnnn]
  最高位=0（停止标志），低7位存储n
  
n ∈ [128, 16383]（14位）:
  编码为 2 个字节:
  字节1: [1|nnnnnnn]  （n的低7位，最高位=1表示继续）
  字节2: [0|nnnnnnn]  （n的高7位，最高位=0表示停止）
  
n ∈ [16384, 2097151]（21位）:
  编码为 3 个字节（类似）
```

### 2.3 编解码示例

```
数字 5:
  二进制: 101
  编码:   00000101  → 1字节: 0x05

数字 127:
  二进制: 1111111
  编码:   01111111  → 1字节: 0x7F

数字 128:
  二进制: 10000000
  需要 2 字节:
    字节1（低7位）: 1|0000000 = 10000000 = 0x80（最高位=1，继续）
    字节2（高7位）: 0|0000001 = 00000001 = 0x01（最高位=0，停止）
  编码: [0x80, 0x01]

数字 1000:
  二进制: 1111101000
  低7位: 1101000, 高位: 0000111
  字节1: 1|1101000 = 0xE8
  字节2: 0|0000111 = 0x07
  编码: [0xE8, 0x07]
  
验证: 0xE8 & 0x7F = 0x68 = 104（低7位）
      0x07 = 7（高7位）
      104 + 7×128 = 104 + 896 = 1000 ✓
```

### 2.4 VByte 编解码实现

```python
def vbyte_encode(numbers: list) -> bytes:
    """
    变长字节编码
    对差值编码后的列表进行压缩
    """
    result = bytearray()
    
    for n in numbers:
        assert n >= 0, "VByte 只支持非负整数"
        
        while n >= 128:
            # 取低7位，最高位设为1（继续）
            result.append((n & 0x7F) | 0x80)
            n >>= 7
        
        # 最后一个字节，最高位为0（停止）
        result.append(n & 0x7F)
    
    return bytes(result)


def vbyte_decode(data: bytes) -> list:
    """变长字节解码"""
    result = []
    n = 0
    shift = 0
    
    for byte in data:
        if byte & 0x80:  # 最高位为1，继续
            n |= (byte & 0x7F) << shift
            shift += 7
        else:            # 最高位为0，完成
            n |= byte << shift
            result.append(n)
            n = 0
            shift = 0
    
    return result


def encode_posting_list(doc_ids: list) -> bytes:
    """
    对 posting list（有序 DocID 列表）进行差值编码 + VByte 压缩
    """
    # Step 1: 差值编码
    gaps = [doc_ids[0]]
    for i in range(1, len(doc_ids)):
        gaps.append(doc_ids[i] - doc_ids[i-1])
    
    # Step 2: VByte 压缩
    return vbyte_encode(gaps)


def decode_posting_list(data: bytes, first_doc_id: int = None) -> list:
    """解码 posting list"""
    gaps = vbyte_decode(data)
    
    # 从差值还原原始 DocID
    doc_ids = [gaps[0]]
    for gap in gaps[1:]:
        doc_ids.append(doc_ids[-1] + gap)
    
    return doc_ids


# 效率测试
import sys

doc_ids = [2, 5, 11, 23, 34, 56, 78, 100, 234, 1000, 5000, 100000]
encoded = encode_posting_list(doc_ids)
decoded = decode_posting_list(encoded)

print(f"原始数据: {doc_ids}")
print(f"差值: {[doc_ids[0]] + [doc_ids[i]-doc_ids[i-1] for i in range(1,len(doc_ids))]}")
print(f"原始大小: {len(doc_ids) * 4} 字节（int32）")
print(f"VByte 压缩后: {len(encoded)} 字节")
print(f"压缩比: {len(doc_ids) * 4 / len(encoded):.2f}x")
print(f"解码正确: {doc_ids == decoded}")
```

### 2.5 VByte 压缩率分析

| 值范围 | VByte 字节数 | 固定4字节 | 压缩比 |
|--------|------------|---------|-------|
| [0, 127] | 1 | 4 | 4x |
| [128, 16383] | 2 | 4 | 2x |
| [16384, 2097151] | 3 | 4 | 1.33x |
| [2097152, 268435455] | 4 | 4 | 1x |
| ≥ 268435456 | 5 | 4 | 0.8x（膨胀！） |

**实际场景（差值分布）：**
- 高频词（"the"）: 差值接近 1 → 几乎全是 1 字节
- 中频词: 差值 1-1000 → 1-2 字节
- 低频词: 差值 1000-100000 → 2-3 字节

**平均压缩比: 3-6x（典型网页搜索场景）**

---

## 3. Elias 编码系列

### 3.1 Unary 编码

```
编码正整数 n：n个1 后跟一个0

n=1: 10
n=2: 110
n=3: 1110
n=4: 11110
n=5: 111110

特点: 小数字编码短，大数字极长
      只适合编码很小的整数（n < 10）
```

### 3.2 Elias Gamma 编码

```
编码正整数 n：

Step 1: 计算 k = ⌊log₂(n)⌋  （n的位数-1）
Step 2: 写 k 个 0，然后写 1
Step 3: 写 n 的二进制表示（不含最高位）

示例:
n=1: k=0, unary(1)=1, 剩余=""   → "1"        (1位)
n=2: k=1, unary(1)=01,剩余="0"  → "010"      (3位)
n=3: k=1, unary(1)=01,剩余="1"  → "011"      (3位)
n=4: k=2, unary(1)=001,剩余="00"→ "00100"    (5位)
n=7: k=2, unary(1)=001,剩余="11"→ "00111"    (5位)
n=8: k=3, unary(1)=0001,剩余="000"→"0001000"  (7位)

位数: 2⌊log₂(n)⌋ + 1
```

### 3.3 Elias Delta 编码

改进 Gamma：用 Gamma 编码来编码位长度前缀：

```
编码 n：
Step 1: k = ⌊log₂(n)⌋ + 1  （n的位数）
Step 2: 写 k 的 Gamma 编码
Step 3: 写 n 的低 (k-1) 位

示例:
n=9: 
  二进制: 1001, k=4
  Gamma(4) = 00100
  低3位: 001
  Delta(9) = 00100001    (8位)

对比 Gamma(9):
  Gamma(9) = 0001001     (7位)
  
Delta 在大数时比 Gamma 更高效
```

---

## 4. PForDelta（Patched Frame of Reference Delta）

### 4.1 动机

VByte 每次操作需要检查 MSB → 分支预测不友好 → CPU 效率低

PForDelta 的思路：**批量处理，利用 SIMD 指令**

### 4.2 PForDelta 原理

```
对一批 128 个差值（gap）:

Step 1: 分析这批数据
  大多数差值可以用 b 位表示
  选择 b 使得 90% 的差值适合 b 位（exceptions < 10%）

Step 2: 主体压缩
  所有值用固定 b 位存储（不管是否超出范围）
  超出范围的值（exceptions）存储特殊标记

Step 3: 异常值处理（Patching）
  异常值单独存储在一个补丁数组（patch list）中
  在解码时，用补丁值替换特殊标记

示例（b=8，128个差值）:
  正常值（≤255）: 120个，直接8位存储
  异常值（>255）: 8个，存储在补丁列表
  
  主体大小: 128 × 8 = 1024 bits = 128 字节
  补丁大小: 8 × 32 = 256 bits = 32 字节
  总大小: 160 字节
  
  vs VByte: 128 × 平均2字节 = 256 字节
  
  PForDelta 优势: 更小 + SIMD 可解码主体部分
```

### 4.3 PForDelta 实现（简化版）

```python
import numpy as np
from typing import Tuple, List

BLOCK_SIZE = 128  # 每块处理的差值数量

def pfordelta_encode_block(gaps: np.ndarray, b: int) -> Tuple[np.ndarray, List]:
    """
    对一个 128 个差值的块进行 PForDelta 编码
    
    Args:
        gaps: 差值数组（长度 BLOCK_SIZE）
        b: 位宽
    Returns:
        (主体数组, 补丁列表)
        补丁列表: [(位置, 真实值), ...]
    """
    max_val = (1 << b) - 1  # b位能表示的最大值
    exception_marker = max_val  # 用最大值作为异常标记
    
    body = gaps.copy()
    patches = []
    
    for i, val in enumerate(gaps):
        if val >= exception_marker:
            body[i] = exception_marker  # 标记为异常
            patches.append((i, val))    # 记录真实值
    
    return body, patches


def pfordelta_decode_block(body: np.ndarray, patches: List, b: int) -> np.ndarray:
    """解码一个 PForDelta 块"""
    gaps = body.astype(np.int64).copy()
    
    # 应用补丁
    for pos, real_val in patches:
        gaps[pos] = real_val
    
    return gaps


def choose_bit_width(gaps: np.ndarray, exception_ratio: float = 0.1) -> int:
    """
    选择合适的位宽 b：使得 exception < exception_ratio
    """
    n = len(gaps)
    max_exceptions = int(n * exception_ratio)
    
    # 从小到大试验位宽
    for b in range(1, 33):
        max_val = (1 << b) - 1
        num_exceptions = np.sum(gaps >= max_val)
        if num_exceptions <= max_exceptions:
            return b
    
    return 32  # 最坏情况


def pfordelta_encode(doc_ids: List[int]) -> dict:
    """
    完整的 PForDelta 编码
    """
    # 差值编码
    gaps = np.array([doc_ids[0]] + [
        doc_ids[i] - doc_ids[i-1]
        for i in range(1, len(doc_ids))
    ], dtype=np.int64)
    
    # 分块处理
    n_blocks = (len(gaps) + BLOCK_SIZE - 1) // BLOCK_SIZE
    blocks = []
    
    for block_idx in range(n_blocks):
        start = block_idx * BLOCK_SIZE
        end = min(start + BLOCK_SIZE, len(gaps))
        block_gaps = gaps[start:end]
        
        # 补零到 BLOCK_SIZE
        if len(block_gaps) < BLOCK_SIZE:
            block_gaps = np.pad(block_gaps, (0, BLOCK_SIZE - len(block_gaps)))
        
        b = choose_bit_width(block_gaps)
        body, patches = pfordelta_encode_block(block_gaps, b)
        
        blocks.append({
            "b": b,
            "body": body,
            "patches": patches,
            "size": end - start,
        })
    
    return {"n_docs": len(doc_ids), "blocks": blocks}


def pfordelta_decode(encoded: dict) -> List[int]:
    """完整的 PForDelta 解码"""
    all_gaps = []
    
    for block in encoded["blocks"]:
        gaps = pfordelta_decode_block(block["body"], block["patches"], block["b"])
        all_gaps.extend(gaps[:block["size"]].tolist())
    
    # 从差值还原 DocID
    doc_ids = [int(all_gaps[0])]
    for gap in all_gaps[1:]:
        doc_ids.append(doc_ids[-1] + int(gap))
    
    return doc_ids


# 性能测试
import time

def benchmark():
    # 生成测试数据：1万个有序 doc_id
    np.random.seed(42)
    gaps = np.random.geometric(p=0.1, size=10000)  # 幂律分布的差值
    doc_ids = np.cumsum(gaps).tolist()
    
    # VByte 压缩
    t = time.time()
    vbyte_compressed = encode_posting_list(doc_ids)
    vbyte_time = time.time() - t
    
    # PForDelta 压缩
    t = time.time()
    pfd_compressed = pfordelta_encode(doc_ids)
    pfd_time = time.time() - t
    
    # 计算大小
    vbyte_size = len(vbyte_compressed)
    pfd_size = sum(
        b["b"] * BLOCK_SIZE // 8 + len(b["patches"]) * 8
        for b in pfd_compressed["blocks"]
    )
    
    print(f"原始大小: {len(doc_ids) * 4} 字节")
    print(f"VByte:    {vbyte_size} 字节, 压缩时间: {vbyte_time*1000:.2f}ms")
    print(f"PForDelta:{pfd_size} 字节, 压缩时间: {pfd_time*1000:.2f}ms")
    print(f"压缩比: VByte={len(doc_ids)*4/vbyte_size:.2f}x, "
          f"PFD={len(doc_ids)*4/pfd_size:.2f}x")

benchmark()
```

---

## 5. Simple-9 / Simple-16

**核心思想：** 将多个小整数打包进一个 32 位整数，用头部几位表示打包方案。

### 5.1 Simple-9 原理

```
32 位整数结构:
  [4位选择器][28位数据]

28位数据可以有9种打包方式（Simple-9的"9"）:

选择器 | 每整数位数 | 可打包数量 | 最大值
  0   |     28    |     1    | 2^28-1
  1   |     14    |     2    | 2^14-1
  2   |      9    |     3    | 2^9-1
  3   |      7    |     4    | 2^7-1
  4   |      5    |     5    | 2^5-1   ← 最常用（差值通常<32）
  5   |      4    |     7    | 2^4-1
  6   |      3    |     9    | 2^3-1
  7   |      2    |     14   | 2^2-1
  8   |      1    |     28   | 1       ← 全0/1序列

编码算法:
  尝试用最紧凑方式打包，选择使单次32位整数容纳最多差值的方案
```

### 5.2 Simple-9 vs VByte 对比

```
差值序列: [1, 2, 1, 3, 1, 1, 2, 4, 1, 1, 2, 1, 3, 2, ...]

VByte: 每个差值1字节（都<128）= 15字节
Simple-9: 选择器=8（每值1位），28个1可以打包 = 1×32位整数 = 4字节
压缩比: Simple-9 更优（约4x vs VByte）

但当差值较大时:
差值序列: [100, 5000, 200, 10000, ...]
Simple-9: 需要 14 位，2个值打包 = 1×32位 = 4字节/2值
VByte: 100(1B) + 5000(2B) = 3字节/2值
此时 VByte 更优
```

---

## 6. 词典压缩（Dictionary Compression）

词典本身也需要压缩，常用方法：

### 6.1 前缀编码（Front Coding）

```
原始词典（已排序）:
  automata
  automate
  automatic
  automation
  automobile
  automotive

前缀共享编码:
  8,automata
  7,e          → automata + e = automate（共享前7字符，追加e）
  8,ic         → automata + ic（共享前8字符...等等，应该是automat）
  
实际格式:
  8,automata   → 完整词
  7,e          → 共享前7字符 + "e" = automate
  9,ic         → 共享前9字符 + "ic" = automatic
  10,ion       → 共享前10字符 + "ion" = automation
  6,mobile     → 共享前6字符 + "mobile" = automobile
  9,ive        → 共享前9字符 + "ive" = automotive

压缩比: 通常词典大小减少 50-70%
```

### 6.2 块级前缀编码（Blocked Front Coding）

```
将词典分块（如每4个词一块）:
第1块（完整词 + 差分）:
  automation  ← 完整词
  *e          ← 共享前9字符 + e
  *mobile     ← 共享前5字符 + mobile  
  *motive     ← 共享前4字符 + motive

优点: 随机访问时只需找到所在块的完整词，解压少量词
缺点: 压缩率略低于纯前缀编码

这是 Lucene 词典压缩的实际策略
```

---

## 7. 各压缩算法综合对比

| 算法 | 压缩率 | 编码速度 | 解码速度 | SIMD友好 | 适用场景 |
|------|-------|---------|---------|---------|---------|
| **无压缩** | 1x | - | ★★★★★ | ✓ | 内存充足时 |
| **VByte** | 3-5x | ★★★★★ | ★★★★ | 部分 | 通用，工业主流 |
| **Elias Gamma** | 3-6x | ★★★ | ★★★ | ✗ | 小差值分布 |
| **Elias Delta** | 4-7x | ★★★ | ★★★ | ✗ | 较大差值时更优 |
| **Simple-9** | 4-6x | ★★★★ | ★★★★★ | ✓ | 小差值密集 |
| **PForDelta** | 4-8x | ★★★ | ★★★★★ | ✓ | 高性能检索 |
| **SIMD-BP128** | 5-9x | ★★★ | ★★★★★ | ✓✓✓ | 现代CPU最优 |
| **前缀编码** | 词典50-70% | - | ★★★★ | - | 词典压缩 |

---

## 8. 现代搜索引擎的实际压缩策略

### 8.1 Lucene/Elasticsearch

```
词典:
  FST（有限状态转换器）压缩
  + 块级前缀编码

Posting List:
  VInt（变长整数，类似VByte）用于小posting list
  FrameOfReference（FOR）用于大posting list（>4096个文档）
  
FOR 原理（类似PForDelta的简化版）:
  取最小值 min，所有值减 min
  用 bitPacking 压缩（确定所有值的最大位数，统一存储）
```

### 8.2 压缩感知的查询执行

```
重要优化: 解压与处理流水线化

传统:
  读取压缩数据 → 完全解压到缓冲区 → 遍历处理

优化版（流式解压）:
  边解压边处理，每次解压一个块（128/256个值）
  → 减少峰值内存使用
  → 更好的缓存局部性
  
  DAAT + PForDelta 流水线:
    decode_block() → process_block() → decode_block() → ...
```

### 8.3 压缩率 vs 查询速度权衡

```
压缩率高（如Elias Delta）:
  磁盘/内存 占用小 ✓
  I/O 时间短 ✓
  CPU 解码时间长 ✗

压缩率低（如Simple-9 / PForDelta）:
  I/O 时间略长
  CPU 解码极快（SIMD批量解压）✓✓

现代硬件（NVMe SSD + 多核CPU）:
  CPU 速度远快于 I/O
  → 倾向于使用压缩率高的算法减少 I/O

全内存场景（Redis Search / Tantivy）:
  I/O 不是瓶颈
  → 倾向于快速解码算法（PForDelta, SIMD-BP128）
```

---

## 9. 完整搜索引擎组件整合

```
┌───────────────────────────────────────────────────────────────────┐
│                  完整传统搜索引擎组件关系                              │
│                                                                   │
│  ① 文档输入                                                         │
│     ↓                                                             │
│  ② 文本预处理（第2篇）                                               │
│     tokenize + normalize + stop words + stemming                  │
│     ↓ 词条流                                                       │
│  ③ 索引构建（第3篇）                                                  │
│     SPIMI → posting lists → 差值编码                               │
│     ↓                                                             │
│  ④ 索引压缩（第8篇）← 本篇                                            │
│     VByte / PForDelta → 压缩的倒排索引                              │
│     词典: FST / B+Tree / Trie                                     │
│     ↓                                                             │
│  ⑤ 查询处理（第6篇）                                                  │
│     拼写纠错 → 查询解析 → 查询扩展 → AST                            │
│     ↓                                                             │
│  ⑥ 倒排索引查找 + 解压缩                                              │
│     ↓                                                             │
│  ⑦ Posting List 合并 + WAND 剪枝（第7篇）                            │
│     ↓                                                             │
│  ⑧ BM25 / TF-IDF 评分（第4、5篇）                                    │
│     ↓                                                             │
│  ⑨ Top-K 最小堆维护                                                  │
│     ↓                                                             │
│  ⑩ 结果返回（排名列表）                                               │
└───────────────────────────────────────────────────────────────────┘
```

---

## 10. 系列总结：关键数字参考

| 指标 | 典型值 | 说明 |
|------|-------|------|
| 词典大小 | 1-10M 词条 | 1亿文档的语料库 |
| 倒排索引大小 | 原始文本的20-40% | 压缩后 |
| VByte 压缩比 | 3-5x | 相对于原始4字节整数 |
| PForDelta 压缩比 | 5-8x | 相对于原始4字节整数 |
| 词典查找延迟 | < 1μs | 内存中的 FST/HashTable |
| Posting List 解码 | 500MB/s | VByte；PFD 可达 2GB/s |
| BM25 打分 QPS | 10K-100K | 单机，百万文档规模 |
| WAND 跳过率 | 70-95% | 取决于查询和 Top-K |
| 端到端查询延迟 | 20-200ms | 包括网络、多阶段检索 |

---

*© 传统搜索引擎深度解析系列 — 第 8 篇 / 