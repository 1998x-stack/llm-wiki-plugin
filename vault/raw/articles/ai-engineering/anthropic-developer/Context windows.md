---
title: "Context windows"
source: "https://platform.claude.com/docs/en/build-with-claude/context-windows"
author:
published:
created: 2026-04-16
description: "Claude API Documentation"
tags:
  - "clippings"
---
This feature is eligible for [Zero Data Retention (ZDR)](https://platform.claude.com/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.此功能符合零数据保留（ZDR）</b>的条件。当你的组织签订了零数据保留协议后，通过此功能发送的数据在API响应返回后不会被存储。

As conversations grow, you'll eventually approach context window limits. This guide explains how context windows work and introduces strategies for managing them effectively.随着对话的增长，您最终会接近上下文窗口限制。本指南解释了上下文窗口的工作原理，并介绍了有效管理它们的策略。

For long-running conversations and agentic workflows, [server-side compaction](https://platform.claude.com/docs/en/build-with-claude/compaction) is the primary strategy for context management. For more specialized needs, [context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing) offers additional strategies like tool result clearing and thinking block clearing.对于长时间运行的对话和智能体工作流， [服务端压缩](https://platform.claude.com/docs/en/build-with-claude/compaction) 是上下文管理的主要策略。针对更专业的需求， [上下文编辑](https://platform.claude.com/docs/en/build-with-claude/context-editing) 提供了额外策略，例如工具结果清理和思维块清理。

## Understanding the context window 了解上下文窗口

The "context window" refers to all the text a language model can reference when generating a response, including the response itself. This is different from the large corpus of data the language model was trained on, and instead represents a "working memory" for the model. A larger context window allows the model to handle more complex and lengthy prompts, but more context isn't automatically better. As token count grows, accuracy and recall degrade, a phenomenon known as *context rot*. This makes curating what's in context just as important as how much space is available.“上下文窗口”指的是语言模型在生成回复时可参考的所有文本，包括回复本身。这与语言模型所训练的海量数据集不同，而是相当于模型的“工作记忆”。更大的上下文窗口能让模型处理更复杂、更长的提示词，但更多的上下文并非必然更优。随着标记数量增加，模型的准确率和召回率会下降，这一现象被称为 *上下文退化* 。因此，筛选上下文内容与预留上下文空间同样重要。

Claude achieves state-of-the-art results on long-context retrieval benchmarks like [MRCR](https://arxiv.org/abs/2501.03276) and [GraphWalks](https://arxiv.org/abs/2412.04360), but these gains depend on what's in context, not just how much fits.Claude 在 [MRCR](https://arxiv.org/abs/2501.03276) 和 [GraphWalks](https://arxiv.org/abs/2412.04360) 等长上下文检索基准测试中取得了最先进的成果，但这些提升取决于上下文的内容，而不仅仅是能容纳的信息量。

For a deep dive into why long contexts degrade and how to engineer around it, see [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).要深入了解为什么长上下文会降级以及如何围绕它进行工程，请参阅 [有效上下文工程](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) 。

The diagram below illustrates the standard context window behavior for API requests <sup>1</sup>:下图说明了API请求1的标准上下文窗口行为：

![Context window diagram](https://platform.claude.com/docs/images/context-window.svg)

*<sup>1</sup> For chat interfaces, such as for [claude.ai](https://claude.ai/), context windows can also be set up on a rolling "first in, first out" system.1\. 对于聊天界面（例如 [claude.ai](https://claude.ai/) 的界面），上下文窗口也可采用滚动式“先进先出”系统进行设置。*

- **Progressive token accumulation:** As the conversation advances through turns, each user message and assistant response accumulates within the context window. Previous turns are preserved completely.**渐进式令牌累积：** 随着对话逐轮推进，每位用户的消息和助手的回复都会累积到上下文窗口中。之前的对话轮次会被完整保留。
- **Linear growth pattern:** The context usage grows linearly with each turn, with previous turns preserved completely.**线性增长模式：** 上下文使用量随每一轮呈线性增长，且之前的轮次会被完全保留。
- **Context window capacity:** The total available context window (up to 1M tokens) represents the maximum capacity for storing conversation history and generating new output from Claude.**上下文窗口容量：** 可用的总上下文窗口（最大可达100万个标记）是Claude存储对话历史和生成新输出的最大容量。
- **Input-output flow:** Each turn consists of:**输入-输出流程：** 每一轮包含：
	- **Input phase:** Contains all previous conversation history plus the current user message **输入阶段：** 包含所有过往对话历史以及当前的用户消息
		- **Output phase:** Generates a text response that becomes part of a future input **输出阶段：** 生成一段文本回复，该回复将成为未来输入的一部分

## The context window with extended thinking扩展思维的上下文窗口

When using [extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking), all input and output tokens, including the tokens used for thinking, count toward the context window limit, with a few nuances in multi-turn situations.使用 [扩展思考](https://platform.claude.com/docs/en/build-with-claude/extended-thinking) 功能时，所有输入和输出的token（包括用于思考的token）都会计入上下文窗口限制，在多轮对话场景中存在一些细微差别。

The thinking budget tokens are a subset of your `max_tokens` parameter, are billed as output tokens, and count towards rate limits. With [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking), Claude dynamically decides its thinking allocation, so actual thinking token usage may vary per request.思考预算令牌是你 `max_tokens` 参数的一个子集，按输出令牌计费，并计入速率限制。借助 [自适应思考](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking) 功能，Claude 会动态决定其思考分配，因此实际思考令牌使用量可能因请求而异。

However, previous thinking blocks are automatically stripped from the context window calculation by the Claude API and are not part of the conversation history that the model "sees" for subsequent turns, preserving token capacity for actual conversation content.不过，Claude API 会自动从上下文窗口计算中剔除之前的思维块，这些思维块不会出现在模型为后续对话轮次“查看”的对话历史中，从而为实际的对话内容保留令牌容量。

The diagram below demonstrates the specialized token management when extended thinking is enabled:下图展示了启用扩展思考时的专用令牌管理机制：

![Context window diagram with extended thinking](https://platform.claude.com/docs/images/context-window-thinking.svg)

- **Stripping extended thinking:** Extended thinking blocks (shown in dark gray) are generated during each turn's output phase, **but are not carried forward as input tokens for subsequent turns**. You do not need to strip the thinking blocks yourself. The Claude API automatically does this for you if you pass them back.**剥离扩展思考内容：** 扩展思考块（深灰色显示）会在每一轮的输出阶段生成， **但不会作为后续轮次的输入标记继续传递** 。你无需自行剥离思考块。如果你将其回传，Claude API 会自动为你完成这一操作。
- **Technical implementation details: 技术实现细节：**
	- The API automatically excludes thinking blocks from previous turns when you pass them back as part of the conversation history.当你将思考块作为对话历史的一部分传回时，API 会自动将其从之前的对话轮次中排除。
		- Extended thinking tokens are billed as output tokens only once, during their generation.扩展思考标记仅在生成过程中被计为一次输出标记。
		- The effective context window calculation becomes: `context_window = (input_tokens - previous_thinking_tokens) + current_turn_tokens`.有效上下文窗口的计算方式为： `context_window = (input_tokens - previous_thinking_tokens) + current_turn_tokens` 。
		- Thinking tokens include `thinking` blocks.思考令牌包含 `thinking` 块。

This architecture is token efficient and allows for extensive reasoning without token waste, as thinking blocks can be substantial in length.该架构在令牌使用上效率很高，并且能够进行深度推理而不会造成令牌浪费，因为思考块的长度可以很长。

You can read more about the context window and extended thinking in the [extended thinking guide](https://platform.claude.com/docs/en/build-with-claude/extended-thinking).你可以在 [扩展思维指南](https://platform.claude.com/docs/en/build-with-claude/extended-thinking) 中了解更多关于上下文窗口和扩展思维的内容。

## The context window with extended thinking and tool use具有扩展思维和工具使用的上下文窗口

The diagram below illustrates the context window token management when combining extended thinking with tool use:下图展示了将扩展思考与工具使用相结合时的上下文窗口令牌管理情况：

![Context window diagram with extended thinking and tool use](https://platform.claude.com/docs/images/context-window-thinking-tools.svg)

1. First turn architecture 首轮架构
	- **Input components:** Tools configuration and user message **输入组件：** 工具配置与用户消息
	- **Output components:** Extended thinking + text response + tool use request **输出组件：** 扩展思考+文本回复+工具使用请求
	- **Token calculation:** All input and output components count toward the context window, and all output components are billed as output tokens.**令牌计算：** 所有输入和输出组件均计入上下文窗口，所有输出组件均按输出令牌计费。
2. Tool result handling (turn 2) 工具结果处理（第二轮）
	- **Input components:** Every block in the first turn as well as the `tool_result`. The extended thinking block **must** be returned with the corresponding tool results. This is the only case wherein you **have to** return thinking blocks.**输入组件：** 第一轮中的每个模块以及 `tool_result` 。扩展思考模块 **必须** 与对应的工具结果一起返回。这是你 **必须** 返回思考模块的唯一情况。
	- **Output components:** After tool results have been passed back to Claude, Claude will respond with only text (no additional extended thinking until the next `user` message).**输出组件：** 工具结果回传给 Claude 后，Claude 仅会以文本形式回复（在下一条 `user` 消息到来前不进行额外的扩展思考）。
	- **Token calculation:** All input and output components count toward the context window, and all output components are billed as output tokens.**令牌计算：** 所有输入和输出组件均计入上下文窗口，所有输出组件均按输出令牌计费。
3. Third Step 第三步
	- **Input components:** All inputs and the output from the previous turn is carried forward with the exception of the thinking block, which can be dropped now that Claude has completed the entire tool use cycle. The API will automatically strip the thinking block for you if you pass it back, or you can feel free to strip it yourself at this stage. This is also where you would add the next `User` turn.**输入组件：** 除思考块外，所有输入和上一轮的输出都会被保留。既然 Claude 已完成整个工具使用周期，思考块现在可以舍弃。若你将其回传，API 会自动为你移除思考块，你也可在这一阶段自行移除。同时，你需要在此处添加下一轮 `User` 的内容。
	- **Output components:** Since there is a new `User` turn outside of the tool use cycle, Claude generates a new extended thinking block and continues from there.**输出组件：** 由于在工具使用周期之外出现了新的 `User` 轮次，Claude 会生成一个新的扩展思考块并从中继续执行。
	- **Token calculation:** Previous thinking tokens are automatically stripped from context window calculations. All other previous blocks still count as part of the token window, and the thinking block in the current `Assistant` turn counts as part of the context window.**Token 计算：** 之前的思考 Token 会从上下文窗口计算中自动剔除。所有其他之前的模块仍计入 Token 窗口，且当前 `Assistant` 轮次中的思考模块计入上下文窗口。

- **Considerations for tool use with extended thinking:结合扩展思维使用工具的注意事项：**
	- When posting tool results, the entire unmodified thinking block that accompanies that specific tool request (including signature portions) must be included.发布工具结果时，必须附带该特定工具请求的完整未修改的思考块（包括签名部分）。
		- The effective context window calculation for extended thinking with tool use becomes: `context_window = input_tokens + current_turn_tokens`.结合工具使用的扩展思考的有效上下文窗口计算结果为： `context_window = input_tokens + current_turn_tokens` 。
		- The system uses cryptographic signatures to verify thinking block authenticity. Failing to preserve thinking blocks during tool use can break Claude's reasoning continuity. Thus, if you modify thinking blocks, the API returns an error.该系统使用加密签名来验证思维块的真实性。在工具使用过程中未能保留思维块会破坏Claude的推理连续性。因此，如果你修改了思维块，API会返回一个错误。

Claude 4 models support [interleaved thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking#interleaved-thinking), which enables Claude to think between tool calls and make more sophisticated reasoning after receiving tool results.Claude 4 模型支持 [交错式思考](https://platform.claude.com/docs/en/build-with-claude/extended-thinking#interleaved-thinking) ，这使得 Claude 能够在工具调用之间进行思考，并在获取工具结果后进行更复杂的推理。

Claude Sonnet 3.7 does not support interleaved thinking, so there is no interleaving of extended thinking and tool calls without a non- `tool_result` user turn in between.Claude Sonnet 3.7 不支持交错式思考，因此在没有非工具结果（non- `tool_result` ）的用户回合介入的情况下，扩展思考与工具调用不会交错进行。

For more information about using tools with extended thinking, see the [extended thinking guide](https://platform.claude.com/docs/en/build-with-claude/extended-thinking#extended-thinking-with-tool-use).有关如何结合扩展思维使用工具的更多信息，请参阅 [扩展思维指南](https://platform.claude.com/docs/en/build-with-claude/extended-thinking#extended-thinking-with-tool-use) 。

[Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.6, and Claude Sonnet 4.6 have a 1M-token context window. Other Claude models, including Claude Sonnet 4.5 and Sonnet 4 (deprecated), have a 200k-token context window.[Claude 神话预览](https://anthropic.com/glasswing) 、Claude Opus 4.6 和 Claude Sonnet 4.6 拥有 100 万令牌的上下文窗口。其他 Claude 模型（包括 Claude Sonnet 4.5 以及已停用的 Sonnet 4）的上下文窗口为 20 万令牌。

A single request can include up to 600 images or PDF pages (100 for models with a 200k-token context window). When sending many images or large documents, you may approach [request size limits](https://platform.claude.com/docs/en/api/overview#request-size-limits) before the token limit.单次请求最多可包含 600 张图片或 PDF 页面（上下文窗口为 20 万 token 的模型最多为 100）。发送大量图片或大型文档时，可能会在达到 token 限制前就触碰到 [请求大小限制](https://platform.claude.com/docs/en/api/overview#request-size-limits) 。

## Context awareness in Claude Sonnet 4.6, Sonnet 4.5, and Haiku 4.5Claude Sonnet 4.6、Sonnet 4.5 以及 Haiku 4.5 中的上下文感知能力

Claude Sonnet 4.6, Claude Sonnet 4.5, and Claude Haiku 4.5 feature **context awareness**. This capability lets these models track their remaining context window (i.e. "token budget") throughout a conversation. This enables Claude to execute tasks and manage context more effectively by understanding how much space it has to work. Claude is trained to use this context precisely, persisting in the task until the very end rather than guessing how many tokens remain. For a model, lacking context awareness is like competing in a cooking show without a clock. Claude 4.5+ models change this by explicitly informing the model about its remaining context, so it can take maximum advantage of the available tokens.Claude Sonnet 4.6、Claude Sonnet 4.5 以及 Claude Haiku 4.5 具备 **上下文感知** 功能。该功能使这些模型能够在整个对话过程中追踪其剩余上下文窗口（即“令牌预算”）。通过了解自身可用的操作空间，Claude 能更高效地执行任务和管理上下文。Claude 经过训练可精准利用这一上下文，始终坚持完成任务直至最后，而非盲目猜测剩余令牌数量。对模型而言，缺乏上下文感知就如同在烹饪比赛中没有时钟参赛。Claude 4.5 及更高版本的模型通过明确告知模型其剩余上下文，解决了这一问题，从而使其能最大化利用可用令牌。

**How it works: 工作原理：**

At the start of a conversation, Claude receives information about its total context window:在对话开始时，Claude 会获取其上下文窗口的总容量信息：

```
<budget:token_budget>1000000</budget:token_budget>
```

The budget is set to 1M tokens (200k for models with a smaller context window).预算设定为100万个标记（上下文窗口较小的模型则为20万个标记）。

After each tool call, Claude receives an update on remaining capacity:每次调用工具后，Claude 都会收到剩余容量的更新：

```
<system_warning>Token usage: 35000/1000000; 965000 remaining</system_warning>
```

This awareness helps Claude determine how much capacity remains for work and enables more effective execution on long-running tasks. Image tokens are included in these budgets.这种感知能力有助于 Claude 确定剩余的工作容量，并使其能更高效地执行长时间运行的任务。这些预算中包含图像标记。

**Benefits: 优势：**

Context awareness is particularly valuable for:上下文感知尤其适用于以下场景：

- Long-running agent sessions that require sustained focus 需要持续专注的长期智能体会话
- Multi-context-window workflows where state transitions matter 状态转换至关重要的多上下文窗口工作流
- Complex tasks requiring careful token management 需要谨慎管理令牌的复杂任务

For agents that span multiple sessions, design your state artifacts so that context recovery is fast when a new session starts. The [memory tool's multi-session pattern](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool#multi-session-software-development-pattern) walks through a concrete approach. See also [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).对于跨多个会话的智能体，设计你的状态组件时，要确保新会话启动时上下文恢复速度很快。 [记忆工具的多会话模式](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool#multi-session-software-development-pattern) 详细介绍了一种具体方法。另见 [长运行智能体的高效控制框架](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) 。

For prompting guidance on leveraging context awareness, see the [prompting best practices guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#context-awareness-and-multi-window-workflows).有关如何利用上下文感知的提示指导，请参阅 [提示最佳实践指南](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#context-awareness-and-multi-window-workflows) 。

## Managing context with compaction 通过压缩来管理上下文

If your conversations regularly approach context window limits, [server-side compaction](https://platform.claude.com/docs/en/build-with-claude/compaction) is the recommended approach. Compaction provides server-side summarization that automatically condenses earlier parts of a conversation, enabling long-running conversations beyond context limits with minimal integration work. It is currently available in beta for Claude Opus 4.6 and Sonnet 4.6.如果你的对话经常接近上下文窗口限制， [服务器端压缩](https://platform.claude.com/docs/en/build-with-claude/compaction) 是推荐的方法。压缩提供服务器端摘要功能，可自动精简对话的早期内容，让长对话突破上下文限制，且集成工作量极小。目前该功能在 Claude Opus 4.6 和 Sonnet 4.6 中处于测试阶段。

For more specialized needs, [context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing) offers additional strategies:针对更特殊的需求， [上下文编辑](https://platform.claude.com/docs/en/build-with-claude/context-editing) 提供了额外的策略：

- **Tool result clearing** - Clear old tool results in agentic workflows **工具结果清除** - 清除智能体工作流中的旧工具结果
- **Thinking block clearing** - Manage thinking blocks with extended thinking **思考块清理** - 通过扩展思考来管理思考块

## Context window management with newer Claude models新版 Claude 模型的上下文窗口管理

Newer Claude models (starting with Claude Sonnet 3.7) return a validation error when prompt and output tokens exceed the context window, rather than silently truncating. This change provides more predictable behavior but requires more careful token management.较新的 Claude 模型（从 Claude Sonnet 3.7 开始）在提示词和输出令牌超出上下文窗口时会返回验证错误，而非静默截断。这一变更带来了更可预测的行为，但也要求对令牌进行更细致的管理。

Use the [token counting API](https://platform.claude.com/docs/en/build-with-claude/token-counting) to estimate token usage before sending messages to Claude. This helps you plan and stay within context window limits.在向 Claude 发送消息之前，使用 [令牌计数 API](https://platform.claude.com/docs/en/build-with-claude/token-counting) 来估算令牌使用量。这有助于你进行规划，并将使用量控制在上下文窗口限制范围内。

See the [model comparison](https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison) table for a list of context window sizes by model.请查看 [模型对比](https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison) 表格，获取各模型的上下文窗口大小列表。[Compaction 压缩](https://platform.claude.com/docs/en/build-with-claude/compaction)

[

The recommended strategy for managing context in long-running conversations.这是长期对话中管理上下文的推荐策略。

](https://platform.claude.com/docs/en/build-with-claude/compaction)[

Context editing 上下文编辑

Fine-grained strategies like tool result clearing and thinking block clearing.像工具结果清理和思考块清理这样的细粒度策略。

](https://platform.claude.com/docs/en/build-with-claude/context-editing)[

Model comparison table 模型对比表

See the model comparison table for a list of context window sizes and input / output token pricing by model.查看模型对比表，获取各模型的上下文窗口大小以及输入/输出令牌定价列表。

](https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison)[

Extended thinking overview 扩展思维概述

Learn more about how extended thinking works and how to implement it alongside other features such as tool use and prompt caching.了解更多关于扩展思维的工作原理，以及如何将其与工具使用、提示词缓存等其他功能结合实施。

](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)

Was this page helpful? 此页面是否有帮助？