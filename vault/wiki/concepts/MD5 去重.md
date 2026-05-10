---
type: concept
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [deduplication, hash, md5, idempotent, mempalace]
aliases: ["MD5 Deduplication", MD5 Hash 去重, 内容哈希去重]
relates_to:
  - target: "[[挖掘管道]]"
    type: part_of
  - target: "[[MemPalace]]"
    type: part_of
  - target: "[[增量挖掘]]"
    type: implements
  - target: "[[ChromaDB]]"
    type: uses
supersedes: null
---

# MD5 去重

## 概述
[[挖掘管道|MemPalace 挖掘]]管道使用 MD5 哈希值进行内容去重的机制，确保相同内容不会被重复存储到 [[ChromaDB]] 中。

## 关键内容
- **实现方式**：
  ```python
  import hashlib
  
  def should_store(content: str, existing_hashes: set) -> bool:
      h = hashlib.md5(content.encode()).hexdigest()
      if h in existing_hashes:
          return False  # 已存在，跳过
      existing_hashes.add(h)
      return True
  ```
- **工作流程**：挖掘前先从 ChromaDB 加载所有现有 MD5 哈希到 `existing_hashes` 集合，每个新块[[计算]] MD5 后检查是否已存在
- **去重粒度**：以 chunk（切块）为单位进行去重，不是以文件为单位
- **幂等性保证**：同一内容多次挖掘，只有第一次会被存储
- **性能考量**：MD5 [[计算]]速度快，集合查找 O(1)，适合大规模内容去重
- **与[[增量挖掘]]的关系**：MD5 去重是[[增量挖掘]]能够安全执行的基础机制

## 来源
- [[raw/articles/ai-tools/mempalace/mempalace_05_mining_pipelines.md]] — MemPalace 深度解析第五篇：三种挖掘管道

## 相关
- [[挖掘管道]] — part_of
- [[MemPalace]] — part_of
- [[增量挖掘]] — implements
- [[ChromaDB]] — uses
