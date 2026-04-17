# wiki:ingest

处理 raw/ 中的源材料，将知识编译到 wiki/ 中。

## 输入

$ARGUMENTS — 源文件路径（相对于 raw/），或 "all" 处理所有未处理的文件。

## 流程

1. **读取源文件**
   - 读取 `raw/$ARGUMENTS`
   - 如果文件不存在 → 报告错误并停止
   - 支持格式：`.md`（直接读取）、`.jsonl`（按行解析）
   - 非 markdown 格式（`.pdf`, `.docx`, `.pptx`, `.xlsx`, `.html`, `.epub`, `.csv`）→ 提示用户先运行 `wiki:convert-to-markdown` 转换，然后停止
   - 其他不支持的格式 → 报告错误并停止

2. **提取实体和概念**
   - 识别文中提到的人物、公司、项目、工具、论文、书籍
   - 识别文中的核心概念和主题
   - 参考 `_schema/entity-types.md` 确定实体类型

3. **查找已有页面**
   - 读取 `index.md` 的「全部页面」段落，快速检查提取的实体/概念是否已有对应 wiki 页面
   - 如需更多上下文（概述、confidence），读取对应主题的 `maps/*.md`
   - 如果 `maps/` 不存在或为空，回退到读取完整 `index.md`

4. **创建或更新页面**
   - **新实体** → 在 `wiki/entities/` 创建新页面，使用 `templates/wiki-page.md` 模板
   - **新概念** → 在 `wiki/concepts/` 创建新页面
   - **已有页面** → 读取现有页面，追加新信息，更新 confidence 和 source_count
   - 文件名用自然中文：`游戏资产语义搜索.md`
   - 每个页面创建/更新后，执行 BM25 索引更新：
     ```
     Bash: bash scripts/wiki.sh bm25_index update <wiki_file_path>
     ```

5. **建立关系**
   - 在每个新建/更新的页面的 frontmatter relates_to 中添加关系
   - 参考 `_schema/relationship-types.md` 选择关系类型
   - 同时更新被关联页面的 relates_to（双向）

6. **矛盾检查**
   - 如果新信息与已有页面矛盾：
     - 新页面的 relates_to 加 `type: contradicts`
     - 如果新信息更可靠（更新、更多来源），用 supersedes 标记旧声明

7. **同步 index.md**
   - 执行：`Bash: bash scripts/wiki.sh snapshot_index --slim`
   - 脚本完整重建 index.md（统计表 + 全部页面列表）
   - 注意：index.md 只含 `## 统计` 和 `## 全部页面`，详细清单见各 `maps/*.md`，不要手动编辑

8. **更新 log.md**
   - 追加条目：`## [YYYY-MM-DD HH:MM] ingest | 源文件名`
   - 列出创建了哪些页面、更新了哪些页面

9. **验证**
   - 对每个新建的页面运行：`Bash: bash scripts/wiki.sh lint_wiki --file <path> --json`
   - 如有 ERROR 级别问题，立即修复

## 质量要求

- 每个新页面必须满足 `_schema/quality-rules.md` 中的必须标准
- 概述部分不超过 200 字符
- 中文为主，专有名词保留英文
- 第一次提到的重要概念必须加 [[链接]]

## 输出

完成后报告：
- 处理了哪个源文件
- 创建了 N 个新页面
- 更新了 N 个已有页面
- 发现了 N 个矛盾（如有）
- lint 验证结果
