---
type: concept
status: active
confidence: 0.88
created: 2026-04-15
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 8
tags: [技术, AI, 方法论, Agent系统]
aliases: ["ACI", "Agent-Computer Interface", "Agent工具接口设计", "tool ergonomics"]
relates_to:
  - target: "[[Agent工作流模式]]"
    type: part_of
    confidence: 0.9
  - target: "[[Context-Engineering]]"
    type: related_to
    confidence: 0.82
  - target: "[[MCP协议层]]"
    type: related_to
    confidence: 0.8
  - target: "[[SWE-bench]]"
    type: uses
    confidence: 0.9
  - target: "[[ACI 设计原则]]"
    type: extends
    confidence: 0.95
  - target: "[[Guardrails]]"
    type: uses
    confidence: 0.9
  - target: "[[Localization]]"
    type: uses
    confidence: 0.85
  - target: "[[Context Management]]"
    type: uses
    confidence: 0.85
  - target: "[[Ablation Study]]"
    type: uses
    confidence: 0.85
  - target: "[[环境反馈设计]]"
    type: uses
    confidence: 0.9
  - target: "[[状态变化感知]]"
    type: uses
    confidence: 0.9
  - target: "[[恢复机制]]"
    type: uses
    confidence: 0.85
supersedes: null
---

# Agent 计算机接口（ACI）

## 概述

Agent [[计算]]机接口（[[ACI (Agent-Computer Interface)|Agent-Computer Interface]], ACI）是类比人机接口（HCI）的概念：为 L[[LM Agent]] 设计工具接口需要与 HCI 同等的工程投入。工具的设计质量直接决定 Agent 的成功率——[[Anthropic]] 在 [[SWE-bench]] 中花费在工具优化上的时间多于整体提示词优化。

## 关键内容

### SWE-agent 论文的 ACI 贡献

Princeton 的 [[SWE-agent]] 论文（"[[SWE-agent]]: [[ACI (Agent-Computer Interface)|Agent-Computer Interface]]s Enable Automated Software Engineering"）是 ACI 理念的开创性实证研究。其核心论点：

> 软件工程 agent 的效果，很大程度上取决于它和[[计算]]机交互的"接口设计"是否合适。

**论文真正想回答的问题**：LLM agent 在软件工程任务上的瓶颈，到底来自模型能力不足，还是来自交互界面设计太差？作者的判断是后者至少同样重要。

三大核心观点：
1. **软件工程不是纯文本生成任务**，而是"读[[仓库]] → 定位问题 → 修改文件 → 运行测试 → 继续迭代"的交互式任务
2. **ACI 是关键创新**——给模型设计专门的交互方式（浏览代码库、查看文件、编辑代码、执行测试），而非只靠 prompt engineering
3. **Agent 上限由"模型 × 工具 × 界面"的系统乘积决定**，不只是模型参数规模

**为什么不能直接把 Linux shell 丢给 Agent**：
- 命令空间太开放，容易乱走
- 编辑操作不稳定
- 文件改坏了不一定有清晰反馈
- 长输出容易让上下文失控
- 在大型[[仓库]]中导航效率很差

因此 [[SWE-agent]] 不是让模型直接裸用电脑，而是通过 ACI 提供一套更适合 Agent 的动作抽象。**把"界面设计"从工程细节提升成研究对象**，这是论文最有思想含量的贡献。

实验结果：[[SWE-agent]] 在 [[SWE-bench]] 上 pass@1 达到 12.5%，在 [[HumanEvalFix]] 上达到 87.7%。两者差距说明 ACI 设计在复杂任务上的价值远大于简单任务。

### ACI vs. HCI

| | HCI（Human-Computer Interface） | ACI（[[ACI (Agent-Computer Interface)|Agent-Computer Interface]]） |
|--|--|--|
| 使用者 | 人类 | L[[LM Agent]] |
| 设计约束 | 视觉认知、操作直觉 | Token 有限性、输入格式偏好、幻觉风险 |
| 文档形式 | 用户手册、UI 标签 | 工具名称、描述、参数定义 |
| 测试方法 | 用户测试 | 工具调用评估 + transcript 分析 |

### 工具设计五大原则

**1. 选择正确的工具（而非多多益善）**

更多工具不一定更好。常见错误：简单包装 API 端点而不考虑 Agent 的工作方式。

- 实现高影响力工作流的**少数精选工具**，优于大量低质量工具
- 工具应**合并功能**（减少 Agent 决策负担）：
  - ✅ `search_contacts(name)` 而非 `list_contacts()` + 手动筛选
  - ✅ `schedule_event(participants, topic)` 内部处理查找可用时间 + 创建事件
  - ✅ `get_customer_context(id)` 合并历史、交易、备注

**2. 工具命名空间（Namespacing）**

使用前缀或后缀[[区分]]不同来源的工具，避免 Agent 混淆类似工具：
- 按[[服务]]：`asana_search`, `jira_search`
- 按资源：`asana_projects_search`, `asana_users_search`

**3. 返回有意义的上下文**

工具响应应优先返回对 Agent 下游决策有用的字段，而非技术标识符：
- ✅ `name`, `image_url`, `file_type`
- ❌ `uuid`, `256px_image_url`, `mime_type`
- 将任意字母数字 UUID 解析为语义化标识符（或简单的 0-indexed ID）可显著减少幻觉

**4. 优化 Token 效率**

长响应使用分页/范围选择/过滤/截断。[[Claude Code]] 默认将工具响应限制在 25,000 tokens。截断时应给出明确指导，引导 Agent 使用更精准的查询，而非盲目依赖截断。

**5. 工具描述的[[Prompt Engineering|提示工程]]**

工具描述是最高效的 Agent 调优手段之一：
- 像给新团队成员写文档一样编写：包含专业查询格式、领域术语定义、资源间关系
- 参数名应无歧义（`user_id` 优于 `user`）
- 细微的描述改进可带来显著性能变化——[[SWE-bench]] 中仅改工具描述就达到 SOTA

### 工具开发的评估驱动循环

[[Anthropic]] 推荐的工具开发流程：

1. **构建原型** — 快速实现，用 [[Claude Code]] 测试基础功能
2. **生成评估任务** — 基于真实使用场景的 prompt-response 对（包含需要多步工具调用的复杂任务）
3. **运行评估** — 使用简单 agentic 循环程序化运行；收集精度、运行时间、工具调用次数、Token 消耗等指标
4. **分析结果** — 阅读 transcript 和工具调用；让 Agent 分析自身的 transcript 找出改进点
5. **让 Agent 改进工具** — 将评估 transcript 粘贴给 [[Claude Code]]，让它[[重构]]工具；对 [[Slack]] [[MCP 服务器]]的实验显示 [[Claude_Code|Claude]] 优化后的工具性能高于人工编写版本

### 使用 Tool Use Examples 补充 Schema

JSON Schema 定义什么是**结构上有效**的，但无法表达**使用模式**。通过在工具定义中提供示例，直接展示：
- 日期格式约定（"2024-11-06" vs ISO 8601）
- ID 格式约定（"USR-12345" vs 整数）
- 嵌套对象何时填写（critical bug vs feature request 的不同处理）
- 可选参数的关联规则

[[Anthropic]] 内部测试显示，添加 [[Tool-Use|Tool Use]] Examples 将复杂参数处理准确率从 72% 提升至 **90%**。

## 来源

- [[raw/articles/ai-engineering/anthropic-engineering/Building Effective AI Agents.md]]
- [[raw/articles/ai-engineering/anthropic-engineering/Writing effective tools for AI agents—using AI agents.md]]
- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/01-SWE agent论文 主要讲解什么核心点，什么观点？.md]] — SWE-agent 论文核心观点总结
- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/02-SWE-agent 论文的 5 页读书笔记版".md]] — SWE-agent 论文 5 页读书笔记
- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/03-SWE-agent 论文的所有核心概念 展开详细分析 一个一个.md]] — SWE-agent 24 个核心概念词条分析
- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/04-SWE agent 如何保证 搜索是否高效、编辑是否稳定、反馈是否足够、上下文是否可控、恢复机制是否.md]] — SWE-agent 五大保障机制分析
- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/05-SWE agent 有哪些图表，每个图表核心内容和核心观点是什么？.md]] — SWE-agent 论文图表分析
- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/07-SWE-agent 轨迹 格式长什么样，怎么进行分析，怎么判断轨迹中哪些问题导致了后续任务的失败？.md]] — SWE-agent 轨迹分析方法论

## 相关

- [[Agent工作流模式]] — part_of（良好的 ACI 是所有工作流模式正常运作的前提）
- [[Context-Engineering]] — related_to（工具响应的 Token 效率是上下文工程的组成部分）
- [[MCP协议层]] — related_to（MCP 工具的描述质量直接体现 ACI 原则）
- [[Agent评估方法论]] — related_to（工具评估是 ACI 开发循环的核心环节）
- [[SWE-bench]] — uses（ACI 设计质量的验证基准）
- [[HumanEvalFix]] — uses（ACI 在简单任务上的验证基准，87.7% pass@1）
- [[ACI 设计原则]] — extends（ACI 研究的方法论贡献：四条核心原则）
- [[Guardrails]] — uses（ACI 的错误 containment 策略）
- [[Localization]] — uses（ACI 的核心子任务：代码定位）
- [[Context Management]] — uses（ACI 的工作记忆管理组件）
- [[Ablation Study]] — uses（验证 ACI 各组件贡献的方法论）
- [[环境反馈设计]] — uses（ACI 的反馈设计组件：specific & concise）
- [[状态变化感知]] — uses（ACI 的状态可见性组件）
- [[恢复机制]] — uses（ACI 的错误恢复组件）
