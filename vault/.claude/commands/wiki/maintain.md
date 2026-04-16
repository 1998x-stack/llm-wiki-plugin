---
description: "一键维护：relink → reindex → check → lint → build 全流水线"
---

# wiki:maintain

一键执行完整知识库维护流水线：relink → reindex → check → lint → build。

> 等价于依次运行 `wiki:relink`、`wiki:reindex`、`wiki:check`、`wiki:lint`、`wiki:build`，但在关键步骤失败时提前终止。

## 输入

无参数。对整个知识库执行。

## 流程

### 1. Relink — 自动链接术语提及

执行 `wiki:relink` 的完整流程：

```bash
bash scripts/wiki.sh relink
```

- 构建术语词典（标题 + 别名）
- 按长度降序扫描，最长匹配优先
- 在 wiki 页面正文中插入 `[[wikilinks]]`
- 跳过 frontmatter、代码块、标题、已有链接、来源/相关段落

记录添加的链接数，继续下一步。

### 2. Reindex — 索引完整性 + 主题分类

执行 `wiki:reindex` 的完整流程（步骤 1-8）：

- `bash scripts/wiki.sh snapshot_index` 检查完整性
- 修复缺失/孤条目
- 保存快照
- 按 tags 构建主题分类
- 审查 tags 质量
- 生成 `maps/*.md`（含 `## 概述`，由 `build_maps.py` 脚本生成）
- 精简 `index.md` 为统计表 + 全局名称列表
- 同步 `_schema/CLAUDE.md` 当前 Topics 列表（topics 集合有变化时）

**终止条件**：snapshot_index.py 执行出错（脚本异常，非数据问题）→ 报告错误并停止。

### 3. Check — 只读诊断 + gotchas 追加

执行 `wiki:check` 的完整流程（步骤 1-6）：

- 运行 `bash scripts/wiki.sh lint_wiki --json`
- 扫描所有 wiki/ 页面
- 执行 A-I 检查项 + 语义检查
- 生成诊断报告
- **追加新 gotchas**：将发现的新模式写入 `../docs/gotchas/`（仓库根目录，非 vault/），并同步更新 `../docs/gotchas.md` 索引

记录 ERROR / WARNING / INFO 数量及新增 gotchas 条数，继续下一步。

### 4. Lint — 自动修复

基于步骤 3 的诊断结果，执行 `wiki:lint` 的修复流程：

- 自动修复可修复的问题（frontmatter、断链、index.md、BM25）
- 跳过需人工处理的问题（矛盾、模板、图谱）
- 生成 lint 报告

### 5. Build — 构建所有静态产出

执行 `wiki:build` 的完整流程（步骤 1-7）：

- `bash scripts/wiki.sh build_graph` 构建图谱
- `cp graph.json ../static/graph.json` 同步
- `bash scripts/wiki.sh build_statistics` 构建统计
- `bash scripts/wiki.sh build_wiki_pages` 构建 HTML
- 验证所有产出
- 更新 `log.md`

### 6. 汇总报告

输出完整维护摘要：

```
=== wiki:maintain 完成 ===

[1/5] Relink
  - 术语: T 个, 扫描: S 页, 新链接: L 条

[2/5] Reindex
  - 完整性: OK (N 页面)
  - 主题分类: K 个 cluster
  - Tags 修复: M 个页面
  - Maps: G 个 map 生成（含概述）
  - Index: 精简为 L 行
  - Schema 同步: _schema/CLAUDE.md Topics 已更新 / 无变化

[3/5] Check
  - ERROR: A 个 | WARNING: B 个 | INFO: C 个
  - 新 gotchas: G 条 → ../docs/gotchas/[file].md

[4/5] Lint
  - 自动修复: X 个
  - 需人工处理: Y 个

[5/5] Build
  - 知识图谱: N 节点, M 边, K 孤页, C 连通分量
  - 静态产出: graph.json + statistics + wiki HTML (P 页)
```

### 7. 更新 log.md

在 `log.md` 的 frontmatter 之后、第一个 `##` 之前插入：

```
## [YYYY-MM-DD HH:MM] maintain
- Relink: T terms, L new links across P pages
- Reindex: OK (N 页面, K clusters, G maps) | Index: L 行 | Schema 同步: 已更新/无变化
- Check: A errors, B warnings, C info (G new gotchas → ../docs/gotchas/[file].md)
- Lint: X 修复, Y 待处理
- Build: N 节点, M 边 → static/ 已同步
```

### 8. Git commit

将所有变更提交：

```bash
git add -A && git commit -m "chore: wiki:maintain — relink + reindex + check + lint + build (YYYY-MM-DD)"
```

提交信息包含本次 maintain 的关键数据（节点数、边数等）。
