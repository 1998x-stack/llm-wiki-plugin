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
