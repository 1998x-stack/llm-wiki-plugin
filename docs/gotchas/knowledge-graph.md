# Knowledge Graph Gotchas

图谱构建和孤儿检测相关的问题。

---

## #1 — O1: Graph orphan_count 与 lint O1 检查结果不一致

**Status**: New (2026-04-19)

**问题描述**:

`graph.json` 报告 `orphan_count: 0`，但 `lint_wiki.py --json` 报告 **76 个孤儿页面**。

**根因分析**:

两种检测逻辑不同：

| 工具 | 检测逻辑 | 数据来源 |
|------|---------|---------|
| `build_graph.py` | 基于 `relates_to` 关系和文件存在性 | frontmatter 中的 relates_to |
| `lint_wiki.py O1` | 基于 wikilink 语法解析 `[[...]]` | 页面正文中的双链引用 |

**示例**: 
- 页面 A 在 frontmatter 中声明 `relates_to: [{target: B}]` → Graph 认为 A-B 有连接
- 页面 B 在正文中没有 `[[A]]` 链接 → Lint 认为 A 是孤儿

**When it bites**:
- 对孤儿定义产生困惑
- 不知道该相信哪个数据源
- 可能导致过度链接或遗漏真正的孤立页面

**Workaround/Fix**:
- 明确孤儿定义：
  - **Graph 孤儿**: 无 relates_to 关系（语义孤立）
  - **Lint 孤儿**: 无 wikilink 入链（导航孤立）
- 建议维护者同时关注两个指标
- 长期 fix: 统一孤儿定义，或明确区分两种孤儿的报告

---

## #2 — H1: 存在 5 个连通分量

**Status**: New (2026-04-19)

**问题描述**:

`graph.json` 显示 `"component_count": 5`，表示知识图谱存在 5 个不连通的子图。

**When it bites**:
- 某些主题的知识完全孤立，无法通过链接导航到达
- 查询时可能遗漏相关跨主题内容

**Workaround/Fix**:
- 运行 `wiki:relink` 自动链接相关概念
- 手动在边界页面添加跨主题链接
- 检查是否有应该连接但未连接的主题对

---
