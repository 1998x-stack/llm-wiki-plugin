---
type: concept
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 2
tags: [技术, AI, 方法论, AI工程]
aliases: ["Agent Evaluation", "Agent Evals", "Agent评估", "eval方法论", "LLM评估"]
relates_to:
  - target: "[[生成器-评估器架构]]"
    type: related_to
    confidence: 0.85
  - target: "[[LLM-as-Judge]]"
    type: uses
    confidence: 0.9
  - target: "[[Agent工作流模式]]"
    type: related_to
    confidence: 0.8
supersedes: null
---

# Agent 评估方法论

## 概述

[[Anthropic]] 从内部实践和客户协作中提炼的 Agent 系统评估（Eval）系统方法论：词汇体系、评分器类型、能力评估与回归评估、pass@k vs pass^k 非确定性指标、以及从零构建评估体系的路线图。

## 关键内容

### 核心词汇体系

| 术语 | 定义 |
|------|------|
| **任务（Task）** | 单个测试，含明确输入和成功标准 |
| **试次（Trial）** | 对任务的一次尝试；模型输出随机性需多次试次 |
| **评分器（Grader）** | 评分某方面性能的逻辑；一个任务可含多个评分器 |
| **记录（Transcript / Trace）** | 试次完整记录：输出、工具调用、推理、中间结果 |
| **结果（Outcome）** | 试次结束时环境的最终状态（与 Transcript 区别：agent 说"已预订"≠数据库中有预订记录）|
| **评估 Harness** | 端到端运行 eval 的基础设施 |
| **[[Agent Harness模式|Agent Harness]]（Scaffold）** | 使模型作为 Agent 运行的系统；评估的是 Harness + 模型的组合 |
| **评估套件（Eval Suite）** | 测试特定能力或行为的任务集合 |

### 三类评分器

**代码评分器（Code-based）**：
- 字符串匹配、正则、二值测试（fail-to-pass）
- 静态分析（lint、类型、安全）、结果验证、工具调用验证
- 优势：快速、客观、可复现、易调试
- 劣势：对有效变体脆弱，缺乏细微判断

**模型评分器（Model-based / [[LLM-as-Judge]]）**：
- 基于 Rubric 评分、自然语言断言、成对比较、多评判员共识
- 优势：灵活、可扩展、捕捉细微差别
- 劣势：不确定性、成本较高、需用人类标注校准
- 建议：为每个维度单独调用 LLM judge；给 LLM 提供"Unknown"逃生路线防止幻觉

**人类评分器（Human）**：
- 领域专家审查、众包判断、A/B 测试
- 优势：黄金标准质量，用于校准模型评分器
- 劣势：昂贵、慢、难以大规模

### 能力评估 vs. 回归评估

**能力评估（Capability Evals）**：
- 问"这个 Agent 能做什么？"
- 从低通过率开始，目标是有努力攀登的"山丘"
- 当 Agent 饱和（100% 通过）后，转化为回归套件

**回归评估（Regression Evals）**：
- 问"Agent 还能处理它过去处理的所有任务吗？"
- 应接近 100% 通过率，下降信号有问题
- **eval 饱和（Eval Saturation）**：通过率接近 100%，不再提供改进信号；需要更难的评估

### pass@k vs pass^k 指标

应对 Agent 行为非确定性的两个互补指标：

**pass@k**：k 次尝试中至少一次正确的概率
- k 增大 → pass@k 升高
- 适合"一次成功就行"的工具场景（代码生成）

**pass^k**：k 次尝试全部正确的概率
- k 增大 → pass^k 下降
- 适合"需要每次可靠"的面向用户场景（客服 Agent）

两者在 k=1 时相同；随 k 增大急剧分化——pass@k 趋向 100%，pass^k 趋向 0%。

### 从零到可信评估体系：8步路线图

**数据集构建阶段：**
1. **尽早开始**：20-50 个从真实失败中提取的任务即可启动，无需等待大规模套件
2. **从手动测试中转化**：将已有的手动检查、bug 报告、用户反馈转化为测试用例
3. **编写无歧义任务与参考解答**：两名领域专家能独立达成相同 pass/fail 判断；创建已知可通过的参考解答验证评分器
4. **构建平衡问题集**：同时测试"应该触发"和"不应该触发"的情况，避免单侧优化

**Harness 和评分器设计：**
5. **构建稳健的评估 Harness**：每次试次从干净环境出发；防止跨试次共享状态
6. **评分器设计**：优先使用确定性评分器；LLM judge 在必要时使用并用人类校准；支持部分分数；**评估轨迹而非具体路径**（Agent 可能发现有效的非预期解法）

**长期维护：**
7. **阅读 Transcript**：分辨是真正的错误还是评分器拒绝了有效解法；验证评估确实在测量重要指标
8. **监控饱和并持续贡献**：eval 套件是活的工件，需明确所有权和持续维护

### 不同 Agent 类型的评估策略

**编码 Agent**：确定性评分器（单元测试 pass/fail）是自然选择；可加 LLM Rubric 评估代码质量和交互方式

**对话 Agent**：多维成功（状态检查 + Transcript 约束 + LLM Rubric）；常需第二个 LLM 模拟用户

**研究 Agent**：接地性检查 + 覆盖度检查 + 来源质量检查；LLM judge 需频繁用专家人类判断校准

**计算机使用 Agent**：需要在真实或沙箱环境运行；URL/页面状态检查 + 后端状态验证（确认行动已实际发生）

### 评估与其他方法的关系（多层防御）

| 方法 | 主要优势 | 局限 |
|------|---------|------|
| 自动化 Evals | 快速迭代，可在 CI 中运行 | 需要维护，可能与真实使用模式脱节 |
| 生产监控 | 揭示真实用户行为 | 反应性，问题先到达用户 |
| A/B 测试 | 测量真实用户结果 | 慢，需要足够流量 |
| 用户反馈 | 发现未预料的问题 | 稀疏，偏向严重问题 |
| 手动 Transcript 审查 | 发现细微问题，建立直觉 | 不可扩展 |
| 系统性人类研究 | 黄金标准 | 昂贵、慢 |

类似安全工程中的"瑞士奶酪模型"：没有单一评估层能捕捉所有问题，多层组合使失误无处遁形。

## 来源

- [[raw/articles/ai-engineering/anthropic-engineering/Demystifying evals for AI agents.md]]
- [[raw/articles/ai-engineering/anthropic-engineering/Quantifying infrastructure noise in agentic coding evals.md]]

## 相关

- [[LLM-as-Judge]] — uses（模型评分器是三类评分器之一）
- [[生成器-评估器架构]] — related_to（评估者-优化者是 Agent 内嵌的在线评估机制）
- [[Agent工作流模式]] — related_to（不同工作流类型需要不同评估策略）
- [[Agent Harness模式]] — related_to（评估 Harness 是独立基础设施）
