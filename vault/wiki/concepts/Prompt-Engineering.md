---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [ai-engineering, prompt-engineering, llm, AI工程]
aliases: ["提示词工程", "Prompt Engineering"]
relates_to: 
  - target: "[[GPT-3]]"
    type: enabled_by
    confidence: 0.8
  - target: "[[InstructGPT]]"
    type: popularized_by
    confidence: 0.8
  - target: "[[ChatGPT]]"
    type: popularized_by
    confidence: 0.9
  - target: "[[In-Context-Learning]]"
    type: extends
    confidence: 0.8
  - target: "[[Chain-of-Thought]]"
    type: implements
    confidence: 0.8
supersedes: null
---

# Prompt Engineering

## 概述
[[Prompt Engineering]] 是通过精心设计自然语言指令，最大化 LLM 单次/多次调用的输出质量的方法论体系。它是 LLM 工程化的第一个可操作[[规范化理论|范式]]。

## 关键内容

1. **定义与核心工作**：
   - [[Prompt Engineering]] 是对 LLM 输入端的精细化设计艺术，核心工作包括指令设计、示例工程、[[Chain-of-Thought|思维链]]诱导、格式控制和负向指令。

2. **技术发展史**：
   - **2020年**: [[GPT-3]] 首次展示"few-shot learning"，证明 LLM 能从示例中推断任务意图
   - **2022年**: [[InstructGPT]] RLHF 对齐训练使模型真正服从自然语言指令
   - **2022年11月**: [[ChatGPT]] 普及，让数百万人首次感知到"怎么问"影响"怎么答"

3. **核心技术模式**：
   - **[[CO-STAR-Framework|CO-STAR 框架]]**: Context, Objective, Style, Tone, Audience, Response
   - **[[Chain-of-Thought]] (CoT)**: 诱导模型逐步推理，显著提升复杂推理准确率
   - **Few-Shot 示例设计**: 通常 3-8 个示例效果最优
   - **角色扮演 (Role Prompting)**: 激活模型特定知识域的权重激活模式
   - **结构化输出控制**: 通过 XML 或 JSON 格式约束输出
   - **[[Meta-Prompting|元提示]] ([[Meta-Prompting]])**: 先生成最佳提示词，再用它来回答问题

4. **高级技术**：
   - **[[Self-Consistency]]**: 多次采样取多数答案，适用于数学/逻辑推理
   - **[[Tree-of-Thought]]**: 树形搜索推理路径，适用于复杂规划问题
   - **[[ReAct]]**: 交错 Reasoning + Acting，适用于工具调用
   - **[[Least-to-Most]]**: 分解子问题递进解决，适用于复杂分步任务
   - **[[Generated-Knowledge|Generated Knowledge]]**: 先生成背景知识再回答，适用于知识密集型任务

5. **局限性与挑战**：
   - [[上下文窗口]]瓶颈、幻觉问题、不稳定性
   - [[可维护性]]差、跨模型不可移植
   - 知识截止问题、复杂任务天花板

## 来源
- [[ai-engineering--01_prompt_engineering]] — 第一阶段：Prompt Engineering（提示词工程）
- [[GPT-3]] — 技术起源参考

## 相关
- [[GPT-3]] — enabled_by
- [[InstructGPT]] — popularized_by
- [[ChatGPT]] — popularized_by
- [[CO-STAR-Framework]] — implements
- [[Meta-Prompting]] — implements
- [[In-Context-Learning]] — extends
- [[Chain-of-Thought]] — implements