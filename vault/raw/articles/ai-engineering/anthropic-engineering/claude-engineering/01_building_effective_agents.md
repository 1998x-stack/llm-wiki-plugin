# 构建高效 AI Agent：Anthropic 的工程实践总结

> **原文**：[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)  
> **发布日期**：2024 年 12 月 19 日  
> **作者**：Erik S. & Barry Zhang  
> **类别**：Agent 架构 · 工程实践

---

## 摘要

本文是 Anthropic Engineering Blog 中被引用最广泛的一篇奠基性文章。基于与数十个行业团队合作的实战经验，Anthropic 工程师提出了 Agent 系统的分类学框架，系统阐述了从"增强型 LLM"到"完全自主 Agent"的五种核心模式，并给出了何时使用、何时规避 Agent 的决策原则。这篇文章本质上是 Anthropic 对 AI Agent 工程化的"第一性原理"宣言。

---

## 一、核心论点：简单胜于复杂

文章的开篇立论令人印象深刻——Anthropic 观察到，**最成功的 Agent 实现并非依赖复杂框架，而是使用简单的可组合模式（simple, composable patterns）**。

这个判断在 AI 工程界具有重要指导意义。当市面上各类 Agent 框架（LangChain、AutoGen 等）竞相推出越来越精密的抽象层时，Anthropic 选择回归第一性原理：

> "我们建议开发者首先直接使用 LLM API，许多模式仅需几行代码即可实现。"

这种"反框架偏见"背后的技术逻辑在于：框架的抽象层往往遮蔽了底层的 prompt 与响应，使调试变得困难，并诱导开发者在不必要时引入额外复杂性。

---

## 二、Agent vs Workflow：关键架构区分

文章提出了一个非常重要的概念区分，业界对此常有混淆：

| 概念 | 定义 | 特征 |
|---|---|---|
| **Workflow（工作流）** | LLM 和工具通过**预定义代码路径**进行协调 | 确定性、可预测、适合结构化任务 |
| **Agent（智能体）** | LLM **动态指导**自己的过程和工具使用 | 灵活性、自主性、适合开放性任务 |

这个区分的工程价值在于：工作流提供确定性和一致性，Agent 提供灵活性和模型驱动决策。选择错误的范式会带来巨大的维护成本。

---

## 三、五种核心构建模式

### 3.1 基础构建块：增强型 LLM

这是所有 Agent 系统的基础——LLM 配备检索（Retrieval）、工具（Tools）和记忆（Memory）三类增强能力。

**工程要点**：这些增强能力的接口设计至关重要，需要：
- 为特定用例量身定制
- 提供清晰、文档良好的 LLM 调用接口
- 可通过 Model Context Protocol（MCP）集成第三方工具生态

### 3.2 工作流模式一：Prompt Chaining（提示链）

将任务分解为顺序步骤，每个 LLM 调用处理上一个的输出，可在中间步骤插入程序化检查（gate）。

```
Input → [LLM1] → Gate? → [LLM2] → Gate? → [LLM3] → Output
```

**适用场景**：任务能被清晰拆分为固定子任务，以延迟换取更高精度。  
**典型案例**：生成营销文案 → 翻译成目标语言；写文档大纲 → 检验大纲 → 基于大纲撰写正文。

### 3.3 工作流模式二：Routing（路由）

对输入进行分类并路由到专业化的后续任务，实现关注点分离。

```
Input → [Classifier] → Route A: [LLM-A]
                     → Route B: [LLM-B]  
                     → Route C: [LLM-C]
```

**适用场景**：存在需要差异化处理的明确类别，且分类精度有保障（LLM 分类器或传统 ML 模型）。  
**典型案例**：客服路由（退款/技术支持/一般询问）；根据问题难度路由到 Haiku vs Sonnet。

### 3.4 工作流模式三：Parallelization（并行化）

LLM 同时处理任务，输出以程序化方式聚合，有两个关键变体：

- **分区（Sectioning）**：将任务分解为并行独立子任务
- **投票（Voting）**：同一任务运行多次，获取多样输出

```
Input → [LLM-1] ─┐
      → [LLM-2] ─┼→ [Aggregator] → Output
      → [LLM-3] ─┘
```

**适用场景**：子任务可并行加速，或需要多视角/多次尝试以获得高置信度结果。  
**工程意义**：内容安全审查（主任务 + 安全检查并行）是一个经典应用，比让同一 LLM 同时处理两个关注点效果更好。

### 3.5 工作流模式四：Orchestrator-Workers（编排器-工作者）

中央 LLM（Orchestrator）动态分解任务、委派给工作 LLM，并综合结果。

```
Input → [Orchestrator] → [Worker-A]
                      → [Worker-B]  → [Synthesizer] → Output
                      → [Worker-C]
```

**与并行化的关键区别**：子任务是由 Orchestrator 根据具体输入**动态确定**的，而非预先定义。  
**适用场景**：无法预判所需子任务数量的复杂任务（如修改多个文件的代码任务）。

### 3.6 工作流模式五：Evaluator-Optimizer（评估器-优化器）

一个 LLM 生成响应，另一个提供评估和反馈，形成循环。

```
Input → [Generator] → [Evaluator] → Pass? → Output
                    ↑_______________|
                    (Feedback Loop)
```

**适用场景**的两个判断标准：
1. LLM 响应在人工反馈后可明显改进
2. LLM 能提供有效的反馈

**典型案例**：文学翻译（翻译器 + 评论器）；复杂搜索任务（多轮搜索+分析）。

---

## 四、真正的 Agent：何时使用自主体

文章将真正的 Agent 定位为"当 LLM 能力成熟时才出现的生产级系统"，强调 Agent 需要具备：

- 理解复杂输入
- 推理和规划
- 可靠使用工具
- 从错误中恢复

**适用场景**：无法预判步骤数量的开放性问题，且对模型决策能力有一定信任基础。

**三大核心原则**：
1. **简洁性（Simplicity）**：保持 Agent 设计的简单性
2. **透明性（Transparency）**：明确展示 Agent 的规划步骤
3. **工具文档（Tool Documentation）**：通过充分的工具文档和测试精心设计 ACI（Agent-Computer Interface）

---

## 五、深度辨析：ACI 与 HCI 的类比

文章中最具洞见的观点之一是将 ACI（Agent-Computer Interface）与 HCI（Human-Computer Interface）进行类比：

> "思考投入到人机界面（HCI）中的工作量，并计划投入同等工作量来创建良好的 Agent-计算机接口（ACI）。"

这意味着工具定义（tool definitions）需要与 prompt 工程同等重视。文章给出了具体建议：

- 好的工具定义通常包含**示例用法、边缘情况、输入格式要求、与其他工具的清晰边界**
- 参数名称要让意图显而易见，如同给初级开发者写优质文档
- 使用 poka-yoke（防错设计）思维：改变参数使错误更难发生

**SWE-bench 的实证案例**：Anthropic 在 SWE-bench Agent 中发现，模型在 agent 离开根目录后使用相对路径时会出错。解决方案是要求工具**始终使用绝对路径**，这一改变使模型运行"无懈可击"。

---

## 六、批判性分析

### 优点

1. **分类学的实用价值**：五种模式的分类经过了实际验证，避免了过度抽象
2. **"何时不用"的明确建议**：文章明确指出优化单次 LLM 调用通常就足够了，这种克制的建议在当时颇为罕见
3. **ACI 概念的提出**：将工具接口设计提升到与 HCI 同等重要性，是工程实践的重要认知升级

### 局限性

1. **缺乏失败案例分析**：文章主要描述成功模式，对各模式的失败场景着墨较少
2. **评估（Evaluation）视角缺失**：文章未深入讨论如何评估不同架构的实际效果，这在后续文章中才得到补充
3. **安全性讨论不足**：多 Agent 系统的 prompt injection 风险、权限传播等问题未在此文中涉及

---

## 七、行业影响与延伸思考

这篇文章发布后迅速成为 AI Agent 领域的核心参考文献。其"简单优于复杂"的核心论点对当时盛行的"万能框架"思维形成了有力反驳。

从历史视角看，Anthropic 提出的这五种模式与软件工程中的经典设计模式（如 Chain of Responsibility、Observer、Mediator）存在深刻对应关系：

- Prompt Chaining ↔ Chain of Responsibility / Pipeline
- Routing ↔ Strategy Pattern
- Parallelization ↔ Fork-Join / MapReduce
- Orchestrator-Workers ↔ Master-Worker / Actor Model
- Evaluator-Optimizer ↔ Feedback Control Loop

这种对应关系暗示 Agent 工程正在经历与传统软件工程类似的演化路径——从特例到模式，从模式到框架，从框架到工程原则。

---

## 八、对实践者的建议

基于本文的核心思想，给 Agent 工程师的具体建议：

1. **先求最小可行 prompt**：在引入 Agent 架构之前，先测试单次优化的 LLM 调用是否满足需求
2. **工具文档是第一等公民**：编写工具定义时，投入与 prompt 工程相同的精力
3. **从工作流开始**：除非任务天然开放且步骤无法预判，否则工作流通常优于自主 Agent
4. **建立 ACI 测试框架**：使用工作台（workbench）运行大量示例输入，观察工具使用错误并迭代

---

## 参考与扩展阅读

- [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) — 工具生态集成协议
- [SWE-bench Sonnet](https://www.anthropic.com/research/swe-bench-sonnet) — 文中提及的编码 Agent 评测
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — 上下文工程进阶版
- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) — 多 Agent 系统的生产实践

---

*本文分析基于 Anthropic Engineering Blog 原文，写于 2026 年 4 月。*
