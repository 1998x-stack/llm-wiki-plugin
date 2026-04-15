---
description: "构建知识图谱 graph.json"
---

# wiki:graph

对 wiki/ 执行健康检查后构建知识图谱 JSON 文件。

## 流程

1. **执行 lint 检查**
   - 重点检查：
     - **B. 孤页检查** — 找出没有被任何其他页面链接到的页面
     - **C. 断链检查** — 找出所有 [[链接]] 指向不存在的页面的情况
   - 自动修复可修复的问题：
     - 近似名称的断链 → 自动修正
     - 缺失的 index.md 条目 → 自动添加

2. **构建图谱**
   - 执行：`Bash: cd vault && python3 scripts/build_graph.py`
   - 解析输出 JSON 获取统计信息

3. **读取并报告统计**
   - 读取 `vault/graph.json`
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
