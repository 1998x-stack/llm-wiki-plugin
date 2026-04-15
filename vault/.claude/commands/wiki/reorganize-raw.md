---
description: "wiki:reorganize-raw"
---

# wiki:reorganize-raw

分析 `raw/` 全部内容（articles + books + assets），生成嵌套分类结构，执行文件移动并同步更新 wiki 来源引用。

**核心流程**：Claude 生成分类方案 → 写入 re-map.json → 脚本执行移动 + 更新 wiki

## 输入

无参数。对整个 `raw/` 目录执行。

## 产出

| 文件 | 路径 | 说明 |
|------|------|------|
| re-map.json | `raw/re-map.json` | 文件夹级映射（旧路径 → 新路径） |
| raw-wiki-map.json | `raw/raw-wiki-map.json` | raw 文件 → wiki 页面列表映射 |
| log.md | `log.md` | 追加操作记录 |

## 流程

### 1. 分析 raw/ 现状

扫描 `raw/` 全部目录结构（articles、books、assets）：

```bash
find raw -type d | sort
find raw -type f ! -name '.DS_Store' ! -name '.gitkeep' ! -path '*/.obsidian/*' | wc -l
```

记录：
- 当前目录树结构
- 各目录的文件数量
- 总文件数（作为完整性基线 pre_count）

### 2. 设计新的嵌套分类结构

基于 raw/ 内容的**主题相似性**，设计 2-3 层嵌套目录结构。

设计原则：
- **按主题聚合**：相关内容归入同一父目录（如 AI 工具分析 → `ai-tools/`）
- **保持叶子目录不变**：如 `claude-mem/` 内的文件结构不动，只改变其父路径
- **覆盖全部 raw/**：articles、books、assets 都参与分类
- **已经结构良好的目录可以保持不变**（如 `raw/qa/` 不动）
- **顶层分类数 5-10 个**，避免过多或过少

示例输出（展示给用户确认）：

```
raw/
├── ai-tools/           claude-code, claude-mem, claude-skills, codex, ...
├── ai-engineering/     prompt-context, search-retrieval, ...
├── ai-papers/          foundations, machine-learning, cv-models, ...
├── game-dev/           engine, testing, asset-search, taptap-maker
├── programming/        cpp, lua, lsp, cli-tools
├── academic/           statistics, neuroscience, sociology, ...
├── essays/             thinking-series, social, product-design
├── books/              (from raw/books/)
├── assets/             (from raw/assets/)
├── personal/           xd-docs
└── qa/                 (保持不动)
```

### 3. 生成 raw/re-map.json

将分类方案写为**文件夹级映射**：

```json
{
  "raw/articles/claude-mem": "raw/ai-tools/claude-mem",
  "raw/articles/claude-analysis": "raw/ai-tools/claude-code",
  "raw/books/数值分析": "raw/books/math/numerical-analysis",
  "raw/assets/RL-papers": "raw/assets/ai/rl-papers"
}
```

规则：
- key = 旧文件夹路径（相对 vault/）
- value = 新文件夹路径（相对 vault/）
- 只包含**需要移动**的文件夹，不动的不写入
- 文件夹下的所有文件整体移动，保持内部结构
- 多个旧文件夹可以映射到同一新文件夹（合并）

用 Write 工具写入 `raw/re-map.json`。

### 4. Dry-run 确认

```bash
bash scripts/wiki.sh reclassify_raw --dry-run
```

解析 JSON 输出：
- `status: "dry_run"` → 检查 `file_moves`、`would_move`、`conflicts_resolved`
- `status: "noop"` → 无需移动（re-map.json 中的文件夹都已在目标位置）
- `status: "error"` → 检查原因，修正 re-map.json 后重试

确认 `would_move` 数量合理、无意外冲突。

### 5. 执行重分类

```bash
bash scripts/wiki.sh reclassify_raw
```

脚本自动完成：
1. 读取 `raw/re-map.json`
2. 快照 pre_count
3. 展开文件夹映射为逐文件移动
4. 解决文件名冲突（同名文件加 `原文件夹--` 前缀）
5. 移动文件到新目录
6. 快照 post_count，**校验 pre_count == post_count**
7. 扫描全部 wiki 页面 `## 来源` 段落，构建 `raw/raw-wiki-map.json`
8. 更新所有 wiki 页面中 `[[raw/...]]` 引用路径
9. 清理空目录

### 6. 解析执行结果

解析 JSON 输出：

| 字段 | 含义 |
|------|------|
| `status` | `"ok"` 成功 / `"error"` 失败 |
| `pre_count` | 移动前文件总数 |
| `post_count` | 移动后文件总数 |
| `moved` | 实际移动文件数 |
| `conflicts_resolved` | 文件名冲突解决数 |
| `map_entries` | raw-wiki-map 条目数 |
| `wiki_files_updated` | 更新的 wiki 文件数 |
| `wiki_refs_updated` | 更新的来源引用数 |
| `dirs_removed` | 清理的空目录数 |

**如果 `status` 为 `"error"`** → 检查 `missing` 数组，**立即终止**。

### 7. 验证 wiki 引用

抽检 3-5 个 `wiki_files_updated` 中的文件：
- 读取 `## 来源` 段落
- 确认 `[[raw/...]]` 路径指向的文件实际存在
- 如有断链，报告

### 8. 更新 log.md

在 `log.md` 的 frontmatter 之后、第一个 `##` 之前插入：

```
## [YYYY-MM-DD HH:MM] reorganize-raw
- 完整性: N (pre) → N (post) ✓
- 移动: M 个文件, C 个冲突解决, D 个空目录清理
- Wiki 更新: F 个文件, R 条引用
- raw-wiki-map: E 条映射
```

### 9. 报告汇总

```
=== wiki:reorganize-raw 完成 ===

[1] 分析: raw/ 共 N 个文件, X 个目录
[2] 分类: 生成 re-map.json (Y 条文件夹映射)
[3] 完整性: N → N ✓ (0 丢失)
[4] 移动: M 个文件, C 个冲突解决, D 个空目录清理
[5] Wiki: F 个文件 / R 条引用已更新
[6] 产出: raw/re-map.json + raw/raw-wiki-map.json
```

## re-map.json 格式

```json
{
  "old_folder_path": "new_folder_path",
  ...
}
```

- 路径相对于 vault/（如 `raw/articles/claude-mem`）
- 文件夹级映射：文件夹下所有文件整体移动
- 只包含需要移动的文件夹
- 脚本自动处理文件名冲突、大小写、空目录清理
