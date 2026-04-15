---
description: "重建知识库索引：验证完整性 + 按主题分类到 maps/"
---

# wiki:reindex

验证 index.md 完整性，按主题分类生成 maps/*.md 索引文件。

## 流程

### 1. 完整性检查

- 执行：`python3 scripts/snapshot_index.py`
- 如有 missing → `python3 scripts/snapshot_index.py --update`
- 如有 orphaned → 从 index.md 移除
- 确保 `ok: true`

### 2. 保存快照

- 执行：`python3 scripts/snapshot_index.py --snapshot`

### 3. 构建主题分类

- 扫描 wiki/**/*.md 的 tags 字段
- 按 tag 频率分组，< 3 页合并到"其他"
- 写入 `.claude/reindex.tmp.json`

### 4. 生成 maps/*.md

对每个 cluster 生成 `maps/{topic}.md`（frontmatter type: map）。
清理旧 maps/*.md，写入新文件。

### 5. 清理 + 日志

- 删除 `.claude/reindex.tmp.json`
- 更新 log.md
