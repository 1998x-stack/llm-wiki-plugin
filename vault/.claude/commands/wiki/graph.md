---
description: "构建知识图谱 graph.json"
---

# wiki:graph

对 wiki/ 执行健康检查后构建知识图谱 JSON 文件。

## 流程

1. **执行 lint 检查（只读，不修复）**
   - 执行：`Bash: python3 scripts/lint_wiki.py --json`
   - 解析 JSON 输出，报告 errors/warnings 数量
   - **不要自动修复任何问题** — 仅报告，修复由 `wiki:lint` 命令负责
   - 如有 errors > 0，报告但继续构建图谱

2. **构建图谱 + 静态站点**
   - 执行：`Bash: python3 scripts/build_graph.py --full`
   - 这会同时构建 graph.json、graph-statistics.json、static/wiki/ HTML 页面
   - 解析输出 JSON 获取统计信息

3. **读取并报告统计**
   - 读取 `graph.json`
   - 报告：
     - 总节点数、总边数
     - 孤页数量及列表
     - 连通分量数量及大小
     - Top-10 最多连接的节点

4. **更新 log.md**
   - 追加条目：
     ```
     ## [YYYY-MM-DD HH:MM] graph
     - 构建知识图谱: N 节点, M 边, K 孤页, C 连通分量
     ```
