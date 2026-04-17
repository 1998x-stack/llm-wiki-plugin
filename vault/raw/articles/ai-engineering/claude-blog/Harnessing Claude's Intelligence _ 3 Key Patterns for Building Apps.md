---
title: "Harnessing Claude's Intelligence | 3 Key Patterns for Building Apps"
source: "https://claude.com/blog/harnessing-claudes-intelligence"
author:
published: 2001-04-02
created: 2026-04-16
description: "Three patterns for building on the Claude Platform that keep pace with Claude's evolving intelligence while balancing latency and cost."
tags:
  - "clippings"
---
One of Anthropic’s co-founders, Chris Olah, [says](https://www.darioamodei.com/post/the-urgency-of-interpretability) that generative AI systems like Claude are grown more than they are built. Researchers set the conditions to direct growth, but the exact structure or capabilities that emerge aren’t always predictable.Anthropic 的联合创始人之一克里斯·奥拉（Chris Olah） [表示](https://www.darioamodei.com/post/the-urgency-of-interpretability) ，像 Claude 这样的生成式人工智能系统是“培育”出来的，而非单纯“构建”而成。研究人员设定条件来引导其成长，但最终出现的具体结构或功能并非总能预测。

This creates a challenge for building with Claude: [agent harnesses encode assumptions](https://www.anthropic.com/engineering/harness-design-long-running-apps) about what Claude can’t do on its own, but those assumptions grow stale as Claude gets more capable. Even lessons shared in articles like this deserve frequent revisiting. 这给使用 Claude 进行开发带来了一个挑战： [智能体框架会编码一些假设](https://www.anthropic.com/engineering/harness-design-long-running-apps) ，即关于 Claude 自身无法完成的任务，但随着 Claude 能力的不断提升，这些假设会逐渐过时。即使是像本文这样的文章中分享的经验，也值得反复回顾。

In this article, we share three patterns that teams should use when building applications that keep pace with Claude’s evolving intelligence while balancing latency and cost: use what it already knows, ask what you can stop doing, and carefully set boundaries with the agent harness.在本文中，我们分享了团队在构建应用程序时应遵循的三种模式，这些应用程序需跟上 Claude 不断进化的智能水平，同时平衡延迟与成本：利用其已掌握的能力、思考可以停止执行的操作，以及为智能体框架审慎设定边界。

### 1\. Use what Claude knows 1. 利用 Claude 的知识

We suggest building applications using tools that Claude understands well. 我们建议使用 Claude 熟悉的工具来构建应用程序。

In late 2024, Claude 3.5 Sonnet reached 49% on SWE-bench Verified—then [state of the art](https://www.anthropic.com/engineering/swe-bench-sonnet) —with only a [bash tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool) and a [text editor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool) for viewing, creating, and editing files. Claude Code is grounded in these same tools. [Bash](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool) wasn’t designed for building agents, but it's a tool that Claude *knows* how to use and gets better at using over time. 2024年末，Claude 3.5 Sonnet在SWE-bench Verified基准测试中达到了49%的成绩——当时为 [当前最优水平](https://www.anthropic.com/engineering/swe-bench-sonnet) ——仅依靠 [bash工具](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool) 和 [文本编辑器工具](https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool) 来查看、创建和编辑文件。Claude Code正是基于这些相同的工具构建而成。 [Bash](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool) 并非为构建智能体而设计，但它是Claude *掌握* 使用方法的工具，且随着时间推移，Claude对它的使用会愈发熟练。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69cd8747994e07042a959518_image2.png)

Scores on the SWE-bench Verified benchmark across Claude model versions highlight its evolution. Claude 模型各版本在 SWE-bench Verified 基准测试中的得分体现了其发展演变。

We've seen Claude compose these general tools into patterns that solve different problems. For instance, [Agent Skills](https://agentskills.io/home), [programmatic tool calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling), and [the memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) are all built from the bash and text editor tools.我们已经看到 Claude 将这些通用工具组合成可解决不同问题的模式。例如， [智能体技能](https://agentskills.io/home) 、 [程序化工具调用](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling) 和 [记忆工具](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) 均基于 bash 和文本编辑器工具构建而成。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69cd8835161641fba4aa1def_image4.png)

Programmatic tool calling, skills, and memory are compositions of our bash and text editor tools. 程序化工具调用、技能和记忆是我们的 Bash 工具与文本编辑器工具的组合功能。

### 2\. Ask ‘what can I stop doing?’2. 询问“我可以停止做什么？”

[Agent harnesses encode assumptions](https://www.anthropic.com/engineering/harness-design-long-running-apps) about what Claude can’t do on its own. As Claude gets more capable, those assumptions should be tested.[智能体框架包含了对Claude自身无法完成事项的假设](https://www.anthropic.com/engineering/harness-design-long-running-apps) 。随着Claude能力的提升，这些假设应当得到验证。

**Let Claude orchestrate its own actions 让 Claude 自主规划行动**

A common assumption is that every tool result should flow back through Claude’s [context window](https://platform.claude.com/docs/en/build-with-claude/context-windows) to inform the next action. Processing tool results in tokens can be slow, costly, and unnecessary if it only needs to be passed to the next tool or if Claude only cares about a small slice of the output. 一个常见的假设是，每个工具的结果都应回流至 Claude 的 [上下文窗口](https://platform.claude.com/docs/en/build-with-claude/context-windows) ，为下一次操作提供参考。如果工具结果仅需传递给下一个工具，或者 Claude 只关注输出中的一小部分内容，那么以标记（token）形式处理这些结果的过程可能会变得缓慢、成本高昂，且并无必要。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69cd889c76e6e17dbe4ff4b9_image7.png)

Claude calls tools, which are executed in an environment. Claude 调用工具，工具在一个环境中执行。

Consider reading a large table to reason about a single column: the whole table lands in context and Claude pays the token cost for every row it doesn't need. It’s possible to tackle this in tool design, using [hard-coded filters](https://platform.claude.com/docs/en/about-claude/models/migration-guide#additional-recommended-changes). But this does not address the fact that the agent harness is making an *orchestration decision* that Claude is better positioned to make.试想读取一个大表来推理某一列：整个表都会进入上下文，而Claude要为所有它不需要的行支付令牌成本。在工具设计中，通过 [硬编码筛选器](https://platform.claude.com/docs/en/about-claude/models/migration-guide#additional-recommended-changes) 可以解决这个问题，但这无法回避一个事实——智能体框架做出的 *编排决策* ，其实更适合由Claude来完成。

Giving Claude a [code execution](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool) tool (e.g., [bash tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool) or [language-specific REPL](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool)) addresses this: it allows Claude to write code to express tool calls and the logic between them. Rather than the harness deciding that every tool call result is processed as tokens, Claude decides what results to pass through, filter, or pipe into the next call without touching the context window. Only the output of code execution reaches Claude’s context window.为 Claude 配备一个 [代码执行](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool) 工具（例如 [bash 工具](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool) 或 [特定语言的 REPL](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool) ）就能解决这一问题：它让 Claude 可以编写代码来表达工具调用以及调用之间的逻辑关系。不再由框架决定将每个工具调用结果都作为标记处理，而是由 Claude 决定对哪些结果进行传递、过滤或传递到下一次调用，且这一过程不会触及上下文窗口。只有代码执行的输出结果才会进入 Claude 的上下文窗口。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69cd891f5b4d2dea57b008d1_image6.png)

Claude can write code that expresses tool calls and the logic between them. Claude 可以编写能表达工具调用及其之间逻辑的代码。

The orchestration decision moves from the harness to the model. Since code is a general way for Claude to orchestrate actions, a strong coding model is also a strong *general* agent. Claude shows strong performance [on non-coding evals](https://claude.com/blog/improved-web-search-with-dynamic-filtering) using this pattern: on BrowseComp, a [benchmark](https://arxiv.org/abs/2504.12516) that tests the ability of agents to browse the web, giving Opus 4.6 the ability to filter its own tool outputs brought accuracy from 45.3% to 61.6%. 编排决策从工具框架转移到了模型。由于代码是 Claude 编排各类操作的通用方式，因此一个强大的编码模型同时也是一个强大的 *通用* 智能体。采用这种模式，Claude 在 [非编码类评估](https://claude.com/blog/improved-web-search-with-dynamic-filtering) 中表现出色：在 BrowseComp 这个用于测试智能体网页浏览能力的 [基准测试](https://arxiv.org/abs/2504.12516) 中，为 Opus 4.6 赋予自主过滤工具输出的能力后，其准确率从 45.3% 提升至 61.6%。

**Let Claude manage its own context 让 Claude 管理自身的上下文**

Task-specific context steers Claude’s use of general tools like bash and the text editor tool. A common assumption is that [system prompts](https://platform.claude.com/docs/en/release-notes/system-prompts) should be hand-crafted with task-specific instructions. The problem is that pre-loading prompts with instructions does not scale across many tasks: every token added depletes [Claude’s attention budget](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) and it is wasteful to pre-load context with rarely used instructions.针对特定任务的上下文会引导 Claude 使用 bash 和文本编辑器工具等通用工具。一个普遍的假设是， [系统提示词](https://platform.claude.com/docs/en/release-notes/system-prompts) 应结合针对特定任务的指令来手动编写。问题在于，预先在提示词中加载指令无法适用于众多任务：每添加一个标记就会消耗 [Claude 的注意力预算](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) ，而预先加载包含极少使用指令的上下文是一种浪费。

Giving Claude the ability to access [skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) addresses this: the YAML frontmatter of each skill is a short description pre-loaded into the context window, providing an overview of the skill contents. The full skill can be progressively disclosed by Claude calling a read file tool if a task calls for it.让 Claude 具备访问 [技能](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) 的能力就能解决这一问题：每个技能的 YAML 前置内容都是一段简短描述，会预先加载到上下文窗口中，从而提供该技能内容的概览。如果任务需要，Claude 可以通过调用读取文件工具逐步披露完整的技能内容。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69cd895f7f04456cccf7b7e0_image3.png)

Claude can use skills to progressively disclose task-relevant context. Claude 可以利用技能逐步披露与任务相关的上下文。

While skills give Claude the freedom to assemble its own context window, [context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing) is the inverse, providing a way to selectively remove context that’s become stale or irrelevant, such as old tool results or thinking blocks. 虽然技能赋予了 Claude 构建自身上下文窗口的自由度，但 [上下文编辑](https://platform.claude.com/docs/en/build-with-claude/context-editing) 则是其反向操作，它提供了一种有选择地移除过时或无关上下文的方式，例如旧的工具结果或思考模块。

With [subagents](https://code.claude.com/docs/en/sub-agents), Claude is getting better at knowing when to fork into a fresh context window to isolate work on a specific task. [With Opus 4.6](https://www-cdn.anthropic.com/0dd865075ad3132672ee0ab40b05a53f14cf5288.pdf), the ability to spawn subagents improved results on BrowseComp by 2.8% over the best single-agent runs. 借助 [子智能体](https://code.claude.com/docs/en/sub-agents) ，Claude 越来越擅长判断何时需要分支到一个新的上下文窗口，以隔离特定任务的工作。在 [Opus 4.6](https://www-cdn.anthropic.com/0dd865075ad3132672ee0ab40b05a53f14cf5288.pdf) 版本中，子智能体的生成能力使 BrowseComp 的结果相比最佳的单智能体运行提升了 2.8%。

**Let Claude persist its own context 让 Claude 保留自身的上下文**

Long-running agents can exceed the limit of a single [context window](https://platform.claude.com/docs/en/build-with-claude/context-windows). A common assumption is that memory systems should rely on retrieval infrastructure around the model. Much of our work has focused on giving Claude simple ways to *choose for itself* what content to persist.长期运行的智能体可能会超出单个 [上下文窗口](https://platform.claude.com/docs/en/build-with-claude/context-windows) 的限制。一个普遍的假设是，记忆系统应围绕模型构建检索基础设施。我们的大部分工作都聚焦于为 Claude 提供简单的方法，使其能够 *自主选择* 要保留的内容。

For example, [compaction](https://platform.claude.com/docs/en/build-with-claude/compaction) lets Claude summarize its past context in order to maintain continuity on long-horizon tasks. Over several releases, Claude has gotten better at choosing what to remember. [On BrowseComp](https://www-cdn.anthropic.com/14e4fb01875d2a69f646fa5e574dea2b1c0ff7b5.pdf), for example, an agentic search task, Sonnet 4.5 stayed flat at 43% regardless of the compaction budget we gave it. Yet Opus 4.5 scaled to 68% and Opus 4.6 reached 84% with the same setup. 例如， [压缩](https://platform.claude.com/docs/en/build-with-claude/compaction) 功能让 Claude 能够总结其过往上下文，从而在长周期任务中保持连贯性。在多个版本的迭代中，Claude 在选择记忆内容方面的表现愈发出色。以智能体搜索任务 [BrowseComp](https://www-cdn.anthropic.com/14e4fb01875d2a69f646fa5e574dea2b1c0ff7b5.pdf) 为例，在相同配置下，Sonnet 4.5 的得分始终维持在 43%，无论我们为其分配的压缩预算是多少。而 Opus 4.5 的得分提升至 68%，Opus 4.6 更是达到了 84%。

A [memory folder](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) is another approach, allowing Claude to write context to files and later read them as needed. We’ve seen Claude use this for agentic search. On BrowseComp-Plus, giving Sonnet 4.5 a memory folder [lifted accuracy from 60.4% to 67.2%](https://www-cdn.anthropic.com/bf10f64990cfda0ba858290be7b8cc6317685f47.pdf).[记忆文件夹](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) 是另一种方法，它允许 Claude 将上下文写入文件，之后再根据需要读取这些文件。我们已经看到 Claude 将这种方法用于智能体搜索。在 BrowseComp-Plus 上，为 Sonnet 4.5 配备一个 [记忆文件夹后，其准确率从 60.4% 提升到了 67.2%](https://www-cdn.anthropic.com/bf10f64990cfda0ba858290be7b8cc6317685f47.pdf) 。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69cd89bfccdc7c50beb40e0d_image5.png)

Claude can persist context to a memory folder. Claude 可以将上下文持久化到记忆文件夹中。

[Long-horizon games](https://www.youtube.com/watch?v=CXhYDOvgpuU), such as Pokémon, are an example of Claude’s improved ability to use a memory folder. Sonnet 3.5 treated memory as a transcript, writing down what non-player characters (NPCs) said rather than what mattered. After 14,000 steps it had 31 files—including two near-duplicates about caterpillar Pokémon—and was still in the second town:[长时程游戏](https://www.youtube.com/watch?v=CXhYDOvgpuU) （例如《宝可梦》）是 Claude 改进的记忆文件夹使用能力的一个例子。3.5 版 Sonnet 将记忆视为一份抄本，只记录非玩家角色（NPC）说过的话，而非关键信息。在进行了 14000 步后，它生成了 31 个文件——其中包含两个关于毛毛虫类宝可梦的近乎重复的文件——但仍停留在第二个城镇：

```json
caterpie_weedle_info:
- Caterpie and Weedle are both caterpillar Pokémon.
- Caterpie is a caterpillar Pokémon that does not have poison.
- Weedle is a caterpillar Pokémon that does have poison.
- This information is crucial for future encounters and battles.
- If our Pokémon get poisoned, we should seek healing at a Pokémon
  Center as soon as possible.
```

Later models wrote tactical notes. Opus 4.6, at the same step count, had 10 files organized into directories, three gym badges, and a learnings file distilled from its own failures:后续的模型会撰写战术笔记。在相同的步数下，4.6 号作品包含了10个按目录整理的文件、三枚健身徽章，以及一份从自身失败中提炼出的学习文件：

```json
/gameplay/learnings.md:
- Bellsprout Sleep+Wrap combo: KO FAST with BITE before Sleep
  Powder lands. Don't let it set up!
- Gen 1 Bag Limit: 20 items max. Toss unneeded TMs before dungeons.
- Spin tile mazes: Different entry y-positions lead to DIFFERENT
  destinations. Try ALL entries and chain through multiple pockets.
- B1F y=16 wall CONFIRMED SOLID at ALL x=9-28 (step 14557)
```

### 3\. Set boundaries carefully 3. 谨慎设定边界

Agent harnesses provide structure around Claude to enforce UX, cost, or security.智能体框架为Claude提供了结构化的运行环境，以强化用户体验、成本控制或安全性。

**Design context to maximize cache hits 设计上下文以最大化缓存命中率**

The [Messages API](https://platform.claude.com/docs/en/build-with-claude/working-with-messages) is stateless. Claude cannot see the conversation history of prior turns. This means that the agent harness needs to package new context alongside all past actions, tool descriptions, and instructions for Claude at each turn.[消息 API](https://platform.claude.com/docs/en/build-with-claude/working-with-messages) 是无状态的。Claude 无法查看先前对话轮次的对话历史。这意味着智能体框架需要在每一轮都将新的上下文与所有过往操作、工具描述以及给 Claude 的指令打包在一起。

Prompts can be cached based on set [breakpoints](https://platform.claude.com/docs/en/build-with-claude/prompt-caching). In other words, the Claude API writes context up until a breakpoint to the cache and checks whether the context matches any prior cache entries. 提示词可基于设置的 [断点](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) 进行缓存。也就是说，Claude API 会将断点之前的上下文写入缓存，并检查该上下文是否与任何先前的缓存条目匹配。

Since cached tokens [are 10% the cost](https://platform.claude.com/docs/en/about-claude/pricing) of base input tokens, here are a few principles in the agent harness help maximize cache hits: 由于缓存令牌的成本是基础输入令牌的 [十分之一](https://platform.claude.com/docs/en/about-claude/pricing) ，以下是智能体工具中帮助实现缓存命中率最大化的几项原则：

| Principle 原则 | Description 说明 |
| --- | --- |
| Static first, dynamic last 静态优先，动态后置 | Order requests so that stable content (system prompt, tools) come first.订购请求，以便稳定的内容（系统提示、工具）放在首位。 |
| Messages for updates 用于更新的消息 | Append a `<system-reminder>` in messages instead of editing the prompt.在消息中附加 `<system-reminder>` ，而非编辑提示词。 |
| Don't change models 不要更换模型 | Avoid switching models during a session. Caches are model-specific; switching breaks them. If you need a cheaper model, use a subagent.避免在会话期间切换模型。缓存是特定于模型的；切换会导致缓存失效。如果需要使用更经济的模型，请使用子代理。 |
| Carefully manage tools 谨慎管理工具 | Tools sit in the cached prefix. Adding or removing one invalidates it. For dynamic discovery, use **tool search**, which appends without breaking cache.工具位于缓存前缀中。添加或移除某个工具会使其失效。对于动态发现，请使用 **工具搜索** ，该操作会在不破坏缓存的情况下进行追加。 |
| Update breakpoints 更新断点 | For multi-turn applications (e.g., agents), move the breakpoint to the latest message in order to keep the cache up-to-date. Use **auto-caching** for this.对于多轮应用（例如智能体），将断点移至最新消息以保持缓存为最新状态。为此请使用 **自动缓存** 。 |

**Use declarative tools for UX, observability, or security boundaries 针对用户体验、可观测性或安全边界，使用声明式工具**

Claude doesn't necessarily know an application's security boundary or UX surface. Claude emits tool calls, which are handled by the harness. A bash tool gives Claude broad programmatic leverage to perform actions, but it gives the harness only a command string—the same shape for every action. Promoting actions to dedicated tools gives the harness an action-specific hook with typed arguments it can intercept, gate, render, or audit.Claude 未必了解应用的安全边界或用户体验界面。Claude 会发出工具调用，这些调用由控制框架处理。bash 工具为 Claude 提供了强大的编程能力来执行操作，但它给控制框架的只是一个命令字符串——所有操作的格式都相同。将操作升级为专用工具后，控制框架就能获得针对特定操作的钩子，该钩子带有可被拦截、控制、渲染或审计的类型化参数。

Actions that require a security boundary are natural candidates for dedicated tools. Reversibility is often a good criterion, and hard-to-reverse actions such as external API calls can be gated by user confirmation. Write tools like `edit` can include a staleness check so Claude doesn't overwrite a file that changed since it was last read.需要安全边界的操作天然适合使用专用工具。可逆性通常是一个不错的判断标准，而外部 API 调用这类难以撤销的操作可通过用户确认来限制执行。像 `edit` 这类工具可加入过期检查，这样 Claude 就不会覆盖自上次读取后发生变更的文件。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69cd8ebecb4a73207c8b2ffc_image1.png)

Dedicated tools can be used for actions based upon security, UX, or observability considerations. 可基于安全性、用户体验或可观测性方面的考量，将专用工具用于各类操作。

Tools are also useful when an action needs to be presented to a user. For example, they can be rendered as a modal to display a question clearly to the user, give the user multiple options, or block the agent loop until a user provides feedback.当需要向用户展示某个操作时，工具也十分实用。例如，它们可以被渲染为模态框，向用户清晰地展示一个问题，为用户提供多个选项，或者在用户提供反馈之前阻塞智能体循环。

Finally, tools are useful for observability. When the action is a typed tool, the harness gets structured arguments it can log, trace, and replay.最后，工具对于可观测性十分有用。当操作是类型化工具时，测试工具会获取可用于记录、追踪和重放的结构化参数。

The decision to promote actions to tools should be continually re-evaluated. For example, Claude Code's [auto-mode](https://www.anthropic.com/engineering/claude-code-auto-mode) (in research mode at the time of publication) provides a security boundary around the bash tool: it has a second Claude read the command string and judge whether it's safe. This pattern can *limit* the need for dedicated tools, and should only be used for tasks where users trust the general direction. Dedicated tools can still earn their place for certain high-stakes actions. 将功能推广至工具的决策需要持续重新评估。例如，Claude Code 的 [自动模式](https://www.anthropic.com/engineering/claude-code-auto-mode) （发布时处于研究模式）为 bash 工具提供了一道安全边界：它会让另一个 Claude 读取命令字符串并判断其是否安全。这种模式可以 *减少* 对专用工具的需求，且仅应在用户信任整体方向的任务中使用。对于某些高风险操作，专用工具仍能占据一席之地。

### Looking forward 展望

The frontier of Claude’s intelligence is always changing. Assumptions about what Claude can’t do need to be re-tested with each step change in its capability. Claude 智能的边界始终在不断变化。关于 Claude 无法完成之事的假设，需要随着其能力的每一次阶段性升级重新进行验证。

We see this pattern repeat itself. In an [agent we built for long-horizon tasks](https://www.anthropic.com/engineering/harness-design-long-running-apps), Sonnet 4.5 would wrap up prematurely as it sensed the context limit approaching. We added resets to clear the context window in order to address this "context anxiety." With Opus 4.5, the behavior was gone. The context resets we built to compensate had become dead weight in the agent harness.我们看到这种模式反复出现。在我们为 [长周期任务构建的智能体](https://www.anthropic.com/engineering/harness-design-long-running-apps) 中，Sonnet 4.5 会在感知到上下文限制即将达到时提前结束。我们添加了重置功能来清空上下文窗口，以解决这种“上下文焦虑”问题。而在 Opus 4.5 中，这一问题消失了。我们为弥补这一问题而构建的上下文重置功能，也成了智能体框架中的多余负担。

Removing this dead weight is important [because it can bottleneck](http://www.incompleteideas.net/IncIdeas/BitterLesson.html) Claude’s performance. Over time, the structure or boundaries in our applications should be pruned based the question: *what can I stop doing?*去除这一累赘至关重要 [因为它可能会成为瓶颈](http://www.incompleteideas.net/IncIdeas/BitterLesson.html) Claude 的性能。随着时间的推移，我们应基于这样一个问题来精简应用中的结构或边界： *我可以停止做哪些事？*

*To use all tools and patterns discussed here, check out* [*our claude-api skill*](https://github.com/anthropics/skills/tree/main/skills/claude-api)*.**要使用本文讨论的所有工具和模式，请查看* [*我们的 claude-api 技能*](https://github.com/anthropics/skills/tree/main/skills/claude-api) *。*

### Acknowledgements 致谢

Written by Lance Martin, member of technical staff on the Claude Platform team. Special thanks to Thariq Shihipar, Barry Zhang, Mike Lambert, David Hershey, and Daliang Li for helpful discussion on the topics covered. Thanks to Lydia Hallie, Lexi Ross, Katelyn Lesse, Andy Schumeister, Rebecca Hiscott, Jake Eaton, Pedram Navid, and Molly Vorwerck for their editorial review and feedback. 本文由 Claude 平台团队技术成员兰斯·马丁撰写。特别感谢塔里奇·希希帕尔、巴里·张、迈克·兰伯特、大卫·赫希和李大亮就所涉主题提供的有益讨论。感谢莉迪亚·哈利、莱克西·罗斯、凯特琳·莱斯、安迪·舒迈斯特、丽贝卡·希斯科特、杰克·伊顿、佩德拉姆·纳维德和莫莉·沃沃克克进行编辑审阅并提供反馈。