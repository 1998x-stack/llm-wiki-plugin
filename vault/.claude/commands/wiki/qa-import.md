# wiki:qa-import

批量导入 QA 对话数据，提取洞见到 wiki。

## 输入

$ARGUMENTS — QA 文件路径（相对于 raw/qa/），或 "all" 处理所有。

## 支持格式

- `.jsonl` — 每行一个 JSON 对象，必须有 `question` 和 `answer` 字段
- `.md` — ChatGPT 导出格式（Prompt/Response 交替）

## 流程

1. **解析 QA 数据**
   - 读取源文件
   - 提取所有 Q&A 对
   - 记录每个 QA 的行号/位置（用于溯源）

2. **主题聚类**
   - 将 QA 按主题分组（同一概念/项目的归到一起）
   - 每个聚类标注主题关键词

3. **提取洞见**
   - 对每个聚类：
     - 提取跨多个 QA 的关键发现
     - 过滤掉纯操作性内容（"怎么安装 X"），保留有知识价值的洞见
     - 评估每个洞见的 confidence（基于 QA 数量和一致性）

4. **创建洞见页面**
   - 对每个高价值洞见，在 `wiki/qa-insights/` 创建页面
   - frontmatter:
     ```yaml
     type: qa-insight
     source_file: "raw/qa/文件名"
     source_lines: [行号列表]
     topics: ["主题1", "主题2"]
     confidence: X.X
     created: YYYY-MM-DD
     status: active
     tags: []
     aliases: []
     relates_to: []
     ```
   - 内容包含：发现摘要、证据、关联知识的 [[链接]]

5. **建立双向链接**
   - 找到 wiki/ 中与洞见主题相关的已有页面
   - 在已有页面的 relates_to 中添加指向新洞见页面的链接
   - 在洞见页面的 relates_to 中添加指向已有页面的链接

6. **更新 index.md 和 log.md**
   - index.md: 在 "QA 洞见" 分类下添加新条目
   - log.md: `## [YYYY-MM-DD] qa-import | 文件名 → N 个洞见`
