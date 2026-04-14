# wiki:ingest

处理 raw/ 中的源材料，将知识编译到 wiki/ 中。

## 输入

$ARGUMENTS — 源文件路径（相对于 vault/raw/），或 "all" 处理所有未处理的文件。

## 流程

1. **读取源文件**
   - 完整阅读 `raw/$ARGUMENTS`
   - 如果是 .docx，使用 `pandoc` 或直接读取文本内容
   - 如果是 .jsonl，按行解析
   - 如果是 .pdf，提取文本

2. **提取实体和概念**
   - 识别文中提到的人物、公司、项目、工具、论文、书籍
   - 识别文中的核心概念和主题
   - 参考 `_schema/entity-types.md` 确定实体类型

3. **查找已有页面**
   - 读取 `index.md` 查看已有页面列表
   - 对每个提取的实体/概念，检查是否已有对应 wiki 页面

4. **创建或更新页面**
   - **新实体** → 在 `wiki/entities/` 创建新页面，使用 `templates/wiki-page.md` 模板
   - **新概念** → 在 `wiki/concepts/` 创建新页面
   - **已有页面** → 读取现有页面，追加新信息，更新 confidence 和 source_count
   - 文件名用自然中文：`游戏资产语义搜索.md`

5. **建立关系**
   - 在每个新建/更新的页面的 frontmatter relates_to 中添加关系
   - 参考 `_schema/relationship-types.md` 选择关系类型
   - 同时更新被关联页面的 relates_to（双向）

6. **矛盾检查**
   - 如果新信息与已有页面矛盾：
     - 新页面的 relates_to 加 `type: contradicts`
     - 如果新信息更可靠（更新、更多来源），用 supersedes 标记旧声明

7. **更新 index.md**
   - 在对应分类下添加新页面条目
   - 格式：`- [[页面名]] — 一行摘要 (confidence: X.X)`
   - 更新统计数字

8. **更新 log.md**
   - 追加条目：`## [YYYY-MM-DD] ingest | 源文件名`
   - 列出创建了哪些页面、更新了哪些页面

## 质量要求

- 每个新页面必须满足 `_schema/quality-rules.md` 中的必须标准
- 概述部分不超过 200 字
- 中文为主，专有名词保留英文
- 第一次提到的重要概念加 [[链接]]

## 输出

完成后报告：
- 处理了哪个源文件
- 创建了 N 个新页面
- 更新了 N 个已有页面
- 发现了 N 个矛盾（如有）
