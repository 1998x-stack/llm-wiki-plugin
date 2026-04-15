# wiki:query

基于知识库回答问题，使用 BM25 搜索增强检索，将问答记录写入本地文件。

## 输入

$ARGUMENTS — 要回答的问题。

## 流程

1. **BM25 搜索**
   - 执行：`Bash: python3 scripts/bm25_index.py query "$ARGUMENTS" -n 10`
   - 解析 JSON 结果，获取 top-10 相关页面路径和评分

2. **扩展搜索**
   - 读取 `index.md` 找到可能相关的页面（关键词匹配）
   - 读取 BM25 命中页面的 frontmatter，沿 relates_to 扩展搜索范围
   - 如果相关页面不够，用 Grep 在 wiki/ 中搜索关键词
   - 合并所有搜索结果（BM25 + index + relates_to + grep），去重

3. **读取相关页面**
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

7. **自动导入洞见**
   - 执行 wiki:qa-import 处理今天的 QA 文件：
     按 qa-import 命令的流程处理 `qa/YYYY-MM-DD.md`

8. **更新 last_accessed**
   - 更新所有被引用页面的 `last_accessed` 字段为今天日期
