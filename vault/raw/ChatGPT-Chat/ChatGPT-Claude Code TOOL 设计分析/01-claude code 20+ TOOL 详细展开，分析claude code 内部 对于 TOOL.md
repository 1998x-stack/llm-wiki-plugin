# claude code 20+ TOOL 详细展开，分析claude code 内部 对于 TOOL的严谨设计，TOOL工具的迭代过程和思考过程，为什么要这个工

> Source: Claude Code TOOL 设计分析
> Time: 2026/4/16 15:19:04

## Question

claude code 20+ TOOL 详细展开，分析claude code 内部 对于 TOOL的严谨设计，TOOL工具的迭代过程和思考过程，为什么要这个工具，而不是其他工具；调查更多的博客研究 如 https://claude.com/blog/seeing-like-an-agent https://x.com/RLanceMartin/article/2027450018513490419 https://x.com/trq212/status/2024574133011673516

## Answer

我先把你给的几篇材料和 Claude Code 相关的一手资料一起梳理，重点拆三层：工具集合本身、这些工具背后的设计约束、以及它们为什么会这样演化。再补一些公开博客/讨论做交叉验证，最后给你一个“工具设计方法论”层面的结论。


我已经拿到官方 tools reference，当前公开可见的内置工具是 30 个左右，不只是大家常说的 Bash / Read / Write 那几个。下一步我在补两类证据：一类是“新增/废弃/预览”轨迹，另一类是 Anthropic 官方关于 agent 观察、权限和安全的设计说明。


我在补你点名的两条 X 讨论。X 原链接本身有访问限制，我会尽量找可验证的镜像或同主题一手资料来还原它们的核心观点，并明确区分“官方事实”和“社区解读”。

Searching web for Claude Code tools and docs


学习 Claude Code 的工具使用 - 知乎
Claude Code 工具系统：内置工具的实现剖析 • Jerry's Blog
Tools reference - Claude Code Docs
AI时代的终端革命：Claude Code 完全指南_claude-code ...
GitHub - anthropics/claude-code: Claude Code is an agentic coding tool ...
Claude Code Built-in Tools Reference - vtrivedy
Claude Code | Anthropic's agentic coding system
Claude Code 深度使用指南：从入门到精通


Reading official documentation and tools references


Tools reference - Claude Code Docs
Claude Code | Anthropic's agentic coding system  \ Anthropic
GitHub - anthropics/claude-code: Claude Code is an agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster by executing routine tasks, explaining complex code, and handling git workflows - all through natural language commands. · GitHub


Finding tool names and patterns in references


Tools reference - Claude Code Docs


Editing tool table to add more lines


Tools reference - Claude Code Docs


Investigating tool iterations and updates


I need to dive into official documentation to understand tool permissions, subagents, and design considerations. The user wants insights on the tool iteration process. I'll look for a changelog or "What's New" details for tools like Monitor v2.1.98 and others to track recent updates.


Searching release notes for tool updates and changes


Searching web for GitHub changelog terms


GitHub - anthropics/claude-code: Claude Code is an agentic coding tool ...
Tools reference - Claude Code Docs
Windows 上的 Claude Code：四条命令，从零到 Opus 4.6


Checking changelog for tool updates


I’ll open the chang


Opening changelog and locating tool entries


Changelog - Claude Code Docs


Searching changelog for relevant tool updates


I need to search through the changelog for details on when tools like Monitor, ToolSearch, and others were introduced, including features like team management, plan mode, and worktree. The user seems to be focused on tools, so that's where I'll focus my search. I'll use the find function in the changelog.


Searching changelog for new tool-related features


Changelog - Claude Code Docs


Finding updates on Agent Teams and features


I need to find when features like Agent Teams, Worktree, and Plan Mode were introduced. A search through the updates should help pinpoint when these were added, and it'll help narrow down the timeline of tool improvements. I'll look into the details shortly!


Searching for Agent Teams, worktree, and plan mode


Changelog - Claude Code Docs


Looking for the "Seeing like an agent" blog


I should search for the official blog post or article titled "Seeing like an agent" to understand more about what it covers. This could give me more context on how the agent's perspective works and might help clarify things for the user. Time to go find it!


Searching for "Seeing like an Agent" blog posts


Alignment Science Blog
red.anthropic.com


Looking for the direct link on claude.com


I’ll try searching for a direct URL that might open the content, possibly on the claude.com domain specifically. I want to make sure I’m accessing the right source, so I’ll look into it and see if I can find the precise link needed. Let's see what I can find!


Searching for specific URL on claude.com domain


Seeing like an agent: how we design tools in Claude Code | Claude


Looking into lines from 319 onward


I should open more lines starting from line 319 onward to get a better understanding of the context. This will give me a clearer view of what’s happening further down, and I might find additional relevant details to complete the task. I'll check those out next.


Opening lines from 319 onward


Seeing like an agent: how we design tools in Claude Code | Claude


Looking into official blogs and tool evolution


I should check out the lines related to ExitPlanTool for context and rationale, maybe even referenced on x.com. Exploring other blogs about subagents, session management, and agent redesign could be useful for tool evolution, particularly compaction and subagents. I'll see if I can find any relevant posts!


Searching for blogs and tools on subagents and context


How and when to use subagents in Claude Code | Claude


Exploring session management details


I should take a look at the session management lines, maybe finding relevant information on how it works within the system. Searching within these might help me gather the details I need for better context and clarity. Let's dive in and see what I can uncover!


Searching session management and relevant information


Using Claude Code: session management and 1M context | Claude


Investigating programmatic tool calling article


I think it would be helpful to look for the article by RLanceMartin on programmatic tool calling with the Claude API. Maybe there’s a link to it in a blog footnote, possibly not just on X. I’ll search for relevant queries to locate this article. Let’s see what I can find!


Searching for RLanceMartin article on Claude API tool


程序化工具调用 - Claude API Docs
blog.langchain.dev
在 Claude Code 中使用 Anthropic API 进行程序化工具调用
research/tools-and-integrations/programmatic-tool-calling-claude/index ...
Programmatic Tool Calling | anthropics/claude-cookbooks | DeepWiki
构建 Claude Code 的经验教训：像智能体一样思考 - 网闻录
Programmatic Tool Calling with Claude Code: The Developer's Guide to ...
Advanced Claude Tool Use: Tool Search, Programmatic Calling & Usage ...
构建 Claude Code 的经验教训：像 Agent 一样观察 - 在线工具
Introducing advanced tool use on the Claude Developer Platform
构建 Claude Code 的经验教训：以 Agent 的视角 | 登链社区 ...


Looking for official blog on advanced tool use


I should check out the official engineering blog for any posts related to advanced tool usage. This could provide useful insights. It would be great to explore some detailed resources, so I’m going to open that and see what I can find. Maybe there’s something on enhancing tool


Searching for advanced engineering tools and resources


Introducing advanced tool use on the Claude Developer Platform \ Anthropic
程序化工具调用 - Claude API Docs


Inspecting X posts from user


The user provided direct URLs to X posts. I should check those links directly to get the article and status information. I'll try accessing the X article and review its content to see if it meets the user's needs. Let's see what insights I can gather from it!


Inspecting X articles for accessibility and status


X


Searching for accessible mirrors or discussions


It looks like I can't access the X post directly, so I’ll try searching for mirrors or discussions that may reference it. I can search by its ID or content to find relevant discussions or sources that might serve as a good alternative. Let’s see what comes up!


Searching for references using IDs and content


像智能体一样观察：Anthropic 团队谈 Claude Code 工具设计 ...
Lessons from Building Claude Code: Prompt Caching Is Everything
Anthropic工程师揭秘：Agent工具设计的“艺术与科学”_博客-飞 ...


Exploring mirror sources for information


I've found an interesting tool.lu mirror for the TRQ212 prompt caching article — I think that could work! There's also an RLanceMartin article I need to track down, though search results point to an X status, not the article itself. I’ll try searching another mirror or blog to see if I can locate it.


Searching for RLanceMartin article on programmatic tool calling


构建 Claude Code 的经验教训：像 Agent 一样观察 - Online ...


Searching for prompt caching info


I’m looking for official or mirrored information on prompt caching, particularly detailed info from X if it's available. I'll search tool.lu to see if I can find more insights or relevant references from there. Should help me gather all the details I need!


Searching for prompt caching and task tool details


Lessons from Building Claude Code: Prompt Caching Is Everything - 在线工具


Finding task tool details


The prompt caching article is really relevant, so that's excellent. I might also need more detailed info on the Task tool, specifically the status 201448. I'll try to find a mirror or additional sources to check on that. Let's search to see what I can uncover!


Searching for Task tool and Claude Code information


Claude Code 全攻略：命令大全 + 实战工作流（建议收藏）
时间戳 (Unix timestamp)转换工具 - 在线工具
Claude Code 超详细完整指南（2026最新版） - 知乎
Claude Code使用教程：2026最新实战，接入MiniMax M2.7 ...
Claude Code 新手必备：9命令×8快捷键 | Polaris的小站
Claude Code的Tasks功能：AI编程助手迈向真正的项目协作
Claude Code常用命令速查 - Nickey103 - 博客园
在线工具 - 你的工具箱


Looking for authoritative task tool docs


The Tencent news summary on the task tool gives some specifics, but it might not be the most authoritative source. I'll try to find more trustworthy alternatives, like official documentation for tasks. Time to search for those reliable resources!


Searching official docs for task management tools


Claude Code /tasks 命令详解：后台任务尽在掌控 — Vincent ...
Create custom subagents - Claude Code Docs
Claude Code CLI 源码解读 #17：任务系统 (tasks/ 目录)
claude-code-sessions/skills/session-tasks/SKILL.md at main - GitHub


Searching for permissions and safety docs


It seems like the user is asking about the detailed and safe design of the tool. I’ll need to look up more about open commands, permissions, and auto modes for clarity on safe design practices. I’ll search for documentation on permissions and safety to better explain.


Searching permissions, safety, and auto mode documentation


Configure permissions - Claude Code Docs
Claude Code auto mode: a safer way to skip permissions
Trust Center - Anthropic


Searching for agent design methodology


It seems like a great idea to search for effective tool design specifically for agents. I'll search for something like “Writing effective tools for agents” as it might provide the methodologies around creating tools and agents in a way that's relevant to the user's needs.


Searching for tools and methodologies for agents


Effective harnesses for long-running agents \ Anthropic


Inspecting auto mode and sandboxing sections


I need to take a closer look at the auto mode and sandboxing lines, as they seem important here. I'll go ahead and check out the relevant sections where these terms are mentioned to better understand how they might relate to this task.


Inspecting auto mode and sandboxing lines


Claude Code auto mode: a safer way to skip permissions \ Anthropic


Looking into permissions and modes documentation


I should look for official documentation on permissions and modes to understand options like auto-allow for safe commands. The user also asked about Claude Code internal tool design, so I might want to find related articles, including the "thinking tool" article from March 2025 for analogy. This could be extra background.


Searching for Claude Code tool permissions and design


The "think" tool: Enabling Claude to stop and think \ Anthropic
claude-code-memory-bank/creative_mode_think_tool.md at main ...
The AI for Problem Solvers | Claude by Anthropic


Exploring article on effective tools for agents


The article about writing effective tools for agents seems relevant. I should open and examine it to gather useful information. It could provide key insights into the right approach to developing such tools for agents.


Searching for tools to improve agent effectiveness


Writing effective tools for AI agents—using AI agents \ Anthropic


Checking permission and security docs


I might need to look up official documentation on permissions to get more details on modes and their precision. Additionally, reviewing the security-related documentation could help ensure I'm addressing all the relevant aspects properly. I’ll open those sections to gather more specific information.


Searching for official permission and security documentation


Configure permissions - Claude Code Docs


Reviewing deferred tools and prompt caching


I might need to check the tool search documentation, especially since it’s important for handling deferred tools and prompt caching. Figuring out how those systems interact will help me manage things efficiently. I’ll look for relevant sections to get more specific details on this.


Searching documentation for deferred tools and caching


Scale to many tools with tool search - Claude Code Docs


Considering tool categorization and news sources


I’m thinking using a navlist for recent developments might be useful, especially since the user asked for analysis. But then, I’m not sure if the search results will come from news sources or not. Should I categorize the tools instead? I'm counting now, and I think there are 35.


Analyzing tool sets and third-party input


I’m wondering if the tools vary based on the platform or provider settings. Tools docs mention that the available set can depend on those factors, so it’s something worth noting. Also, I need to look into why tools are used instead of something like a single Bash script. A blog or third-party analysis, like Jerry’s or vtrivedy’s, might be useful here. Definitely need reliable sources for citations.


Searching for third-party analysis of Claude Code system


Claude Code 工具系统：内置工具的实现剖析 • Jerry's Blog
Claude Code Tool Search：从全量加载到按需发现
Internal claude code tools implementaion · GitHub
Introducing advanced tool use on the Claude Developer Platform
How Claude Code Works: Architecture & Internals
Tool search tool - Claude API Docs
Tool Architecture | affaan-m/everything-claude-code | DeepWiki
Claude Code New Features: MCP Tool Search & Checkpoints (2026)
【LLM+Code】Claude Code Agent 0.2.9 版本Prompt&Tools ...
How Claude Code’s New MCP Tool Search Slashes Context Bloat and ...
Claude Code Built-in Tools Reference - vtrivedy
Claude Code 搜索工具完整指南：Tool Search Tool + Glob ...


Focusing on authoritative sources and third-party input


I’m thinking about using a mix of official docs and third-party insights, but not too many. Official docs should remain the primary source, with maybe a few blog contributions like Jerry’s for perspective. It’s crucial to prioritize high-quality, authoritative content. I should also mention instances where I can’t directly verify some details.


Considering reliable sources and mirrors


I’m thinking about using the tool.lu mirror for the trq212 prompt caching, but not counting on RLanceMartin’s article. Instead, it seems better to rely on official advanced tool use and PTC docs. For the X article, I’m leaning toward searching for an official version instead of focusing on possibly inaccessible reposts.


Searching authoritative sources on Claude system architecture


实测Claude computer use | AI能像人一样操控电脑了！熬夜 ...
research/tools-and-integrations/programmatic-tool-calling ... - GitHub
Computer use tool - Claude API Docs
在 Claude Code 中使用 Anthropic API 进行程序化工具调用
Home \ Anthropic
24. 给 Claude 一台电脑，它不只会用工具，它会写程 · 墨问


Looking into potential guardrails for edits


I need to check if there’s a reference to the "Write tool informs model when you edit proposed content in IDE diff" feature, as it might relate to handling stale edits. Searching the documentation for specific terms around "edit/write behavior" could help, and I might also look into blog explanations for staleness handling.


Searching documentation for Write/Edit staleness features


Checkpointing - Claude Code Docs


Organizing task tools and design principles


I’m thinking it might be useful to categorize tool references into functional groups, like discovery, execution, planning, and orchestration. This could help understand tool names better, like "20+" and the current 35. Also, I could look deeper into the design principles, such as prioritizing cognitive load and progressive disclosure.


Understanding tools, evolution, and constraints


Tools act as control surfaces when bash isn’t enough, helping with UX, guardrails, and observability. I see them evolving with model capabilities—like the shift from TodoWrite to task tools. Prompt caching requires static tool order and careful planning. Future changes could reduce explicit tools or evolve orchestration patterns for better safety and hygiene.


Reviewing tool impact and future improvements


I noticed a 37% reduction in average token usage and a 25% improvement in internal knowledge retrieval. The 1M context window isn't directly tied to tool design, but context management plays a role. Research into system tool descriptions improved task completion times by 40%, and I may need to explore PTC metrics and tool search caching further.


Analyzing PTC metrics and tool search performance


Introducing advanced tool use on the Claude Developer Platform \ Anthropic


Inspecting tool search docs for better integration


I need to check the current documentation for Tool Search in Claude Code, especially regarding MCP connections. It's important to link this information to the official product docs, not just the API. I’ll open the relevant resources to gather more details.


Inspecting current Tool Search docs for MCP connectivity


Connect Claude Code to tools via MCP - Claude Code Docs


Searching for RLanceMartin article and related topics


research/tools-and-integrations/programmatic-tool-calling ... - GitHub
Claude Code 的 Agent harness 构建经验：像 Agent 一样思考
Claude code 课程：工具的使用-5.工具选择 - CSDN博客
兰斯·马丁（@RLanceMartin） - 齐思 - 最新最有趣的科技 ...
24. 给 Claude 一台电脑，它不只会用工具，它会写程 · 墨问
构建 Claude Code 的经验教训：像 Agent 一样观察 - Online ...


Opening GitHub mirror results


The search results point to a GitHub mirror, so I’ll proceed by opening it to review the content. Let’s see what’s available there and how it fits into what I need. I'll check if it offers the right kind of information.


Opening GitHub mirror results


research/tools-and-integrations/programmatic-tool-calling-claude/index.md at main · n00el/research · GitHub
24. 给 Claude 一台电脑，它不只会用工具，它会写程 · 墨问


Reviewing GitHub mirror and considering next steps


The GitHub mirror is a community summary rather than an official version, so I’ll cautiously treat it as a reconstruction. I should search for a direct or already available version of trq212 status. I might also pull relevant tool descriptions from the official guidelines for more context. I'll aim to retrieve around 150 lines.


Searching for open lines in turn217462view0


Writing effective tools for AI agents—using AI agents \ Anthropic
How and when to use subagents in Claude Code | Claude


Checking official docs and opening lines


I’ll search the official docs for specific tool search lines with clear context and possibly relevant PTC. We seem to have enough information for now, but I may need to open around line 800 on one source and line 92 on another for further details. Let’s proceed there.


Searching official docs for tool search lines


Connect Claude Code to tools via MCP - Claude Code Docs
Introducing advanced tool use on the Claude Developer Platform \ Anthropic
程序化工具调用 - Claude API Docs


Opening relevant lines for further insight


I’m thinking the auto mode lines didn’t show because I might have been using the wrong line number. I’ll try opening line 0 and maybe the relevant sections nearby to find what I need. Let’s start there and see if it yields something useful.


Opening around line 0 for analysis


Claude Code auto mode: a safer way to skip permissions \ Anthropic


Reviewing tools list and relevant lines


I need to check the tools list closely, especially around the exact lines. I'll open line 52 of the website, but I might also explore line 53 for more details on the table. We already have access to the website, and I’ll make sure to cite that. Also, it’s worth noting that the exact tool set depends on the provider, platform, or settings. Let’s open line 170 for further context.


Opening file at specified lines for tool details


Tools reference - Claude Code Docs
Claude Code | Anthropic's agentic coding system  \ Anthropic
Seeing like an agent: how we design tools in Claude Code | Claude
Lessons from Building Claude Code: Prompt Caching Is Everything - 在线工具


Reviewing prompt caching plan details


I think I need to dive into details about the caching plan for the prompt. I'll open more lines from the website, starting around line 77, to get the specifics. This could help clarify how it's structured and work out any gaps in understanding. Let’s see what we can find.


Browsing prompt caching strategy and relevant code sections


Lessons from Building Claude Code: Prompt Caching Is Everything - 在线工具
Changelog - Claude Code Docs


Exploring tool descriptions for detailed categorization


I think more information is needed about the Task tool and TeamCreate. While I could explore team tool docs, they might not be central. The user wants 20+ tools detailed, and we may need an appendix listing all current tools. To execute well, I’ll gather additional tool table lines, from lines 58-130, to ensure references are thorough.


Researching internal tools and expanding tool references


Tools reference - Claude Code Docs


Gathering more on Monitor and PowerShell


I think I might need more information on Monitor and PowerShell for a fuller understanding. To get that, I’ll open lines around 118 and 128 to see if additional details are available. This should allow me to cover any gaps in the current context.


Providing additional lines for Monitor and PowerShell


Tools reference - Claude Code Docs


Counting tools and considering skill invocation


It looks like the current official count is 35 tools based on the docs. I’ll list them out to confirm. This includes everything from Agent to Write. However, I might also need to check if the docs specify the exact names for permissions or subagent tools. Regarding skills, those will run through the existing Skill tool, not as new entries.


Addressing user's skill and tool inquiry


The user asked about skills, but actually, they seem to be referring to Claude Code tools. There's no directly matching skill, though I could mention the "huang-yimeng style," though it's not highly relevant. I'll provide a structured response, likely grouping the 35 built-in tools by category with a one-line description and design detail for each.


Clarifying tool count and timeline


I’ll explain that the official blog from April 10, 2026, states Claude Code has about 20 tools, while the current docs list 35 built-ins. The difference seems to be due to the blog referring to overall concepts while the docs include task, team, and deprecated tools separately. I'll also provide key timeline events, including new skills and subagents releases, and check the exact changelog for the Monitor addition.


**Analyzing tool documentation and release timeline

**

Changelog - Claude Code Docs


Structuring a detailed response


I think the answer might need to be a bit lengthy, but we can keep it manageable by organizing it into sections. I’ll start with a clear conclusion, then provide a full overview of the tools (grouped by their functions), discuss the design principles, tool evolution, decision matrix, and address the links the user provided. Each section will include citations, and I'll aim to avoid over-complication with too many bullets.


Summarizing tool capabilities and updates


Each new tool expands the action space, which raises the bar. Users tend to prefer subagent use or progressive disclosure over new tools being added. Tool descriptions need careful prompt engineering, including managing parameters and pagination errors. Cache management, safety features, and subagents help improve process efficiency and control context. Overall, design adjusts based on the model’s preferred tool use.


Summarizing tool evolution stories


The evolution of tools has been a process of refining and adapting to new needs. For example, the AskUserQuestion tool evolved from an initial attempt with parameters to a dedicated version for direct responses. Similarly, TodoWrite was replaced with Tasks for better agent communication. Other changes involve improving indexing with skills and optimizing caching strategies for tool selection accuracy. The goal has always been to create a balance between accuracy, efficiency, and context management.


Backgrounding tool development


Monitor and Worktree tools were introduced to handle streaming events from background scripts and provide more control over the work environment. The subagent's dynamic model selection was added to improve task accuracy, as seen in Haiku's Explore.


Why specialized tools over Bash
Specialized tools offer better interaction, context efficiency, and guardrails for safer and more structured execution. Unlike the Bash shell—where each process lacks persistence—tools like Edit, Write, and LSP manage states, permissions, and offer more robust handling of tasks, especially with improved file-awareness and auto-warnings.


Why not rely solely on Bash


Bash is too general, offering weak semantics and high approval costs. It's noisy in context, which makes it harder for models to safely infer its usage. Specialized tools like Read, Grep, Glob, and LSP allow precise retrieval without the overhead, while others like Edit/Write and AskUserQuestion provide structured control.


Regarding blogs and links
The official source emphasizing seeing as an agent is critical. The trq212 status is accessible through a mirror and it's essential for understanding prompt caching's impact on tool architecture. For the RLanceMartin article, I couldn't access the X link but found a GitHub mirror that aligns with Anthropic’s official docs.


Creating a Timeline for Key Releases


I’m compiling a short reading list of official documents and engineering materials. Since citations are already there, I’ll include timeline bullets for key dates: starting from skills support in October 2025 to the Seeing like an Agent blog in April 2026. Dates also help show iteration. I might need to look up exact Monitor changelog dates for clarification.


Creating timeline and reading list with milestones


Changelog - Claude Code Docs


Ensuring Proper Citations for Final Answer


We have enough sources, so I just need to make sure every factual claim is properly cited. Since I used many web sources, I'll provide citations for every paragraph (maybe including multiple per paragraph!). I should avoid raw URLs and instead suggest referring to relevant sources. I'll clarify that some articles were unavailable due to access restrictions but cross-checked using mirrors.


Ensuring citations and tool clarification


X


Final Structure and Citation Handling


For the final response, I’m thinking of organizing it into sections like:


Opening Conclusion

Overview of Current Tools

Thoughtful Design Methodology

Key Evolution Case Studies

Why This Tool Over Others

My Judgment On Your Suggested Materials

Option for Detailing Tool Access/Context/Interaction


Citations


Designing Tools in Action and Time Management


The tools serve not just as actions but also as units that manage time, background execution, session isolation, and migration costs. I'll document the core of the design with succinct bullet points on tool actions, progressive disclosures, architecture, safety, prompt engineering, and model evolution. Then, I’ll link stories like AskUserQuestion, TodoWrite, RAG, and ToolSearch, each with citations.


Citing Sources and Structuring Research


The "Seeing like an agent" concept provides insights into tool failures and iterations. I’ll mention that prompt caching impacts architecture decisions, and cross-check the inaccessibility of an article with a GitHub mirror summary and official docs for honesty. A brief reading list on advanced tool use, multi-agent research, and auto modes could be helpful, keeping citation requirements minimal while maintaining clarity.


Clarifying Citation Sources and Token Savings


The context window and internal evaluation improvements can be cited from trusted sources, with budget compliance numbers (43,588->27,297 tokens) found in official and mirrored docs. While one source provides the exact token savings, the community summary is also valid. We can include relevant citations as long as we are confident in their accuracy, noting any differences between official and mirrored info.


Securing Citation for Official Stats


I’ll refer to the advanced tool docs from the available official source (website)/1/3. The IDs from my previous analysis are helpful, but since I haven't opened them recently, I’ll double-check lines 40 and 43,588. This will ensure I have the correct references for the citation.


Searching for budget compliance and evaluation references


Introducing advanced tool use on the Claude Developer Platform \ Anthropic


Searching for Tool Reference


I should search for the exact reference to "around 20 tools" in the "seeing-like-agent" section. Let me look through the document or source again to locate that specific mention and ensure that I have the correct and relevant details for citing. Should be pretty straightforward to track down.


Searching for "around 20 tools" in seeing-like-agent


Seeing like an agent: how we design tools in Claude Code | Claude


Locating AskUserQuestion Details


I should check around line 281 in the document to find the exact reference for the second attempt of AskUserQuestion, as well as the final tool. I already have line 283, so I’ll just ensure I have the full context and can tie everything together accurately. Let’s get this right.


Locating lines for AskUserQuestion attempt and tool


Seeing like an agent: how we design tools in Claude Code | Claude


Evaluating key details for user response


I’m considering whether to mention examples of product page adoption or the definition of agentic; they might not be needed, though. I could address the tool names in permission rules and the "PowerShell permission hardening" as evidence of security improvements. It would highlight how iterative changes shape the system architecture, but it's optional.


Drafting the final response with clarity and precision


I might include the mention of "TaskOutput deprecated" for simplicity in tool surface area and "ToolSearch auto mode" from the changelog. It's important not to be verbose, though, aiming for 14-18 paragraphs with citations. Additionally, I’ll need to be mindful of correctly using Chinese terms and explaining key concepts to avoid confusion. The count for "35 named built-ins" can be backed up via reasoning from the list but may not need a citation.


Thought for 17m 19s

下面这版不是凭感觉猜，而是尽量用 Anthropic 公开博客、官方文档、changelog，再加上你给的几条讨论，去还原 Claude Code 团队设计 TOOL 的思路。我的总判断是：Claude Code 的工具体系，本质上不是“功能菜单”，而是给 agent 设计的 action space / control surface。他们关心的不是“能不能做这件事”，而是“模型能不能稳定、低成本、低歧义、可审计地做这件事”。Anthropic 自己就把问题表述成：到底该给一个通用工具，还是五十个专用工具；关键是工具要“贴合模型的能力”，而不是贴合工程师的想象。Claude+2Anthropic+2


“Claude Code 20+ TOOL” 现在到底是多少



按当前官方 tools reference 逐项数，Claude Code 公开列出的命名内置工具是 35 个条目；但官方 2026 年 4 月的《Seeing like an agent》又写的是 “currently has ~20 tools”。我倾向于把这理解成两种口径：博客按“概念工具簇”说，文档按“具体工具名”列；再加上 Anthropic 明确说明，实际会话里加载的工具集会因 provider、platform、settings 不同而变化。所以你说“20+ tools”没错，但按今天文档看，公开命名工具已经到 30+ 了。Claude+3Claude+3Claude+3


把这 35 个工具摊开看，最清楚的方式不是逐个背名字，而是看它们分成了哪几层：


找上下文 / 建上下文：Read、Glob、Grep、LSP、WebSearch、WebFetch、ListMcpResourcesTool、ReadMcpResourceTool、ToolSearch、Skill。它们服务的不是“多一个能力”，而是让模型以更低歧义、更低 token 成本去获得上下文。Anthropic 还专门强调：工具描述、参数命名、分页/截断、错误信息，本身就是 prompt engineering。Anthropic+3Claude+3Claude+3

改东西 / 执行动作：Edit、Write、NotebookEdit、Bash、PowerShell。这里已经能看出“语义分层”：能结构化编辑，就别全塞进 shell；能原生支持 Windows，就别强迫一切都走 Git Bash。Bash / PowerShell 仍在，但被放到了更高风险、更高权限的一层。Claude+2Claude+2

规划与澄清：EnterPlanMode、ExitPlanMode、AskUserQuestion。它们解决的不是“缺功能”，而是 agent loop 里最难做好的两件事：模式切换和低摩擦澄清。Claude+2Claude+2

并行与协作：Agent、SendMessage、TeamCreate、TeamDelete、TaskCreate / Get / List / Update / Stop。Claude Code 把多代理和任务状态做成了显式控制面，而不是靠模型在长对话里自己“记住”。Claude+3Claude+3Claude+3

长时运行 / 后台 / 隔离：Monitor、CronCreate / Delete / List、EnterWorktree、ExitWorktree、TodoWrite、TaskOutput（其中后两者一个被弱化、一个已 deprecated）。这说明 TOOL 在 Claude Code 里不只是“动作”，还是时间、后台执行、隔离边界、会话迁移成本的管理单元。Claude+3Claude+3Claude+3


Claude Code 对 TOOL 的“严谨”，严谨在哪



第一层严谨，是 把“加一个工具”当成加一个认知负担。Anthropic 明说，新增工具门槛很高，因为这会给模型“再多一个需要思考的选项”。所以他们并不是能工具化就工具化，而是优先想：能不能靠渐进披露、子代理、技能、文档搜索来解决，而不是扩张 action space。Claude+1


第二层严谨，是 把 prompt caching 当成一等约束。Claude Code 团队甚至说“整个 harness 都围绕 prompt caching 来建”，缓存命中率低到一定程度会报警、会当 SEV 处理。也正因为 tools 属于缓存前缀的一部分，会话中途增减工具会直接打碎缓存。这不是细节，而是反过来塑造了工具设计本身。在线工具+2在线工具+2


第三层严谨，是 把权限语义绑定到工具语义。官方权限系统不是粗暴地“模型能/不能用工具”，而是分成 read-only、bash、file modification 三大层；deny > ask > allow，且规则可以进版本控制。也就是说，工具名不是纯 UI 文案，而是权限、hook、subagent tool list 的基础标识。Claude+1


第四层严谨，是 把安全设计嵌进工具边界，而不是事后补丁。比如 auto mode 里，真正高风险动作才进入 transcript classifier；这个 classifier 只看用户消息和可执行 payload，故意剥离 assistant prose 和 tool output，避免被模型自己“说服”或被工具结果 prompt injection 污染。Anthropic 也很坦诚：这套机制显著优于完全跳过权限，但并不能替代高风险场景的人类审查。Anthropic+2Anthropic+2


第五层严谨，是 把工具格式本身当作模型工程。Anthropic 反复强调：参数名要少歧义，例如 user_id 比 user 好；工具返回要支持分页、过滤、截断；错误信息要帮助模型修正下一次调用，而不是丢一串 opaque traceback。换句话说，Claude Code 不是先定义 API 再让模型适应，而是直接把 tool schema 当作 prompt surface 来优化。Anthropic+1


第六层严谨，是 承认工具会过时。他们公开写了一个很关键的经验：模型能力提升后，原本有帮助的工具，可能反而变成束缚。所以 tool 不是只增不减，而是要持续复盘、替换、收缩。Claude+1


最能体现“思考过程”的几个演化案例



A. 为什么有 AskUserQuestion，而不是让模型自己问


Anthropic 先试了把“提问数组”塞进 ExitPlanTool，结果把“给计划”和“问问题”混在了一次调用里，Claude 会困惑：如果用户回答和计划冲突怎么办，是否要调用两次。第二种方案是让模型按约定 markdown 输出问题，再由前端解析成 UI；结果格式不稳定，Claude 会自己加句子、漏选项、放弃结构。最后才落到专门的 AskUserQuestion tool：可在任意时刻调用、特别适合 plan mode、会阻塞 agent loop 等待用户回答、输出结构化、还能复用到 SDK 和 skills 里。Anthropic 的原话甚至是：“Claude seemed to like calling this tool.” 这句话很关键，说明他们最后选的不是工程上最优雅的方案，而是 对模型最顺手的方案。Claude+1


B. 为什么 TodoWrite 后来不够了，得换成 Task


Claude Code 刚发布时，Anthropic 发现模型需要 todo list 才能不跑偏，于是有了 TodoWrite，甚至还每 5 个 turn 注入一次 system reminder。但模型变强后，这套东西开始“反作用”：Claude 会过度遵守旧 todo，而不是根据新发现改计划；更麻烦的是，subagents 很难围绕一个共享 todo 协作。于是他们把 TodoWrite 让位给 Task：任务可以有依赖、可在子代理间同步、可修改、可删除，更像真正的 agent coordination primitive。这里最重要的不是 Task 本身，而是 Anthropic 公开承认：同一个工具，在不同代模型上会从帮助变成束缚。Claude+2Claude+2


C. 为什么从 RAG 走向 Grep / Read / Skills


Claude Code 内部早期其实用过 RAG：预索引代码库，再把相关片段塞给 Claude。它快，也强，但有 setup 成本、环境脆弱性，更大的问题是：上下文是“被给到模型”的，不是“被模型自己找到的”。后来他们改成 Grep，让 Claude 自己查代码；再往后引入 Skills，把“逐层发现信息”的做法正式化，甚至可以 skill 文件引用其他文件递归展开。这个演化背后的判断是：更强的模型，更适合自己建上下文，而不是被动吃检索结果。Claude+1


D. 为什么很多需求最后没有变成新工具，而是变成“渐进披露 + 子代理”


Anthropic 发现 Claude 经常答不好“Claude Code 自己怎么用”的问题。最直觉的做法是把这些文档常识塞进 system prompt，但他们放弃了，因为这会造成 context rot，干扰主任务。后来试过给 Claude 文档链接让它自己查，但主会话会把大段文档拖进上下文。最终方案不是新工具，而是 Claude Code Guide subagent：文档搜索在独立上下文完成，只把答案带回来。这个例子特别典型：能不加 tool，就不加 tool；先用子代理隔离噪音。Claude+3Claude+3Claude+3


E. 为什么后来一定要有 ToolSearch


当工具库一多，“全部 upfront 塞进上下文”会立刻出问题。Anthropic 官方给的例子很直接：50+ MCP 工具时，工具定义本身就可能吃掉 72K token；他们内部甚至见过 134K token 的工具开销。Tool Search 的办法是：前面只放一个轻量 search tool，真正需要时再加载 3-5 个相关工具。官方给出的结果也很硬：上下文从约 77K 降到 8.7K，保住 95% 的上下文窗口，token 使用下降约 85%，而且大工具库下的 MCP 选择准确率也显著提升。更重要的是，这个设计还与 prompt caching 相容，因为 deferred tools 不会破坏稳定前缀。Claude+3Claude+3Anthropic+3


F. 为什么会走到 PTC：给 Claude “一台电脑”，而不是再加更多离散工具


你给的 RLanceMartin 那条讨论，核心其实就是 Anthropic 官方后来系统化的 PTC（Programmatic Tool Calling，程序化工具调用）：不是让 Claude 一次次自然语言地调用工具、读回中间结果、再调用下一个工具，而是让 Claude 在 code execution 容器里写 Python 代码去编排工具调用。这样中间数据不必反复进上下文，模型 round-trip 也显著减少。Anthropic 官方数据里，复杂研究任务平均 token 从 43,588 降到 27,297，降幅 37%；内部知识检索与 GIA 指标也有提升。Claude平台+2Anthropic+2


但这不等于“以后都别做专用工具，只要 code execution 就行”。这一点恰好也是 RLanceMartin 那个公开讨论里最有价值的地方：当你需要用户交互、审批语义、观测日志、并发控制、或更清晰的安全边界时，离散工具仍然比代码编排更好。 我这里没法直接读到那条 X Article 原文，X 在当前环境只给了登录页；我参考了一个可访问的 GitHub 镜像摘要，并和 Anthropic 官方 PTC 文档交叉验证，结论是一致的。Anthropic+3X (formerly Twitter)+3GitHub+3


为什么“这个工具”，而不是“别的工具”



我把 Claude Code 的取舍压缩成一句话：


专用工具，是为了把“正确的动作”变成模型最容易做出的动作。


更展开一点，就是 5 条判断：


需要更好的用户交互，就做专用工具。 AskUserQuestion 不是能力扩展，而是把“提问”从低带宽文本问答变成阻塞式、结构化、多选式交互。Claude+1

需要更清楚的审批与安全边界，就做专用工具。 Edit / Write / Bash 分层，WebFetch 单独算风险面，PowerShell 预览时也单独做权限硬化。Claude+2Claude+2

需要省上下文、省缓存、省推理轮次，就做 ToolSearch、Subagent、PTC。 这些不是“更花哨”，而是为了控制 token economics。Claude+3在线工具+3Anthropic+3

需要后台观察、持续反馈、并行协作，就做 Monitor / Task / Agent / Worktree。 单靠 Bash 很难把“长时运行的状态”稳定地变成 agent loop 的一部分。Claude+3Claude+3Claude+3

如果只是偶发能力，而不是高频核心动作，就尽量别加 tool。 用 Skills、文档搜索、Guide subagent 这种渐进披露机制更划算。Claude+1


从 changelog 看，Claude Code 的 TOOL 迭代不是一次性设计，而是持续修正



这条时间线很说明问题：2025-10-15 有 Skills 和 Explore subagent；10-18 加入 interactive question tool；10-27 又把 plan mode 升级成 Plan subagent，并允许子代理动态选模型；2026-02-05 出现 research preview agent teams；02-19 增加 --worktree 与后台 agent 相关能力；03-10 加 ExitWorktree；03-26 PowerShell 作为 Windows 预览工具加入；04-09 才新增 Monitor；与此同时，TaskOutput 又被 deprecated，MCP Tool Search 变成默认自动模式。这个轨迹说明 Anthropic 不是先设计一套“完整工具宇宙”再发布，而是 围绕真实失败模式不断加、改、收、替换。Claude+8Claude+8Claude+8


你给的三篇材料，我的判断



《Seeing like an agent》是最核心的一手材料，因为它第一次把 Claude Code 团队的工具设计失败史、取舍逻辑、以及“看待模型能力”的方法直接讲出来。它的关键词不是“更多工具”，而是 elicitation、progressive disclosure、tool surface、context rot。Claude+2Claude+2


trq212 那条关于 prompt caching 的讨论，我认为价值非常高，因为它把一个常被忽视的工程现实讲透了：tool 设计不是只受产品需求约束，还受缓存拓扑约束。 Plan mode 为什么做成 EnterPlanMode / ExitPlanMode 这类工具，而不是切换一整套 tool set，本质上就是 cache-aware design。在线工具+2在线工具+2


RLanceMartin 那条内容，我这里没法直接打开原文，但从可访问镜像和 Anthropic 官方 PTC 文档交叉看，核心观点就是：当工具编排本身成为主要复杂度时，与其继续堆离散工具，不如“给 Claude 一台电脑”，让它在代码里编排工具；但凡涉及 UX、guardrails、observability、approval boundary，离散工具仍然必要。 我认为这恰好补全了 Claude Code 的另一半设计哲学：不是“专用工具 vs 通用工具”二选一，而是 把两者放在合适层级共存。 GitHub+2Claude平台+2


一句话收尾：
Claude Code 的 TOOL 设计，不是在做 API catalog，而是在做 agent operating system。
工具之所以严谨，是因为每个工具同时承担了四个角色：能力接口、上下文压缩器、安全边界、行为引导器。而它们之所以不断迭代，是因为 Claude 变了，缓存约束变了，安全目标变了，真正“最适合模型”的工具形状也就跟着变。Anthropic+3Claude+3Claude+3


你要的话，我下一条可以继续把这 35 个工具逐个拆成一张“工具名 / 解决什么失败模式 / 为什么不是 Bash / 为什么不是子代理”的对照表。



Sources:


https://claude.com/blog/seeing-like-an-agent

https://code.claude.com/docs/en/tools-reference

https://tool.lu/zh_CN/article/7GX/preview

https://www.anthropic.com/engineering/claude-code-auto-mode

https://platform.claude.com/docs/zh-CN/agents-and-tools/tool-use/programmatic-tool-calling

https://x.com/RLanceMartin/article/2027450018513490419

https://github.com/n00el/research/blob/main/tools-and-integrations/programmatic-tool-calling-claude/index.md
