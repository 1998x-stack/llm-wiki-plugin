---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tool, methodological-discipline, claude-code]
aliases: [Superpowers, obra/superpowers]
entity_type: project
relates_to: 
  - target: "[[Jesse Vincent]]"
    type: implements
  - target: "[[Claude Code]]"
    type: extension_for
  - target: "[[gstack]]"
    type: compares_to
  - target: "[[Compound Engineering]]"
    type: compares_to
  - target: "[[TDD]]"
    type: implements_methodology
supersedes: null
---

# Superpowers

## 概述
[[Jesse Vincent]]开发的方法论强制执行工具，通过纪律约束和TDD强制来提升[[Claude Code]]的代码质量。

## 关键内容
1. **核心理念**：Superpowers认为[[Claude Code]]的问题是"缺乏纪律"，AI有能力但跳过测试、忽略边界情况、草率实现，因此提出强制执行严格的方法论，不能跳步。

2. **主要功能**：
   - Brainstorm：苏格拉底式对话，挖掘真实需求
   - Spec：可供用户审读的规格说明（分块展示）
   - Plan：微任务分解（2-5分钟每任务）
   - TDD：写测试→确认测试失败→写实现（不可跳过）
   - Subagent：多Agent并行执行任务列表
   - Review：[[代码审查]]员Agent
   - Finalize：验收+文档更新

3. **技术特点**：
   - 实现技术：Markdown + Node.js脚本
   - 触发机制：自动触发（Session Hook）
   - Agent数量：多个子Agent（规模较小）
   - 并行度：高（子Agent并行）

4. **强制机制**：
   - [[TDD强制执行]]：检测到代码写在测试前→删除代码，重新开始
   - 自动触发的会话Hook，不需要任何命令

5. **适用场景**：想要TDD纪律的团队、中型复杂项目、质量优先的产品等。

## 来源
- [[claude-code-tools-comparison]] — 分析时间：2026年4月

## 相关
- [[Jesse Vincent]] — implements
- [[gstack]] — compares_to
- [[Compound Engineering]] — compares_to
- [[TDD]] — implements_methodology
- [[Claude Code]] — extension_for