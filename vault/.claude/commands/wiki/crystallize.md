# wiki:crystallize

将当前会话的探索过程蒸馏为结构化摘要，写入 wiki 和记忆系统。

## 输入

$ARGUMENTS — 可选的会话主题描述。如果不提供，自动从当前对话上下文推断。

## 流程

1. **回顾当前会话**
   - 分析本次对话中讨论了什么
   - 识别关键发现、决策、洞见

2. **写入 Working Memory**
   - 创建 `_memory/working/YYYY-MM-DD-NN.md`（NN 为当天的序号）
   - frontmatter:
     ```yaml
     type: working-memory
     session: YYYY-MM-DD-NN
     created: YYYY-MM-DDTHH:MM:SS
     status: unprocessed
     observations: N
     ```
   - 列出本次会话的关键观察

3. **判断是否值得结晶**
   - 如果会话产生了新的综合洞见（连接了 3+ 个已有概念）：
     - 在 `wiki/syntheses/` 创建新页面
     - 更新相关页面的 relates_to
     - 更新 index.md

4. **强化已有知识**
   - 如果会话确认了已有 semantic memory 中的事实：
     - 更新对应 semantic memory 的 last_confirmed 和 confirmation_count
     - 重置衰减曲线

5. **记录**
   - 追加 log.md：`## [YYYY-MM-DD] crystallize | 会话主题`
