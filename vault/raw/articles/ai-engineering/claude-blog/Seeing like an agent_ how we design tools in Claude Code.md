---
title: "Seeing like an agent: how we design tools in Claude Code"
source: "https://claude.com/blog/seeing-like-an-agent"
author:
published: 2001-04-10
created: 2026-04-16
description: "Building Claude Code: How Anthropic designs and refines AI agent tools like AskUserQuestion and Task tool. The key is progressive disclosure and learning to \"see like an agent\" to maximize effectiveness."
tags:
  - "clippings"
---
One of the hardest parts about building an agent harness is constructing its tools.构建智能体工具套件最困难的部分之一是搭建其工具。

Claude acts completely through [tool calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview), but there are a number of ways tools can be constructed in the Claude API with primitives like [bash](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool), [skills](https://code.claude.com/docs/en/skills) and [code execution](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool). (You can read more about programmatic tool calling on the Claude API in [@RLanceMartin's new article](https://x.com/RLanceMartin/status/2027450018513490419)).Claude 完全通过 [工具调用](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) 运行，但在 Claude API 中，可通过 [bash](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool) 、 [技能](https://code.claude.com/docs/en/skills) 和 [代码执行](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool) 等原语以多种方式构建工具。（你可以在 [RLanceMartin 的新文章](https://x.com/RLanceMartin/status/2027450018513490419) 中了解更多关于 Claude API 程序化工具调用的内容）。

So how do you design your agents' tools? Do you give it one general-purpose tool like bash or code execution? Or fifty specialized tools, one for each use case?那么你该如何设计智能体的工具呢？是给它配备一个通用工具（比如 bash 或代码执行工具），还是配备五十个专用工具，每个工具对应一个使用场景？

To put yourself in the mind of the model, imagine being given a difficult math problem. What tools would you want in order to solve it? It would depend on your own skill set!站在模型的角度思考一下，假设你被给到一道很难的数学题。为了解开它，你希望拥有哪些工具？这取决于你自身的能力水平！

Paper would be the minimum, but you’d be limited by manual calculations. A calculator would be better, but you would need to know how to operate the more advanced options. The fastest and most powerful option would be a computer, but you would have to know how to use it to write and execute code.用纸笔是最基础的方式，但会受限于人工计算。使用计算器会更高效，但你得知道如何操作其更高级的功能。而电脑是速度最快、功能最强大的选择，不过你得学会用它编写并运行代码。

This is a useful framework for designing your agent. You want to give it tools that are shaped to its own abilities. But how do you know what those abilities are? You pay attention, read its outputs, experiment. You learn to see like an agent.这是一个设计智能体的实用框架。你需要为其配备契合自身能力的工具。但你如何知晓这些能力是什么？你需要专注观察、研读其输出结果、不断尝试。你要学会像智能体一样去观察。

If you're building an agent, you'll face the same questions we did: when to add a tool, when to remove one, and how to tell the difference. Here's how we've answered them while building Claude Code, including where we got it wrong first.如果你正在开发一个智能体，你会遇到和我们当初一样的问题：何时添加工具、何时移除工具，以及如何区分这两种情况。以下是我们在开发 Claude Code 时解决这些问题的思路，包括我们最初犯下的错误。

## Improving elicitation with the AskUserQuestion tool借助 AskUserQuestion 工具优化启发式提问

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69d919d46e9dceaa0cf307d9_b089e3d3.png)

When building the AskUserQuestion tool, our goal was to improve Claude’s ability to ask questions (often called elicitation).在开发 AskUserQuestion 工具时，我们的目标是提升 Claude 提出问题（通常称为启发式提问）的能力。

While Claude could just ask questions in plain text, we found answering those questions felt like they took an unnecessary amount of time. How could we lower this friction and increase the bandwidth of communication between the user and Claude?虽然Claude可以直接用纯文本提问，但我们发现回答这些问题似乎花费了不必要的时间。我们该如何降低这种沟通阻力，提升用户与Claude之间的沟通效率呢？

### Attempt 1: Editing the ExitPlanTool尝试一：修改退出计划工具

The first approach we tried was adding a parameter to the ExitPlanTool to have an array of questions alongside the plan. This was the easiest fix to implement, but it confused Claude because we were simultaneously asking for a plan and a set of questions about the plan. What if the user’s answers conflicted with what the plan said? Would Claude need to call the ExitPlanTool twice? We knew this tactic wouldn’t work, so we went back to the drawing board. (You can read more about why we made an ExitPlanTool in [our post on prompt caching](https://x.com/trq212/status/2024574133011673516)) 我们尝试的第一种方法是给 ExitPlanTool 添加一个参数，让计划旁边附带一组问题。这是最容易实现的修复方式，但这让 Claude 陷入了困惑，因为我们同时要求它生成计划以及一组关于该计划的问题。如果用户的回答与计划内容相矛盾该怎么办？Claude 是否需要两次调用 ExitPlanTool？我们清楚这种策略行不通，于是重新开始构思方案。（你可以在 [我们关于提示词缓存的文章](https://x.com/trq212/status/2024574133011673516) 中了解更多关于我们为何开发 ExitPlanTool 的原因）

### Attempt 2: Changing output format 尝试2：更改输出格式

Next, we tried updating Claude’s output instructions to serve a slightly modified markdown format that it could use to ask questions. For example, we could ask it to output a list of bullet point questions with alternatives in brackets. We could then parse and format that question as UI for the user.接下来，我们尝试更新 Claude 的输出指令，以采用一种稍作修改的 Markdown 格式，让它可以用这种格式来提出问题。例如，我们可以让它输出带括号内备选答案的项目符号问题列表。随后，我们就能解析这些问题并将其格式化为用户界面展示给用户。

Claude could usually produce this format, but not reliably. It would append extra sentences, drop options, or abandon the structure altogether. Onto the next approach.Claude 通常能生成这种格式，但并不稳定。它会额外添加句子、遗漏选项，或者直接放弃这种结构。那就试试下一种方法吧。

### Attempt 3: The AskUserQuestion Tool尝试3：AskUserQuestion 工具

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69d919d46e9dceaa0cf307dc_208fceac.png)

Finally, we landed on creating a tool that Claude could call at any point, but it was particularly prompted to do so during plan mode. When the tool triggered we would show a modal to display the questions and block the agent's loop until the user answered.最后，我们最终确定开发一款可让 Claude 在任意时刻调用的工具，而在计划模式下，会特别提示它调用该工具。工具触发时，我们会弹出一个模态框显示问题，并在用户回答前阻止智能体的循环运行。

This tool allowed us to prompt Claude for a structured output and it helped us ensure that Claude gave the user multiple options. It also gave users ways to compose this functionality, for example calling it in the [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) or using referring to it in skills.该工具让我们可以向 Claude 发出指令，获取结构化输出，还能确保 Claude 为用户提供多种选择。它也为用户提供了组合该功能的方式，比如在 [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) 中调用它，或是在技能中引用它。

Most importantly, Claude seemed to like calling this tool and we found its outputs worked well. After all, even the best designed tool doesn’t work if Claude doesn’t understand how to call it.最重要的是，Claude似乎很喜欢调用这个工具，而且我们发现它的输出效果很不错。毕竟，如果Claude不了解如何调用一个工具，即便它的设计再精良，也无法发挥作用。

Is this the final form of elicitation in Claude Code? We doubt it. As Claude gets more capable, the tools that serve it have to evolve too. The next section shows a case where a tool that once helped started getting in the way.这就是 Claude Code 中启发式方法的最终形式吗？我们对此表示怀疑。随着 Claude 的能力不断提升，为其服务的工具也必须不断演进。下一部分将展示一个案例，说明曾经提供帮助的工具后来反而成了阻碍。

### Updating with capabilities: tasks & todos基于功能更新：任务与待办事项

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69d919d46e9dceaa0cf307df_9f83e911.png)

When we first launched Claude Code, we realized that the model needed a [todo list](https://platform.claude.com/docs/en/agent-sdk/todo-tracking) to keep it on track. Todos could be written at the start and checked off as the model did work. To do this we gave Claude the TodoWrite tool, which would write or update Todos and display them to the user.当我们首次推出 Claude Code 时，我们意识到该模型需要一个 [待办事项清单](https://platform.claude.com/docs/en/agent-sdk/todo-tracking) 来保持进度。待办事项可以在一开始就列出，并在模型开展工作时逐一勾选。为了实现这一点，我们为 Claude 配备了 TodoWrite 工具，该工具可以编写或更新待办事项，并将其展示给用户。

But even then, we often saw Claude forgetting what it had to do. To adapt, we inserted system reminders every 5 turns that reminded Claude of its goal.但即便如此，我们也经常发现 Claude 会忘记自己需要完成的任务。为了解决这个问题，我们每 5 轮就插入一次系统提醒，让 Claude 记起自己的目标。

As models improved, they found To-do lists limiting. Being sent reminders of the todo list made Claude think that it had to stick to the list instead of modifying it when it realized it needed to change course. We also saw Opus 4.5 also get much better at using subagents, but how could subagents coordinate on a shared todo list?随着模型不断优化，它们发现待办清单存在局限性。当收到待办清单的提醒时，Claude 会认为自己必须严格遵守这份清单，而无法在意识到需要调整方向时对其进行修改。我们还发现 Opus 4.5 在调用子智能体方面的能力也大幅提升，但子智能体该如何在共享的待办清单上进行协作呢？

Seeing this, we replaced the TodoWrite feature with [the Task tool](https://x.com/trq212/status/2014480496013803643). Whereas todos are focused on keeping the model on track, tasks help agents communicate with each other. Tasks could include dependencies, share updates across subagents and the model could alter and delete them.看到这一情况，我们将 TodoWrite 功能替换为了 [任务工具](https://x.com/trq212/status/2014480496013803643) 。待办事项专注于让模型保持正常运行，而任务则能帮助智能体之间进行沟通。任务可以包含依赖关系，还能在子智能体之间共享更新内容，并且模型可以对其进行修改和删除。

As model capabilities increase, the tools that your models once needed might now be constraining them. It’s important to constantly revisit previous assumptions on what tools are needed. This is also why it's useful to stick to a small set of models to support that have a fairly similar capabilities profile.随着模型能力的提升，你曾经依赖的那些工具如今反而可能限制模型的发展。不断重新审视关于所需工具的先前假设至关重要。这也是为何坚持使用少数几个能力特征相当相似的模型来提供支持会很有帮助。

## Designing a search interface 设计搜索界面

The most consequential tools we've built are the ones that let Claude find its own context.我们打造的最关键工具是那些能让Claude自主查找上下文的工具。

When Claude Code was first released internally, we used RAG: a vector database would pre-index the codebase, and the harness would retrieve relevant snippets and hand them to Claude before each response.. While RAG was powerful and fast, it required indexing and setup and could be fragile across a host of different environments. Most importantly, Claude was *given* this context instead of finding the context itself.Claude Code 首次内部发布时，我们采用了检索增强生成（RAG）技术：向量数据库会预先为代码库建立索引，在每次生成回复前，工具会检索相关代码片段并将其提供给 Claude。尽管检索增强生成技术功能强大且速度快，但它需要进行索引和设置，且在多种不同环境中可能不够稳定。最重要的是，Claude 是 *被* 提供了这些上下文，而非自行去查找上下文。

But if Claude could search on the web, why couldn’t it also search your codebase? By giving Claude a Grep tool, we could let it search for files and build context itself.但如果 Claude 可以联网搜索，那它为什么不能搜索你的代码库呢？通过为 Claude 配备一个 Grep 工具，我们就能让它自行搜索文件并构建上下文。

As Claude gets smarter, it becomes increasingly good at building its context when given the right tools. 随着Claude变得越来越智能，在配备合适工具的情况下，它也越来越擅长构建自身的上下文。

When we introduced [Agent Skills](https://agentskills.io/home), we formalized the idea of progressive disclosure, which allows agents to incrementally discover relevant context through exploration.在我们介绍 [智能体技能](https://agentskills.io/home) 时，我们将渐进式披露的概念进行了形式化定义，这一机制允许智能体通过探索逐步发现相关上下文。

Claude could now read skill files and those files could then reference other files that the model could read recursively. In fact, a common use of skills is to add more search capabilities to Claude like giving it instructions on how to use an API or query a database.Claude 现在可以读取技能文件，且这些文件可引用模型可递归读取的其他文件。实际上，技能的一个常见用途是为 Claude 添加更多搜索功能，比如为其提供如何使用 API 或查询数据库的指令。

Over the course of a year, Claude went from not really being able to build its own context to being able to do nested search across several layers of files to find the exact context it needed.在一年的时间里，Claude 从几乎无法构建自身的上下文，发展到能够跨多层文件进行嵌套搜索，以找到所需的确切上下文。

Progressive disclosure is now a common technique we use to add new functionality without adding a tool. In the next section, we explain why.渐进式披露如今已成为我们在不新增工具的情况下添加新功能的常用技巧。在下一节中，我们将解释其中的原因。

## Progressive disclosure: the Claude Code Guide agent渐进式披露：Claude Code Guide 智能体

Claude Code currently has ~20 tools, and our team frequently revisits if we need all of them for Claude to be most effective. The bar to add a new tool is high, because this gives the model one more option to think about.Claude Code 目前拥有约 20 个工具，我们团队也经常重新审视，为了让 Claude 发挥最大效用，是否需要保留所有这些工具。新增工具的门槛很高，因为这会给模型多增加一个需要考量的选项。

For example, we noticed that Claude did not know enough about how to use Claude Code. If you asked it how to add a MCP or what a slash command did, it would not be able to reply.例如，我们注意到Claude对如何使用Claude Code了解得不够多。如果你问它如何添加MCP或斜杠命令有什么作用，它无法给出回答。

We could have put all of this information in the system prompt, but given that users rarely asked about this, it would have added context rot and interfered with Claude Code’s main job: writing code.我们本可以把所有这些信息都放入系统提示词中，但考虑到用户很少询问相关内容，这么做会导致上下文失效，还会干扰 Claude Code 的核心工作：编写代码。

Instead, we tried progressive disclosure: we gave Claude a link to its docs that it could load and search when needed. This worked, but Claude would pull large chunks of documentation into context to find an answer the user could have gotten in one sentence.相反，我们尝试了渐进式披露的方法：我们给了Claude一个文档链接，让它在需要时加载并搜索。这种方法有效，但Claude会将大量文档内容拉入上下文来寻找答案，而用户本可以一句话就找到答案。

So we built the Claude Code Guide — a subagent Claude calls whenever a user asks about Claude Code itself. The subagent does the doc-searching in its own context, follows detailed instructions on how to search and what to extract, and hands back only the answer. The main agent's context stays clean.于是我们开发了Claude代码指南——这是一个子智能体，每当用户询问有关Claude代码本身的问题时，Claude就会调用它。该子智能体会在自身的语境中进行文档搜索，遵循关于搜索方式和提取内容的详细指令，然后只返回答案。主智能体的语境则保持整洁。

While this isn’t a perfect solution (Claude can still get confused when you ask it about how to set itself up), we were able to add things to Claude's action space without adding a new tool.虽然这并非完美方案（当你询问 Claude 如何进行自我设置时，它仍可能出现理解混乱的情况），但我们无需新增工具，就能为 Claude 的行动空间添加相关内容。

### Seeing like an agent is an art, not a science以智能体的视角看待事物是一门艺术，而非一门科学

Designing the tools for your models is as much an art as it is a science. It depends heavily on the model you're using, the goal of the agent and the environment it’s operating in.为你的模型设计工具既是一门科学，也是一门艺术。这在很大程度上取决于你所使用的模型、智能体的目标以及它所处的运行环境。

Our best advice? Experiment often, read your outputs, try new things. And most importantly, try to see like an agent.我们最好的建议是什么？多做尝试，审视自己的输出结果，探索新的方法。而最重要的是，试着像智能体一样思考。

*Get started with* [*Claude Code*](https://code.claude.com/docs/en/overview) *today.**立即开始使用* [*Claude Code*](https://code.claude.com/docs/en/overview) *吧。*

***About the author:*** *Thariq Shihipar is a member of technical staff at Anthropic, working on Claude Code.* ***作者简介：*** *塔里克·希希帕尔是 Anthropic 公司的技术人员，主要负责 Claude Code 相关工作。*