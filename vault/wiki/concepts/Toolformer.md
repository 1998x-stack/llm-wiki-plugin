---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [LLM, 工具调用, 自监督学习]
aliases: ["Toolformer: Language Models Can Teach Themselves to Use Tools"]
relates_to: []
supersedes: null
---

# Toolformer

## 概述
Toolformer是由Schick等人提出的模型，能够自学使用工具的[[Language-Model|语言模型]]。其核心创新是让模型自己生成工具调用[[标注]]，从而减少人工[[标注]]数据的需求，通过自监督学习掌握何时以及如何使用工具。

## 关键内容

1. **核心动机**：
   - [[标注]]"何时调用工具、调用参数是什么"的数据成本极高
   - 提出让模型自己生成工具调用[[标注]]，实现自监督学习工具使用

2. **技术方法**：
   - Step 1：生成候选[[标注]]：用few-shot prompt让模型在合适位置插入API调用
   - Step 2：过滤有效[[标注]]：[[计算]]插入工具调用后后续token的预测损失是否降低
   - Step 3：微调模型：用过滤后的[[标注]]数据微调模型，使其学会工具调用

3. **支持的工具类型**：
   - Calculator(expr)：数学[[计算]]
   - WikiSearch(query)：百科检索
   - MT(text, lang)：机器翻译
   - Calendar()：日期查询
   - QA(question)：问答

4. **关键贡献**：
   - 首次证明模型可以自学工具调用
   - 提出了基于损失减少的工具有效性评估标准
   - 在GPT-J 6.7B上超越了更大参数量的[[GPT-3]]在某些任务上的表现

## 来源
- [[llm-skill-research-series.md]] — LLM Skill研究系列
- [[Paper]] — "Toolformer: Language Models Can Teach Themselves to Use Tools", NeurIPS 2023

## 相关
- [[LLM-Skill-技术全景]] — relates_to
- [[Self-Taught-Tools]] — relates_to
- [[ReAct]] — relates_to
- [[Tool-Use]] — relates_to
- [[Self-Supervised-Learning]] — relates_to