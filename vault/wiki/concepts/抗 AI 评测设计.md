---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [evaluation, hiring, ai-era, technical-interview, AI工程]
aliases: ["AI-resistant evaluation", "抗 AI 评测", "抗 AI 技术评估"]
relates_to:
  - target: "[[评测通货膨胀]]"
    type: relates_to
  - target: "[[评测驱动开发]]"
    type: relates_to
  - target: "[[提示工程]]"
    type: relates_to
supersedes: null
---

# 抗 AI 评测设计

## 概述
在 AI 助手普及时代，设计能够真实评测候选人技术能力而非 AI 使用能力的评估方法论，强调理解深度、判断力和 AI 协作智慧。

## 关键内容

1. **设计背景**：
   - [[GitHub Copilot]]、[[Claude Code]] 等工具可在几秒内解决经典[[算法]]题
   - 传统评测（如 Leetcode）假设候选人独立解题的前提被打破
   - 导致"[[评测通货膨胀]]"——通过评测不再意味着具备目标能力

2. **AI 时代持久的核心能力**：
   - **问题诊断能力**：识别代码根本问题而非症状
   - **系统思维**：理解大规模系统权衡（延迟 vs 吞吐，一致性 vs 可用性）
   - **调试能力**：在 AI 生成代码出错时找到真正问题
   - **评估能力**：判断 AI 生成代码是否正确、高效、安全

3. **新兴关键能力**：
   - **AI 协作效率**：有效分解任务并与 AI 协作
   - **输出质量判断**：识别 AI 生成的错误或次优方案
   - **[[提示工程]]**：清晰表达需求，引导 AI 产出有用结果

4. **四大设计策略**：
   - **策略一：解释而非实现**——让候选人解释代码问题、权衡修复方案，而非单纯实现
   - **策略二：系统诊断**——提供已有问题的系统，要求综合多种信息推理
   - **策略三：动态深入**——根据候选人回答动态追问，测试真实理解而非预制答案
   - **策略四：明确允许使用 AI**——评测重点转向"与 AI 协作的能力"

5. **理解层次差别**：
   - 层次一（可被 AI 替代）：机械实现，如"用 [[Python]] 实现快速排序"
   - 层次二（困难替代）：解释特定条件下的行为，如"解释为什么退化为 O(n²)"
   - 层次三（真实理解标志）：结合实际场景的权衡分析

6. **工程师角色演变**：
   - 未来工程师更像"AI 系统的架构师和[[质量保障]]者"
   - 决定用 AI 做什么、不做什么
   - 验证 AI 输出正确性，处理边缘情况

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/19_ai_resistant_evals.md]] — 设计抗 AI 的技术评估（Anthropic Engineering Blog, 2026-01-21）

## 相关
- [[评测通货膨胀]] — relates_to（抗 AI 评测设计要解决的核心问题）
- [[评测驱动开发]] — relates_to（评测方法论的演进方向）
- [[提示工程]] — relates_to（AI 协作的核心能力之一）
- [[GitHub Copilot]] — relates_to（推动抗 AI 评测需求的工具之一）
- [[Claude Code]] — relates_to（推动抗 AI 评测需求的工具之一）
- [[Anthropic]] — part_of（Anthropic 工程团队的研究方向之一）
