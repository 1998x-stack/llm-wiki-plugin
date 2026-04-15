# wiki:lint

对知识库进行全面健康检查，自动修复可修复的问题。结合脚本检查和语义分析。

## 流程

1. **运行脚本检查**
   - 执行：`Bash: python3 scripts/lint_wiki.py --json`
   - 解析 JSON 报告获取所有脚本级别的问题

2. **扫描所有 wiki/ 页面**
   - 读取 wiki/ 下所有 .md 文件
   - 解析每个文件的 frontmatter

3. **检查项**

   **A. Frontmatter 完整性**
   - 检查每个页面是否有所有必需的 frontmatter 字段
   - 缺失字段 → 自动填入默认值（confidence 根据 source_count 估算）

   **B. 孤页检查**
   - 找出没有被任何其他页面链接到的页面
   - 尝试在相关页面中添加链接
   - 无法自动链接的 → 报告为需人工处理

   **C. 断链检查**
   - 找出所有 [[链接]] 指向不存在的页面的情况
   - 如果存在近似名称的页面 → 自动修正
   - 否则 → 报告为需创建的页面

   **D. 矛盾检查**
   - 扫描 relates_to 中 type=contradicts 的关系
   - 检查是否已有 supersedes 解决
   - 未解决的矛盾 → 基于 confidence 和 source_count 提出建议

   **E. 过期检查**
   - 找出 confidence < 0.3 的页面 → 标记为 stale
   - 找出 last_accessed 超过 180 天的页面 → 报告为可能需要复查

   **F. index.md 一致性**
   - 确保 wiki/ 中所有页面都出现在 index.md 中
   - 确保 index.md 中没有指向已删除页面的条目

   **G. BM25 索引一致性**
   - 读取 `index/BM25/docmap.json`
   - 与实际 wiki/ 文件对比
   - 缺失条目 → 执行：`Bash: python3 scripts/bm25_index.py update <missing_file>`

   **H. 图谱连通性**
   - 执行：`Bash: python3 scripts/build_graph.py`
   - 读取 graph.json，检查是否有小于 3 个节点的孤立子图
   - 报告为 WARNING

   **I. 模板合规性**
   - 检查页面是否包含其模板要求的必需章节
   - 对于 wiki-page 类型：必须有 概述、关键内容、来源、相关 四个章节
   - 缺失章节 → 报告为 WARNING

4. **语义检查**（Claude 独有）
   - 矛盾合理性：`contradicts` 关系是否有合理的解决方案？
   - 置信度合理性：confidence 是否与 source_count 匹配？
   - 标签一致性：相似主题的页面是否使用相似的标签？

5. **生成报告**
   - 按严重程度分类：ERROR（必须修复）/ WARNING（建议修复）/ INFO（参考信息）
   - 追加到 log.md，格式：
     ```
     ## [YYYY-MM-DD HH:MM] lint
     - 扫描: N 个页面
     - ERROR: M 个 | WARNING: K 个 | INFO: J 个
     - 自动修复: X 个
     - 需要人工处理: Y 个
     ```
   - 列出具体问题清单

6. **更新 dashboard.md**
   - 更新 "最近 lint" 日期
