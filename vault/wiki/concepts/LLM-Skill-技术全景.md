---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 8
tags: [LLM, 工具调用, Agent, 技能文件, 技能编排, LLM能力]
aliases: ["LLM Skill Research Series", "LLM Skill 技术研究系列"]
relates_to: []
supersedes: null
---

# LLM Skill 技术全景

## 概述
LLM [[Skills|Skill]]技术是指让大型[[Language-Model|语言模型]]能够调用外部工具、使用API以及执行具体任务的工程技术体系。该领域从2022年的[[ReAct]][[规范化理论|范式]]起步，逐步发展出包括工具调用、[[Skills|技能]]库建设、工具生成、大规模工具检索和任务编排在内的完整生态。

## 关键内容

1. **第一代：工具增强的朴素尝试**
   - **MRKL Systems**：最早系统性提出"神经符号混合"架构，通过LLM[[网关与路由器|路由器]]将查询路由到专业模块（[[计算]]器/数据库/搜索引擎）
   - **WebGPT**：首批将工具调用与RLHF结合的工作，模型学习何时触发搜索、如何点击链接和整合信息

2. **第二代：[[ReAct]][[规范化理论|范式]]的统一**
   - **[[ReAct]]**：将[[Chain-of-Thought]]推理与动作执行交织在同一序列中（Thought → Act → Obs → Thought），解决了纯CoT的幻觉问题
   - 核心创新是将推理轨迹与真实环境交互相结合

3. **第三代：[[Agent Skills|技能系统]]化**
   - 关注点转向[[Skills|技能]]的来源、存储、复用和边界定义
   - 发展出三条主要研究路线：工具调用基础、[[Skills|技能]]库建设、工具生成

4. **工具调用基础研究**
   - **[[Toolformer]]**：让模型自己生成工具调用[[标注]]，通过自监督学习使用工具
   - **ToolkenGPT**：将工具作为特殊token，冻结LLM只训练工具[[Embedding|嵌入向量]]
   - **Gorilla**：连接LLM与真实API生态，采用[[检索增强生成|检索增强]]微调

5. **[[Skills|技能]]库[[规范化理论|范式]]**
   - **[[Voyager]]**：在Minecraft中实现自动课程学习，包含[[Skills|技能]]库的持久化存储与检索
   - **GITM**：[[任务分解]]与记忆模块，将复杂[[任务分解]]为子目标树
   - **SkiLL-IT**：[[Skills|技能]]依赖图，按拓扑顺序组织[[Skills|技能]]学习

6. **LLM作为工具制造者**
   - **LATM**：双LLM架构，GPT-4制造工具，[[GPT-3]].5使用工具，降低成本
   - **[[CRAFT]]**：维护代码片段库，新任务时检索相关代码并组合
   - **Creator**：工具创建、决策、执行、修正的统一框架

7. **大规模工具检索**
   - **[[ToolBench]]/ToolLLM**：大规模API工具调用基准，提出DFSDT[[决策树]]搜索
   - **[[AnyTool]]**：层次化工具检索，自反思机制
   - **[[API-Bank]]**：端到端评估工具增强LLM的基准

8. **任务规划与[[Skills|技能]]编排**
   - **[[HuggingGPT]]**：[[探索-规划-编码工作流|四阶段工作流]]（任务规划、[[模型选择]]、任务执行、响应生成）
   - **[[AssistGPT]]**：PEIL框架（Plan-[[Execute]]-Inspect-Learn）带有主动检查机制

9. **代码即[[Skills|技能]]统一[[规范化理论|范式]]**
   - **[[CodeAct]]**：使用可执行[[Python]]代码作为统一动作空间，优于JSON和自然语言
   - **[[OpenAgents]]**：专门化Agent平台，包含DataAgent、[[Plugins]]Agent、WebAgent
   - **[[AgentBench]]**：全面评估Agent能力的八大测试环境

## 来源
- [[llm-skill-research-series.md]] — 源文件整理

## 相关
- [[ReAct]] — relates_to
- [[Chain-of-Thought]] — relates_to
- [[Tool-Use]] — relates_to
- [[Agent-Programming]] — relates_to
- [[Context-Engineering]] — relates_to
- [[Harness-Engineering]] — relates_to