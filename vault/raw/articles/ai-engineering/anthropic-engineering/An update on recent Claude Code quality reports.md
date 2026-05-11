---
title: "An update on recent Claude Code quality reports"
source: "https://www.anthropic.com/engineering/april-23-postmortem"
author:
published:
created: 2026-04-24
description: "Anthropic is an AI safety and research company that's working to build reliable, interpretable, and steerable AI systems."
tags:
  - "clippings"
---
Over the past month, we’ve been looking into reports that Claude’s responses have worsened for some users. We’ve traced these reports to three separate changes that affected Claude Code, the Claude Agent SDK, and Claude Cowork. The API was not impacted.过去一个月，我们一直在调查有关部分用户反馈 Claude 回复质量下降的情况。经排查，这些反馈源于三项独立的变更，分别影响了 Claude 代码、Claude 智能体软件开发工具包（SDK）以及 Claude 协同办公工具。应用程序编程接口（API）未受影响。

All three issues have now been resolved as of April 20 (v2.1.116).截至4月20日（v2.1.116版本），这三个问题均已全部解决。

In this post, we explain what we found, what we fixed, and what we’ll do differently to ensure similar issues are much less likely to happen again.在这篇博文中，我们会说明我们的发现、修复的问题，以及我们将做出哪些改变，以确保类似问题再次发生的可能性大幅降低。

We take reports about degradation very seriously. We never intentionally degrade our models, and we were able to immediately confirm that our API and inference layer were unaffected.我们非常重视有关模型性能下降的报告。我们从未故意降低模型性能，并且我们能够立即确认我们的API和推理层未受任何影响。

After investigation, we identified three different issues:经过调查，我们发现了三个不同的问题：

1. On March 4, we changed Claude Code's default reasoning effort from `high` to `medium` to reduce the very long latency—enough to make the UI appear frozen—some users were seeing in `high` mode. This was the wrong tradeoff. We reverted this change on April 7 after users told us they'd prefer to default to higher intelligence and opt into lower effort for simple tasks. This impacted Sonnet 4.6 and Opus 4.6.3月4日，我们将Claude Code的默认推理工作量从 `high` 调整为 `medium` ，以降低过长的延迟——这种延迟曾导致部分用户在 `high` 模式下出现界面卡顿的情况。但这是一个错误的权衡。4月7日，在用户反馈更倾向于默认使用更高智能级别、并愿意为简单任务选择较低推理工作量后，我们恢复了这一更改。此调整影响了Sonnet 4.6和Opus 4.6版本。
2. On March 26, we shipped a change to clear Claude's older thinking from sessions that had been idle for over an hour, to reduce latency when users resumed those sessions. A bug caused this to keep happening every turn for the rest of the session instead of just once, which made Claude seem forgetful and repetitive. We fixed it on April 10. This affected Sonnet 4.6 and Opus 4.6.3月26日，我们推出了一项更新，用于清除闲置超过一小时的会话中Claude的旧思考内容，以减少用户恢复这些会话时的延迟。一个漏洞导致该操作在会话剩余的每一轮中都持续发生，而非仅执行一次，这使得Claude表现出健忘和重复的问题。我们已于4月10日修复了该问题。此问题影响了Sonnet 4.6和Opus 4.6版本。
3. On April 16, we added a system prompt instruction to reduce verbosity. In combination with other prompt changes, it hurt coding quality and was reverted on April 20. This impacted Sonnet 4.6, Opus 4.6, and Opus 4.7.4月16日，我们添加了一条系统提示指令以减少冗余表述。结合其他提示词修改，这一操作降低了编码质量，因此我们于4月20日将其恢复。此次调整对Sonnet 4.6、Opus 4.6以及Opus 4.7产生了影响。

Because each change affected a different slice of traffic on a different schedule, the aggregate effect looked like broad, inconsistent degradation. While we began investigating reports in early March, they were challenging to distinguish from normal variation in user feedback at first, and neither our internal usage nor evals initially reproduced the issues identified.由于每一次变更都在不同时间节点影响了不同范围的流量，整体影响呈现出大范围、无规律的性能下降。我们从3月初就开始调查相关反馈，但起初这些反馈很难与用户反馈中的正常波动区分开，且无论是内部实际使用还是评估测试，最初都未能复现所发现的问题。

This isn’t the experience users should expect from Claude Code. As of April 23, we’re resetting usage limits for all subscribers.这并非用户在使用 Claude Code 时应有的体验。自 4 月 23 日起，我们将重置所有订阅用户的使用限额。

## A change to Claude Code's default reasoning effort对 Claude Code 默认推理强度的调整

When we released Opus 4.6 in Claude Code in February, we set the default reasoning effort to `high`.2月我们在Claude Code中推出Opus 4.6版本时，已将默认推理强度设为 `high` 。

Soon after, we received user feedback that Claude Opus 4.6 in high effort mode would occasionally think for too long, causing the UI to appear frozen and leading to disproportionate latency and token usage for those users.不久之后，我们收到了用户反馈，称处于高算力模式的 Claude Opus 4.6 偶尔会思考过久，导致界面（UI）看起来处于冻结状态，还让这些用户的延迟和令牌使用量异常偏高。

In general, the longer the model thinks, the better the output. Effort levels are how Claude Code lets users set that tradeoff—more thinking versus lower latency and fewer usage limit hits. As we calibrate effort levels for our models, we take this tradeoff into account in order to pick points along the test-time-compute curve that give people the best range of options. In the product layer, we then choose which point along this curve we set as our default, and that is the value we send to the Messages API as the effort parameter; we then make the other options available via `/effort`.通常来说，模型思考的时间越长，输出的结果就越好。努力等级是 Claude Code 让用户设定这种权衡的方式——更多的思考时间对应着更低的延迟和更少的使用限额触发次数。在为模型校准努力等级时，我们会考虑这一权衡，以便在测试时计算曲线上选取能为用户提供最佳选择范围的点。随后在产品层，我们会确定将曲线上的哪个点设为默认值，这个值会作为努力参数传递给 Messages API；而其他选项则通过 `/effort` 提供。

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fde3bcf9733b61f57234d8c45e663b1bd48677ea1-3840x2160.png&w=3840&q=75)

In our internal evals and testing, medium effort achieved slightly lower intelligence with significantly less latency for the majority of tasks. It also didn’t suffer from the same issues with occasional very long tail latencies for thinking, and it helped maximize users’ usage limits. As a result, we rolled out a change making medium the default effort, and explained the rationale via in-product dialog.在我们的内部评估和测试中，中等力度模式在大多数任务上实现了略低的智能水平，同时延迟显著降低。它也没有出现思考时偶尔出现的超长尾延迟问题，并且有助于最大化用户的使用限额。因此，我们推出了一项更改，将中等力度设为默认模式，并通过产品内对话框说明了这样做的基本原理。

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F459b2a8a0baa88937eebcbe4566dde4d6cc7f185-3794x2260.png&w=3840&q=75)

Soon after rolling out, users began reporting that Claude Code felt less intelligent. We shipped a number of design iterations to make the current effort setting clearer in order to alert people they could change the default (notices on startup, an inline effort selector, and bringing back ultrathink), but most users retained the medium effort default.推出后不久，用户就反馈 Claude Code 的智能程度有所下降。我们推出了多项设计迭代方案，以明确当前的工作量设置，从而提醒用户可以修改默认设置（包括启动时的提示、嵌入式工作量选择器，以及恢复 ultrathin 功能），但大多数用户仍保留了中等工作量的默认设置。

After hearing feedback from more customers, we reversed this decision on April 7. All users now default to `xhigh` effort for Opus 4.7, and `high` effort for all other models.在收到更多客户的反馈后，我们于4月7日撤销了这一决定。现在所有用户默认对Opus 4.7使用 `xhigh` 算力，对其他所有模型使用 `high` 算力。

## A caching optimization that dropped prior reasoning一项移除了先前推理的缓存优化

When Claude reasons through a task, that reasoning is normally kept in the conversation history so that on every subsequent turn, Claude can see why it made the edits and tool calls it did.当Claude对一项任务进行推理时，其推理过程通常会保留在对话历史中，这样在后续的每一轮对话中，Claude都能清楚自己为何做出了相应的编辑和工具调用。

On March 26, we shipped what was meant to be an efficiency improvement to this feature. We use prompt caching to make back-to-back API calls cheaper and faster for users. Claude writes the input tokens to the cache when it makes an API request, then after a period of inactivity the prompt is evicted from cache, making room for other prompts. Cache utilization is something we manage carefully (more on our [approach](https://x.com/trq212/status/2024574133011673516)).3月26日，我们推出了一项旨在提升该功能效率的改进。我们采用提示词缓存技术，为用户降低连续API调用的成本并提升其速度。Claude在发起API请求时会将输入标记写入缓存，随后经过一段非活动期，提示词会从缓存中移除，为其他提示词腾出空间。缓存的利用率是我们精心管控的（有关我们的 [方法](https://x.com/trq212/status/2024574133011673516) ，详见下文）。

The design should have been simple: if a session has been idle for more than an hour, we could reduce users’ cost of resuming that session by clearing old thinking sections. Since the request would be a cache miss anyway, we could prune unnecessary messages from the request to reduce the number of uncached tokens sent to the API. We’d then resume sending full reasoning history. To do this we used the `clear_thinking_20251015` API header along with `keep:1`.设计本应很简单：如果某个会话闲置超过一小时，我们可以通过清除旧的思考部分来降低用户恢复该会话的成本。由于该请求无论如何都会是缓存未命中，我们可以从请求中剔除不必要的消息，以减少发送到 API 的未缓存令牌数量。之后我们会恢复发送完整的推理历史。为此，我们使用了 \` `clear_thinking_20251015` \` API 标头以及 \` `keep:1` \`。

The implementation had a bug. Instead of clearing thinking history once, it cleared it on every turn for the rest of the session. After a session crossed the idle threshold once, each request for the rest of that process told the API to keep only the most recent block of reasoning and discard everything before it. This compounded: if you sent a follow-up message while Claude was in the middle of a tool use, that started a new turn under the broken flag, so even the reasoning from the current turn was dropped. Claude would continue executing, but increasingly without memory of why it had chosen to do what it was doing. This surfaced as the forgetfulness, repetition, and odd tool choices people reported.该实现存在一个漏洞。它并非只清除一次思考历史，而是在会话剩余的每一轮都进行清除。一旦某个会话首次超过空闲阈值，该会话剩余过程中的每一次请求都会指示 API 仅保留最新的推理块，并丢弃之前的所有内容。问题还进一步加剧：如果在 Claude 正在使用工具时发送后续消息，就会在错误标记下开启新一轮，即便当前轮次的推理内容也会被丢弃。Claude 会继续执行，但对自身行为的决策缘由会越来越缺乏记忆。这也正是用户反馈的健忘、重复回答以及工具选择异常等问题的根源。

Because this would continuously drop thinking blocks from subsequent requests, those requests also resulted in cache misses. We believe this is what drove the separate reports of usage limits draining faster than expected.由于这会持续删除后续请求的思考块，这些请求也导致了缓存未命中。我们认为这就是为何有单独报告称使用限制消耗速度快于预期的原因。

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F332d9c487bb73c8078686068dcbe1b616720a8dd-3016x1198.png&w=3840&q=75)

Two unrelated experiments made it challenging for us to reproduce the issue at first: an internal-only server-side experiment related to message queuing; and an orthogonal change in how we display thinking suppressed this bug in most CLI sessions, so we didn’t catch it even when testing external builds.两项不相关的实验起初让我们难以复现该问题：一项是与消息队列相关的仅限内部使用的服务端实验；另一项是关于思维显示方式的正交变更，这项变更在大多数命令行界面会话中消除了该漏洞，因此即便在测试外部版本时我们也未能发现它。

This bug was at the intersection of Claude Code’s context management, the Anthropic API, and extended thinking. The changes it introduced made it past multiple human and automated code reviews, as well as unit tests, end-to-end tests, automated verification, and dogfooding. Combined with this only happening in a corner case (stale sessions) and the difficulty of reproducing the issue, it took us over a week to discover and confirm the root cause.这个漏洞出现在 Claude Code 的上下文管理、Anthropic API 以及扩展思考功能的交叉点。它所引入的修改通过了多轮人工和自动化代码审查，同时也通过了单元测试、端到端测试、自动化验证和内部 dogfooding 测试。再加上该问题仅出现在特定边缘场景（过期会话）中，且复现难度较大，我们花了一周多时间才发现并确认根本原因。

As part of the investigation, we back-tested [Code Review](https://code.claude.com/docs/en/code-review) against the offending pull requests using Opus 4.7. When provided the code repositories necessary to gather complete context, Opus 4.7 found the bug, while Opus 4.6 didn't. To prevent this from happening again, we are now landing support for additional repositories as context for code reviews.作为调查的一部分，我们使用 Opus 4.7 针对有问题的拉取请求对 [代码审查](https://code.claude.com/docs/en/code-review) 进行了回测。在提供了用于收集完整上下文所需的代码仓库后，Opus 4.7 成功发现了该漏洞，而 Opus 4.6 则未能做到。为防止此类情况再次发生，我们目前正在新增对将额外代码仓库作为代码审查上下文的支持。

We fixed this bug on April 10 in v2.1.101.我们已于4月10日在v2.1.101版本中修复了此漏洞。

## A system prompt change to reduce verbosity一项减少冗余的系统提示词修改

Our latest model, Claude Opus 4.7, has a notable behavioral quirk relative to its predecessor: as we [wrote about](https://www.anthropic.com/news/claude-opus-4-7) at launch, it tends to be quite verbose. This makes it smarter on hard problems, but it also produces more output tokens.我们的最新模型 Claude Opus 4.7 相较于其前代版本有一个明显的行为特点：正如我们在发布时 [撰写的内容](https://www.anthropic.com/news/claude-opus-4-7) 所述，它往往会输出大量内容。这让它在解决复杂问题时更具优势，但同时也会生成更多的输出令牌。

A few weeks before we released Opus 4.7, we started tuning Claude Code in preparation. Each model behaves slightly differently, and we spend time before each release optimizing the harness and product for it.在我们发布 Opus 4.7 之前的几周，我们开始优化 Claude Code 以做准备。每个模型的表现都略有不同，因此我们会在每次发布前花时间为其优化测试框架和产品。

We have a number of tools to reduce verbosity: model training, prompting, and improving thinking UX in the product. Ultimately we used all of these, but one addition to the system prompt caused an outsized effect on intelligence in Claude Code:我们有多种工具来减少冗余：模型训练、提示工程以及优化产品中的思维用户体验。最终我们采用了所有这些方法，但对系统提示的一项补充，对 Claude Code 的智能水平产生了显著影响：

> *“Length limits: keep text between tool calls to ≤25 words. Keep final responses to ≤100 words unless the task requires more detail.” “长度限制：工具调用之间的文本不超过25个单词。除非任务需要更多细节，否则最终回复不超过100个单词。”*

After multiple weeks of internal testing and no regressions in the set of evaluations we ran, we felt confident about the change and shipped it alongside Opus 4.7 on April 16.经过数周的内部测试，且我们执行的一系列评估中未出现任何回归问题，我们对此次修改充满信心，并于4月16日随Opus 4.7版本一同正式发布。

As part of this investigation, we ran more ablations (removing lines from the system prompt to understand the impact of each line) using a broader set of evaluations. One of these evaluations showed a 3% drop for both Opus 4.6 and 4.7. We immediately reverted the prompt as part of the April 20 release.作为本次调查的一部分，我们开展了更多的消融实验（从系统提示词中删除内容，以了解每一行内容的影响），并采用了更广泛的评估指标。其中一项评估显示，Opus 4.6 和 4.7 的性能均下降了3%。作为4月20日版本发布的一部分，我们立即恢复了原提示词。

## Going forward 未来展望

We are going to do several things differently to avoid these issues: we’ll ensure that a larger share of internal staff use the exact public build of Claude Code (as opposed to the version we use to test new features); and we'll make improvements to our [Code Review](https://code.claude.com/docs/en/code-review) tool that we use internally, and ship this improved version to customers.我们将从几个方面做出改变以避免这些问题：我们会确保更多内部员工使用 Claude Code 的正式公开版本（而非我们用于测试新功能的版本）；同时我们会对内部使用的 [代码审查](https://code.claude.com/docs/en/code-review) 工具进行改进，并将这个升级版提供给客户。

We’re also adding tighter controls on system prompt changes. We will run a broad suite of per-model evals for every system prompt change to Claude Code, continuing ablations to understand the impact of each line, and we have built new tooling to make prompt changes easier to review and audit. We've additionally added guidance to our CLAUDE.md to ensure model-specific changes are gated to the specific model they're targeting. For any change that could trade off against intelligence, we'll add soak periods, a broader eval suite, and gradual rollouts so we catch issues earlier.我们还在对系统提示词的修改增加更严格的控制。针对 Claude Code 的每一次系统提示词修改，我们都会运行一套全面的单模型评估，持续进行消融实验以理解每一行修改的影响，并且我们已开发新工具来简化提示词修改的审查与审计工作。此外，我们在 CLAUDE.md 中补充了指导原则，确保针对特定模型的修改仅应用于目标模型。对于任何可能影响模型智能性的修改，我们都会设置试运行期、开展更全面的评估并逐步推送，以便尽早发现问题。

We recently created @ClaudeDevs on X to give us the room to explain product decisions and the reasoning behind them in depth. We'll share the same updates in centralized threads on GitHub.我们最近在 X 平台上创建了 @ClaudeDevs 账号，以便有足够空间深入解释产品决策及其背后的逻辑。我们也会在 GitHub 的集中式讨论帖中同步相同的最新动态。

Finally, we’d like to thank our users: the people who used the `/feedback` command to share their issues with us (or who posted specific, reproducible examples online) are the ones who ultimately allowed us to identify and fix these problems. Today we are resetting usage limits for all subscribers.最后，我们要感谢我们的用户：那些使用 `/feedback` 命令向我们分享问题（或在网上发布具体、可复现示例）的用户，正是他们最终帮助我们发现并修复了这些问题。今天，我们将重置所有订阅者的使用限制。

We’re immensely grateful for your feedback and for your patience.我们非常感谢您的反馈和耐心。