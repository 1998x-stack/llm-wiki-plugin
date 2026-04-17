---
type: entity
entity_type: project
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, LLM, LLaMA, 指令调优]
aliases: [TALLRec]
relates_to:
  - {target: P5 论文, type: extends}
  - {target: 指令调优, type: implements}
  - {target: 生成式 LLM 推荐, type: part_of}
  - {target: Zero-shot 推荐, type: extends}
supersedes: null
---

# TALLRec

## 概述
首个尝试用大语言模型 LLaMA 进行推荐任务微调的工作，使用[[指令调优]]使 LLaMA 适配推荐场景。

## 关键内容

1. **开创性贡献**：首个尝试用大语言模型（LLaMA）进行推荐任务微调的工作，标志着 LLM 推荐从 T5 时代（60M-223M 参数）进入 LLaMA 时代（7B+ 参数）。

2. **技术方法**：使用[[指令调优]]使 LLaMA 适配推荐场景，将推荐任务转化为自然语言指令格式，通过 LoRA 等参数高效微调方法进行训练。

3. **与 P5 的关系**：借鉴了 [[P5 论文]] 的任务统一思想，但用 LLaMA 替代 T5 作为骨干模型，用[[指令调优]]替代 Prompt 模板，代表了从 P5 到现代 LLM 推荐的关键演进。

4. **Zero-shot 能力**：通过[[指令调优]]，TALLRec 展示了强大的 zero-shot 推荐能力，能够遵循未见过的指令完成推荐任务。

5. **在 LLM 推荐谱系中的位置**：属于[[生成式 LLM 推荐]][[规范化理论|范式]]，与 [[InstructRec]]、[[LC-Rec]]、[[LLMRec]] 等工作共同推动了 LLM 推荐的发展。

## 来源
- TALLRec 论文 — LLaMA-based Recommendation with Instruction Tuning
- Shijie Geng et al. — P5: Recommendation as Language Processing, RecSys 2022

## 相关
- [[P5 论文]] — TALLRec 的思想来源
- [[指令调优]] — TALLRec 的核心技术
- [[生成式 LLM 推荐]] — TALLRec 所属范式
- [[Zero-shot 推荐]] — TALLRec 展示的能力
- [[InstructRec]] — 同期的指令调优推荐工作
- [[LC-Rec]] — 同期的 LLM 推荐工作
- [[LLMRec]] — 同期的 LLM 推荐工作
