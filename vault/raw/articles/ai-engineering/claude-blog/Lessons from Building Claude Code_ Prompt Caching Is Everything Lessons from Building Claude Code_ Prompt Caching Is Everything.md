---
title: "Lessons from Building Claude Code: Prompt Caching Is Everything Lessons from Building Claude Code: Prompt Caching Is Everything"
source: "https://x.com/trq212/status/2024574133011673516"
author:
  - "[[@trq212]]"
published: 2026-02-20
created: 2026-04-16
description: "It is often said in engineering that \"Cache Rules Everything Around Me\", and the same rule holds for agents.It is often said in engineering ..."
tags:
  - "clippings"
---
![Image](https://pbs.twimg.com/media/HBixJgAbsAAM61V?format=jpg&name=large)

It is often said in engineering that "Cache Rules Everything Around Me", and the same rule holds for agents.It is often said in engineering that "Cache Rules Everything Around Me", and the same rule holds for agents.

Long running agentic products like Claude Code are made feasible by **prompt caching** which allows us to reuse computation from previous roundtrips and significantly decrease latency and cost. Long running agentic products like Claude Code are made feasible by **prompt caching** which allows us to reuse computation from previous roundtrips and significantly decrease latency and cost.

What is prompt caching, how does it work and how do you implement it technically? [Read more in @RLanceMartin's piece on prompt caching and our new auto-caching launch.Read more in @RLanceMartin's piece on prompt caching and our new auto-caching launch.](https://x.com/RLanceMartin/status/2024573404888911886)What is prompt caching, how does it work and how do you implement it technically? [Read more in @RLanceMartin's piece on prompt caching and our new auto-caching launch.](https://x.com/RLanceMartin/status/2024573404888911886)

At Claude Code, we build our entire harness around prompt caching. A high prompt cache hit rate decreases costs and helps us create more generous rate limits for our subscription plans, so we run alerts on our prompt cache hit rate and declare SEVs if they're too low.At Claude Code, we build our entire harness around prompt caching. A high prompt cache hit rate decreases costs and helps us create more generous rate limits for our subscription plans, so we run alerts on our prompt cache hit rate and declare SEVs if they're too low.

These are the (often unintuitive) lessons we've learned from optimizing prompt caching at scale.These are the (often unintuitive) lessons we've learned from optimizing prompt caching at scale.

## Lay Out Your Prompt for CachingLay Out Your Prompt for Caching

![Image](https://pbs.twimg.com/media/HBipHa1boAAXD_A?format=jpg&name=large)

Prompt caching works by prefix matching — the API caches everything from the start of the request up to each cache\_control breakpoint. This means the order you put things in matters enormously, you want as many of your requests to share a prefix as possible.Prompt caching works by prefix matching — the API caches everything from the start of the request up to each cache\_control breakpoint. This means the order you put things in matters enormously, you want as many of your requests to share a prefix as possible.

The best way to do this is static content first, dynamic content last. For Claude Code this looks like:The best way to do this is static content first, dynamic content last. For Claude Code this looks like:

1. **Static system prompt** & Tools (globally cached)**Static system prompt** & Tools (globally cached)
2. **Claude.MD** (cached within a project)**Claude.MD** (cached within a project)
3. **Session context** (cached within a session)**Session context** (cached within a session)
4. **Conversation messagesConversation messages**

This way we maximize how many sessions share cache hits.This way we maximize how many sessions share cache hits.

But this can be surprisingly fragile! Examples of reasons we’ve broken this ordering before include: putting an in-depth timestamp in the static system prompt, shuffling tool order definitions non-deterministically, updating parameters of tools (e.g. what agents the AgentTool can call), etc.But this can be surprisingly fragile! Examples of reasons we’ve broken this ordering before include: putting an in-depth timestamp in the static system prompt, shuffling tool order definitions non-deterministically, updating parameters of tools (e.g. what agents the AgentTool can call), etc.

## Use Messages for UpdatesUse Messages for Updates

There may be times when the information you put in your prompt becomes out of date, for example if you have the time or if the user changes a file. It may be tempting to update the prompt, but that would result in a cache miss and could end up being quite expensive for the user.There may be times when the information you put in your prompt becomes out of date, for example if you have the time or if the user changes a file. It may be tempting to update the prompt, but that would result in a cache miss and could end up being quite expensive for the user.

Consider if you can pass in this information via messages in the next turn instead. In Claude Code, we add a <system-reminder> tag in the next user message or tool result with the updated information for the model (e.g. it is now Wednesday), which helps preserve the cache.Consider if you can pass in this information via messages in the next turn instead. In Claude Code, we add a <system-reminder> tag in the next user message or tool result with the updated information for the model (e.g. it is now Wednesday), which helps preserve the cache.

## Don't change Models Mid-SessionDon't change Models Mid-Session

Prompt caches are unique to models and this can make the math of prompt caching quite unintuitive.Prompt caches are unique to models and this can make the math of prompt caching quite unintuitive.

If you're 100k tokens into a conversation with Opus and want to ask a question that is fairly easy to answer, it would actually be more expensive to switch to Haiku than to have Opus answer, because we would need to rebuild the prompt cache for Haiku.If you're 100k tokens into a conversation with Opus and want to ask a question that is fairly easy to answer, it would actually be more expensive to switch to Haiku than to have Opus answer, because we would need to rebuild the prompt cache for Haiku.

If you need to switch models, the best way to do it is with subagents, where Opus would prepare a "handoff" message to another model on the task that it needs done. We do this often with the Explore agents in Claude Code which use Haiku.If you need to switch models, the best way to do it is with subagents, where Opus would prepare a "handoff" message to another model on the task that it needs done. We do this often with the Explore agents in Claude Code which use Haiku.

## Never Add or Remove Tools Mid-SessionNever Add or Remove Tools Mid-Session

Changing the tool set in the middle of a conversation is one of the most common ways people break prompt caching. It seems intuitive — you should only give the model tools you think it needs right now. But because tools are part of the cached prefix, adding or removing a tool invalidates the cache for the entire conversation.Changing the tool set in the middle of a conversation is one of the most common ways people break prompt caching. It seems intuitive — you should only give the model tools you think it needs right now. But because tools are part of the cached prefix, adding or removing a tool invalidates the cache for the entire conversation.

**Plan Mode — Design Around the CachePlan Mode — Design Around the Cache**

Plan mode is a great example of designing features around caching constraints. The intuitive approach would be: when the user enters plan mode, swap out the tool set to only include read-only tools. But that would break the cache.Plan mode is a great example of designing features around caching constraints. The intuitive approach would be: when the user enters plan mode, swap out the tool set to only include read-only tools. But that would break the cache.

Instead, we keep all tools in the request at all times and use EnterPlanMode and ExitPlanMode as tools themselves. When the user toggles plan mode on, the agent gets a system message explaining that it's in plan mode and what the instructions are — explore the codebase, don't edit files, call ExitPlanMode when the plan is complete. The tool definitions never change.Instead, we keep all tools in the request at all times and use EnterPlanMode and ExitPlanMode as tools themselves. When the user toggles plan mode on, the agent gets a system message explaining that it's in plan mode and what the instructions are — explore the codebase, don't edit files, call ExitPlanMode when the plan is complete. The tool definitions never change.

This has a bonus benefit: because EnterPlanMode is a tool the model can call itself, it can autonomously enter plan mode when it detects a hard problem, without any cache break.This has a bonus benefit: because EnterPlanMode is a tool the model can call itself, it can autonomously enter plan mode when it detects a hard problem, without any cache break.

**Tool Search — Defer Instead of RemoveTool Search — Defer Instead of Remove**

The same principle applies to our tool search feature. Claude Code can have dozens of MCP tools loaded, and including all of them in every request would be expensive. But removing them mid-conversation would break the cache.The same principle applies to our tool search feature. Claude Code can have dozens of MCP tools loaded, and including all of them in every request would be expensive. But removing them mid-conversation would break the cache.

Our solution: defer\_loading. Instead of removing tools, we send lightweight stubs — just the tool name, with defer\_loading: true — that the model can "discover" via a ToolSearch tool when needed. The full tool schemas are only loaded when the model selects them. This keeps the cached prefix stable: the same stubs are always present in the same order.Our solution: defer\_loading. Instead of removing tools, we send lightweight stubs — just the tool name, with defer\_loading: true — that the model can "discover" via a ToolSearch tool when needed. The full tool schemas are only loaded when the model selects them. This keeps the cached prefix stable: the same stubs are always present in the same order.

Luckily you can use the [tool searchtool search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool) tool through our API to simplify this.Luckily you can use the [tool search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool) tool through our API to simplify this.

## Forking Context — CompactionForking Context — Compaction

![Image](https://pbs.twimg.com/media/HBitEdRbUAMVSnM?format=jpg&name=large)

Compaction is what happens when you run out of the context window. We summarize the conversation so far and continue a new session with that summary.Compaction is what happens when you run out of the context window. We summarize the conversation so far and continue a new session with that summary.

Surprisingly, compaction has many edge cases with prompt caching that can be unintuitive.Surprisingly, compaction has many edge cases with prompt caching that can be unintuitive.

In particular, when we compact we need to send the entire conversation to the model to generate a summary. If this is a separate API call with a different system prompt and no tools (which is the simple implementation), the cached prefix from the main conversation doesn't match at all. You pay full price for all those input tokens, drastically increasing the cost for the user.In particular, when we compact we need to send the entire conversation to the model to generate a summary. If this is a separate API call with a different system prompt and no tools (which is the simple implementation), the cached prefix from the main conversation doesn't match at all. You pay full price for all those input tokens, drastically increasing the cost for the user.

**The Solution — Cache-Safe ForkingThe Solution — Cache-Safe Forking**

When we run compaction, we use the exact same system prompt, user context, system context, and tool definitions as the parent conversation. We prepend the parent's conversation messages, then append the compaction prompt as a new user message at the end.When we run compaction, we use the exact same system prompt, user context, system context, and tool definitions as the parent conversation. We prepend the parent's conversation messages, then append the compaction prompt as a new user message at the end.

From the API's perspective, this request looks nearly identical to the parent's last request — same prefix, same tools, same history — so the cached prefix is reused. The only new tokens are the compaction prompt itself.From the API's perspective, this request looks nearly identical to the parent's last request — same prefix, same tools, same history — so the cached prefix is reused. The only new tokens are the compaction prompt itself.从 API 的角度来看，此请求与父级的上一次请求几乎完全相同——相同的前缀、相同的工具、相同的历史记录——因此会复用缓存的前缀。唯一新增的标记就是压缩提示本身。

This does mean however that we need to save a "compaction buffer" so that we have enough room in the context window to include the compact message and the summary output tokens.This does mean however that we need to save a "compaction buffer" so that we have enough room in the context window to include the compact message and the summary output tokens.不过这确实意味着我们需要保存一个“压缩缓冲区”，这样我们就能在上下文窗口中留出足够空间，以容纳压缩后的消息以及摘要的输出标记。

Compaction is tricky but luckily, you don't need to learn these lessons yourself — based on our learnings from Claude Code we built [compaction compaction 压缩](https://platform.claude.com/docs/en/build-with-claude/compaction#prompt-caching) directly into the API, so you can apply these patterns in your own applications.Compaction is tricky but luckily, you don't need to learn these lessons yourself — based on our learnings from Claude Code we built [compaction](https://platform.claude.com/docs/en/build-with-claude/compaction#prompt-caching) directly into the API, so you can apply these patterns in your own applications.压缩操作颇具挑战性，但幸运的是，你无需亲自摸索这些经验——基于我们从 Claude Code 中获得的经验，我们直接在 API 中内置了[压缩](https://platform.claude.com/docs/en/build-with-claude/compaction#prompt-caching)功能，因此你可以在自己的应用程序中应用这些模式。

## Lessons LearnedLessons Learned 经验总结

1. **Prompt caching is a prefix match.** Any change anywhere in the prefix invalidates everything after it. Design your entire system around this constraint. Get the ordering right and most of the caching works for free.**Prompt caching is a prefix match.** Any change anywhere in the prefix invalidates everything after it. Design your entire system around this constraint. Get the ordering right and most of the caching works for free.提示缓存采用前缀匹配机制。前缀中任意位置的更改都会使其后的所有内容失效。请围绕这一约束设计整个系统。只要排序合理，大部分缓存功能都能自动实现。
2. **Use messages instead of system prompt changes**. You may be tempted to edit the system prompt to do things like entering plan mode, changing the date, etc. but it would actually be better to insert these into messages during the conversation.**Use messages instead of system prompt changes**. You may be tempted to edit the system prompt to do things like entering plan mode, changing the date, etc. but it would actually be better to insert these into messages during the conversation.使用消息而非修改系统提示。你可能会想通过编辑系统提示来进入计划模式、修改日期等操作，但实际上在对话过程中将这些指令插入到消息中会更好。
3. **Don't change tools or models mid-conversation.** Use tools to model state transitions (like plan mode) rather than changing the tool set. Defer tool loading instead of removing tools.**Don't change tools or models mid-conversation.** Use tools to model state transitions (like plan mode) rather than changing the tool set. Defer tool loading instead of removing tools.不要在对话中途更换工具或模型。应使用工具来实现模型状态转换（如规划模式），而非更换工具集。延迟加载工具，而非移除工具。
4. **Monitor your cache hit rate like you monitor uptime.** We alert on cache breaks and treat them as incidents. A few percentage points of cache miss rate can dramatically affect cost and latency.**Monitor your cache hit rate like you monitor uptime.** We alert on cache breaks and treat them as incidents. A few percentage points of cache miss rate can dramatically affect cost and latency.像监控正常运行时间一样监控缓存命中率。我们会在缓存出现中断时发出警报，并将其视为故障事件。缓存未命中率仅几个百分点的变化，就可能对成本和延迟产生显著影响。
5. **Fork operations need to share the parent's prefix.** If you need to run a side computation (compaction, summarization, skill execution), use identical cache-safe parameters so you get cache hits on the parent's prefix.**Fork operations need to share the parent's prefix.** If you need to run a side computation (compaction, summarization, skill execution), use identical cache-safe parameters so you get cache hits on the parent's prefix.Fork 操作需要共享父进程的前缀。如果需要执行辅助计算（压缩、汇总、技能执行），请使用相同的缓存安全参数，以便在父进程前缀上实现缓存命中。

Claude Code is built around prompt caching from day one, you should do the same if you’re building an agent.Claude Code is built around prompt caching from day one, you should do the same if you’re building an agent.Claude Code 从一开始就围绕提示词缓存构建，如果你正在构建一个智能体，也应该这么做。