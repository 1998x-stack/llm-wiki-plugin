---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tool, virtual-team, claude-code]
aliases: [gstack, Garry Tan's gstack]
entity_type: project
relates_to: 
  - target: "[[Garry Tan]]"
    type: implements
  - target: "[[Claude Code]]"
    type: extension_for
  - target: "[[Superpowers]]"
    type: compares_to
  - target: "[[Compound Engineering]]"
    type: compares_to
supersedes: null
---

# gstack

## 概述
[[Garry Tan]]开发的虚拟工程团队工具包，通过角色分工和认知切换来提升[[Claude Code]]的输出质量。

## 关键内容
1. **核心理念**：gstack认为[[Claude Code]]的问题是"认知角色混淆"，同一个Agent既要当CEO又要当QA，输出质量不稳定，因此提出强制认知分工，每次只扮演一个角色。

2. **主要功能**：
   - /office-hours：像YC partner一样对话，澄清产品方向
   - /autoplan：CEO + Design + Eng三重审查计划
   - /review：工程审查（必选[[门控机制（Gating Mechanism）|门控]]）
   - /qa：浏览器测试
   - /ship：同步主干 + 测试 + 开PR
   - /retro：团队复盘

3. **技术特点**：
   - 实现技术：Markdown + Bash脚本
   - 触发机制：用户手动/命令
   - Agent数量：23个工具（非独立Agent）
   - 支持平台：8+

4. **知识持久化**：通过~/.gstack/projects/{project}/learnings/目录管理系统学习

5. **适用场景**：创始人/技术CEO、独立开发者、全栈工程师等需要跨越多维度思考的用户。

## 来源
- [[claude-code-tools-comparison]] — 分析时间：2026年4月

## 相关
- [[Garry Tan]] — implements
- [[Superpowers]] — compares_to
- [[Compound Engineering]] — compares_to
- [[Claude Code]] — extension_for