---
title: "Skills explained: How Skills compares to prompts, Projects, MCP, and subagents"
source: "https://claude.com/blog/skills-explained"
author:
published: 2001-11-13
created: 2026-04-16
description: "Skills are an increasingly powerful tool for creating custom AI workflows and agents, but where do they fit in the Claude stack? We explain what tool to use when - and how they all work together."
tags:
  - "clippings"
---
Since introducing [Skills](https://www.anthropic.com/news/skills), there's been interest in understanding how the various components of Claude's agentic ecosystem work together. 自推出 [技能](https://www.anthropic.com/news/skills) 功能以来，人们一直希望了解Claude智能体生态系统的各个组件是如何协同工作的。

Whether you're building sophisticated workflows in [Claude Code](https://www.claude.com/product/claude-code), creating enterprise solutions with the API, or maximizing your productivity on [Claude.ai](http://claude.ai/redirect/claudedotcom.v1.ab82fc0b-7619-451b-9c16-e658270364f2), knowing which tool to reach for—and when—can transform how you work with Claude.无论你是在 [Claude Code](https://www.claude.com/product/claude-code) 中构建复杂的工作流、通过API创建企业级解决方案，还是在 [Claude.ai](http://claude.ai/redirect/claudedotcom.v1.ab82fc0b-7619-451b-9c16-e658270364f2) 上最大化工作效率，了解该选择哪种工具以及何时使用，都能改变你与Claude协作的方式。

This guide breaks down each building block, explains when to use what, and shows you how to combine them for powerful agentic workflows.本指南拆解了每个构建模块，解释了何时使用何种模块，并展示了如何将它们组合起来，打造强大的智能体工作流。

## Understanding your agentic building blocks了解你的智能体构建模块

### What are Skills? 什么是技能？

![](https://www.youtube.com/watch?v=IoqpBKrNaZI)

Skills are folders containing instructions, scripts, and resources that Claude discovers and loads dynamically when relevant to a task. Think of them as specialized training manuals that give Claude expertise in specific domains—from working with Excel spreadsheets to following your organization's brand guidelines.技能是包含指令、脚本和资源的文件夹，当与任务相关时，Claude 会动态发现并加载这些文件夹。可以将它们视为专门的培训手册，能让 Claude 具备特定领域的专业能力——从处理 Excel 电子表格到遵守你所在机构的品牌规范。

**How Skills work:** When Claude encounters a task, it scans available Skills to find relevant matches. Skills use progressive disclosure: metadata loads first (~100 tokens), providing just enough information for Claude to know when a Skill is relevant. Full instructions load when needed (<5k tokens), and bundled files or scripts load only as required.**技能的工作原理：** 当 Claude 遇到一项任务时，它会扫描可用的技能以找到相关的匹配项。技能采用渐进式披露机制：元数据首先加载（约 100 个标记），仅提供足够的信息让 Claude 判断某项技能是否相关。完整说明会在需要时加载（少于 5000 个标记），而捆绑的文件或脚本则仅在有需要时才加载。

**When to use Skills:** Choose Skills when you need Claude to perform specialized tasks consistently and efficiently. They're ideal for:**何时使用技能：** 当你需要 Claude 持续且高效地执行专业任务时，请选择技能。技能适用于以下场景：

- **Organizational workflows**: Brand guidelines, compliance procedures, document templates **组织工作流程** ：品牌指南、合规流程、文档模板
- **Domain expertise:** Excel formulas, PDF manipulation, data analysis **专业领域能力：** Excel 公式、PDF 处理、数据分析
- **Personal preferences:** Note-taking systems, coding patterns, research methods **个人偏好：** 笔记系统、编码模式、研究方法

**Example:** Create [a brand guidelines Skill](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines) that includes your company's color palette, typography rules, and layout specifications. When Claude creates presentations or documents, it automatically applies these standards without you needing to explain them each time.**示例：** 创建 [品牌指南技能](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines) ，其中包含贵公司的配色方案、排版规则和版式规范。当 Claude 制作演示文稿或文档时，会自动应用这些标准，而无需你每次都进行说明。

[Learn more](https://support.claude.com/en/articles/12512176-what-are-skills) about Skills and check out [our growing Skills library](https://github.com/anthropics/skills).[了解更多](https://support.claude.com/en/articles/12512176-what-are-skills) 关于技能的信息，并查看 [我们不断扩充的技能库](https://github.com/anthropics/skills)

### What are prompts? 什么是提示词？

![](https://www.youtube.com/watch?v=ysPbXH0LpIE)

[Prompts](https://docs.claude.com/en/prompt-library/library) are the instructions you provide to Claude in natural language during a conversation. They're ephemeral, conversational, and reactive—you provide context and direction in the moment.[提示词](https://docs.claude.com/en/prompt-library/library) 是你在对话中以自然语言向Claude提供的指令。它们具有短暂性、对话性和反应性——你可以在当下提供上下文和方向。

**When to use prompts:** Use prompts for:**提示词的使用场景：** 提示词适用于以下情况：

- One-off requests: "Summarize this article" 一次性请求：“总结这篇文章”
- Conversational refinement: "Make that tone more professional" 对话优化：“让那个语气更专业一些”
- Immediate context: "Analyze this data and identify trends" 即时语境：“分析这份数据并识别趋势”
- Ad-hoc instructions: "Format this as a bulleted list" 临时指令：“将其格式化为项目符号列表”

**Example: 示例：**

*Please conduct a comprehensive security review of this code. I'm looking for:请对这段代码进行全面的安全审查。我需要检查的内容包括：*

*1\. Common vulnerabilities including:1\. 常见漏洞，包括：*

- *Injection flaws (SQL, command, XSS, etc.) 注入漏洞（SQL 注入、命令注入、跨站脚本等）*
- *Authentication and authorization issues 身份验证和授权问题*
- *Sensitive data exposure 敏感数据泄露*
- *Security misconfigurations 安全配置错误*
- *Broken access control 访问控制失效*
- *Cryptographic failures 加密失败*
- *Input validation problems 输入验证问题*
- *Error handling and logging issues 错误处理与日志记录问题*

*2\. For each issue you find, please provide:2\. 针对你发现的每个问题，请提供：*

- *Severity level (Critical/High/Medium/Low) 严重程度等级（严重/高/中/低）*
- *Location in the code (line numbers or function names) 代码中的位置（行号或函数名）*
- *Explanation of why it's a security risk and how it could be exploited 说明其为何存在安全风险以及可能被利用的方式*
- *Specific fix recommendation with code examples where possible 具体的修复建议（尽可能附上代码示例）*
- *Best practice guidance to prevent similar issues 预防类似问题的最佳实践指导*

*3\. Code context: \[Describe what the code does, the language/framework, and the environment it runs in - e.g., "This is a Node.js REST API that handles user authentication and processes payment data"\] 3\. 代码上下文：\[描述代码的功能、所用语言/框架以及运行环境 - 例如，“这是一个用于处理用户身份验证和支付数据处理的 Node.js REST 应用程序接口”\]*

*4\. Additional considerations: 4\. 额外注意事项：*

- *Are there any OWASP Top 10 vulnerabilities present?是否存在 OWASP 十大漏洞？*
- *Does the code follow security best practices for \[specific framework/language\]?代码是否遵循\[特定框架/语言\]的安全最佳实践？*
- *Are there any dependencies with known vulnerabilities?是否存在存在已知漏洞的依赖项？*

*Please prioritize findings by severity and potential impact.请按严重程度和潜在影响对发现结果进行优先排序。*

**Pro-tip:** Prompts are your primary way of interacting with Claude, but they don't persist across conversations. For repeated workflows or specialized knowledge, consider capturing prompts as Skills or project instructions.**专业提示：** 提示词是你与 Claude 交互的主要方式，但它们不会在不同对话间保留。对于重复的工作流程或专业知识，建议将提示词整理为技能或项目说明。

**When to use a Skill instead:** If you find yourself typing the same prompt repeatedly across multiple conversations, it's time to create a Skill. Transform recurring instructions like "review this code for security vulnerabilities using OWASP standards" or "format this analysis with executive summary, key findings, and recommendations" into Skills. This saves you from re-explaining procedures each time and ensures consistent execution.**何时应改用技能：** 如果你发现自己在多次对话中反复输入相同的提示，就该创建一个技能了。将“按照OWASP标准审查此代码是否存在安全漏洞”或“将这份分析报告整理为包含执行摘要、关键发现和建议的格式”这类重复指令转化为技能。这样能避免你每次都重新说明流程，还能确保执行结果保持一致。

Check out our [prompt library](https://docs.claude.com/en/prompt-library/library), [prompting best practices](http://claude.com/blog/prompt-engineering-best-practices), or [our smart prompt maker](https://claude.ai/redirect/claudedotcom.v1.ab82fc0b-7619-451b-9c16-e658270364f2/public/artifacts/3796db7e-4ef1-4cab-b70c-d045778f23ec) to get started.查看我们的 [提示词库](https://docs.claude.com/en/prompt-library/library) 、 [提示词编写最佳实践](http://claude.com/blog/prompt-engineering-best-practices) 或 [智能提示词生成工具](https://claude.ai/redirect/claudedotcom.v1.ab82fc0b-7619-451b-9c16-e658270364f2/public/artifacts/3796db7e-4ef1-4cab-b70c-d045778f23ec) ，即可开始使用。

### What are Projects? 什么是项目？

![](https://www.youtube.com/watch?v=nbG2DO6Xsek)

Available on all paid Claude plans, [Projects](https://support.claude.com/en/articles/9517075-what-are-projects) are self-contained workspaces with their own chat histories and knowledge bases. Each project includes a 200K context window where you can upload documents, provide context, and set custom instructions that apply to all conversations within that project.所有付费版 Claude 计划都提供 [项目](https://support.claude.com/en/articles/9517075-what-are-projects) 功能，它是独立的工作区，拥有专属的聊天记录和知识库。每个项目都配备 20 万上下文窗口，你可在其中上传文档、提供上下文，并设置适用于该项目内所有对话的自定义指令。

**How Projects work:** Everything you upload to a project's knowledge base becomes available across all chats within that project. Claude automatically uses this context to provide more informed, relevant responses. When your project knowledge approaches context limits, Claude seamlessly enables Retrieval Augmented Generation (RAG) mode to expand capacity by up to 10x.**项目工作原理：** 你上传到项目知识库的所有内容，都可在该项目的所有聊天对话中使用。Claude 会自动利用这些上下文，提供更具针对性和参考价值的回复。当你的项目知识库内容接近上下文限制时，Claude 会无缝启用检索增强生成（RAG）模式，将容量扩大多达10倍。

**When to use Projects:** Choose Projects when you need:**何时使用项目：** 当你需要以下内容时，请选择项目：

- **Persistent context:** Background knowledge that should inform every conversation **持久上下文：** 应指导每次对话的背景知识
- **Workspace organization:** Separate contexts for different initiatives 工作区组织：</b>为不同项目设置独立的上下文
- **Team collaboration:** Shared knowledge and conversation history (on Team and Enterprise plans) **团队协作：** 共享知识和对话历史（适用于团队版和企业版计划）
- **Custom instructions:** Project-specific tone, perspective, or approach **自定义指令：** 项目特定的语气、视角或方法

**Example:** Create a "Q4 Product Launch" project containing market research, competitor analysis, and product specifications. Every chat in this project has access to this knowledge without you needing to re-upload or re-explain the context.**示例：** 创建一个包含市场调研、竞品分析和产品规格的“第四季度产品上线”项目。该项目中的每一次对话都可直接使用这些知识，无需你重新上传或解释上下文。

**When to use a Skill instead:** Projects give Claude persistent context for a specific body of work—your company's codebase, a research initiative, an ongoing client engagement. Skills teach Claude how to do something. A Project might contain all the background on your product launch, while a skill could teach Claude your team's writing standards or code review process. If you find yourself copying the same instructions across multiple Projects, that's a signal to create a skill instead.**何时改用技能：** 项目为 Claude 提供特定工作内容的持久上下文——比如你公司的代码库、一项研究计划、一个正在进行的客户项目。技能则是教 Claude 如何完成某项任务。一个项目可能包含产品上线的所有背景资料，而一个技能可以教会 Claude 你团队的写作规范或代码评审流程。如果你发现自己需要在多个项目中复制相同的指令，这就是创建技能的信号。

[Learn](https://support.claude.com/en/articles/9517075-what-are-projects) more about Projects. [了解](https://support.claude.com/en/articles/9517075-what-are-projects) 更多关于项目的信息。

### What are subagents? 什么是子代理？

[Subagents](https://docs.claude.com/en/docs/claude-code/sub-agents) are specialized AI assistants with their own context windows, custom system prompts, and specific tool permissions. Available in Claude Code and the Claude Agent SDK, subagents handle discrete tasks independently and return results to the main agent.[子智能体](https://docs.claude.com/en/docs/claude-code/sub-agents) 是具备专属上下文窗口、自定义系统提示词以及特定工具权限的专业人工智能助手。子智能体可在 Claude Code 及 Claude 智能体软件开发工具包中使用，能够独立处理独立任务并将结果反馈给主智能体。

**How subagents work:** Each subagent operates with its own configuration—you define what it does, how it approaches problems, and which tools it can access. Claude automatically delegates tasks to appropriate subagents based on their descriptions, or you can explicitly request a specific subagent.**子代理的工作原理：** 每个子代理都有自己的配置——你可以定义其职责、解决问题的方式以及可使用的工具。Claude 会根据子代理的描述自动将任务分配给合适的子代理，你也可以明确指定使用某个特定的子代理。

**When to use subagents:** Use subagents for:**何时使用子智能体：** 将子智能体用于以下场景：

- **Task specialization:** Code review, test generation, security audits **任务专业化：** 代码审查、测试生成、安全审计
- **Context management:** Keep the main conversation focused while offloading specialized work **上下文管理：** 让主对话保持专注，同时将专业工作分流出去
- **Parallel processing:** Multiple subagents can work on different aspects simultaneously **并行处理：** 多个子智能体可以同时处理不同方面的任务
- **Tool restriction:** Limit specific subagents to safe operations (e.g., read-only access) **工具限制：** 将特定子代理限制在安全操作范围内（例如只读权限）

**Example: 示例：**

```
Create a code-reviewer subagent with access to Read, Grep, and Glob tools but not Write or Edit. When you modify code, Claude automatically delegates to this subagent for quality and security review without risking unintended code changes.
```

**When to use a Skill instead:** If multiple agents or conversations need the same expertise—like security review procedures or data analysis methods—create a Skill rather than building that knowledge into individual subagents. Skills are portable and reusable, while subagents are purpose-built for specific workflows. Use Skills to teach expertise that any agent can apply; use subagents when you need independent task execution with specific tool permissions and context isolation.**何时改用技能：** 如果多个智能体或对话需要相同的专业知识——例如安全审查流程或数据分析方法——请创建一个技能，而不是将该知识构建到各个子智能体中。技能具有可移植性和可复用性，而子智能体则是为特定工作流量身定制的。使用技能来传授任何智能体都能应用的专业知识；当你需要具备特定工具权限和上下文隔离的独立任务执行时，再使用子智能体。

[Learn more](https://code.claude.com/docs/en/sub-agents) about subagents. [了解更多](https://code.claude.com/docs/en/sub-agents) 关于子智能体的内容。

### What is MCP? 什么是MCP？

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69141f0993d68ff4c536f316_619a5262.png)

MCP creates a universal connection layer between AI applications and your existing tools and data sources. MCP 在人工智能应用与你现有的工具和数据源之间构建了一个通用连接层。

The Model Context Protocol (MCP) is an open standard for connecting AI assistants to external systems where data lives—content repositories, business tools, databases, and development environments.模型上下文协议（MCP）是一项开放标准，用于将人工智能助手与存储数据的外部系统相连接，这些系统包括内容库、业务工具、数据库和开发环境。

**How MCP works:** MCP provides a standardized way to connect Claude to your tools and data sources. Instead of building custom integrations for each data source, you build against a single protocol. MCP servers expose data and capabilities; MCP clients (like Claude) connect to these servers.**MCP 的工作原理：** MCP 提供了一种将 Claude 连接到你的工具和数据源的标准化方式。无需为每个数据源构建自定义集成，你只需基于单一协议进行开发。MCP 服务器公开数据和功能；MCP 客户端（如 Claude）连接到这些服务器。

**When to use MCP:** Choose MCP when you need Claude to:**何时使用 MCP：** 当你需要 Claude 实现以下功能时，请选择 MCP：

- Access external data: Google Drive, Slack, GitHub, databases 访问外部数据：谷歌云端硬盘、Slack、GitHub、数据库
- Use business tools: CRM systems, project management platforms 使用业务工具：客户关系管理系统、项目管理平台
- Connect to development environments: Local files, IDEs, version control 连接开发环境：本地文件、集成开发环境、版本控制
- Integrate with custom systems: Your proprietary tools and data sources 与自定义系统集成：你的专有工具和数据源

**Example:** Connect Claude to your company's Google Drive via MCP. Now Claude can search documents, read files, and reference internal knowledge without manual uploads—the connection persists and updates automatically.**示例：** 通过 MCP 将 Claude 连接到你公司的 Google 云端硬盘。现在 Claude 可以无需手动上传即可搜索文档、读取文件并引用内部知识——该连接会持续存在并自动更新。

**When to use a Skill instead:** MCP connects Claude to data; Skills teach Claude what to do with that data. If you're explaining *how* to use a tool or follow procedures—like "when querying our database, always filter by date range first" or "format Excel reports with these specific formulas"—that's a Skill. If you need Claude to *access* the database or Excel files in the first place, that's MCP. Use both together: MCP for connectivity, Skills for procedural knowledge.**何时改用技能：** MCP 用于将 Claude 连接到数据；技能则用于教会 Claude 如何处理这些数据。如果你是在解释 *如何* 使用工具或遵循流程——比如“查询我们的数据库时，始终先按日期范围筛选”或“用这些特定公式格式化 Excel 报告”——这就属于技能范畴。如果你需要 Claude 首先 *访问* 数据库或 Excel 文件，那就是 MCP 的工作。两者可结合使用：MCP 负责连接，技能负责流程性知识。

[Learn more](https://www.anthropic.com/news/model-context-protocol) about MCP and check out [documentation](https://modelcontextprotocol.io/docs/develop/build-server) on how to build an MCP server.[了解更多](https://www.anthropic.com/news/model-context-protocol) 关于 MCP 的信息，并查看 [文档](https://modelcontextprotocol.io/docs/develop/build-server) 了解如何构建 MCP 服务器。

## How they work together 它们如何协同工作

The real power emerges when you combine these building blocks. Each serves a distinct purpose, and together they create sophisticated agentic workflows.当你将这些构建模块结合起来时，真正的强大之处便显现出来。每个模块都有其独特的用途，它们共同构成了复杂的智能体工作流。

### Comparison: choosing the right tool对比：选择合适的工具

| Feature 功能 | Skills 技能 | Prompts 提示词 | Projects 项目 | Subagents | MCP |
| --- | --- | --- | --- | --- | --- |
| **What it provides 提供的内容** | Procedural knowledge 程序性知识 | Moment-to-moment instructions 即时指令 | Background knowledge 背景知识 | Task delegation | Tool connectivity |
| **Persistence 持久性** | Across conversations 跨对话 | Single conversation 单次对话 | Within project 在项目内 | Across sessions | Continuous connection |
| **Contains 包含** | Instructions + code + assets 说明+代码+资源 | Natural language 自然语言 | Documents + context 文档 + 上下文 | Full agent logic | Tool definitions |
| **When it loads 加载时机** | Dynamically, as needed 按需动态加载 | Each turn 每一轮 | Always in project 始终在项目中 | When invoked | Always available |
| **Can include code 可包含代码** | Yes 是 | No 否 | No 否 | Yes | Yes |
| **Best for 最适合** | Specialized expertise 专业知识 | Quick requests 快速请求 | Centralized context 集中式上下文 | Specialized tasks | Data access |

### Example agentic workflow: research agent示例智能体工作流：研究型智能体

Let's build a comprehensive research agent that combines multiple building blocks. This example shows how to assemble and activate an agent for competitive analysis.我们来构建一个结合多个基础模块的综合研究智能体。本示例将展示如何组装并激活一个用于竞争分析的智能体。

**Step 1: Set up your Project 步骤1：设置你的项目**

Create a "Competitive Intelligence" project and upload:创建一个“竞争情报”项目并上传：

- Industry reports and market analyses 行业报告与市场分析
- Competitor product documentation 竞争对手产品文档
- Customer feedback from your CRM 来自你的客户关系管理系统的客户反馈
- Previous research summaries 过往研究摘要

Add project instructions: 添加项目说明：

*Analyze competitors through the lens of our product strategy. Focus on differentiation opportunities and emerging market trends. Present findings with specific evidence and actionable recommendations.结合我们的产品战略分析竞争对手。重点关注差异化机会和新兴市场趋势。结合具体证据和可行建议呈现分析结果。*

**Step 2: Connect data sources via MCP 步骤2：通过MCP连接数据源**

Enable MCP servers for: 为以下内容启用 MCP 服务器：

- Google Drive (to access shared research documents) Google 云端硬盘（用于访问共享的研究文档）
- GitHub (to review competitor open-source repositories) GitHub（用于查看竞争对手的开源代码仓库）
- Web search (for real-time market information) 网页搜索（用于获取实时市场信息）

**Step 3: Create specialized Skills 步骤3：创建专业技能**

Create a "competitive-analysis" skill:创建一个“竞争分析”技能：

```
# My Company GDrive Navigation Skill

## Overview
Optimized search and retrieval strategy for Meridian Tech's Google Drive structure. Use this skill to efficiently locate internal documents, research, and strategic materials.

## Drive Organization

**Top-level structure:**
- \`/Strategy & Planning/\` - OKRs, quarterly plans, board decks
- \`/Product/\` - PRDs, roadmaps, technical specs
- \`/Research/\` - Market research, competitive intel, user studies
- \`/Sales & Marketing/\` - Case studies, pitch decks, campaign materials
- \`/Customer Success/\` - Implementation guides, success metrics
- \`/Company Ops/\` - Policies, org charts, team directories

**Naming conventions:**
- Format: \`YYYY-MM-DD_DocumentName_vX\`
- Final versions marked with \`_FINAL\`
- Drafts include \`_DRAFT\` or \`_WIP\`

## Search Best Practices

1. **Start broad, then filter** - Use folder context + keywords
2. **Target document owners** - Sales materials from Sales/, not root
3. **Check recency** - Prioritize documents from last 6 months for current strategy
4. **Look for "source of truth"** - Files with \`_FINAL\`, \`_APPROVED\`, or in \`/Archives/Official/\`

## Research Agent Workflow

1. Identify topic category (product, market, customer)
2. Search relevant folder with targeted keywords
3. Retrieve 3-5 most recent/relevant documents
4. Cross-reference with \`/Strategy & Planning/\` for context
5. Cite sources with file names and dates
```

**Step 4: Configure subagents (Claude Code/SDK only) 步骤4：配置子代理（仅适用于 Claude Code/SDK）**

Create specialized subagents: 创建专业子代理：

`market-researcher` subagent: `market-researcher` 子代理：

```
name: market-researcher
description: Research market trends, industry reports, and competitive landscape data. Use proactively for competitive analysis.
tools: Read, Grep, Web-search
---
You are a market research analyst specializing in competitive intelligence.

When researching:
1. Identify authoritative sources (Gartner, Forrester, industry reports)
2. Gather quantitative data (market share, growth rates, funding)
3. Analyze qualitative insights (analyst opinions, customer reviews)
4. Synthesize trends and patterns

Present findings with citations and confidence levels.
```

`technical-analyst ` subagent: `technical-analyst ` 子代理：

```
name: technical-analyst
description: Analyze technical architecture, implementation approaches, and engineering decisions. Use for technical competitive analysis.
tools: Read, Bash, Grep
---
You are a technical architect analyzing competitor technology choices.

When analyzing:
1. Review public repositories and technical documentation
2. Assess architecture patterns and technology stack
3. Evaluate scalability and performance approaches
4. Identify technical strengths and limitations

Focus on actionable technical insights that inform our product decisions.
```

**Step 5: Activate your research agent 步骤5：激活你的研究智能体**

Now when you ask Claude: "Analyze how our top three competitors are positioning their new AI features and identify gaps we can exploit" 现在当你向 Claude 提问：“分析我们的三大竞争对手如何定位其新人工智能功能，并找出我们可以利用的市场空白”

Here's what happens: 具体流程如下：

1. **Project context loads**: Claude accesses your uploaded research documents and follows project instructions **项目上下文加载** ：Claude 访问你上传的研究文档并遵循项目指令
2. **MCP connections activate**: Claude searches your Google Drive for recent competitor briefs and pulls GitHub data **MCP 连接已激活** ：Claude 会在你的 Google 云端硬盘中搜索最新的竞争对手简报，并提取 GitHub 数据
3. **Skills engage**: The competitive-analysis Skill provides the analytical framework **技能启动** ：竞争分析技能提供分析框架
4. **Subagents execute** (in Claude Code): The market-researcher gathers industry data while the technical-analyst reviews technical implementations **子智能体执行** （在 Claude Code 中）：市场研究员收集行业数据，技术分析师审查技术实现方案
5. **Prompts refine**: You provide conversational guidance: "Focus especially on enterprise customers in healthcare" **提示词优化** ：你提供对话式指导：“特别关注医疗保健领域的企业客户”

**The result:** A comprehensive competitive analysis that draws from multiple data sources, follows your analytical framework, leverages specialized expertise, and maintains context throughout your research project.**结果：** 一份全面的竞争分析报告，该报告整合多个数据源、遵循你的分析框架、借助专业专业知识，并在整个研究项目中保持上下文连贯性。

## Common questions 常见问题

#### How do Skills work? 技能是如何运作的？

Skills use [progressive disclosure](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) to keep Claude efficient. When working on tasks, Claude first scans Skill metadata (descriptions and summaries) to identify relevant matches. If a Skill matches, Claude loads the full instructions. Finally, if the Skill includes executable code or reference files, those load only when needed.技能使用 [渐进式披露](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) 来保持 Claude 的高效性。在处理任务时，Claude 首先扫描技能元数据（描述和摘要）以识别相关匹配项。若有技能匹配，Claude 会加载完整说明。最后，若技能包含可执行代码或参考文件，这些内容仅在需要时加载。

This architecture means you can have many Skills available without overwhelming Claude's context window. Claude accesses exactly what it needs, when it needs it.这种架构意味着你可以拥有大量可用的技能，而不会让 Claude 的上下文窗口不堪重负。Claude 会在需要时精准获取所需内容。

#### Skills vs. subagents: when to use what技能与子智能体：何时使用何种方式

**Use Skills when:** You want capabilities that any Claude instance can load and use. Skills are like training materials—they make Claude better at specific tasks across all conversations.**使用技能的场景：** 你希望获得任何 Claude 实例都能加载和使用的功能。技能就像训练材料——能让 Claude 在所有对话中更擅长特定任务。

**Use subagents when:** You need complete, self-contained agents designed for specific purposes that handle workflows independently. Subagents are like specialized employees with their own context and tool permissions.**在以下情况下使用子代理：** 你需要为特定用途设计的完整、独立的代理来独立处理工作流。子代理就像拥有自身上下文和工具权限的专业员工。

**Use them together when:** You want subagents with specialized expertise. For example, a code-review subagent can use Skills for language-specific best practices, combining the independence of a subagent with the portable expertise of Skills.**在以下情况下结合使用它们：** 你需要具备专业技能的子智能体。例如，代码审查子智能体可以利用技能来实现特定语言的最佳实践，将子智能体的独立性与技能的可移植专业知识相结合。

#### Skills vs. prompts: when to use what技能与提示词：何时使用何种方式

**Use prompts when:** You're giving one-time instructions, providing immediate context, or having a conversational back-and-forth. Prompts are reactive and ephemeral.**使用提示词的场景：** 你在下达一次性指令、提供即时上下文，或是进行来回的对话交流。提示词具有反应性和临时性。

**Use Skills when:** You have procedures or expertise that you'll need repeatedly. Skills are proactive—Claude knows when to apply them—and persistent across conversations.**使用技能的场景：** 你有需要反复使用的流程或专业知识。技能具有主动性——Claude 知道何时应用它们——且在对话中持续有效。

**Use them together:** Prompts and Skills complement each other naturally. Use Skills to provide foundational expertise, then use prompts to provide specific context and refinement for each task.**结合使用二者：** 提示词与技能自然互补。先用技能奠定专业基础，再用提示词为每项任务提供具体的场景设定与优化调整。

#### Skills vs. Projects: when to use what技能与项目：何时使用何种功能

**Use Projects when:** You need background knowledge and context that should inform all conversations about a specific initiative. Projects provide static reference material that's always loaded.**使用项目的场景：** 你需要能为所有关于特定计划的对话提供背景知识和上下文的内容。项目会提供始终加载的静态参考资料。

**Use Skills when:** You need procedural knowledge and executable code that activates only when relevant. Skills provide dynamic expertise that loads on-demand, saving your context window.**使用技能的场景：** 你需要仅在相关时才激活的程序性知识和可执行代码。技能提供按需加载的动态专业知识，能节省你的上下文窗口。

**Use them together when:** You want both persistent context and specialized capabilities. For example, a "Product Development" project containing product specs and user research, combined with Skills for creating technical documentation and analyzing user feedback data.**在以下情况下结合使用它们：** 你既需要持久的上下文信息，又需要专业的功能。例如，一个包含产品规格和用户研究的“产品开发”项目，结合用于创建技术文档和分析用户反馈数据的技能。

**Key difference:** Projects say "here's what you need to know." Skills say "here's how to do things." Projects provide a knowledge base you work within. Skills provide capabilities that work everywhere—any conversation, any project.**核心区别：** 项目说“这是你需要了解的内容”。技能说“这是做事的方法”。项目提供你在其中开展工作的知识库。技能提供适用于任何场景的能力——任何对话、任何项目都适用。

#### Can subagents use Skills? 子智能体可以使用技能吗？

Yes. In Claude Code and the Agent SDK, subagents can access and use Skills just like the main agent. This creates powerful combinations where specialized subagents leverage portable expertise.是的。在 Claude Code 和 Agent SDK 中，子智能体可以像主智能体一样访问和使用技能。这形成了强大的组合，专门的子智能体可以借助可移植的专业能力。

For example, your python-developer subagent can use the pandas-analysis Skill to perform data transformations following your team's conventions, while your documentation-writer subagent uses the technical-writing skill to format API documentation consistently.例如，你的 Python 开发子智能体可以使用 pandas 分析技能，按照团队的约定执行数据转换，而文档撰写子智能体则可运用技术写作技能，统一格式化 API 文档。

## Getting started 快速入门

Ready to build with Skills? Here's how to start:准备好使用 Skills 进行开发了吗？以下是开始的方法：

[**Claude.ai**](https://claude.ai/) **users:** [**Claude.ai**](https://claude.ai/) **用户：**

- Enable Skills in Settings → Features 在设置→功能中启用技能
- Create your first project at claude.ai/projects 在 claude.ai/projects 创建你的第一个项目
- Try combining project knowledge with Skills for your next analysis task 在你的下一个分析任务中，尝试将项目知识库与技能功能结合使用

**API developers: API 开发者：**

- Explore the Skills endpoint in [documentation](https://docs.anthropic.com/) 探索 [文档](https://docs.anthropic.com/) 中的技能端点
- Check out our [skills cookbook](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction) 查看我们的 [技能食谱](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction)

**Claude Code users: Claude Code 用户：**

- Install Skills via [plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) 通过 [插件市场](https://code.claude.com/docs/en/plugin-marketplaces) 安装技能
- Check out our [skills cookbook](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction) 查看我们的 [技能食谱](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction)

eBook 电子书

## Agent Skills 智能体技能

Start using Skills with Claude to build more powerful applications today.立即开始结合 Claude 使用技能，打造更强大的应用程序。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6915038fea2f5466c171c21f_Hand-NodeWeb.svg) ![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/691503928e574d7dc8407b4a_Hand-NodeWeb-1.svg)