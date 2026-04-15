# wiki:query

基于知识库回答问题，使用统一搜索（BM25 + maps 主题扩展 + 图谱遍历）增强检索，将问答记录写入本地文件。

## 输入

$ARGUMENTS — 要回答的问题。

## 流程

1. **统一搜索**
   - 执行：`Bash: python3 scripts/search_wiki.py "$ARGUMENTS" --top 15 --json`
   - 解析 JSON 结果，获取按相关度排序的页面列表
   - 注意 `topic_context` 字段 — 如果匹配到主题，优先深读该主题下的页面
   - 注意 `sources` 字段 — 多来源命中的页面更可信

2. **读取相关页面**
   - 读取所有找到的相关页面的完整内容
   - 注意 confidence 值——低置信度的信息标注 "（置信度较低）"

4. **综合回答**
   - 用中文回答
   - 引用来源页面：`来源：[[页面名]]`
   - 如果信息不足，明确说明哪些方面缺少数据

5. **结晶化判断**
   - 如果回答综合了 3+ 个页面的信息，且形成了新的洞见：
     - 在 `wiki/syntheses/` 创建新页面保存这个分析
     - 更新 index.md
     - 追加 log.md

6. **写入 QA 记录**
   - 将问答写入 `qa/YYYY-MM-DD.md`（使用 Write 工具）
   - 如果文件不存在，先创建文件头：
     ```markdown
     ---
     type: qa-log
     date: YYYY-MM-DD
     ---

     # QA Log — YYYY-MM-DD
     ```
   - 追加本次问答（使用 Edit 工具 append 到文件末尾）：
     ```markdown
     ---

     ## Prompt

     <原始问题>

     ## Response

     <完整回答，包含引用>

     ---
     ```

7. **更新 last_accessed**
   - 更新所有被引用页面的 `last_accessed` 字段为今天日期
