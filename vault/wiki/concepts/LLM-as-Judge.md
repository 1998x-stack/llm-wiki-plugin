---
type: concept
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 3
tags: [AI, 评估, LLM, 测试, 机器学习, AI工程, 评分器]
aliases: [LLM评判器, LLM Judge, LLM as Judge]
relates_to:
  - target: "[[DeepAgents评估体系]]"
    type: related_to
    note: DeepAgents 通过 LLMJudge 将其接入 SuccessAssertion 体系
    confidence: 0.9
  - target: "[[Agent 评测体系]]"
    type: part_of
  - target: "[[评测驱动开发]]"
    type: uses
  - target: "[[评分器设计]]"
    type: implements
supersedes: null
---

# LLM-as-Judge

## 概述

使用 LLM 作为自动评判器（Judge），对 AI 系统的输出按预定义**准则**打分，代替人工评估。适用于难以用规则/子串匹配表达的**语义正确性、风格、完整性、多条件综合**等评估目标。核心假设：强模型（如 Claude Sonnet）对人类语言理解足够准确，其判断可近似替代人工标注。

## 关键内容

### 适用场景

| 方式 | 适用 | 优点 | 注意 |
|------|------|------|------|
| **确定性断言**（子串/文件相等） | 事实性短答案、精确固定短语 | 成本低、可复现、无模型方差 | 无法覆盖语义等价表述 |
| **LLM-as-Judge** | 语义正确性、语气风格、推理完整性、多条件组合 | 灵活，接近人类验收标准 | 成本/延迟更高；需固定 judge 模型以便横向对比 |

### 工作原理

1. 将 Agent 输出（或完整轨迹）序列化
2. 对每条评判**准则**单独调用 LLM：`evaluator(outputs=..., criterion=...)`
3. LLM 返回 `{"score": ..., "comment": ...}`
4. **所有**准则 score 为真 → 评判通过

### 最佳实践

- **能用确定性断言处不用 Judge**（节省成本和方差）
- 每条准则应**单条可判定**、无歧义，不在一条内堆砌多个要求
- 准则涉及工具调用行为（如"必须调用 `edit_file`"）时，需将完整轨迹送入评判上下文（[[DeepAgents]] 中用 `include_tool_calls=True`）
- 固定 `judge_model` 版本，保证跨次运行可横向对比
- **给 LLM 评分器"退路"**：当信息不足时允许返回 "Unknown"
- **为每个评测维度创建独立的 LLM-as-judge**（而非一个模型评测所有维度）
- 使用清晰的结构化评分标准（Rubric），而非模糊指令
- **定期与人类专家进行校准验证**以确保评分一致性

### DeepAgents 实现（`LLMJudge`）

- 继承 `SuccessAssertion`，接入 `TrajectoryScorer.success()` 作为硬性失败断言
- 依赖 `openevals` 库的 `create_llm_as_judge`
- 默认 judge 模型：`claude-sonnet-4-6`
- `include_tool_calls=True` 时将 `trajectory.pretty()`（含工具名/参数）送入提示
- 评分结果写入 LangSmith（键 `llm_judge_all_passed`），可在 UI 过滤分析
- 内部缓存 `_last_results`，避免 `check()` 与 `describe_failure()` 重复计费

```python
scorer = TrajectoryScorer().success(
    llm_judge(
        "答案正确提到了巴黎是法国首都",
        "语气自然，非机器人式",
        include_tool_calls=False,
    )
)
```

### 局限性

- LLM 本身存在随机性，相同输入可能得到不同判断（需固定模型+温度）
- Judge 模型的偏好可能与人类评估者不一致（存在 judge 偏见）
- 成本与延迟显著高于确定性断言，不适合高频/大规模运行

## 来源
- [[raw/books/deepagents-book-main/21-LLM-as-Judge评估模式.md]]
- [[05_multi_agent_research]] — 第四节：评估体系（LLM-as-Judge 的最佳实践）
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/12_demystifying_evals.md]] — 基于模型的评分器章节

### Anthropic Research 系统的 LLM-as-Judge 实践
- 单次 LLM 调用 + 单一 prompt 输出 0.0-1.0 评分 + 通过/失败等级
- 比多评判器方案**更一致**，且与人工判断更对齐
- 评估维度：事实准确性、引用准确性、完整性、信源质量、工具效率

## 相关
- [[DeepAgents评估体系]]
- [[DeepAgents]]
