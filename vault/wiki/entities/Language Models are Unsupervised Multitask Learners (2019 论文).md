---
type: entity
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [paper, NLP, GPT, AI工程]
aliases: [Radford et al. 2019, GPT-2 论文]
relates_to:
  - target: Alec Radford
    relation: authored_by
  - target: GPT 系列
    relation: extends
  - target: 零样本学习
    relation: demonstrated
supersedes: null
---

# Language Models are Unsupervised Multitask Learners (2019 论文)

## 概述
GPT-2 论文，展示大规模[[Language-Model|语言模型]]具备[[零样本学习]]能力，可以在未见过的任务上泛化。

## 关键内容

1. **[[零样本学习]]**：GPT-2 在 15 亿参数规模下，无需微调即可通过自然语言提示完成翻译、问答、摘要等任务。
2. **模型规模**：相比 GPT-1 的 1.17 亿参数，GPT-2 扩大到 15 亿，展示了规模扩展对能力的显著影响。
3. **安全考量**：[[OpenAI]] 因担心滥用风险，最初未完全开源 GPT-2，引发 AI 安全讨论。

## 来源
- [[ai_papers_timeline.md]] — 2019 年时间线条目

## 相关
- [[Alec Radford]] — authored_by
- [[GPT 系列]] — extends
- [[零样本学习]] — demonstrated
