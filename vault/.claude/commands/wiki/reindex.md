---
description: "重建知识库索引：验证完整性 + 按主题分类到 maps/"
---

# wiki:reindex

验证 index.md 完整性，按主题分类生成 maps/*.md 索引文件。

## 输入

无参数。对整个 wiki/ 目录执行。

## 流程

### 1. 完整性检查

```bash
bash scripts/wiki.sh snapshot_index
```

解析 JSON 输出：
- `ok: true` → 继续步骤 2
- `missing` 非空 → 执行 `bash scripts/wiki.sh snapshot_index --update`，报告新增条目
- `orphaned` 非空 → 手动从 index.md 删除对应行，报告删除条目
- 再次执行确认 `ok: true`

### 2. 保存快照

```bash
bash scripts/wiki.sh snapshot_index --snapshot
```

快照保存到 `.claude/reindex.snapshot.json`，用于下次 reindex 时对比差异。

### 3. 构建主题分类

扫描所有 wiki/**/*.md 的 frontmatter `tags` 字段：

```python
# 伪代码
tags_map = {}  # tag → [page_name, ...]
for page in wiki_pages:
    for tag in page.tags:
        tags_map[tag].append(page.stem)
```

分类规则：
- 按 tag 出现频率排序
- 每个页面归入其**最高频** tag 对应的 cluster
- cluster 页面数 < 3 → 合并到"其他"

将分类计划写入 `.claude/reindex.tmp.json`：

```json
{
  "generated": "2026-04-15T14:00:00",
  "clusters": {
    "数值分析": ["牛顿法", "欧拉方法", "高斯求积公式"],
    "概率论": ["贝叶斯定理", "正态分布", "大数定律"],
    "矩阵理论": ["奇异值分解", "Schur分解", "QR算法"],
    "其他": ["bun-vs-uv", "modern-cli-tools"]
  }
}
```

### 4. 审查 tags 质量

检查每个页面的 tags 是否合理：
- **无 tags** → 根据页面 type + 内容关键词推断 tags，更新 frontmatter
- **tags 过于宽泛**（如只有 `研究`）→ 添加更具体的 tag（如 `数值分析`、`概率论`）
- 允许的 tags 参考：`数学`、`数值分析`、`概率论`、`矩阵理论`、`AI`、`工具`、`方法论`、`研究`

### 5. 生成 maps/*.md

对每个 cluster：

1. 删除旧的 `maps/*.md`（保留 `reindex.snapshot.json`）
2. 生成新文件 `maps/{topic}.md`：

```markdown
---
type: map
topic: "{topic}"
page_count: 15
updated: 2026-04-15
---

# {topic}

## 概念

- [[牛顿法]] — 数值分析最基本迭代求根算法，二次收敛速度 (confidence: 0.95)
- [[欧拉方法]] — 数值分析最基础ODE解法 (confidence: 0.95)

## 实体

- [[艾萨克·牛顿]] — 英国数学家，微积分奠基人 (confidence: 0.95)

## 综合分析

- [[矩阵谱理论的统一叙事]] — 三种证明范式的知识谱系 (confidence: 0.92)
```

每个 section 内按 title 字母序排列。

### 6. 同步 _schema/CLAUDE.md 的 Topics 列表

maps/ 变化后，更新 `_schema/CLAUDE.md` 中 **"当前 Topics"** 小节，保持文档与实际目录同步。

**读取实际 maps：**

遍历刚生成的 `maps/*.md`，从每个文件的 frontmatter 读取 `topic` 和 `page_count`，按 page_count 降序排列（`其他` 固定最后）。

**替换规则：**

定位 `_schema/CLAUDE.md` 中的以下边界块：

```
实际 cluster 数量随内容动态变化，当前存在的 topics（从 `maps/` 目录读取）：
- `...` — ...
...
```

将 `- \`...\`` 行全部替换为新列表，格式：

```markdown
- `{topic}` — {描述}（{page_count} 页）
```

描述规则（根据 topic 名称固定映射，未知 topic 则写"综合主题"）：

| topic | 描述 |
|-------|------|
| AI | AI 工程、Agent、LLM 工具 |
| 技术 | 通用技术、工程模式 |
| 机器人学 | 机器人学、运动规划、控制 |
| 研究 | 数学、概率论、数值分析等研究型内容 |
| 数学 | 纯数学概念 |
| 方法论 | 方法论、流程设计 |
| 工具 | 开发工具、软件生态 |
| 其他 | 小型 cluster 合并 |

**仅当 topics 集合有变化时才写入**（新增或删除了 topic），无变化则跳过此步。

**示例结果：**

```markdown
实际 cluster 数量随内容动态变化，当前存在的 topics（从 `maps/` 目录读取）：
- `研究` — 数学、概率论、数值分析等研究型内容（165 页）
- `AI` — AI 工程、Agent、LLM 工具（62 页）
- `机器人学` — 机器人学、运动规划、控制（45 页）
- `数学` — 纯数学概念（12 页）
- `技术` — 通用技术、工程模式（13 页）
- `其他` — 小型 cluster 合并（8 页）
```

### 7. 清理 + 日志

- 删除 `.claude/reindex.tmp.json`
- 更新 `log.md`：

```markdown
## [YYYY-MM-DD HH:MM] reindex
- 完整性: OK (121 页面, 0 缺失, 0 孤条目)
- 主题分类: 5 个 → 数值分析(25), 概率论(18), 矩阵理论(20), AI(8), 其他(10)
- Tags 修复: 3 个页面补充了 tags
- Schema 同步: _schema/CLAUDE.md Topics 已更新（如有变化）
```
