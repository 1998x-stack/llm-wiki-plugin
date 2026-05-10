---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [knowledge-base, topic-organization, memory-storage]
aliases: [Topic Files, 主题文件, 按主题组织的知识库]
relates_to: 
  - target: "[[三层记忆架构]]"
    type: part_of
    confidence: 0.8
  - target: "[[MEMORY.md]]"
    type: relates_to
    confidence: 0.8
  - target: "[[Self-Healing Memory]]"
    type: relates_to
    confidence: 0.8
  - target: "[[Transcripts]]"
    type: relates_to
    confidence: 0.8
supersedes: null
---

# Topic Files

## 概述
Topic Files 是 [[Claude Code]] [[三层记忆架构]]的第二层，是存储实际项目知识的文件，按主题组织在 memory/topics/ 目录下。

## 关键内容

1. **存储特征**：
   - 存储实际的项目知识和详细信息
   - 按主题进行组织，如认证系统、数据库模式、API设计模式等
   - 文件位于 memory/topics/ 目录下

2. **访问方式**：
   - [[渐进式披露（Progressive Disclosure）|按需加载]]（On-Demand Fetch）：Agent 只在需要特定领域知识时才读取对应文件
   - 可以包含很详细的内容，没有严格的大小限制
   - 可以包含完整的代码示例、决策记录等详细信息

3. **维护方式**：
   - 由 Agent 自主维护：Agent 在工作过程中会主动更新这些文件
   - 与 [[MEMORY.md]] 索引配合使用，实现快速定位和加载

4. **典型主题**：
   - auth-system.md：认证系统的所有知识
   - db-schema.md：数据库模式文档
   - api-patterns.md：API 设计模式
   - known-issues.md：已知问题和临时方案
   - user-preferences.md：用户偏好[[Settings|设置]]
   - deployment.md：部署相关知识

## 来源
- [[raw/articles/ai-tools/claude-code/03_memory_architecture.md]] — Claude Code 源码泄露深度解析（三）

## 相关
- [[三层记忆架构]] — part_of
- [[MEMORY.md]] — relates_to
- [[Self-Healing Memory]] — relates_to
- [[Transcripts]] — relates_to
