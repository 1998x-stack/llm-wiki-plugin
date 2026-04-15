---
description: "一键维护：reindex → check → lint → build 全流水线"
---

# wiki:maintain

一键执行完整知识库维护流水线：reindex → check → lint → build。

> 等价于依次运行 `wiki:reindex`、`wiki:check`、`wiki:lint`、`wiki:build`，但在关键步骤失败时提前终止。

## 输入

无参数。对整个知识库执行。

## 流程

### 1. Reindex — 索引完整性 + 主题分类

执行 `wiki:reindex` 的完整流程（步骤 1-6）：

- `python3 scripts/snapshot_index.py` 检查完整性
- 修复缺失/孤条目
- 保存快照
- 按 tags 构建主题分类
- 审查 tags 质量
- 生成 `maps/*.md`

**终止条件**：snapshot_index.py 执行出错（脚本异常，非数据问题）→ 报告错误并停止。

### 2. Check — 只读诊断

执行 `wiki:check` 的完整流程（步骤 1-5）：

- 运行 `python3 scripts/lint_wiki.py --json`
- 扫描所有 wiki/ 页面
- 执行 A-I 检查项 + 语义检查
- 生成诊断报告

记录 ERROR / WARNING / INFO 数量，继续下一步。

### 3. Lint — 自动修复

基于步骤 2 的诊断结果，执行 `wiki:lint` 的修复流程（步骤 2-4）：

- 自动修复可修复的问题（frontmatter、断链、index.md、BM25）
- 跳过需人工处理的问题（矛盾、模板、图谱）
- 生成 lint 报告追加到 `log.md`
- 更新 `dashboard.md`

### 4. Build — 构建所有静态产出

执行 `wiki:build` 的完整流程（步骤 1-6）：

- `python3 scripts/build_graph.py` 构建图谱
- `cp graph.json ../static/graph.json` 同步
- `python3 scripts/build_statistics.py` 构建统计
- `python3 scripts/build_wiki_pages.py` 构建 HTML
- 验证所有产出
- 更新 `log.md`

### 5. 汇总报告

输出完整维护摘要：

```
=== wiki:maintain 完成 ===

[1/4] Reindex
  - 完整性: OK (N 页面)
  - 主题分类: K 个 cluster
  - Tags 修复: M 个页面

[2/4] Check
  - ERROR: A 个 | WARNING: B 个 | INFO: C 个

[3/4] Lint
  - 自动修复: X 个
  - 需人工处理: Y 个

[4/4] Build
  - 知识图谱: N 节点, M 边, K 孤页, C 连通分量
  - 静态产出: graph.json + statistics + wiki HTML (P 页)
```

### 6. 更新 log.md

在 `log.md` 的 frontmatter 之后、第一个 `##` 之前插入：

```
## [YYYY-MM-DD HH:MM] maintain
- Reindex: OK (N 页面, K clusters)
- Check: A errors, B warnings, C info
- Lint: X 修复, Y 待处理
- Build: N 节点, M 边 → static/ 已同步
```

### 7. Git commit

将所有变更提交：

```bash
git add -A && git commit -m "chore: wiki:maintain — reindex + lint + build (YYYY-MM-DD)"
```

提交信息包含本次 maintain 的关键数据（节点数、边数等）。
