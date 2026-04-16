---
type: entity
entity_type: project
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, LLM, 指令调优, 微信]
aliases: [InstructRec]
relates_to:
  - {target: P5 论文, type: extends}
  - {target: 指令调优, type: implements}
  - {target: 生成式 LLM 推荐, type: part_of}
  - {target: 生成式推荐 (LLM), type: extends}
supersedes: null
---

# InstructRec

## 概述
微信团队提出的基于[[指令调优]]的推荐方法，借鉴 [[P5 论文|P5]] 的任务统一思想，用指令格式替代 Prompt 模板。

## 关键内容

1. **核心思想**：借鉴 [[P5 论文]] 的任务统一思想，但将固定 Prompt 模板升级为更灵活的[[指令调优]]格式，使模型能够理解更复杂的推荐指令。

2. **与 [[P5 论文|P5]] 的区别**：[[P5 论文|P5]] 使用 47 个预定义的 Prompt 模板，InstructRec 使用自然语言指令，格式更灵活，覆盖更广的任务描述空间。

3. **技术特点**：
   - 使用[[指令调优]]训练 LLM 适配推荐场景
   - 支持多种推荐任务的统一处理
   - 更强的 zero-shot/few-shot 泛化能力

4. **团队背景**：由微信团队提出，代表了工业界对 LLM 推荐方向的探索。

5. **在 LLM 推荐谱系中的位置**：属于[[生成式 LLM 推荐]]范式，与 [[TALLRec]]、[[LC-Rec]]、[[LLMRec]] 等工作共同推动了从 [[P5 论文|P5]] 到现代 LLM 推荐的演进。

## 来源
- InstructRec 论文 — Instruction Tuning for Recommendation
- Shijie Geng et al. — P5: Recommendation as Language Processing, RecSys 2022

## 相关
- [[P5 论文]] — InstructRec 的思想来源
- [[指令调优]] — InstructRec 的核心技术
- [[生成式 LLM 推荐]] — InstructRec 所属范式
- [[生成式推荐 (LLM)]] — InstructRec 的范式基础
- [[TALLRec]] — 同期的指令调优推荐工作
- [[LC-Rec]] — 同期的 LLM 推荐工作
- [[LLMRec]] — 同期的 LLM 推荐工作
