---
title: "Multi-agent coordination patterns: Five approaches and when to use them"
source: "https://claude.com/blog/multi-agent-coordination-patterns"
author:
published: 2001-04-10
created: 2026-04-16
description: "Five multi-agent coordination patterns, their trade-offs, and when to evolve from one to another."
tags:
  - "clippings"
---
In an earlier post, we explored when multi-agent systems provide value and when a single agent is the better choice. This post is for teams that have made that call and now need to decide which coordination pattern fits their problem.在之前的一篇文章中，我们探讨了多智能体系统在何时能创造价值，以及单一智能体在何时是更优选择。本文面向那些已经做出选择、如今需要确定哪种协作模式更契合自身问题的团队。

We've seen teams choose patterns based on what sounds sophisticated rather than what fits the problem at hand. We recommend starting with the simplest pattern that could work, watching where it struggles, and evolving from there. This post examines the mechanics and limitations of five patterns:我们见过不少团队选择模式时，只看重其听起来是否专业，而非是否契合当下的问题。我们建议从可行的最简单模式入手，观察它在哪些地方存在短板，再在此基础上逐步优化。本文将剖析五种模式的运作机制与局限性：

- **Generator-verifier**, for quality-critical output with explicit evaluation criteria **生成器-验证器** ，适用于有明确评估标准的高关键质量输出
- **Orchestrator-subagent**, for clear task decomposition with bounded subtasks **协调器-子智能体** ，用于通过有界子任务实现清晰的任务分解
- **Agent teams**, for parallel, independent, long-running subtasks **智能体团队** ，用于并行、独立且长期运行的子任务
- **Message bus**, for event-driven pipelines with a growing agent ecosystem 消息总线</b>，适用于拥有不断扩展的智能体生态系统的事件驱动型管道
- **Shared-state**, for collaborative work where agents build on each other's findings **共享状态** ，适用于智能体基于彼此的发现开展协作的工作场景

## Pattern 1: Generator-verifier 模式1：生成器-验证器

This is the simplest multi-agent pattern and among the most deployed. We introduced it as the verification subagent pattern in our previous post, and here we use the broader generator-verifier framing because the generator need not be an orchestrator. 这是最简单的多智能体模式，也是应用最广泛的模式之一。我们在上一篇博文中将其称为验证子智能体模式，而在这里我们采用更宽泛的生成器-验证器框架，因为生成器不一定是协调者。

### How it works 工作原理

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69d901978c5cc197e3f1c1c7_1b56c9bc.png)

A generator receives a task and produces an initial output, which it passes to a verifier for evaluation. The verifier checks whether the output meets the required criteria and either accepts it as complete or rejects it with feedback. If rejected, that feedback is routed back to the generator, which uses it to produce a revised attempt. This loop continues until the verifier accepts the output or the maximum number of iterations is reached.生成器接收任务并生成初始输出，随后将该输出传递给验证器进行评估。验证器检查输出是否符合要求的标准，要么将其接受为完成状态，要么附带反馈将其拒绝。若输出被拒绝，该反馈会被回传给生成器，生成器据此进行修改并再次尝试。这一循环会持续进行，直到验证器接受输出，或达到最大迭代次数为止。

### Where it works well 适用场景

Consider a support system that generates email responses to customer tickets. The generator produces an initial response using product documentation and ticket context. The verifier checks accuracy against the knowledge base, evaluates tone against brand guidelines, and confirms the response addresses each issue raised. Failed checks return to the generator with feedback that names the exact problem, such as a feature misattributed to the wrong pricing tier or a ticket issue left unanswered.设想一个为客户工单生成邮件回复的支持系统。生成器会结合产品文档和工单上下文生成初始回复。验证器会对照知识库核查准确性，依据品牌准则评估语气，并确认回复解决了所有提出的问题。验证不通过时，系统会将反馈（明确指出具体问题，例如将某功能错误归到错误的价格套餐，或未解答工单中的某个问题）反馈给生成器进行重新生成。

Use this pattern when output quality is critical and evaluation criteria can be made explicit. It’s effective for code generation (one agent writes code, another writes and runs tests), fact-checking, rubric-based grading, compliance verification, and any domain where an incorrect output costs more than an additional generation cycle.当输出质量至关重要且评估标准可以明确制定时，请使用此模式。它适用于代码生成（一个智能体编写代码，另一个智能体编写并运行测试）、事实核查、基于评分标准的评分、合规性验证，以及任何错误输出的代价高于额外生成周期的领域。

### Where it struggles 适用场景受限之处

The verifier is only as good as its criteria. A verifier told only to check whether output is good, with no further criteria, will rubber-stamp the generator's output. Teams most often fail by implementing the loop without defining what verification means, which creates the illusion of quality control without the substance. (We discussed this early victory problem in the previous post.) 验证器的好坏取决于其标准。如果一个验证器只被要求检查输出是否合格，而没有其他进一步的标准，那么它就会对生成器的输出全盘认可。团队最常失败的原因是，在实现这个循环时没有定义验证的具体含义，这就造成了有质量控制的表象，却无其实质。（我们在上一篇文章中讨论过这个早期胜利的问题。）

The pattern also assumes generation and verification are separable skills. If evaluating a creative approach is as hard as generating one, the verifier may not reliably catch problems.该模式还假设生成与验证是可分离的技能。如果评估一种创意方法的难度与生成该方法相当，那么验证器可能无法可靠地发现问题。

Finally, iterative loops can stall. If the generator can't address the verifier's feedback, the system oscillates without converging. A maximum iteration limit with a fallback strategy (escalate to a human, return the best attempt with caveats) prevents this from becoming an infinite loop.最后，迭代循环可能会陷入停滞。如果生成器无法回应验证者的反馈，系统会反复循环而无法收敛。设置带有后备策略（升级至人工处理、返回带有注意事项的最佳尝试结果）的最大迭代次数限制，可避免出现无限循环的情况。

## Pattern 2: Orchestrator-subagent 模式2：协调者-子智能体

Hierarchy defines this pattern. One agent acts as a team lead that plans work, delegates tasks, and synthesizes results. Subagents handle specific responsibilities and report back.层级结构定义了这一模式。有一个智能体担任团队负责人，负责规划工作、分配任务并整合结果。子智能体则承担具体职责并反馈结果。

### How it works 工作原理

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69d901978c5cc197e3f1c1c4_76abfe32.png)

A lead agent receives a task and determines how to approach it. It may handle some subtasks directly while dispatching others to subagents. Subagents complete their work and return results, which the orchestrator synthesizes into a final output.主智能体接收任务并确定处理方式。它可直接处理部分子任务，同时将其他子任务分发给子智能体。子智能体完成工作并返回结果，协调者将这些结果整合为最终输出。

[Claude Code](https://code.claude.com/docs/en/overview) uses this pattern. The main agent writes code, edits files, and runs commands itself, dispatching subagents in the background when it needs to search a large codebase or investigate independent questions so work continues while results stream back. Each subagent operates in its own context window and returns distilled findings. This keeps the orchestrator's context focused on the primary task while exploration happens in parallel.[Claude Code](https://code.claude.com/docs/en/overview) 采用了这种模式。主智能体负责编写代码、编辑文件并自行运行命令，当需要搜索大型代码库或探究独立问题时，它会在后台调度子智能体，以便在结果返回的同时持续推进工作。每个子智能体都在各自的上下文窗口中运行，并返回提炼后的结论。这使得协调者的上下文能够专注于核心任务，同时并行开展探索工作。

### Where it works well 适用场景

Consider an automated code review system. When a pull request arrives, the system needs to check for security vulnerabilities, verify test coverage, assess code style, and evaluate architectural consistency. Each check is distinct, requires different context, and produces a clear output. An orchestrator dispatches each check to a specialized subagent, collects the results, and synthesizes a unified review.设想一个自动化代码审查系统。当拉取请求到来时，系统需要检查安全漏洞、验证测试覆盖率、评估代码风格以及判断架构一致性。每一项检查都各不相同，需要不同的上下文，并能输出清晰的结果。协调器会将每项检查分派给专门的子代理，收集结果后整合出一份统一的审查意见。

Use this pattern when task decomposition is clear and subtasks have minimal interdependence. The orchestrator maintains a coherent view of the overall goal while subagents stay focused on specific responsibilities.当任务分解清晰且子任务间相互依赖度极低时，可采用此模式。协调器始终对整体目标保持清晰认知，同时子智能体专注于各自的具体职责。

### Where it struggles 适用场景受限之处

The orchestrator becomes an information bottleneck. When a subagent discovers something relevant to another subagent's work, that information has to travel back through the orchestrator. If the security subagent finds an authentication flaw that affects the architecture subagent's analysis, the orchestrator must recognize this dependency and route the information appropriately. After several such handoffs, critical details are often lost or summarized away.协调者会成为信息瓶颈。当某个子代理发现与另一个子代理的工作相关的信息时，该信息必须经由协调者传递。如果安全子代理发现了一个影响架构子代理分析的认证漏洞，协调者必须识别出这种依赖关系并对信息进行适当的路由。经过多次这样的信息传递，关键细节往往会丢失或被概括掉。

Sequential execution also limits throughput. Unless explicitly parallelized, subagents run one after another, meaning the system incurs multi-agent token costs without the speed benefit.顺序执行也会限制吞吐量。除非进行显式并行化，否则子智能体将依次运行，这意味着系统会产生多智能体令牌成本，却无法获得速度方面的优势。

## Pattern 3: Agent teams 模式3：智能体团队

When work decomposes into parallel subtasks that can proceed independently for extended periods, orchestrator-subagent can become unnecessarily constraining.当工作被分解为可长期独立执行的并行子任务时，协调者-子代理模式可能会变得不必要的限制。

### How it works 工作原理

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69d901978c5cc197e3f1c1cd_4282798b.png)

A coordinator spawns multiple worker agents as independent processes. Teammates claim tasks from a shared queue, work on them autonomously across multiple steps, and signal completion.协调器会生成多个工作智能体作为独立进程。团队成员从共享队列中认领任务，在多个步骤中自主完成任务，并发出完成信号。

The difference from orchestrator-subagent is worker persistence. The orchestrator spawns a subagent for one bounded subtask, and the subagent terminates after returning a result. Teammates stay alive across many assignments, accumulating context and domain specialization that improve their performance over time. The coordinator assigns work and collects outcomes but doesn’t reset workers between tasks.与协调器-子代理模式的区别在于工作代理的持久性。协调器会为单个有限子任务生成一个子代理，该子代理在返回结果后即终止。而协作代理会在多次任务分配中持续运行，不断积累上下文和领域专业知识，从而随着时间推移提升自身性能。协调器负责分配工作并收集结果，但不会在不同任务之间重置工作代理。

### Where it works well 适用场景

Consider migrating a large codebase from one framework to another. A teammate can migrate each service independently, with its own dependencies, test suite, and deployment configuration. A coordinator assigns each service to a teammate, and each teammate works through the migration autonomously: dependency updates, code changes, test fixes, validation. The coordinator collects completed migrations and runs integration tests across the full system.设想将一个大型代码库从一个框架迁移到另一个框架。一名团队成员可以独立迁移每个服务，每个服务都有自己的依赖项、测试套件和部署配置。协调员为每位团队成员分配对应的服务，每位成员自主完成迁移工作：依赖项更新、代码修改、测试修复和验证。协调员收集已完成的迁移任务，并在整个系统中运行集成测试。

Use this pattern when subtasks are independent and benefit from sustained, multi-step work. Each teammate builds up context about its domain rather than starting fresh with each dispatch.当子任务相互独立且适合进行持续的多步骤工作时，可采用此模式。每位团队成员都会积累其负责领域的相关背景知识，而非每次分配新任务时都从零开始。

### Where it struggles 适用场景受限之处

Independence is the critical requirement. Unlike orchestrator-subagent, where the orchestrator can mediate between subagents and route information, teammates operate autonomously and can't easily share intermediate findings. If one teammate's work affects another's, neither is aware, and their outputs may conflict.独立性是关键要求。与协调器-子智能体模式不同，协调器可在子智能体之间进行协调并传递信息，而团队成员需自主运作，难以轻松共享中间发现。若一名团队成员的工作对另一成员产生影响，双方均无法察觉，其输出结果可能产生冲突。

Completion detection is also harder. Since teammates work autonomously for variable durations, the coordinator must handle partial completion where one teammate finishes in two minutes and another takes twenty.完成检测也更具难度。由于队友会自主工作不同时长，协调者必须处理部分完成的情况——比如一名队友两分钟就完成任务，而另一名则需要二十分钟。

Shared resources compound both problems. When multiple teammates operate on the same codebase, database, or file system, two teammates may edit the same file or make incompatible changes. The pattern requires careful task partitioning and conflict resolution mechanisms.共享资源会加剧这两个问题。当多名团队成员操作同一个代码库、数据库或文件系统时，可能会出现两名成员编辑同一文件或做出不兼容修改的情况。这种模式需要合理的任务拆分和冲突解决机制。

## Pattern 4: Message bus 模式4：消息总线

As agent count increases and interaction patterns grow complex, direct coordination becomes difficult to manage. A message bus introduces a shared communication layer where agents publish and subscribe to events.随着智能体数量增加、交互模式变得复杂，直接协调变得难以管理。消息总线引入了共享通信层，智能体在该层中发布和订阅事件。

### How it works 工作原理

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69d901978c5cc197e3f1c1c1_78a53f59.png)

Agents interact through two primitives: publish and subscribe. Agents subscribe to the topics they care about, and a router delivers matching messages. New agents with new capabilities can start receiving relevant work without rewiring existing connections.智能体通过两种原语进行交互：发布与订阅。智能体订阅其关注的主题，由路由器传递匹配的消息。具备新功能的新智能体可以开始接收相关任务，而无需重新配置现有连接。

### Where it works well 适用场景

A security operations automation system demonstrates where this pattern excels. Alerts arrive from multiple sources, and a triage agent classifies each by severity and type, routing high-severity network alerts to a network investigation agent and credential-related alerts to an identity analysis agent. Each investigation agent may publish enrichment requests that a context-gathering agent fulfills. Findings flow to a response coordination agent that determines the appropriate action.一套安全运营自动化系统展现出了该模式的优势。警报从多个来源传来，分类代理会按严重程度和类型对每个警报进行分类，将高严重程度的网络警报路由给网络调查代理，将凭证相关警报路由给身份分析代理。每个调查代理可能会发布补充请求，由上下文收集代理来完成。调查结果会提交给响应协调代理，由其确定相应的应对措施。

This pipeline suits the message bus because events flow from one stage to the next, teams can add new agent types as threat categories evolve, and teams can develop and deploy agents independently. 该管道适用于消息总线，因为事件会从一个阶段流向另一个阶段，随着威胁类别的演变，团队可以添加新的代理类型，并且团队能够独立开发和部署代理。

Use this pattern for event-driven pipelines where the workflow emerges from events rather than a predetermined sequence, and where the agent ecosystem is likely to grow.适用于事件驱动型管道的模式，此类管道的工作流由事件而非预设序列生成，且智能体生态系统可能会不断扩展。

### Where it struggles 适用场景受限之处

The flexibility of event-driven communication makes tracing harder. When an alert triggers a cascade of events across five agents, understanding what happened requires careful logging and correlation. Debugging is harder than following an orchestrator's sequential decisions.事件驱动型通信的灵活性让问题追踪变得更加困难。当一条警报触发五个代理之间的一系列级联事件时，要理清事件的来龙去脉，就需要进行细致的日志记录和关联分析。调试工作也比追踪编排器的顺序式决策要难得多。

Routing accuracy is also critical. If the router misclassifies or drops an event, the system fails silently, handling nothing but never crashing. LLM-based routers provide semantic flexibility but introduce their own failure modes.路由准确性也至关重要。如果路由器对事件进行了错误分类或丢弃，系统会无声地失效，除了不崩溃外什么都处理不了。基于大模型的路由器具备语义灵活性，但也会带来其自身的故障模式。

## Pattern 5: Shared state 模式5：共享状态

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69d901978c5cc197e3f1c1ca_d18482f0.png)

Orchestrators, team leads, and message routers in the previous patterns all centrally manage information flow. Shared state removes the intermediary by letting agents coordinate through a persistent store that all can read and write directly.在之前的模式中，协调器、团队负责人和消息路由器都对信息流进行集中管理。共享状态则通过让智能体通过一个所有智能体都可直接读写的持久存储进行协调，从而消除了中间环节。

### How it works 工作原理

Agents operate autonomously, reading from and writing to a shared database, file system, or document. There's no central coordinator. Agents check the store for relevant information, act on what they find, and write their findings back. Work typically begins when an initialization step seeds the store with a question or dataset, and ends when a termination condition is met: a time limit, a convergence threshold, or a designated agent determining the store contains a sufficient answer.智能体自主运行，可读写共享数据库、文件系统或文档，不存在中央协调者。智能体会检索存储库中的相关信息，基于获取的内容执行操作，并将结果写回存储库。工作通常始于初始化步骤，该步骤会向存储库中注入一个问题或数据集，而当满足终止条件时（如达到时间限制、达到收敛阈值，或有指定智能体判定存储库中已包含足够的答案），工作便会结束。

### Where it works well 适用场景

Consider a research synthesis system where multiple agents investigate different aspects of a complex question. One explores academic literature, another analyzes industry reports, a third examines patent filings, a fourth monitors news coverage. Each agent's findings may inform the others' investigations. The academic literature agent might discover a key researcher whose company the industry agent should examine more closely.设想这样一个研究综合系统：多个智能体针对一个复杂问题的不同方面展开调查。一个智能体探究学术文献，另一个分析行业报告，第三个研究专利申请，第四个监控新闻报道。每个智能体的研究结果都可能为其他智能体的调查提供参考。学术文献智能体或许会发现一位关键研究者，而行业报告智能体需要对该研究者所在的公司进行更深入的研究。

With shared state, findings go directly into the store. The industry agent can see the academic agent's discoveries immediately, without waiting for a coordinator to route the information. Agents build on each other’s work, and the shared store becomes an evolving knowledge base.借助共享状态，研究结果会直接存入存储库。行业智能体可以立即查看学术智能体的发现，无需等待协调者传递信息。智能体之间相互借鉴成果，共享存储库也随之成为不断演进的知识库。

Shared state also removes the coordinator as a single point of failure. If any one agent stops, the others continue reading and writing. In orchestrator and message-bus systems, a coordinator or router failure halts everything.共享状态还消除了协调器作为单一故障点的问题。如果任意一个代理停止运行，其他代理仍可继续读写。而在编排器和消息总线系统中，协调器或路由器出现故障会导致所有服务停止运行。

### Where it struggles 适用场景受限之处

Without explicit coordination, agents may duplicate work or pursue contradictory approaches. Two agents might independently investigate the same lead. Agent interactions produce system behavior rather than top-down design, which makes outcomes less predictable.在没有明确协调的情况下，智能体可能会重复工作或采用相互矛盾的方法。两个智能体可能会各自独立调查同一线索。智能体的交互会产生系统行为，而非自上而下的设计，这使得结果更难预测。

The harder failure mode is reactive loops. For example, Agent A writes a finding, Agent B reads it and writes a follow-up, Agent A sees the follow-up and responds. The system keeps burning tokens on work that isn’t converging. Duplicate work and concurrent writes have known engineering fixes (locking, versioning, partitioning). Reactive loops are a behavioral problem and need first-class termination conditions: a time budget, a convergence threshold (no new findings for N cycles), or a designated agent whose job is to decide when the store contains a sufficient answer. Systems that treat termination as an afterthought tend to cycle indefinitely or stop arbitrarily when one agent's context fills.更严重的故障模式是反应式循环。例如，智能体A写出一个发现，智能体B读取后撰写后续内容，智能体A看到后续内容后再作出回应。系统会持续消耗令牌用于无法收敛的工作。重复工作和并发写入已有成熟的工程解决方案（锁定、版本控制、分区）。而反应式循环是行为层面的问题，需要设置专门的终止条件：时间预算、收敛阈值（连续N个周期无新发现），或指定一个专门的智能体来判断知识库中是否已包含足够的答案。若将终止视为事后补救措施，系统往往会无限循环，或在某个智能体的上下文占满时无规律停止。

## Choosing and evolving between patterns选择并在不同模式间演进

The right pattern depends on a handful of structural questions about the system. In our previous post, we argued for context-centric decomposition, which divides work by what context each agent needs rather than by what type of work it does. That principle applies here too. The patterns differ in how they manage context boundaries and information flow.合适的模式取决于关于系统的一系列结构性问题。在我们之前的文章中，我们主张以上下文为中心的分解方式，即根据每个智能体所需的上下文来划分工作，而非依据工作的类型。这一原则在此处同样适用。不同模式的区别在于它们管理上下文边界和信息流的方式各不相同。

### Orchestrator-subagent vs. agent teams编排器-子智能体与智能体团队

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69d901978c5cc197e3f1c1d0_cb379a56.png)

Both involve a coordinator dispatching work to other agents. The question is how long workers need to maintain their context.两者都涉及由协调员向其他智能体分配工作。问题在于员工需要维持其上下文的时长。

- **Choose orchestrator-subagent** when subtasks are short, focused, and produce clear outputs. The code review system works well here because each check runs its analysis, generates a report, and returns within a single bounded invocation. The subagent doesn't need to carry context across multiple cycles.当子任务简短、目标明确且能输出清晰结果时，请 **选择协调器-子智能体** 。代码审查系统在此场景下表现良好，因为每一项检查都会执行自身的分析、生成报告，并在单次有限调用内完成返回。子智能体无需在多个循环中传递上下文。
- **Choose agent teams** when subtasks benefit from sustained, multi-step work. The codebase migration fits here because each teammate develops real familiarity with its assigned service: the dependency graph, test patterns, deployment configuration. That accumulated context improves performance in ways one-shot dispatch can't replicate.当子任务需要持续的多步骤工作时， **选择智能体团队** 。代码库迁移就属于这种情况，因为每个团队成员都会逐渐熟悉其负责的服务：依赖关系图、测试模式、部署配置。这种积累的上下文能以一次性分配任务无法复制的方式提升性能。

When subagents need to retain state across invocations, agent teams are the better fit.当子智能体需要在多次调用之间保留状态时，智能体团队是更合适的选择。

### Orchestrator-subagent vs. message bus编排器-子智能体与消息总线

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69d901978c5cc197e3f1c1dc_4313c333.png)

Both can handle multi-step workflows. The question is how predictable the workflow structure is.两者都能处理多步骤工作流。问题在于工作流结构的可预测性如何。

- **Choose orchestrator-subagent** when the sequence of steps is known in advance. The code review system follows a fixed pipeline: receive a PR, run checks, synthesize results.**当步骤顺序已知时，选择协调器-子代理** 。代码审查系统遵循固定流程：接收拉取请求、运行检查、汇总结果。
- **Choose message bus** when the workflow emerges from events and may vary based on what's discovered. The security operations system can't predict what alerts will arrive or what investigation paths they'll require. New alert types may emerge that need new handling. The message bus accommodates that variability by routing events to capable agents rather than following a predetermined sequence.**选择消息总线** 适用于工作流由事件触发且可能因发现的内容而变化的场景。安全运营系统无法预测会收到哪些警报，也无法预知这些警报需要哪些调查路径。可能会出现需要新处理方式的新型警报。消息总线通过将事件路由至具备相应能力的智能体，而非遵循预设序列，来适应这种可变性。

As conditional logic accumulates in the orchestrator to handle an expanding variety of cases, the message bus makes that routing explicit and extensible.随着编排器中条件逻辑不断累积以应对日益增多的场景，消息总线让这种路由变得明确且可扩展。

### Agent teams vs. shared state 智能体团队与共享状态

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69d901978c5cc197e3f1c1df_a8950920.png)

Both involve agents working autonomously. The question is whether agents need each other's findings.两者都涉及智能体自主工作。问题在于智能体是否需要彼此的研究结果。

- **Choose agent teams** when agents work on separate partitions that don't interact. The codebase migration fits here because each teammate handles its service and the coordinator combines results at the end.当智能体处理互不交互的独立分区时， **选择智能体团队** 。代码库迁移就属于这种情况，因为每个成员负责各自的服务，最后由协调者整合结果。
- **Choose shared state** when agents' work is collaborative and findings should flow between them in real time. The research synthesis system is a better match because the academic agent's discovery of a key researcher immediately becomes relevant to the industry agent's investigation.当智能体的工作具有协作性且研究结果需要在它们之间实时流转时，请 **选择共享状态** 。研究综合系统是更合适的选择，因为学术智能体发现的关键研究人员会立即与行业智能体的调查相关联。

Once teammates need to communicate with each other rather than only share final results, shared state makes that more natural.一旦团队成员需要彼此沟通，而不仅仅是分享最终结果时，共享状态会让这一过程变得更加自然。

### Message bus vs. shared state 消息总线与共享状态

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69d901978c5cc197e3f1c1d4_46c9b982.png)

Both support complex multi-agent coordination. The question is whether work flows as discrete events or accumulates into a shared knowledge base.两者均支持复杂的多智能体协调。问题在于，工作是作为离散事件推进，还是累积到共享知识库中。

- **Choose message bus** when agents react to events in a pipeline. The security operations system processes alerts stage by stage, with each event triggering the next before completing. The pattern is efficient at routing events to capable agents.**选择消息总线** ，适用于智能体对管道中的事件做出反应的场景。安全运营系统分阶段处理警报，每个事件完成前都会触发下一个事件。该模式能高效地将事件路由至具备相应能力的智能体。
- **Choose shared state** when agents build on accumulated findings over time. The research synthesis system gathers knowledge continuously. Agents return to the store repeatedly, seeing what others have discovered and adjusting their investigations.当智能体基于长期积累的研究成果开展工作时， **选择共享状态** 。研究综合系统会持续收集知识。智能体反复返回存储库，查看他人的发现并调整自身的研究方向。

The message bus still has a router, which means a central component decides where events go. Shared state is decentralized. If eliminating single points of failure is a priority, shared state provides that more completely.消息总线仍配备路由器，这意味着有一个核心组件来决定事件的去向。共享状态则是去中心化的。如果将消除单点故障作为首要目标，共享状态能更彻底地实现这一点。

If agents in a message bus system are publishing events to share findings rather than trigger actions, shared state is a better fit.如果消息总线系统中的智能体发布事件是为了分享发现而非触发操作，那么共享状态会是更合适的选择。

## Getting started 快速开始

Production systems often combine patterns. A common hybrid uses orchestrator-subagent for the overall workflow with shared state for a collaboration-heavy subtask. Another uses message bus for event routing with agent team-style workers handling each event type. These patterns are building blocks, not mutually exclusive choices.生产系统通常会组合多种模式。一种常见的混合模式是采用编排器-代理架构处理整体工作流，并为协作密集型子任务配备共享状态。另一种模式是使用消息总线进行事件路由，同时由智能体团队风格的工作节点处理各类事件。这些模式都是构建模块，并非互斥的选择。

The following table summarizes when each pattern is appropriate.下表总结了每种模式的适用场景。

| Situation 适用场景 | Pattern 模式 |
| --- | --- |
| Quality-critical output, explicit evaluation criteria 对质量要求高的输出，有明确的评估标准 | Generator-Verifier 生成-验证模式 |
| Clear task decomposition, bounded subtasks 清晰的任务分解、有边界的子任务 | Orchestrator-Subagent 编排器-子代理 |
| Parallel workload, independent long-running subtasks 并行工作负载，独立的长期运行子任务 | Agent Teams 智能体团队 |
| Event-driven pipeline, growing agent ecosystem 事件驱动型流水线，不断壮大的智能体生态系统 | Message Bus 消息总线 |
| Collaborative research, agents share discoveries 协作式研究，智能体共享研究发现 | Shared State 共享状态 |
| No single point of failure required 无需单点故障 | Shared State 共享状态 |

For most use cases, we recommend starting with orchestrator-subagent. It handles the widest range of problems with the least coordination overhead. Observe where it struggles, then evolve toward other patterns as specific needs become clear.对于大多数使用场景，我们建议从协调器-子代理模式开始。该模式能以最低的协调开销处理最广泛的问题。先观察它在哪些场景下存在不足，待具体需求明确后，再逐步向其他模式演进。

*In upcoming posts, we will examine each pattern in depth with production implementations and case studies. For background on when multi-agent systems are worth the investment, see* [*Building multi-agent systems: when and how to use them*](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them)*.*在接下来的文章中，我们将结合实际落地实现和案例研究，深入探讨每一种模式。若想了解多智能体系统值得投入的背景信息，请参阅 [*构建多智能体系统：何时以及如何应用*](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them) *。*

## Acknowledgements 致谢

Written by Cara Phillips, with contributions from Eugene Yan, Jiri De Jonghe, Samuel Weller, and Erik S.由卡拉·菲利普斯撰写，尤金·严、吉里·德·容赫、塞缪尔·韦勒和埃里克·S. 参与撰稿。