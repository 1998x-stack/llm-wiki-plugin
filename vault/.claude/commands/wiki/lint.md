# wiki:lint

对知识库进行健康检查，自动修复可修复的问题。

## 流程

1. **扫描所有 wiki/ 页面**
   - 读取 wiki/ 下所有 .md 文件
   - 解析每个文件的 frontmatter

2. **检查项**

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

3. **生成报告**
   - 追加到 log.md，格式见 `_schema/quality-rules.md` 中的 Lint 报告格式

4. **更新 dashboard.md**
   - 更新 "最近 lint" 日期
