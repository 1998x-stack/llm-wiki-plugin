---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [file-system, atomic-operation, data-integrity, safety]
aliases: ["Atomic Write", "原子写入", "原子文件写入", "atomic file operation"]
relates_to: 
  - target: "[[Write-Tools]]"
    type: used_by
  - target: "[[File System]]"
    type: relates_to
  - target: "[[Data Integrity]]"
    type: ensures
supersedes: null
---

# atomic_write

## 概述
atomic_write 是一种确保文件写入操作原子性的技术，通过 temp → fsync → rename 三步操作保证数据一致性，即使在系统崩溃或断电的情况下也能确保文件完整性。

## 关键内容

1. **实现原理**：
   ```python
   def atomic_write(path, content):
       dir_path = os.path.dirname(os.path.abspath(path))
       with tempfile.NamedTemporaryFile(mode='w', dir=dir_path, delete=False) as f:
           f.write(content)
           f.flush()
           os.fsync(f.fileno())   # 确保数据落盘
           tmp_path = f.name
       os.replace(tmp_path, path) # POSIX atomic rename
   ```

2. **三步原子操作**：
   - **Temp**：将新内容写入临时文件，位于与目标文件相同目录（同一文件系统）
   - **fsync**：强制将数据和元数据刷入磁盘，确保数据持久化
   - **rename**：使用 POSIX 的 atomic rename 操作，将临时文件重命名为目标文件名

3. **关键细节**：
   - tempfile 必须在同一目录（同一文件系统），否则 `os.replace` 退化为 copy+delete，失去原子性保证
   - 这是不可妥协的数据完整性底线，所有 [[Write-Tools]] 都使用此方法

4. **应用场景**：
   - [[Write-Tools|文件写入工具]]的底层实现
   - [[Configuration|配置]]文件更新
   - 重要数据的持久化存储
   - 防止并发访问冲突

## 来源
- [[write-tools.md]] — 五、Atomic Write — 不可妥协的底线

## 相关
- [[Write-Tools]] — used_by
- [[File System]] — relates_to
- [[Data Integrity]] — ensures