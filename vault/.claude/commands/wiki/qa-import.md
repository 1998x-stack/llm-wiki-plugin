# wiki:qa-import

批量导入 QA 对话数据，提取洞见到 wiki。使用 `raw/qa/qa.snapshot.md` 跟踪已处理文件。

## 输入

$ARGUMENTS — QA 文件路径（相对于 raw/qa/），或 "all" 处理所有未导入的文件。

## 支持格式

- `.jsonl` — 每行一个 JSON 对象，必须有 `question` 和 `answer` 字段
- `.md` — QA 格式（frontmatter 包含 type: qa，正文包含 ## 问题 和 ## 回答）

## 流程

### 0. 读取/初始化快照

- 读取 `raw/qa/qa.snapshot.md`（如果不存在则创建）
- 快照格式：
  ```markdown
  # QA Import Snapshot

  > 跟踪 raw/qa/ 中的 QA 文件导入状态。由 wiki:qa-import 和 wiki:query 维护。

  - [x] qa-20260407-175851.md — imported 2026-04-15
  - [ ] qa-20260408-145529.md — 待处理
  ```
- 解析已勾选（`[x]`）的文件名列表

### 1. 确定待处理文件

- **单文件模式**（`$ARGUMENTS` 不是 "all"）：直接处理指定文件
- **all 模式**：
  - 扫描 `raw/qa/` 中所有 `.md` 和 `.jsonl` 文件（排除 `qa.snapshot.md` 和 `.gitkeep`）
  - 对比快照，找出未勾选（`[ ]`）或不在快照中的文件
  - 将新发现的文件追加到快照（标记为 `[ ]`）
  - 只处理未勾选的文件

### 2. 解析 QA 数据

- 读取源文件
- 提取所有 Q&A 对
- 记录每个 QA 的行号/位置（用于溯源）

### 3. 主题聚类

- 将 QA 按主题分组（同一概念/项目的归到一起）
- 每个聚类标注主题关键词

### 4. 提取洞见

- 对每个聚类：
  - 提取跨多个 QA 的关键发现
  - 过滤掉纯操作性内容（"怎么安装 X"），保留有知识价值的洞见
  - 评估每个洞见的 confidence（基于 QA 数量和一致性）

### 5. 创建洞见页面

- 对每个高价值洞见，在 `wiki/qa-insights/` 创建页面
- frontmatter:
  ```yaml
  type: qa-insight
  source_file: "raw/qa/文件名"
  source_lines: [行号列表]
  topics: ["主题1", "主题2"]
  confidence: X.X
  created: YYYY-MM-DD
  status: active
  tags: []
  aliases: []
  relates_to: []
  ```
- 内容包含：发现摘要、证据、关联知识的 [[链接]]

### 6. 建立双向链接

- 找到 wiki/ 中与洞见主题相关的已有页面
- 在已有页面的 relates_to 中添加指向新洞见页面的链接
- 在洞见页面的 relates_to 中添加指向已有页面的链接

### 7. 更新快照

- 将已处理的文件在 `raw/qa/qa.snapshot.md` 中标记为 `[x]`，追加导入日期
- 格式：`- [x] 文件名 — imported YYYY-MM-DD, N insights`

### 8. 更新 index.md 和 log.md

- 执行：`Bash: python3 scripts/snapshot_index.py --update`
- log.md: `## [YYYY-MM-DD HH:MM] qa-import | 文件名 → N 个洞见`
