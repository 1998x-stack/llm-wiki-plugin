---
title: "Using Claude Code: session management and 1M context"
source: "https://claude.com/blog/using-claude-code-session-management-and-1m-context"
author:
published: 2001-04-15
created: 2026-04-17
description: "Learn how to manage context in Claude Code—when to continue, rewind, compact, or clear a session, and how subagents keep parent context clean."
tags:
  - "clippings"
---
We released **`/usage`**, a new slash command to help you understand your usage with Claude Code. This feature was informed by a number of conversations with customers. 我们推出了 **`/usage`** 这一新的斜杠命令，帮助你了解在 Claude Code 中的使用情况。推出这一功能的灵感，来自于我们与众多客户的多次沟通。

What came up again and again in these calls is that there is a lot of variance in how users manage their sessions, especially with our new update to 1 million context in Claude Code.在这些通话中反复出现的一个问题是，用户管理会话的方式存在很大差异，尤其是在我们将 Claude Code 的上下文更新至 100 万之后。

Do you only use one session or two sessions that you keep open in a terminal? Do you start a new session with every prompt? When do you use [compact](https://platform.claude.com/docs/en/build-with-claude/compaction), rewind or [subagents](https://code.claude.com/docs/en/sub-agents)? What causes a bad compact or bad session?你是只在终端中使用一个会话，还是会保持两个会话同时打开？你是每次都开启新会话来进行提示吗？你会在什么情况下使用 [紧凑模式](https://platform.claude.com/docs/en/build-with-claude/compaction) 、回退操作或 [子智能体](https://code.claude.com/docs/en/sub-agents) ？是什么原因导致出现无效的紧凑模式或会话异常的？

There’s a surprising amount of detail here that can really shape your experience with [Claude Code](https://code.claude.com/docs/en/overview) and almost all of it comes from [managing your context window](https://code.claude.com/docs/en/how-claude-code-works).这里包含了大量能切实影响你使用 [Claude 代码](https://code.claude.com/docs/en/overview) 体验的细节，而几乎所有这些细节都源于 [管理上下文窗口](https://code.claude.com/docs/en/how-claude-code-works) 。

## A quick primer on context, compaction and context rot上下文、压缩与上下文损耗快速入门

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69e02238a3e7e9532cb643de_image6.png)

The context window is everything the model can "see" at once when generating its next response. It includes your system prompt, the conversation so far, every tool call and its output, and every file that's been read. Claude Code has a context window of one million tokens.上下文窗口是模型在生成下一个响应时可以立即“看到”的所有内容。它包括您的系统提示、到目前为止的对话、每个工具调用及其输出以及每个已读取的文件。克劳德代码有一个包含一百万个令牌的上下文窗口。

Unfortunately, using context has a slight impact on performance, which is often called context rot. Context rot is the observation that model performance degrades as context grows because attention gets spread across more tokens, and older, irrelevant content starts to distract from the current task.遗憾的是，使用上下文会对性能产生轻微影响，这种情况通常被称为上下文退化。上下文退化指的是，随着上下文长度增加，模型的性能会下降——这是因为注意力会分散到更多的标记上，而较早的、不相关的内容会开始干扰当前的任务。

Context windows are a hard cutoff, so when you’re nearing the end of the context window, the task you’ve been working on is automatically summarized into a smaller description and the model continues the work in a new context window. We call this compaction. You can also trigger compaction yourself.上下文窗口有硬性限制，因此当你接近上下文窗口末尾时，你正在处理的任务会自动被总结为一段简短的描述，模型会在新的上下文窗口中继续完成工作。我们将这一过程称为压缩。你也可以手动触发压缩操作。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69e02297f13357d9b32d8312_image5.png)

## Every turn as a branching point 每一步都是一个分支点

Say you've just asked Claude to do something and it's finished—you’ve now got some information in context (tool calls, tool outputs, your instructions) and you have a surprising number of options for what to do next:假设你刚让 Claude 完成了某项任务——此时上下文里已经包含了一些信息（工具调用、工具输出、你的指令），而你接下来可以选择的操作其实有很多种：

- **Continue** — send another message in the same session **继续** — 在同一会话中发送另一条消息
- **`/rewind` (esc esc)** — jump back to a previous message and try again from there **`/rewind` （按两次 esc 键）** — 跳回到上一条消息并从那里重新尝试
- **`/clear`** — start a new session, usually with a brief you've distilled from what you just learned **`/clear`** — 开启新对话，通常会基于你刚学到的内容提炼出简要任务方向
- **Compact** — summarize the session so far and keep going on top of the summary **精简** — 总结当前会话，并在总结的基础上继续进行
- **Subagents** — delegate the next chunk of work to an agent with its own clean context, and only pull its result back in **子智能体** — 将下一部分工作委托给拥有独立干净上下文的智能体，然后仅拉回其结果

While the most natural course is just to continue, the other four options exist to help manage your context.虽然最自然的做法是继续下去，但另外四个选项的存在是为了帮助你管理上下文。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69e022cf45e7f9c9d025756d_image3.png)

## When to start a new session 何时开始新会话

When do you keep a long running session vs starting a new one? Our general rule of thumb is when you start a new task, you should also start a new session.你应该在什么情况下保留长时间会话，而不是开启新会话？我们的通用经验法则是：开始一项新任务时，也应开启一个新会话。

While 1M context windows mean that you can now do longer tasks more reliably, for example building a full-stack app from scratch, context rot may occur. 100万上下文窗口意味着你现在可以更可靠地完成更长的任务，比如从零构建一个全栈应用程序，但这可能会出现上下文衰减的问题。

Sometimes you may do related tasks where some of the context is still necessary, but not always. For example, writing the documentation for a feature you just implemented. While you could start a new session, Claude would have to reread the files that you just implemented, which would be slower and more expensive.有时你可能会处理一些相关任务，其中部分上下文仍然有必要保留，但并非总是如此。例如，为你刚实现的功能编写文档。虽然你可以开启一个新会话，但 Claude 不得不重新读取你刚实现的文件，这会更慢且成本更高。

## Rewinding instead of correcting 回溯而非修正

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69e0234c97977d4944bea810_image4.png)

In Claude Code, double-tapping Esc (or running `/rewind`) lets you jump back to any previous message and re-prompt from there. The messages after that point are dropped from the context. 在 Claude Code 中，双击 Esc 键（或运行 `/rewind` ）可跳回到任意之前的消息并从该处重新提问。该时间点之后的消息会从上下文内容中移除。

Rewind is often the better approach to correction. For example, Claude reads five files, tries an approach, and it doesn't work. Your instinct may be to type "that didn't work, try X instead." But the better move may be to rewind to just after the file reads, and re-prompt with what you learned. "Don't use approach A, the foo module doesn't expose that—go straight to B." 回溯往往是更好的纠错方法。例如，Claude 读取了五个文件，尝试了一种方法却没有奏效。你的第一反应可能是输入“那样不行，换用 X 试试”。但更好的做法或许是回溯到刚读取完文件的节点，再结合你得到的经验重新提示：“不要用方法 A，foo 模块没有开放这个功能——直接用 B 就行。”

You can also use *“summarize from here”* or the `/rewind` slash command to have Claude summarize its learnings and create a handoff message, kind of like a message to the previous iteration of Claude from its future self that tried something and it didn’t work.你也可以使用 *“从这里总结”* 或 `/rewind` 斜杠命令，让Claude总结其所学内容并生成交接消息，这有点像是未来尝试了某方法却未成功的Claude，给上一版本的自己发送的一条消息。

## Compacting vs. launching a fresh session精简会话与开启全新会话

Once a session gets long, you have two ways to shed extraneous context: `/compact` or `/clear` (and start fresh). They feel similar but behave very differently.一旦会话变长，你有两种方法来清除多余的上下文： `/compact` 或 `/clear` （并重新开始）。这两个命令感觉相似，但运行方式却大不相同。

**Compact** asks the model to summarize the conversation so far, then replaces the history with that summary. It's lossy, but you didn't have to write anything yourself and Claude might be more thorough in including important learnings or files. You can also steer it by passing instructions (`/compact focus on the auth refactor, drop the test debugging`).**精简** 会让模型总结目前的对话，然后用该摘要替换对话历史。这种方式会丢失部分信息，但你无需自己撰写任何内容，而且 Claude 可能会更全面地纳入重要的经验或文件。你也可以通过传入指令来引导它（ `/compact focus on the auth refactor, drop the test debugging` ）。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69e02427049669efd6bb7604_image1.png)

With `/clear` *you* write down what matters ("we're refactoring the auth middleware, the constraint is X, the files that matter are A and B, we've ruled out approach Y") and start clean. It's more work, but the resulting context is what you decided was relevant. 有了 `/clear` *你* 就能写下关键内容（“我们正在重构身份验证中间件，限制条件是X，相关文件为A和B，我们已经排除了Y方案”），然后重新开始。这样做更费功夫，但最终的上下文就是你认定的相关内容。

## What causes a bad autocompact? 是什么导致自动压缩效果不佳？

If you run a lot of long-running sessions, you might have noticed times in which compacting might be particularly bad. In this case we’ve often found that bad compacts can happen when the model can’t predict the direction your work is going. 如果你运行大量长时间运行的会话，可能会注意到某些时候压缩操作的影响会格外糟糕。在这种情况下，我们经常发现，当模型无法预测你的工作发展方向时，就可能出现糟糕的压缩情况。

In the example above, autocompact fires after a long debugging session and summarizes the investigation and your next message is "now fix that other warning we saw in bar.ts." 在上面的示例中，autocompact 会在长时间的调试会话后触发，并对调查结果进行总结，而你的下一条消息是“现在修复我们在 bar.ts 中看到的另一个警告。”

But because the session was focused on debugging, the other warning might have been dropped from the summary.但由于本次会议的重点是调试，另一个警告可能已从总结中被剔除。

This is particularly difficult, because due to context rot, the model is at its least intelligent point when compacting. With one million context, you have more time to /compact proactively with a description of what you want to do. 这一点尤其困难，因为由于上下文退化，模型在压缩时处于最不智能的状态。拥有一百万的上下文，你就有更多时间主动进行压缩，并描述你想要完成的操作。

## Subagents and fresh context windows 子智能体与全新上下文窗口

[Subagents](https://claude.com/blog/subagents-in-claude-code) tend to work well when you know in advance that a chunk of work will produce a lot of intermediate output you won't need again.[子智能体](https://claude.com/blog/subagents-in-claude-code) 在你提前知道某部分工作会产生大量不再需要的中间输出时，往往能很好地发挥作用。

When Claude spawns a subagent via the Agent tool, that subagent gets its own fresh context window. It can do as much work as it needs to, and then synthesize its results so only the final report comes back to the parent.当 Claude 通过 Agent 工具生成一个子智能体时，该子智能体会拥有独立的全新上下文窗口。它可以完成所需的全部工作，然后整合结果，最终仅将报告反馈给父智能体。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69e0241044643c5402b312a9_image2.png)

The mental test we use at Anthropic: *will I need this tool output again, or just the conclusion?* 我们在 Anthropic 采用的思维测试： *我是否会再次需要这个工具的输出，还是只需要结论？*

While Claude Code will automatically call subagents, you may want to tell it to explicitly do this. For example, you may want to tell it to:虽然 Claude Code 会自动调用子智能体，但你可能希望明确指示它这样做。例如，你可能希望指示它：

- “Spin up a subagent to verify the result of this work based on the following spec file” “启动一个子代理，根据以下规范文件验证此项工作的结果”
- “Spin off a subagent to read through this other codebase and summarize how it implemented the auth flow, then implement it yourself in the same way” “拆分出一个子代理来通读另一个代码库，总结其实现身份验证流程的方式，然后你自己以相同的方式实现它”
- “Spin off a subagent to write the docs on this feature based on my git changes” “启动一个子代理，根据我的git提交记录编写此功能的文档”

**Putting it together 综合整理**

To help you choose which context management feature to use, we put together this helpful table that outlines common situations, what tool to reach for, and why. 为了帮助你选择要使用的上下文管理功能，我们整理了一份实用的表格，其中列出了常见场景、适用工具及选择原因。

| Situation 场景 | Consider reaching for 可考虑使用 | Why 原因 |
| --- | --- | --- |
| Same task, context is still relevant 同一任务，上下文仍然相关 | Continue 继续 | Everything in the window is still load-bearing; don't pay to rebuild it.窗口内的所有内容仍可承载；无需付费重建。 |
| Claude went down a wrong path Claude 走上了错误的道路 | Rewind (double-Esc) 回退（双击 Esc） | Keep the useful file reads, drop the failed attempt, re-prompt with what you learned.保留有用的文件读取操作，放弃失败的尝试，结合所学到的内容重新进行提示。 |
| Mid-task but the session is bloated with stale debugging/exploration 任务进行中但会话中充斥着过时的调试与探索内容 | `/compact <hint>` | Low effort; Claude decides what mattered. Steer it with instructions if needed.投入精力不足；由 Claude 判定关键内容。必要时通过指令引导它。 |
| Starting a genuinely new task 开启一项全新的任务 | `/clear` | Zero rot; you control exactly what carries forward.无冗余信息；你完全掌控需要保留的内容。 |
| Next step will generate lots of output you'll only need the conclusion from (codebase search, verification, doc writing) 下一步会生成大量输出，你只需从（代码库搜索、验证、文档编写）中获取结论即可 | Subagent 子代理 | Intermediate tool noise stays in the child's context; only the result comes back.中间工具产生的冗余信息保留在子上下文内；仅返回最终结果。 |

We look forward to seeing what you build. 我们期待看到你的成果。

*Get started with* [*Claude Code*](https://code.claude.com/docs/en/overview) *today.**立即开始使用* [*Claude Code*](https://code.claude.com/docs/en/overview) *吧。*

***About the author:*** *Thariq Shihipar is a member of technical staff at Anthropic, working on Claude Code.****作者简介：*** *塔里克·希希帕尔是 Anthropic 公司的技术人员，主要负责 Claude Code 相关工作。*

## Transform how your organization operates with Claude借助 Claude 重塑你的组织运营方式

Product updates, how-tos, community spotlights, and more. Delivered monthly to your inbox.产品更新、操作指南、社区亮点等内容，每月发送至你的收件箱。