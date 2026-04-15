---
description: "构建所有静态产出：graph.json + statistics + wiki HTML"
---

# wiki:build

构建所有静态产出：graph.json、graph-statistics.json、static/wiki/ HTML 页面。

**工作目录：`vault/`**

## 产出清单

| 产出 | 路径（相对 vault/） | 来源脚本 |
|------|---------------------|----------|
| graph.json | `graph.json` | build_graph.py |
| graph.json (static) | `../static/graph.json` | cp from vault |
| graph-statistics.json | `../static/graph-statistics.json` | build_statistics.py |
| wiki HTML | `../static/wiki/` | build_wiki_pages.py |
| log.md | `log.md` | 手动追加 |

## 流程

### 1. Lint 检查（只读，不修复）

```bash
bash scripts/wiki.sh lint_wiki --json
```

- 解析 JSON 输出，报告 errors/warnings 数量
- **不自动修复** — 修复由 `wiki:lint` 负责
- 有 errors 也继续构建

### 2. 构建 graph.json

```bash
bash scripts/wiki.sh build_graph
```

- 解析 JSON 输出，记录 nodes/edges/orphans/components 四个数值
- 产出：`graph.json`

### 3. 同步 + 构建 statistics + 构建 HTML

三个操作顺序执行（build_statistics.py 依赖 graph.json）：

```bash
cp graph.json ../static/graph.json && bash scripts/wiki.sh build_statistics && bash scripts/wiki.sh build_wiki_pages
```

- 每条命令都会打印 JSON status，确认 `"status": "ok"`
- 如任何一步失败，报告错误并停止

### 4. 验证所有产出

```bash
ls -la graph.json ../static/graph.json ../static/graph-statistics.json ../static/wiki/index.html
```

- 确认 4 个文件都存在且非空
- 如有缺失，报告哪个文件缺失

### 5. 报告统计

- 从步骤 2 的 JSON 输出中提取：总节点数、总边数、孤页数、连通分量数
- 读取 `../static/graph-statistics.json` 的 `top_connected` 前 10 项
- 用表格或列表展示

### 6. 更新 log.md

在 `log.md` 的 frontmatter 之后、第一个 `##` 之前插入：

```
## [YYYY-MM-DD HH:MM] graph
- 知识图谱: N 节点, M 边, K 孤页, C 连通分量
- 同步: graph.json + graph-statistics.json + wiki HTML (P 页)
```

其中 P 来自 build_wiki_pages.py 的 `pages_converted` 输出。
