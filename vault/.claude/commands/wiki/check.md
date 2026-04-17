# wiki:check

对知识库进行全面健康检查（只读诊断，不修改任何文件）。结合脚本检查和语义分析，生成报告。

> 如需自动修复，请运行 `wiki:lint`。

## 流程

1. **运行脚本检查**
   - 执行：`Bash: bash scripts/wiki.sh lint_wiki --json`
   - 解析 JSON 报告获取所有脚本级别的问题

2. **扫描所有 wiki/ 页面**
   - 读取 wiki/ 下所有 .md 文件
   - 解析每个文件的 frontmatter

3. **检查项**（全部只读，不修改文件）

   **A. Frontmatter 完整性**
   - 检查每个页面是否有所有必需的 frontmatter 字段
   - 缺失字段 → 报告为 ERROR

   **B. 孤页检查**
   - 找出没有被任何其他页面链接到的页面
   - 报告为 WARNING

   **C. 断链检查**
   - 找出所有 [[链接]] 指向不存在的页面的情况
   - 如果存在近似名称的页面 → 报告为 WARNING（建议修正目标）
   - 否则 → 报告为 WARNING（建议创建页面）

   **D. 矛盾检查**
   - 扫描 relates_to 中 type=contradicts 的关系
   - 检查是否已有 supersedes 解决
   - 未解决的矛盾 → 报告为 WARNING

   **E. 过期检查**
   - 找出 confidence < 0.3 的页面 → 报告为 INFO（stale）
   - 找出 last_accessed 超过 180 天的页面 → 报告为 INFO（可能需要复查）

   **F. index.md 一致性**
   - 确保 wiki/ 中所有页面都出现在 index.md 中
   - 确保 index.md 中没有指向已删除页面的条目
   - 不一致 → 报告为 ERROR

   **G. BM25 索引一致性**
   - 读取 `index/BM25/docmap.json`
   - 与实际 wiki/ 文件对比
   - 缺失条目 → 报告为 WARNING

   **H. 图谱连通性**
   - 如果 `graph.json` 存在，读取其内容
   - 如果 `graph.json` 不存在，跳过此检查并报告 INFO: "graph.json 不存在，运行 wiki:build 构建图谱。"
   - 从 graph.json 的 `components` 字段检查是否有小于 3 个节点的孤立子图
   - 从 `orphans` 字段报告孤页
   - 报告为 WARNING

   **I. 模板合规性**
   - 检查页面是否包含其模板要求的必需章节
   - 对于 wiki-page 类型：必须有 概述、关键内容、来源、相关 四个章节
   - 缺失章节 → 报告为 WARNING

   **J. Maps 概述完整性**
   - 检查每个 `maps/*.md` 是否包含 `## 概述` section
   - 检查每个 map 的 `page_count` 是否与实际 wiki 页面数匹配
   - 检查是否有 wiki 页面不属于任何 map（基于 `.claude/topic-to-wiki.json`）
   - 缺失概述或大量页面未分类 → 报告为 WARNING，建议运行 `wiki:reindex`（重建 topic-to-wiki.json）再运行 `wiki:build`（重建 maps）

4. **语义检查**（Claude 独有）
   - 矛盾合理性：`contradicts` 关系是否有合理的解决方案？
   - 置信度合理性：confidence 是否与 source_count 匹配？
   - 标签一致性：相似主题的页面是否使用相似的标签？

5. **生成报告**
   - 按严重程度分类：ERROR / WARNING / INFO
   - 输出汇总：
     ```
     Check 完成: N 个页面
     ERROR: M 个 | WARNING: K 个 | INFO: J 个
     ```
   - 列出所有发现的问题清单（不修复，只报告）

6. **追加 gotchas**（如发现新模式）

   > **路径**：`../docs/gotchas/`（相对于 vault/ 工作目录，即仓库根目录下的 `docs/gotchas/`）

   检查报告中是否存在值得记录的**新模式**。以下情况应追加 gotcha：

   - **脚本误报（false-positive）**：代码块内容被误识别为 wikilink（如 TOML `[[rule]]` 语法触发 B1 警告）
   - **结构性缺陷**：揭示流程设计漏洞（如新建页面无法自动加入 map）
   - **重复出现的问题**：同一错误模式在多个页面出现
   - **非显而易见的修复**：修复方案不直观、将来容易重犯

   **类别 → 文件映射**：

   | 问题类型 | 目标文件 |
   |---------|---------|
   | 代码块内容误触 B1（broken link 误报） | `../docs/gotchas/script-fixes.md` |
   | M2 unmapped 页面的规律性成因 | `../docs/gotchas/knowledge-graph.md` |
   | F1-F4 frontmatter / index 问题 | `../docs/gotchas/ingest-issues.md` |
   | 钩子或脚本行为异常 | `../docs/gotchas/hooks-and-paths.md` |
   | 无合适归类 | 新建 `../docs/gotchas/check-issues.md` |

   **追加流程**：

   1. 扫描 `../docs/gotchas/` 下所有 `*.md`，找到最高 `## #N —` 编号，新条目从 N+1 开始
   2. 在目标文件末尾追加，格式：

      ```markdown
      ## #N — [组件/检查码]: [一行摘要]

      **Status**: New (YYYY-MM-DD)

      [问题描述：触发条件、表现、根因]

      **When it bites**: [具体触发场景]

      **Workaround/Fix**: [已采取的措施或建议]
      ```

   3. 如果追加了新条目，同步更新 `../docs/gotchas.md` 索引表中对应行的 Issues 范围（如 `#15-17` → `#15-18`）
