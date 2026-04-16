---
title: "How to scale agentic coding across your engineering organization"
source: "https://claude.com/blog/scaling-agentic-coding"
author:
published: 2001-10-15
created: 2026-04-16
description: "As Agentic coding tools mature, technical leaders are wrestling with a practical challenge: moving beyond isolated experiments to organization-wide adoption."
tags:
  - "clippings"
---
The difference between successful and struggling implementations often comes down to execution. Teams that deploy agentic coding thoughtfully see meaningful improvements in development velocity and engineer satisfaction. Those that rush deployment without proper planning encounter resistance, inconsistent results, and difficulty demonstrating value.成功与陷入困境的实施之间的差异往往归结于执行。那些深思熟虑地部署智能体式编码的团队，会在开发速度和工程师满意度上看到显著提升。而那些在没有适当规划的情况下仓促部署的团队，则会遇到阻力、结果不一致，且难以证明其价值。

Working with engineering teams across different industries has surfaced common patterns. Successful adoption depends less on the specific tool and more on how you approach workflow changes, skill development, team dynamics, and success measurement.与不同行业的工程团队合作时，我们发现了一些共同的模式。成功采用这些模式，关键不在于具体的工具，而在于你如何应对工作流程调整、技能培养、团队动态变化以及成效衡量等问题。

Let’s dive in. 让我们深入探讨。

## Understanding agentic coding capabilities理解智能体编程能力

Agentic coding tools differ from basic code completion by understanding broader context and handling multi-step tasks. They can plan approaches and work through implementation details with less hand-holding than earlier AI coding assistants.智能体编程工具与基础代码补全的不同之处在于，它们能理解更广泛的上下文并处理多步骤任务。与早期的人工智能编程助手相比，它们在制定解决方案思路和落实实现细节时，所需的人工指导更少。

Common applications include: 常见应用包括：

**Legacy system modernization**: Development teams use these tools to help migrate older codebases to current platforms. Projects that might have taken years can move faster, though they still require careful oversight and testing to preserve business logic correctly.**遗留系统现代化** ：开发团队借助这些工具，助力将旧代码库迁移至当前平台。原本可能耗时数年的项目，推进速度得以加快，不过仍需细致的监督与测试，以确保业务逻辑得到准确保留。

**Faster onboarding**: New engineers can query codebases directly to understand architecture, dependencies, and implementation patterns. This complements traditional documentation and reduces the time before new hires contribute meaningfully.**更快的入职速度** ：新工程师可以直接查询代码库，了解架构、依赖关系和实现模式。这是对传统文档的补充，还能缩短新员工实现有效贡献的时间。

**Incident response assistance**: SRE and DevOps teams build agents that help diagnose and address common operational issues. While human oversight remains important for complex problems, routine incidents can often be handled with less manual intervention.**事件响应协助** ：SRE和DevOps团队构建智能体，用于诊断和解决常见的运营问题。尽管人工监督对于复杂问题仍至关重要，但常规事件通常只需较少的人工干预即可处理。

**Broader technical participation**: Product managers can explore codebase constraints when writing requirements, and designers can create working prototypes from mockups. This doesn't replace engineering work but enables more informed collaboration across functions.**更广泛的技术参与** ：产品经理在编写需求时可以探究代码库约束，设计师则能从原型稿制作可用原型。这不会取代工程工作，但能促进跨职能之间更有针对性的协作。

These represent starting points rather than exhaustive possibilities for agentic coding applications.这些只是智能体编程应用的起点，而非全部可能的选项。

## Planning your expansion approach 规划你的扩展方案

Effective rollouts balance speed with learning. Rather than deploying to everyone at once or creating lengthy pilot phases, successful organizations build expertise incrementally while maintaining momentum.有效的推广需在速度与学习之间取得平衡。成功的组织不会一次性全员部署，也不会设置冗长的试点阶段，而是在保持发展势头的同时，逐步积累专业经验。

### Start with super users 从核心用户入手

Begin with a pilot group of 20-50 developers who already use AI-assisted tools. This group serves multiple purposes: validating the technology against your codebase, identifying useful workflows, and developing the internal expertise that will help broader adoption.从一个由20至50名已在使用AI辅助工具的开发人员组成的试点小组开始。这个小组有多重作用：针对你的代码库验证该技术、找出实用的工作流程，并培养内部专业能力，这将有助于该技术在更大范围内的推广应用。

Give your pilot group time to experiment with common use cases. Direct experience helps identify which customizations provide value and how well the tool integrates with your existing systems. Have them document patterns they discover—both what works and what doesn't.给你的试点小组留出时间，让他们尝试常见的使用场景。亲身体验有助于确定哪些定制化具有价值，以及该工具与你现有系统的集成效果如何。让他们记录自己发现的模式——包括有效的做法和无效的做法。

Practical pilot activities include: 实用试点活动包括：

- Creating custom slash commands for common tasks like database migrations or feature scaffolding 为数据库迁移、功能脚手架搭建等常见任务创建自定义斜杠命令
- Building CLAUDE.md files that capture coding standards and project-specific context 创建用于记录编码标准和项目特定上下文的 CLAUDE.md 文件
- Identifying repetitive workflows worth automating (boilerplate generation, test creation, dependency updates) 识别值得自动化的重复性工作流程（模板生成、测试创建、依赖项更新）
- Setting up a dedicated channel for troubleshooting and knowledge sharing 建立一个专门用于问题排查和知识共享的频道
- Developing wrapper scripts for third-party tool authentication 开发用于第三方工具身份验证的包装脚本

The pilot phase should surface both opportunities and challenges before you expand access more broadly.在更广泛地推广使用之前，试点阶段应同时暴露机遇与挑战。

### Launch with a hackathon 以黑客松启动

Rather than a phased rollout where teams wait for access, consider uniting your organization with a kickoff event. Your pilot users can share techniques and prompts they've developed while everyone experiments together.与其采用团队等待权限的分阶段推出方式，不如通过启动活动来凝聚整个组织。试点用户可以分享他们摸索出的技巧和提示词，同时让所有人一起进行实践尝试。

This format helps demonstrate capabilities in a low-stakes environment. Engineers who are skeptical about AI assistance often change their perspective after hands-on experience. The collaborative atmosphere also surfaces creative applications your pilot group may not have considered.这种模式有助于在低风险环境中展示各项能力。对人工智能辅助持怀疑态度的工程师，往往在亲身体验后会改变看法。这种协作氛围还能催生出试点团队可能未曾考虑过的创意应用。

Keep the event accessible and energizing—food helps with both attendance and morale.让活动保持亲民且充满活力——食物既能提升参与度，也能鼓舞士气。

### Scale through internal expertise 依托内部专业能力扩大规模

As more people use the tools, your pilot group transitions to an advisory role. They can run workshops, create educational content, and serve as resources when others encounter challenges.随着越来越多的人使用这些工具，你的试点团队将转变为顾问角色。他们可以举办研讨会、制作教育内容，并在其他人遇到挑战时提供支持。

This approach tends to work better than external training programs because internal champions understand your specific environment and can provide relevant examples from actual projects. They speak your organization's language and know your particular pain points.这种方法往往比外部培训项目效果更好，因为内部倡导者了解你们的具体环境，还能从实际项目中提供相关案例。他们说的是你们组织的语言，也清楚你们特有的痛点。

## Using CLAUDE.md files effectively 高效使用 CLAUDE.md 文件

CLAUDE.md files document repository conventions, environment setup, and project-specific behaviors. Their value grows when shared systematically across teams.CLAUDE.md 文件记录了代码仓库的约定、环境设置以及项目特定行为。当在团队间系统地共享这些文件时，其价值会得到提升。

**Create project-level files**: Check a CLAUDE.md file into your repository root. This ensures everyone working on the project inherits the same configuration and context automatically.**创建项目级文件** ：在你的代码仓库根目录中提交一个 CLAUDE.md 文件。这能确保参与项目的所有人都自动继承相同的配置和上下文。

**Treat like documentation**: Update CLAUDE.md files when architectural decisions change or new patterns emerge. Include these updates in pull requests alongside code changes.**按文档规范处理** ：当架构决策发生变化或出现新模式时，更新 CLAUDE.md 文件。在拉取请求中随代码更改一同提交这些更新。

**Include in onboarding**: Make reviewing the project's CLAUDE.md file part of your developer onboarding checklist. New team members should understand both the codebase and how to use Claude Code within that context.**纳入入职流程** ：将查看项目的 CLAUDE.md 文件作为开发者入职清单的一部分。新团队成员需要了解代码库，以及如何在该环境中使用 Claude Code。

**Consider branch variations**: For projects with significantly different patterns across branches, maintain branch-specific CLAUDE.md content that reflects each context.**考虑分支差异** ：对于不同分支存在显著不同模式的项目，需维护特定于分支的 CLAUDE.md 内容，以反映各自的上下文。

A typical project-level file might cover development environment requirements, testing and code standards, key architectural patterns, and current focus areas. This creates living documentation that keeps Claude Code aligned with your evolving practices.一个典型的项目级文件可能涵盖开发环境要求、测试与代码规范、关键架构模式以及当前重点领域。这会形成动态文档，让 Claude Code 与你不断发展的实践保持一致。

## Measuring impact 衡量影响

Pilots need clear success criteria. "How do we measure ROI?" remains a central question for driving adoption beyond early enthusiasts.试点项目需要明确的成功标准。“我们如何衡量投资回报率？”仍是推动方案在早期爱好者之外获得广泛采用的核心问题。

Beyond lines of code written—which captures activity but not necessarily value—teams track multiple indicators:除了编写的代码行数（这能反映出工作活跃度，但未必能体现价值）之外，团队还会追踪多个指标：

**Sprint throughput**: Teams with established DevOps practices can correlate adoption timing with changes in feature delivery speed.**冲刺吞吐量** ：采用成熟 DevOps 实践的团队可以将实践的采用时机与功能交付速度的变化关联起来。

**Task completion time**: Measure how long standard tasks take before and after implementation. This granular view shows where agentic coding provides the most value.**任务完成时间** ：衡量标准任务在实施前后所需的时长。这种细致的视角能体现出智能体编程在哪些方面创造的价值最大。

**Migration velocity**: Track time required to modernize legacy systems. Faster migrations free engineering resources for other priorities.**迁移速度** ：跟踪现代化遗留系统所需的时间。更快的迁移能将工程资源释放出来用于其他优先事项。

**Developer satisfaction**: Survey engineers about time spent on repetitive versus creative work. Job satisfaction matters for retention and productivity.**开发者满意度** ：向工程师开展调查，了解其在重复性工作与创造性工作上的时间分配情况。工作满意度对员工留存率和工作生产率有着重要影响。

**Onboarding duration**: Measure how quickly new hires reach meaningful productivity. Shorter ramps reduce training costs and improve team capacity sooner.**入职周期** ：衡量新员工达到有效生产力的速度。更短的适应期能降低培训成本，并更快提升团队产能。

**Cross-functional efficiency**: Track how often other teams need dedicated engineering support for prototyping and testing. Reduced dependencies can indicate broader technical capability.**跨职能效率** ：跟踪其他团队在原型设计和测试方面需要专门工程支持的频率。减少依赖可表明更广泛的技术能力。

Claude Code includes Activity Metrics that track lines of code accepted, suggestion acceptance rates, daily active users and sessions, organization-wide and per-user spending, and individual developer metrics.Claude Code 包含活动指标，可跟踪已接受的代码行数、建议接受率、日活跃用户和会话数、全组织及按用户划分的支出，以及单个开发者指标。

Sometimes the most persuasive measure is the simplest: concrete examples of tasks that now take a fraction of the previous time. When you can point to specific, meaningful efficiency gains, the value becomes self-evident.有时候最有说服力的衡量标准往往最简单：用具体的例子说明如今完成任务所需的时间仅为过去的一小部分。当你能指出具体且有实际意义的效率提升时，其价值便不言而喻。

## Common adoption challenges 常见的采用挑战

Several predictable issues emerge during agentic coding rollouts. Addressing them proactively improves outcomes:在智能体编码部署过程中会出现几个可预见的问题。主动解决这些问题能够提升最终效果：

### Scope tasks appropriately 合理规划任务范围

New users sometimes give agentic tools overly broad tasks without sufficient context, leading to frustrating results. Test-driven development provides helpful structure and clear success criteria.新用户有时会给智能体工具分配过于宽泛的任务，且缺乏足够的上下文，从而导致令人沮丧的结果。测试驱动开发能提供有用的框架和明确的成功标准。

Start by writing tests that define what success looks like: required functionality, edge cases, error handling. Then implement features incrementally—just enough code to make one test pass at a time. For authentication, you might begin with basic login validation, then add password hashing, then session management.先编写测试来定义成功的标准：所需功能、边缘情况、错误处理。然后逐步实现功能——每次只编写刚好能让一个测试通过的代码。对于身份验证，你可以先从基本的登录验证开始，然后添加密码哈希，再进行会话管理。

Run tests after each step and review the changes before proceeding. Claude Code can help analyze test results, but wait until current functionality works before expanding scope.每完成一步后运行测试，并在继续操作前检查修改内容。Claude Code 可协助分析测试结果，但需在当前功能正常运行后再扩大范围。

Add new requirements gradually by writing tests first, then implementing to pass them. This prevents scope creep and maintains quality.先编写测试，再逐步添加新需求并实现以通过测试。这样可以避免范围蔓延，同时保证质量。

Use focused commands like "write tests for user registration" followed by "implement the registration logic to pass these tests" rather than requesting everything at once.使用聚焦式指令，例如先发出“为用户注册编写测试”，再发出“实现注册逻辑以通过这些测试”，而非一次性提出所有需求。

### Provide adequate context 提供充足的上下文信息

Vague descriptions like "this isn't working" or "the button is too big" don't give the AI enough information to help effectively. Be specific:像“这不管用”或“按钮太大了”这类模糊的描述无法为人工智能提供足够有效帮助的信息。请具体说明：

Share complete error information—full error messages, stack traces, and the specific action that triggered the issue. Copy terminal output or browser console errors directly into your session.分享完整的错误信息——包括完整的错误消息、堆栈跟踪以及触发该问题的具体操作。直接将终端输出或浏览器控制台的错误复制到你的会话中。

Document your environment by including operating system, language versions, framework details, and relevant dependencies. The AI needs this context to provide accurate solutions.记录你的环境信息，包括操作系统、语言版本、框架详情以及相关依赖。AI 需要这些上下文信息来提供准确的解决方案。

For UI issues, take screenshots and describe precisely what's wrong: "the login button extends 20 pixels beyond the container border on mobile screens" rather than "the button looks weird." 遇到UI问题时，请截取屏幕截图并准确描述问题所在：例如写“登录按钮在移动设备屏幕上超出容器边框20像素”，而不是写“按钮看起来很奇怪”。

Specify expected versus actual behavior clearly: "Expected: API returns 200 status with user data. Actual: Returns 401 with 'invalid token' message." 明确说明预期行为与实际行为：“预期：API 返回包含用户数据的 200 状态码。实际：返回 401 状态码并附带‘无效令牌’提示。”

Include relevant file contents—the specific code, configuration, or data related to your issue.提供相关的文件内容——即与你的问题相关的具体代码、配置或数据。

### Develop effective prompting habits 养成高效的提问习惯

Communicating clearly with AI tools takes practice. Many developers expect immediate mind-reading and get frustrated when results miss the mark.与AI工具清晰沟通需要练习。许多开发者期望AI能立刻心领神会，当结果不尽如人意时就会感到沮丧。

Consider if a colleague would understand your request. If not, anticipate what questions they'd have and provide that information upfront.想想同事是否能理解你的请求。如果不能，提前预判他们会提出的问题并提供相关信息。

Structure requests with high-level goals first, then add implementation details. "Build a REST API for user management" followed by specific endpoints and requirements works better than mixing everything together.先按高层次目标构建需求，再补充实现细节。先提出“构建一个用于用户管理的 REST API”，再说明具体的接口和需求，这种方式比将所有内容混在一起效果更好。

Use specific technical language instead of vague terms. "Optimize the database query to reduce response time from 2 seconds to under 500ms" beats "make it faster." 使用具体的技术语言而非模糊表述。“优化数据库查询，将响应时间从2秒缩短至500毫秒以内”要优于“让它更快”。

Show what success looks like with concrete examples. "Follow this existing API pattern \[paste code\]" or "Use this coding style \[share guide\]" provides clearer direction than abstract requirements.用具体示例展示成功的模样。“遵循这一现有的 API 模式\[粘贴代码\]”或“采用这种编码风格\[分享指南\]”，比抽象的要求能提供更清晰的指引。

Break complex work into sequential prompts: "Create the database schema," then "implement product catalog API," then "add shopping cart functionality." Each command should focus on one clear objective.将复杂的工作拆解为一系列连续的提示：先“创建数据库架构”，再“实现产品目录API”，最后“添加购物车功能”。每个指令都应聚焦于一个明确的目标。

Start simple and refine iteratively. "Create a basic user login form" followed by "add input validation" then "implement password strength requirements" tends to work better than specifying everything at once.从简单开始，迭代优化。“创建一个基础的用户登录表单”，接着“添加输入验证”，然后“实现密码强度要求”，这种方式往往比一次性指定所有内容效果更好。

Give specific feedback on output. "The error handling is too generic—add specific validation for email format and password length" guides improvement better than "fix the validation." 针对输出给出具体反馈。“错误处理过于通用——针对电子邮件格式和密码长度添加具体的验证规则”比“修复验证问题”更能指导改进方向。

Reference previous work explicitly when building on earlier steps: "Using the authentication middleware from earlier, now add role-based permissions." 在基于先前步骤进行开发时，明确引用之前的工作：“使用之前的身份验证中间件，现在添加基于角色的权限。”

## Moving forward 接下来

Agentic coding shifts software development from writing every line to guiding implementation. Organizations that see good results focus on building foundations rather than rushing deployment.智能体编程将软件开发从编写每一行代码转变为指导实施。取得良好成效的组织注重打好基础，而非急于部署。

Start with a focused pilot group. Develop internal expertise. Build the infrastructure that supports success. Then expand deliberately through events like hackathons and internal champions.从一个专注的试点小组开始。培养内部专业能力。搭建支撑成功的基础设施。然后通过黑客松活动和内部倡导者等方式稳步扩张。

The path from pilot to production requires patience and systematic planning. Organizations that invest in this foundation tend to see meaningful returns: faster development, higher engineer satisfaction, and capacity to tackle previously difficult projects.从试点到正式投入使用的过程需要耐心和系统性的规划。在这一基础上进行投入的组织往往能获得可观的回报：开发速度更快、工程师满意度更高，同时也具备能力处理以往难以推进的项目。

Scale agentic coding across your engineering organization today.