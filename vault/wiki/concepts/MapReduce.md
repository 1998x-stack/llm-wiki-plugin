---
type: concept
status: active
confidence: 0.95
created: 2026-04-17
updated: 2026-04-17
last_accessed: 2026-04-17
source_count: 1
tags:
- 技术
- 研究
- 计算理论
aliases:
- MapReduce
- 映射归约
relates_to:
- target: "[[MapReduce 论文]]"
  type: caused_by
  confidence: 0.99
  note: 论文中首次提出
- target: "[[Jeffrey Dean]]"
  type: caused_by
  confidence: 0.99
  note: 共同发明者
- target: "[[Sanjay Ghemawat]]"
  type: caused_by
  confidence: 0.99
  note: 共同发明者
- target: "[[函数式编程]]"
  type: extends
  confidence: 0.9
  note: 从函数式编程的 map/fold 原语获得灵感
- target: "[[分布式系统]]"
  type: implements
  confidence: 0.9
  note: 大规模数据处理的编程模型
- target: "[[Backus 函数式编程论文]]"
  type: extends
  confidence: 0.7
  note: 函数式思想的延续
supersedes: null
---

# MapReduce

## 概述

MapReduce 是一种用于大规模数据处理的编程模型，用户只需定义 Map 和 Reduce 两个函数，系统便能自动将计算并行化并分布到数千台机器上执行。

## 关键内容

### 编程模型

```
Map:    (k1, v1)       → list(k2, v2)
Reduce: (k2, list(v2)) → list(v2)
```

### 执行流程

1. **输入分片**：将输入数据分割为 M 个分片
2. **Map 阶段**：每个 Worker 处理一个分片，输出中间键值对
3. **Shuffle & Sort**：按中间键排序，将相同键的数据聚集
4. **Reduce 阶段**：对每个键执行 Reduce 函数
5. **输出合并**：结果存储在 R 个输出文件中

### 核心特性

- **自动并行化**：Map 函数无状态，可完全并行
- **透明容错**：Worker 故障自动重新调度
- **数据本地性**：移动计算而非移动数据
- **Combiner 优化**：Map 端预聚合减少网络传输
- **落后者处理**：备份执行减少慢节点影响

### 工业影响

- 催生了 Hadoop 生态系统和整个大数据产业
- [[Google]] 在2004年8月一个月内处理了 3.3 PB 数据

## 来源

- [[raw/books/计算机科学/19-dean-ghemawat-mapreduce.md]]

## 相关

- [[MapReduce 论文]] — 首次提出
- [[Jeffrey Dean]] — 共同发明者
- [[Sanjay Ghemawat]] — 共同发明者
- [[函数式编程]] — 思想来源
- [[分布式系统]] — 应用领域
- [[Backus 函数式编程论文]] — 函数式思想的先驱
