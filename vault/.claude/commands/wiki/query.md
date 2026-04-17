# wiki:query

基于知识库回答问题，使用统一搜索（BM25 + maps 主题扩展 + 图谱遍历）增强检索，将问答记录写入 raw/qa/ 供后续 qa-import。

## 输入

$ARGUMENTS — 要回答的问题。

## 流程

1. **查询改写**
   - 分析 `$ARGUMENTS`，提取核心关键词，生成优化后的搜索查询 `REWRITTEN_QUERY`
   - 改写规则：
     - 去除疑问词和语气助词（什么、如何、为什么、怎么、吗、呢、是否）
     - 展开缩写和别名（如 "RAG" → "RAG 检索增强生成"，"CE" → "CE Context-Engineering"）
     - 如果问题涉及 X 与 Y 的关系，确保两个术语都出现在查询中
     - 保留原始核心术语，追加同义词/扩展词
   - 示例：`"什么是Context Engineering？"` → `"Context-Engineering 上下文工程"`

2. **主题扩展**（利用 maps 系统）
   - 读取 `.claude/topic-to-wiki.json`（若存在）
   - 将 `REWRITTEN_QUERY` 的核心关键词与每个 topic 名和其页面列表做字符串匹配
   - 若找到匹配 topic → 读取 `maps/{MATCHED_TOPIC}.md` 获取该主题的页面清单和概述，作为后续搜索的优先上下文
   - 若未找到匹配 → 继续，不强制扩展

3. **统一搜索**
   - 执行：`Bash: bash scripts/wiki.sh search_wiki "REWRITTEN_QUERY" --top 15 --json`
   - 解析 JSON 结果，获取按相关度排序的页面列表
   - 注意 `sources` 字段 — 多来源命中的页面更可信

4. **读取相关页面**
   - 若步骤 2 找到 `MATCHED_TOPIC`：优先读取 `TOPIC_PAGES` 中相关度最高的页面（最多 8 个），再补充 BM25 结果中未覆盖的页面
   - 若未匹配主题：直接读取 BM25 top 结果（最多 10 个）
   - 注意 confidence 值——低置信度的信息标注 "（置信度较低）"

5. **综合回答**
   - 用中文回答
   - 引用来源页面：`来源：[[页面名]]`
   - 如果找到 `MATCHED_TOPIC`，回答末尾注明：`主题扩展：[[maps/{MATCHED_TOPIC}]]`
   - 如果信息不足，明确说明哪些方面缺少数据

6. **结晶化判断**
   - 如果回答综合了 3+ 个页面的信息，且形成了新的洞见：
     - 在 `wiki/syntheses/` 创建新页面保存这个分析
     - 更新 index.md：`Bash: bash scripts/wiki.sh snapshot_index --update`
     - 追加 log.md

7. **写入 QA 记录**
   - 将问答写入 `raw/qa/qa-YYYYMMDD-HHMMSS.md`（使用 Write 工具）
   - 文件格式：
     ```markdown
     ---
     type: qa
     question: "原始问题"
     date: "YYYY-MM-DD"
     citations: ["页面名1", "页面名2"]
     ---

     ## 问题

     <原始问题>

     ## 回答

     <完整回答，包含引用>
     ```
   - 注意：每次 query 创建独立文件，文件名包含时间戳，避免冲突

8. **更新 QA 快照**
   - 追加新文件到 `raw/qa/qa.snapshot.md`（如果不存在则创建）
   - 追加格式：`- [ ] qa-YYYYMMDD-HHMMSS.md — 主题关键词`

9. **更新 last_accessed**
   - 更新所有被引用页面的 `last_accessed` 字段为今天日期
