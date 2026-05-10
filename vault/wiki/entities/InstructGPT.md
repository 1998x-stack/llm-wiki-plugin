---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [ai-model, language-model, openai, alignment]
aliases: ["InstructGPT", "Instruction Following GPT"]
relates_to: 
  - target: "[[Language-Model]]"
    type: part_of
    confidence: 0.9
  - target: "[[OpenAI]]"
    type: created_by
    confidence: 0.9
  - target: "[[GPT-3]]"
    type: extends
    confidence: 0.8
  - target: "[[ChatGPT]]"
    type: predecessor
    confidence: 0.9
  - target: "[[Prompt-Engineering]]"
    type: enabled
    confidence: 0.9
entity_type: project
supersedes: null
---

# InstructGPT

## 概述
InstructGPT 是 [[OpenAI]] 在2022年推出的一种[[Language-Model|语言模型]]训练方法，通过对 [[GPT-3]] 进行人类反馈[[强化学习]](RLHF)进行对齐训练，使模型更好地遵循人类指令。

## 关键内容

1. **技术创新**：
   - 采用RLHF（[[RLHF|Reinforcement Learning from Human Feedback]]）技术
   - 通过人类偏好数据训练[[奖励模型]]，再使用该[[奖励模型]]进行策略优化
   - 显著提升了模型的指令跟随能力、真实性和无害性

2. **历史意义**：
   - 2022年的RLHF对齐训练标志着模型真正开始服从自然语言指令
   - 使Prompt开始具有"可重复"的效果，为[[Prompt Engineering]]的发展奠定基础
   - 作为[[ChatGPT]]的技术前身，展示了对齐训练对实用AI系统的重要性

3. **技术影响**：
   - 验证了通过人类反馈改进模型行为的可行性
   - 为后续所有基于大模型的应用提供了可重复、可预测的交互[[规范化理论|范式]]
   - 推动了AI对齐(AI Alignment)研究领域的发展

## 来源
- [[ai-engineering--01_prompt_engineering]] — 技术土壤部分提及
- [[GPT-3]] — 基于GPT-3的技术改进

## 相关
- [[GPT-3]] — extends
- [[ChatGPT]] — predecessor
- [[Prompt-Engineering]] — enabled
- [[OpenAI]] — created_by