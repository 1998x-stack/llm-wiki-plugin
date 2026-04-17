---
title: "Best practices for using Claude Opus 4.7 with Claude Code"
source: "https://claude.com/blog/best-practices-for-using-claude-opus-4-7-with-claude-code"
author:
published: 2001-04-16
created: 2026-04-17
description: "Learn how to use recalibrated effort levels, adaptive thinking, and new defaults to optimize your Claude Code setup with Opus 4.7."
tags:
  - "clippings"
---
[Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7) is our strongest generally available model to date for coding, enterprise workflows, and long-running agentic tasks. It handles ambiguity better than Opus 4.6, is much more capable at finding bugs and reviewing code, carries context across sessions more reliably, and can reason through ambiguous tasks with less direction.[Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7) 是我们目前为止在编码、企业级工作流和长期智能体任务方面最强大的通用可用模型。它比 Opus 4.6 更能处理模糊情况，在发现漏洞和审查代码方面的能力大幅提升，跨会话的上下文承载更可靠，且在无需过多指导的情况下，能对模糊任务进行逻辑推理。

In our [launch announcement](https://www.anthropic.com/news/claude-opus-4-7), we noted that two changes—an updated tokenizer and a proclivity to think more at higher effort levels, especially on later turns in longer sessions—impact token usage. As a result, when replacing Opus 4.6 with Opus 4.7, it can take some tuning to achieve the best performance. A few tweaks to prompts and harnesses can make a big difference. 在我们的 [发布公告](https://www.anthropic.com/news/claude-opus-4-7) 中，我们指出有两项变化会影响令牌使用量——一是更新后的分词器，二是模型在更高算力层级下更倾向于深入思考，尤其是在长会话的后续轮次中。因此，将 Opus 4.6 替换为 Opus 4.7 时，需要进行一些调优才能实现最佳性能。对提示词和工具稍加调整，就能带来显著的效果提升。

This post walks through what’s changed and how to most effectively use Opus 4.7 in Claude Code.这篇文章将介绍有哪些新变化，以及如何在 Claude Code 中最有效地使用 Opus 4.7。

## Structuring interactive coding sessions构建交互式编码会话

Opus 4.7’s token usage and behavior can differ depending on whether you’re deploying more autonomous, asynchronous coding agents with a single user turn or more interactive, synchronous coding agents with multiple user turns. In interactive settings, it reasons more after user turns: this improves its coherence, instruction following, and coding quality over long sessions, but it also tends to use more tokens.Opus 4.7 的令牌使用情况和行为会因部署类型而异：部署自主性更强、仅支持单轮用户交互的异步编码代理，或是交互性更强、支持多轮用户交互的同步编码代理。在交互场景中，它会在每轮用户交互后进行更多推理：这能提升长会话下的连贯性、指令遵循能力和编码质量，但同时也会消耗更多令牌。

To get the most out of Opus 4.7 in Claude Code, we’ve found it’s helpful to treat Claude more like a capable engineer you’re delegating to than a pair programmer you’re guiding line by line:要在 Claude Code 中充分发挥 Opus 4.7 的效能，我们发现一个很有用的做法：与其把 Claude 当成逐行指导的结对程序员，不如将其视为一位你可以委派任务的资深工程师。

- **Specify the task up front, in the first turn.** Well-specified task descriptions that incorporate intent, constraints, acceptance criteria, and relevant file locations give Opus 4.7 the context it needs to deliver stronger outputs. Ambiguous prompts conveyed progressively across many turns tend to reduce both token efficiency and, sometimes, overall quality.**在第一轮就提前明确任务。** 包含意图、约束、验收标准以及相关文件位置的清晰任务描述，能为 Opus 4.7 提供生成优质输出所需的上下文信息。在多轮对话中逐步传递的模糊提示，往往会降低令牌使用效率，有时还会影响整体输出质量。
- **Reduce the number of required user interactions.** Every user turn adds reasoning overhead. Batch your questions and give the model the context it needs to keep moving.**减少所需的用户交互次数。** 每一次用户轮次都会增加推理开销。将你的问题分批处理，并为模型提供使其能够持续推进所需的上下文信息。
- **Use** [**auto mode**](https://claude.com/blog/auto-mode) **when appropriate.** For tasks where you trust the model to execute safely without frequent check-ins, auto mode cuts cycle time. It’s an especially good fit for long-running tasks where you’ve provided full context up front. Auto mode is now available in research preview for Claude Code Max users—you can toggle it on using Shift+Tab.**在** [**合适的情况下使用**](https://claude.com/blog/auto-mode) **自动模式。** 对于你信任模型能安全执行且无需频繁检查的任务，自动模式可缩短周期时间。它特别适合你已提前提供完整上下文的长期运行任务。自动模式目前面向 Claude Code Max 用户以研究预览版推出——你可以通过按 Shift+Tab 开启它。
- **Set up notifications for completed tasks**. Ask Claude to play a sound when it’s done with a task, and it can create its own hook-based notifications.**为已完成的任务设置通知** 。让 Claude 在完成任务时播放声音，它还可以创建自己的基于钩子的通知。

## Recommended effort settings for Opus 4.7Opus 4.7 推荐算力设置

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69e10035cf0ea488fe1376c9_a9f300b2.png)

Based on our internal evals, Opus 4.7 outperforms Opus 4.6 across the full effort range, with the largest gains at high and Extended Thinking settings. 根据我们的内部评估，Opus 4.7 在所有难度等级上均优于 Opus 4.6，在高难度设置和扩展思维模式下的提升最为显著。

The default effort level for Opus 4.7 in Claude Code is now xhigh. This is a new effort level between high and max that gives users more control over the tradeoff between reasoning and latency on hard problems. We recommend xhigh for most agentic coding work, especially for intelligence-sensitive tasks like designing APIs and schemas, migrating legacy code, and reviewing large codebases. Claude Code 中 Opus 4.7 的默认算力等级现已设为超高级（xhigh）。这是介于高级（high）和最高级（max）之间的全新算力等级，能让用户更灵活地控制复杂问题上推理能力与响应延迟之间的平衡。我们建议将超高级（xhigh）用于大多数智能体编程工作，尤其是对智能性要求较高的任务，例如设计 API 和架构、迁移遗留代码以及审查大型代码库。

Here’s some additional guidance for each effort level:以下是针对每种努力级别的额外指导：

- **medium and low**: Available for cost-sensitive, latency-sensitive, or tightly scoped work. The model will be less capable on harder tasks than it would be at higher effort levels, but it still outperforms Opus 4.6 running at the same effort level—sometimes with fewer tokens.**中低档位** ：适用于成本敏感、延迟敏感或范围受限的任务。在难度较高的任务上，该模型的能力会低于更高算力档位的表现，但仍优于相同算力档位下运行的 Opus 4.6——有时所需的 token 数量更少。
- **high**: Balances intelligence and cost. Choose high if you’re running concurrent sessions or want to spend less without a large quality drop. **高** ：平衡智能与成本。如果你正在运行并发会话，或者希望在不大幅降低质量的前提下节省成本，请选择高。
- **xhigh (default, recommended)**: The best setting for most coding and agentic uses. It has strong autonomy and intelligence without the runaway token usage that max can produce on long agentic runs.**xhigh（默认，推荐）** ：适用于大多数编码和智能体场景的最佳设置。它具备强大的自主性和智能性，同时不会出现 max 模式在长时间智能体运行中可能产生的无节制令牌消耗问题。
- **max**: Squeezes out additional performance on genuinely hard problems, but shows diminishing returns and is more prone to overthinking. Use it deliberately for tasks like testing the model’s maximum ceiling in evals and for extremely intelligence-sensitive and non-cost-sensitive uses. **最大模式** ：能在真正棘手的问题上榨取额外性能，但会出现收益递减的情况，且更容易陷入过度思考。请针对模型评估中测试其性能上限、以及对智能性要求极高但对成本不敏感的任务，审慎使用该模式。

If you’re upgrading to the new model, we recommend experimenting with effort rather than just porting over an old setting. You can toggle between effort levels during the same task to more effectively manage token usage and reasoning. 如果你要升级到新模型，我们建议尝试调整推理力度，而不是直接沿用旧设置。你可以在同一任务中切换不同的推理力度等级，从而更高效地管理令牌使用和推理过程。

We’ve set the default effort level for Opus 4.7 to xhigh because we believe it’s the best setting for most coding tasks. If you’re an existing Claude Code user but you haven’t manually set your effort level, you’ll be upgraded to xhigh automatically. You can still adjust your effort manually.我们已将 Opus 4.7 的默认工作量级别设为极高（xhigh），因为我们认为这是适用于大多数编码任务的最佳设置。如果您是现有的 Claude Code 用户但尚未手动设置工作量级别，系统将自动为您升级到极高（xhigh）。您仍可以手动调整工作量级别。

## Working with adaptive thinking 运用适应性思维

**Extended Thinking with a fixed thinking budget is not supported in Opus 4.7.** Instead, Opus 4.7 offers adaptive thinking. This makes thinking *optional* at each step and allows the model to decide when to use more thinking based on context. It can respond to simple queries quickly, skip thinking when a step doesn’t benefit from it, and invest its thinking tokens where they’re most likely to be useful. Over an agentic run, this can add up to faster responses and a better user experience.**Opus 4.7 不支持在固定思考预算下进行扩展思考。** 相反，Opus 4.7 提供自适应思考功能。这使得思考在每一步都 *可选* ，并允许模型根据上下文决定何时进行更多思考。它能快速响应简单查询，在某一步无需思考时跳过思考环节，并将思考算力投入到最能发挥作用的地方。在一次智能体运行过程中，这最终能实现更快的响应并带来更优的用户体验。

Adaptive thinking has improved meaningfully in this release—in particular, Opus 4.7 is less prone to overthinking.此版本中的自适应思维能力有了显著提升——具体而言，Opus 4.7 更不容易出现过度思考的情况。

If you want more control over the thinking rate, prompt for it directly:如果你想更好地控制思考速度，直接提出要求即可：

- **If you want more thinking,** try something like, “Think carefully and step-by-step before responding; this problem is harder than it looks.” **如果你想要更深入的思考，** 可以试试这样说：“在回答之前仔细、分步地思考；这个问题比表面看起来更难。”
- **If you want less thinking,** try something like, “Prioritize responding quickly rather than thinking deeply. When in doubt, respond directly.” You’ll save tokens but may lose some accuracy on harder steps. **如果你想减少思考，** 可以试试这样说：“优先快速回应，而非深入思考。不确定时，直接给出回答。”这样能节省令牌，但在较难的步骤上可能会降低准确性。

## Behavior changes worth knowing 值得注意的行为变化

A handful of default behaviors have changed between Opus 4.6 and 4.7 and are worth knowing about if you’ve carefully tuned your prompts or harnesses for the older model.在 Opus 4.6 与 4.7 版本之间，有少数默认行为发生了变化。如果你为旧版本模型精心调整过提示词或工具配置，了解这些变化是很有必要的。

**Response length is calibrated to task complexity.** Opus 4.7 isn’t as default-verbose as Opus 4.6. You can expect shorter answers on simple lookups and longer ones on open-ended analysis. If your use case relies on a specific length or style, state that explicitly in your prompt. We find that positive examples of the voice you want work better than negative “Don’t do this” instructions.**回复长度会根据任务复杂度进行校准。** Opus 4.7 不像 Opus 4.6 那样默认输出内容更冗长。简单查询时你会得到更简短的回答，开放式分析类问题则会得到更长的回答。如果你的使用场景对回复长度或风格有特定要求，请在提示词中明确说明。我们发现，给出你期望的语气的正面示例，比用负面的“不要这样做”类指令效果更好。

**The model calls tools less often and reasons more.** This produces better results in many cases. If you want *more* tool use (say, more aggressive search or file reading during agentic work), provide guidance that explicitly describes when and why the tool should be used.**该模型调用工具的频率更低，推理能力更强。** 这在很多情况下能产生更好的结果。如果你希望 *更多* 地使用工具（例如在智能体工作中进行更激进的搜索或读取文件），请提供明确说明工具使用时机和原因的指导。

**It spawns fewer subagents by default.** Opus 4.7 tends to be more judicious about when to delegate work to subagents. If your use case benefits from parallel subagents (for example, fanning out across files or independent items), we recommend spelling that out. For example:**默认情况下它生成的子智能体数量更少。** Opus 4.7 在何时将工作委托给子智能体方面往往更为审慎。如果你的使用场景能从并行子智能体中获益（例如，跨文件分发或处理独立项），我们建议明确说明这一点。例如：

Do not spawn a subagent for work you can complete directly in a single response (e.g., refactoring a function you can already see). Spawn multiple subagents in the same turn when fanning out across items or reading multiple files.对于可直接在单次回复中完成的工作（例如你已能看到的函数重构），无需生成子代理。当需要遍历多个项或读取多个文件时，可在同一轮中生成多个子代理。

## What to try next 下一步尝试方向

Opus 4.7 performs better on long-running tasks than prior models. This makes it a good fit for tasks where supervision used to be the bottleneck, like complex multi-file changes, ambiguous debugging, code review across a service, and multi-step agentic work.Opus 4.7 在长期运行的任务上表现优于之前的模型。这使其非常适合过去监督是瓶颈的任务，例如复杂的多文件修改、模糊调试、跨服务代码审查以及多步智能体工作。

We recommend keeping effort at xhigh and seeing how far your first turn takes you.我们建议将精力保持在极高水平，看看你的第一轮尝试能走多远。

*Learn more in our* [*Opus 4.7 prompting guide*](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) *and our article on* [*context and session management*](https://claude.com/blog/using-claude-code-session-management-and-1m-context) *in Claude Code.**在我们的* [*Opus 4.7 提示指南*](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) *以及关于* [*Claude Code 中的上下文与会话管理*](https://claude.com/blog/using-claude-code-session-management-and-1m-context) 的文章中了解更多信息。