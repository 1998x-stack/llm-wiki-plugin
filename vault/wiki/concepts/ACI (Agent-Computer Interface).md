---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 2
tags: ["agent-design", "interface", "tool-design", "engineering-principle"]
aliases: ["Agent-Computer Interface", "智能体-计算机接口", "工具接口设计"]
relates_to:
  - "[[AI Agent 架构模式]] — relates_to"
  - "[[Model Context Protocol]] — relates_to"
supersedes: null
---

# ACI (Agent-Computer Interface)

## 概述
Agent-Computer Interface 设计原则，强调工具定义需要与 prompt 工程同等重视，是 Anthropic 提出的核心工程洞见之一。

## 关键内容
1. **核心洞见**：将 ACI 与 HCI（Human-Computer Interface）进行类比——"思考投入到人机界面中的工作量，并计划投入同等工作量来创建良好的 Agent-计算机接口。"
2. **工具定义最佳实践**：好的工具定义通常包含**示例用法、边缘情况、输入格式要求、与其他工具的清晰边界**。参数名称要让意图显而易见，如同给初级开发者写优质文档。
3. **防错设计（Poka-Yoke）**：使用 poka-yoke 思维改变参数使错误更难发生。如 SWE-bench Agent 中发现模型在离开根目录后使用相对路径时会出错，解决方案是要求工具**始终使用绝对路径**。
4. **SWE-bench 实证案例**：Anthropic 在 SWE-bench Agent 中发现，模型在 agent 离开根目录后使用相对路径时会出错。改为要求工具始终使用绝对路径后，模型运行"无懈可击"。
5. **ACI 测试框架**：建立工作台（workbench）运行大量示例输入，观察工具使用错误并迭代。工具文档是第一等公民，投入与 prompt 工程相同的精力。

## 来源
- [[01_building_effective_agents.md]] — 第五章，Anthropic Engineering Blog "Building effective agents"
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/07_swe_bench_sonnet.md]] — SWE-bench 工具优化深度分析

## 相关
- [[AI Agent 架构模式]] — relates_to (Agent 设计三大原则之一)
- [[Model Context Protocol]] — relates_to (工具生态集成协议)
- [[SWE-bench]] — relates_to (实证案例来源)
