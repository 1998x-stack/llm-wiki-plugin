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

### 3. 构建主题分类（subagent）

**3a. 构建页面清单**

扫描所有 wiki/**/*.md，生成紧凑清单（用于 subagent 输入，不需要全文）：

```python
# 伪代码
manifest_lines = []
for page in wiki_pages:
    subdir = page.parent.name          # concepts / entities / syntheses / qa-insights
    fm = parse_frontmatter(page)
    tags = ",".join(fm.get("tags", []))
    overview = 概述段落首句 (≤80字)
    manifest_lines.append(f"{subdir}/{page.stem} | {tags} | {overview}")
```

将清单写入 `/tmp/wiki_manifest.txt`（每行一个页面，格式：`type/name | tags | overview`）。

**3b. 分派 subagent 进行语义聚类**

分派 Agent（`model: haiku`）执行主题分类，prompt 如下：

````
你是一个知识分类专家。下方是一个 wiki 知识库的页面清单，每行格式为：
  `类型/页面名 | 现有tags | 概述`

任务：
1. 分析每个页面的内容特征（类型 + tags + 概述综合判断）
2. 将每个页面分配到**一个**主题 topic（可新建 topic，也可复用现有 topic）
3. topic 命名要求：简洁中文（2-4 字），领域聚焦，页面数 < 3 的 topic 合并为"其他"
4. 输出严格的 JSON，格式：
```json
{
  "topics": {
    "推荐系统": ["矩阵分解", "协同过滤", "冷启动问题"],
    "信息论": ["信息熵", "KL散度", "Shannon-Hartley公式"],
    "数值分析": ["牛顿法", "欧拉方法", "高斯求积公式"],
    "其他": ["bun-vs-uv", "modern-cli-tools"]
  }
}
```
只输出 JSON，不要解释。

--- 页面清单 ---
{manifest_lines 的完整内容}
````

等待 subagent 返回结果。解析 JSON，将 `topics` 对象保存到 `.claude/topic-to-wiki.json`：

```json
{
  "generated": "2026-04-16T14:00:00",
  "topics": {
    "推荐系统": ["矩阵分解", "协同过滤", "冷启动问题"],
    "信息论": ["信息熵", "KL散度", "Shannon-Hartley公式"],
    ...
  }
}
```

**这是唯一的权威主题映射文件**，后续步骤（maps 生成、schema 同步）均从此文件读取。

### 4. 审查 tags 质量（subagent 驱动）

基于步骤 3 的 `.claude/topic-to-wiki.json` 推断哪些页面 tags 不准确：

- 遍历 `topic-to-wiki.json`，对每个 `{topic: [pages]}` 映射：
  - 读取页面 frontmatter 的 `tags`
  - 若页面 tags 中**不包含**该 topic（且 topic 非"其他"）→ 将 topic 追加到 tags
  - 若页面**无任何 tags** → 将 topic 写入 tags
- 使用 Edit 工具修改 frontmatter 的 `tags` 字段
- 记录修复页面数量

> 只追加缺失 tag，不删除已有 tags，避免破坏已有分类语义。

### 5. 生成 maps/*.md

从 `.claude/topic-to-wiki.json` 读取 `topics` 映射，对每个 topic：

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

- 删除 `/tmp/wiki_manifest.txt`
- 保留 `.claude/topic-to-wiki.json`（供后续 maintain/query 步骤引用）
- 更新 `log.md`：

```markdown
## [YYYY-MM-DD HH:MM] reindex
- 完整性: OK (N 页面, 0 缺失, 0 孤条目)
- 主题分类 (subagent): T 个 topics → topic1(N1), topic2(N2), ... → .claude/topic-to-wiki.json
- Tags 修复: M 个页面补充了 tags
- Schema 同步: _schema/CLAUDE.md Topics 已更新（如有变化）
```
