---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: [LLM, 工具调用, 代码执行, 统一动作, AI工程]
aliases: ["Executable Code Actions Elicit Better LLM Agents"]
relates_to: []
supersedes: null
---

# CodeAct

## 概述
CodeAct是由Wang等人提出的概念，主张使用可执行的[[Python]]代码作为LLM代理动作的统一表示形式，以替代传统的结构化JSON或自然语言动作。该方法在15/17任务上表现最优，平均提升20%以上。

## 关键内容

1. **核心理念**：
   - [[Python]]代码是最优的动作格式，相比JSON和自然语言具有更强的表达力、可执行性和可组合性
   - 代码原生支持状态传递、条件分支、循环和函数组合

2. **技术优势**：
   - **表达力**：[[Python]] > JSON > 自然语言
   - **可执行性**：[[Python]] = JSON > 自然语言
   - **可组合性**：[[Python]] >> JSON >> 自然语言
   - **状态传递**：直接引用中间结果，无需特殊变量绑定机制

3. **实验验证**：
   - 在17个多样化任务上比较了Text、JSON和CodeAct三种动作格式
   - CodeAct在15/17任务上表现最优，显著优于其他方法
   - 关键优势在于中间结果的直接引用和复杂的控制流表达

4. **工程意义**：
   - 现代.skill文件倾向于包含可执行代码模板
   - 代码模板让代理可以直接组合和执行[[Skills|技能]]，无需中间解析层
   - 为"代码即[[Skills|技能]]"的统一[[规范化理论|范式]]提供了理论支撑

## 来源
- [[llm-skill-research-series.md]] — LLM Skill研究系列
- [[Paper]] — "Executable Code Actions Elicit Better LLM Agents", ICML 2024

## 相关
- [[LLM-Skill-技术全景]] — relates_to
- [[Tool-Use]] — relates_to
- [[Code-as-Action]] — relates_to
- [[Unified-Action-Space]] — relates_to
- [[Python-Execution]] — relates_to