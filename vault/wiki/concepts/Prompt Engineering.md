---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: ["AI Engineering", "Prompt Engineering", LLM, AI工程]
aliases: ["提示工程", "Prompt Engineering"]
relates_to:
  - {target: Context Engineering, type: supersedes, confidence: 0.9}
  - {target: LLM, type: part_of, confidence: 0.8}
  - {target: Instruction Tuning, type: extends, confidence: 0.7}
  - {target: Chain-of-Thought, type: part_of, confidence: 0.8}
supersedes: null
---

# Prompt Engineering

## 概述
指导和优化大[[Language-Model|语言模型]]输出的技术实践，通过精心设计输入提示（Prompt）中的指令、上下文和示例，引导模型生成更准确、相关和有用的响应。在AI Agent工程中，Prompt Engineering是核心工程工作而非可选项，工具描述的质量直接影响模型行为和最终产品质量。

## 关键内容

1. **核心理念**：
   - 在[[Context Engineering]]兴起之前，关注如何让模型理解用户的指令
   - 重点在于"如何让模型更好地完成任务"
   - 主要关注提示的措辞、结构和格式
   - 在AI Agent工程中，Prompt Engineering不是可选项，而是核心工程工作

2. **关键技术**：
   - Zero-shot prompting：无示例情况下直接给出任务指令
   - Few-shot prompting：提供少量示例帮助模型理解任务模式
   - [[Chain-of-Thought]]：引导模型逐步推理，展示思考过程
   - [[指令调优|Instruction Tuning]]：优化指令格式以提高模型遵循性
   - [[Prompt Chaining]]：将复杂[[任务分解]]为多个简单步骤
   - Tool [[Descript]]ion Optimization：工具描述直接影响模型行为，质量等同于产品质量

3. **发展演变**：
   - 随着模型能力提升，从简单的指令式提示发展到复杂的多步骤提示
   - 在长[[上下文窗口]]出现前，受限于上下文长度，只能进行精简化的提示设计
   - 逐渐被[[Context Engineering]]所超越，后者关注整个[[上下文窗口]]的管理
   - 在AI Agent领域，Prompt作为最灵活的[[算法]]，自然语言描述的行为规范比代码实现的规则更灵活、更易维护

4. **工程应用**：
   - Prompt作为文档：[[Coordinator Mode]]的系统提示词既是代码（控制行为）又是文档（解释意图）
   - 架构决策：[[区分]]稳定（可缓存）和动态（不可缓存）部分以优化[[Prompt Cache]]
   - Agent行为控制：通过Prompt而非代码实现的规则来表达行为规范

## 来源
- AI-Agent--02_context_engineering — Context Engineering的前身概念
- [[Claude Code 源码泄露深度解析（八）]] — 工程实践中工具描述即产品的理念

## 相关
- [[Context Engineering]] — supersedes
- [[LLM]] — part_of
- [[Instruction Tuning]] — extends
- [[Chain-of-Thought]] — part_of
- [[Claude Code 工程设计哲学]] — extends
- [[Prompt Cache]] — extends