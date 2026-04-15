# wiki:journal

辅助写日记、反思或判断，自动链接到相关知识页面。

## 输入

$ARGUMENTS — 日记类型和内容提示。格式：`<type> [topic]`
- `daily` — 创建/打开今天的 daily note
- `reflection <topic>` — 创建一篇新的反思
- `judgment <topic>` — 创建一篇新的判断

## 流程

### daily

1. 检查 `journal/daily/` 中是否已有今天的文件（YYYY-MM-DD.md）
2. 如果没有 → 用 `templates/daily.md` 创建，替换 {{date}} 为今天日期
3. 如果已有 → 读取现有内容
4. 搜索相关知识页面：
   - 执行：`Bash: bash scripts/wiki.sh search_wiki "<today's topics>" --top 5 --json`
   - 从搜索结果中提取页面名称，在 daily note 的"相关"部分添加 [[链接]]
   - 如搜索结果包含 topic_context，在"相关"部分标注主题领域

### reflection

1. 用 `templates/reflection.md` 创建新文件在 `journal/reflections/`
2. 文件名：topic 转为文件名格式
3. 替换 {{date}} 和 {{title}}
4. 搜索相关页面：
   - 执行：`Bash: bash scripts/wiki.sh search_wiki "<topic>" --top 5 --json`
   - 将搜索结果中的页面以 [[链接]] 形式添加到"相关"部分
5. 追加 log.md

### judgment

1. 用 `templates/judgment.md` 创建新文件在 `journal/judgments/`
2. 文件名：topic 转为文件名格式
3. 替换 {{date}} 和 {{title}}
4. 搜索相关页面：
   - 执行：`Bash: bash scripts/wiki.sh search_wiki "<topic>" --top 5 --json`
   - 将搜索结果中的页面以 [[链接]] 形式添加到"相关知识"部分
5. 追加 log.md
