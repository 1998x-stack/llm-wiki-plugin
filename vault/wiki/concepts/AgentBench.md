---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [LLM, 代理评估, 综合能力, AI工程]
aliases: ["AgentBench: Evaluating LLMs as Agents"]
relates_to: []
supersedes: null
---

# AgentBench

## 概述
AgentBench是由Liu等人提出的LLM代理能力全面评估基准，在8个不同环境中测试代理能力。它揭示了GPT-4等顶级模型与其他模型之间的显著能力断层。

## 关键内容

1. **八大测试环境**：
   - OS（[[操作系统]]操作）：Bash命令、文件管理
   - DB（数据库）：SQL查询、数据操作
   - KG（知识图谱）：SPARQL、推理
   - 数字卡牌游戏：规则理解、策略规划
   - 横向思维谜题：创意推理
   - 家务模拟：多步骤物理规划
   - 网购：搜索、比较、决策
   - 网页浏览：DOM操作、信息提取

2. **关键发现**：
   - GPT-4总分约为第二名的2倍（存在显著能力断层）
   - 开源模型在"需要多步规划的环境"（OS、DB）上远落后于GPT-4
   - 工具调用的稳定性（格式正确率）是[[区分]]模型的关键指标

3. **评估维度**：
   - 任务规划能力
   - 工具调用能力
   - 环境交互能力
   - 长期记忆能力

## 来源
- [[llm-skill-research-series.md]] — LLM Skill研究系列
- [[Paper]] — "AgentBench: Evaluating LLMs as Agents", ICLR 2024

## 相关
- [[LLM-Skill-技术全景]] — relates_to
- [[Agent-Evaluation]] — relates_to
- [[Multi-Environment-Testing]] — relates_to
- [[Tool-Stability]] — relates_to