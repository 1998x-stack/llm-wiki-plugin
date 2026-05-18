---
type: concept
status: active
confidence: 0.75
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["agent-architecture", "context-management", "mental-model", "Agent系统"]
aliases: ["Workspace vs Long-term Memory", "工作台与长期记忆", "Context Window as Working Memory", "文件系统作为长期记忆"]
relates_to:
  - target: "[[Ralph Loop]]"
    type: implements
  - target: "[[Context Engineering]]"
    type: part_of
  - target: "[[Session 交接机制]]"
    type: enables
  - target: "[[上下文窗口]]"
    type: relates_to
  - target: "[[LLM-Statelessness]]"
    type: extends
supersedes: null
---

# 工作台 vs 长期记忆

## 概述
一种 AI [[Agent 架构与设计原则|Agent 架构]]心智模型：将[[上下文窗口]]视为用完即扔的临时工作台（[[工作记忆|Working Memory]]），将文件系统视为永久存储的长期记忆（Persistent Memory），每次迭代使用全新的[[上下文窗口]]，从文件读取状态继续工作。

## 关键内容

1. **核心隐喻**：
   ```
   上下文窗口的本质：工作台（working memory）
   文件系统的本质：  长期记忆（persistent memory）

   Ralph 的核心原则：
     工作台用完就扔，换一张新的
     所有重要东西只放在文件系统里
   ```
   这一模型由 [[Geoffrey Huntley]] 在 Ralph Wiggum 技术中提出，是 [[Ralph Loop]] 系统的架构基石。

2. **与 [[LLM-Statelessness|LLM 无状态性]]的关系**：LLM 本质上是无状态的——每次推理调用都是独立的，不保留任何历史。"工作台 vs 长期记忆"模型正视这一本质，而非试图通过技巧让 Agent"记住"之前的对话。所有需要跨迭代保留的信息都必须写入文件。

3. **工作台（[[上下文窗口]]）的特征**：
   - **容量有限**：受限于模型的 context window（如 200k tokens）
   - **高速访问**：Agent 可以直接"看到"上下文中的所有内容
   - **用完即弃**：每次迭代结束后整个工作台被清空
   - **不适合持久化**：依赖上下文记忆会导致信息丢失和[[上下文腐烂]]

4. **长期记忆（文件系统）的特征**：
   - **容量无限**：文件系统大小仅受磁盘限制
   - **持久化**：写入后永久保留，跨会话、跨 Agent 实例共享
   - **[[渐进式披露（Progressive Disclosure）|按需加载]]**：新 Agent 通过读取特定文件获取所需信息
   - **可审计**：所有状态变更都有文件记录，可追溯

5. **在 [[Ralph Loop]] 中的实现**：
   - **prd.json**：任务清单——"要做什么"的权威源
   - **progress.txt**：交班日记——"做了什么"的操作日志
   - **[[项目约定手册|AGENTS.md]]**：经验手册——"学到了什么"的知识积累
   - **Git 历史**：代码变更——"怎么做的"的完整记录

6. **与 [[Context Engineering]] 的关系**：这一模型是[[Context Engineering|上下文工程]]的一种极端实践——**完全外部化状态**。不同于分层记忆或按需检索策略，它选择将所有状态写入文件，每次从零开始重建上下文。这种设计的代价是每次迭代需要重新读取文件，但收益是完全免疫[[上下文腐烂]]和[[上下文焦虑]]。

7. **设计权衡**：
   - **优势**：简单、可靠、可审计、不受[[上下文窗口]]限制
   - **代价**：每次迭代有文件读取开销，Agent 需要重新"理解"项目状态
   - **适用场景**：长时自主编码任务、跨多天的开发项目、需要严格进度追踪的场景

## 来源
- [[raw/articles/ai-tools/ralph-loop/SKILL.md]] — Ralph Loop Skill 核心哲学章节

## 相关
- [[Ralph Loop]] — implements（Ralph Loop 系统的架构基石）
- [[Context Engineering]] — part_of（上下文外部化的极端实践）
- [[Session 交接机制]] — enables（三文件架构是长期记忆的具体实现）
- [[上下文窗口]] — relates_to（上下文窗口作为工作台的本质理解）
- [[LLM-Statelessness]] — extends（正视 LLM 无状态性的架构设计）
- [[Geoffrey Huntley]] — relates_to（原创提出者）
