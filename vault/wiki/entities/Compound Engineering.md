---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tool, knowledge-compounding, claude-code]
aliases: [Compound Engineering, EveryInc/compound-engineering-plugin]
entity_type: project
relates_to: 
  - target: "[[Kieran Klaassen]]"
    type: implements
  - target: "[[Claude]]"
    type: implements_with
  - target: "[[Claude Code]]"
    type: extension_for
  - target: "[[gstack]]"
    type: compares_to
  - target: "[[Superpowers]]"
    type: compares_to
  - target: "[[Knowledge Compounding]]"
    type: core_concept
supersedes: null
---

# Compound Engineering

## 概述
[[Kieran Klaassen]]和[[Claude_Code|Claude]]共同开发的[[知识复利飞轮]]工具，通过积累效应让系统越用越强。

## 关键内容
1. **核心理念**：Compound Engineering认为[[Claude Code]]的问题是"知识无法积累"，每次会话从零开始，无法从过去的错误中学习，因此构建知识积累飞轮，让系统越用越强。

2. **主要功能**：
   - /ce:ideate：发现高价值机会
   - /ce:brainstorm：逐一提问澄清需求
   - /ce:plan：3 Agent并行研究+置信度[[门控机制（Gating Mechanism）|门控]]
   - /ce:work：Git worktree隔离+分阶段执行
   - /ce:review：14+ Agent并行审查+去重合并
   - /ce:compound：将学习结晶化，下次计划自动引用过去方案

3. **技术特点**：
   - 实现技术：Markdown + YAML
   - 触发机制：用户手动/命令
   - Agent数量：35+专业Agent
   - 并行度：极高（14+同时审查）
   - 知识积累：显式飞轮（/ce:compound）

4. **独特优势**：
   - 置信度[[门控机制（Gating Mechanism）|门控]]系统
   - 去重管道（Dedup Pipeline）
   - /deepen-plan超级研究模式（40+个并行研究Agent）
   - 文档审查Agent（7个）
   - 显式知识积累飞轮

5. **适用场景**：长期运营的产品、小团队多产品、Rails/Ruby技术栈、重视知识管理的组织等。

## 来源
- [[claude-code-tools-comparison]] — 分析时间：2026年4月

## 相关
- [[Kieran Klaassen]] — implements
- [[Claude]] — implements_with
- [[gstack]] — compares_to
- [[Superpowers]] — compares_to
- [[Knowledge Compounding]] — core_concept
- [[Claude Code]] — extension_for