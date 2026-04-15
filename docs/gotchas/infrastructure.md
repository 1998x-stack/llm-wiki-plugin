# Infrastructure Issues

> From docs/gotchas.md #5-8

---

## 5. 实体页面的「来源」格式不一致

**问题**：部分已有实体页面的 `来源` 节格式不统一——有些用 `[[raw/...]]` 格式，有些用裸路径字符串。例如：

```markdown
# 不一致的写法：
- [[raw/books/数值分析/06_jacobi_iteration.md]]   <- 带双链（可跳转）
- raw/books/矩阵分析/14_wilkinson_algebraic...    <- 裸字符串（不可跳转）
```

**建议**：标准化为带双链格式 `[[raw/books/...]]`，方便在 Obsidian 中反向溯源。

---

## 6. BM25 索引未同步

**问题**：ingest-loop 中断导致 BM25 索引（`vault/index/BM25/`）未对所有新创建的页面执行更新。

**修复**：
```bash
cd vault
python3 scripts/bm25_index.py build  # 全量重建索引
```

---

## 7. graph.json 未重建

**问题**：大量新页面（数值分析系列 + 概率论系列）添加后，`vault/graph.json` 尚未重建，知识图谱可视化数据已过时。

**修复**：
```bash
/wiki:graph
```
或直接：
```bash
cd vault
python3 scripts/build_graph.py
```

---

## 8. Hook 脚本依赖

**注意**：三个 PostToolUse hook（`hook_lint.sh`, `hook_bm25.sh`, `hook_graph.sh`）会在每次 `wiki/**/*.md` 写入后自动触发。但批量 ingest 时 hook 可能因：
- Python 包未安装（`jieba`, `rank_bm25`, `pyyaml`）
- 路径问题（hook 从 vault/ 目录执行）

**检查安装**：
```bash
pip install jieba rank-bm25 pyyaml
```

**查看 hook 执行日志**：`vault/log.hook.md`

---

## 36. keywords.txt 被年份范围污染（已修复）

**问题**：`build_keywords.py` 将 entity 页面 `aliases:` 字段的所有值无过滤地写入 `wiki/keywords.txt`。部分 person 实体的生卒年（如 `1707--1783`、`1926-`）被当成有效别名，出现在 keywords.txt 开头的 28 行：

```
1643--1727 3 n   ← 艾萨克·牛顿
1685--1731 3 n   ← 布鲁克·泰勒
1707--1783 3 n   ← 莱昂哈德·欧拉
...（共 28 条）
```

这些条目会干扰 jieba 分词（向分词器注入年份区间），且对搜索完全无用。

**根因**：ingest subagent 将生卒年写入了 `aliases:` 字段，而非放在正文或忽略。`build_keywords.py` 没有过滤非词汇字符串。

**修复（2026-04-16）**：
1. 从 28 个 entity 页面的 `aliases:` 中删除所有 `XXXX-XXXX` 或 `XXXX--XXXX` 格式条目
2. `build_keywords.py` 新增 `_is_valid_keyword()` 过滤函数，正则 `^\d{4}-{1,2}\d{0,4}$` 屏蔽年份范围
3. 重建 `wiki/keywords.txt`（从 1781 → 1753 词条）

**预防**：
- Ingest subagent prompt 不应将生卒年放入 `aliases`；生卒年属于正文信息，不是别名
- `build_keywords.py` 的过滤层保证即使 aliases 写错也不会污染 jieba 字典

---

## 37. 来源格式不统一（已修复）

**问题**：125 个 wiki 页面的 `## 来源` 条目不可点击，包括：
- 裸 `raw/...` 路径（78 条）：未用 `[[]]` 包裹
- `` `raw/...` `` 反引号格式（8 条）
- 学术引用纯文本（无 URL/DOI，约 24 条）
- `综合自 wiki 内部引用（xxx）` 未将页名转为 `[[链接]]`（12 条）

**修复（2026-04-16）**：
- 脚本批量修复：raw 路径 → `[[raw/...]]`，综合引用 → `[[页名]]`，URL 前缀格式 → `[text](URL)`
- 学术论文引用：通过 DOI/arXiv lookup table 转换为 `[Title (Author Year)](https://doi.org/...)`
- 最终验证：0 条非标准 `来源` 条目残留
