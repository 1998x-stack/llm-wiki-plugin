# 核心概念启发，深度讲解，构建Managed Agents 完整蓝图

> Source: 文章解读 Anthropic Agent
> Time: 2026/4/16 14:12:04

## Question

核心概念启发，深度讲解，构建Managed Agents 完整蓝图

## Answer

我会把它从“概念启发”推进到“可落地系统设计”：先抽象核心原则，再给出一套从 session、runtime、sandbox、tooling、memory、security 到 ops 的完整蓝图。最后我会补一个适合国内团队分阶段建设的路线图。


我已经把官方工程文和 API 文档对齐起来了。现在能比较清楚地分成两层：上层是 Anthropic 公开出来的产品接口，下层是我基于这些接口反推出的一套“长期有效”的架构蓝图。


我现在不只是沿着 Anthropic 的接口名解释，而是在把它“翻译”成一套可自建、可替换供应商、可长期演进的 Agent OS 蓝图。接下来我会把“原则—架构—运行流程—安全治理—演进路线”完整串起来。

Researching official sources and managed agent documentation


I think the user's asking for a detailed concept, likely about managed agents. Official sources are crucial here, so I plan to rely on article-based findings, official documentation, and a synthesis of that info. Some may require web browsing for updates, including architecture articles or quickstart guides.


Searching for managed agents official docs and concepts


Scaling Managed Agents: Decoupling the brain from the hands
Get started with Claude Managed Agents - Claude API Docs


Searching for relevant documentation on events and vaults


I think I’ll need to look into documentation about events, streaming, environments, and vaults, just to gather more context. There’s still some uncertainty, so I’ll take some time to search for more information and see what else can be useful to provide the best support.


Searching for documentation on events, streaming, and more


会话事件流 - Claude API Docs
Claude Managed Agents：托管式长时智能体的构建与实践 ...


Looking for environment documentation


I think I should look up some documentation about environments. It's a bit unclear, but extra details could definitely help clarify things. I’ll search for the relevant materials to make sure I provide the most accurate and useful information in my response to the user's needs.


Searching for Claude API docs on environments


云环境设置 - Claude API Docs
Claude Managed Agents（托管智能体）开发者参考指南


Searching official docs for agent settings and permissions


Claude Managed Agents overview - Claude API Docs
Agent settings in Microsoft 365 admin center


Looking into prompt caching/compaction in Harness


I think I should check if Harness supports built-in prompt caching and compaction, but I’m wondering if this is necessary for the user’s request. I’ll search for documentation or articles related to it, just in case it’s relevant, though it might not be required for what they need.


Searching for harness built-in prompt caching details


Claude Managed Agents overview - Claude API Docs
Scaling Managed Agents: Decoupling the brain from the hands \ Anthropic


Looking into permission policy and skills


I think I might need to open the permission policy and look into skills, just to be sure about what's needed here. I’m uncertain if this is a necessary step, but it could provide some useful context or clarification, so I’ll check on those details to be thorough.


Creating open permission policy and skill requirements


权限策略 - Claude API Docs


Considering more detailed article lines


I think I might need to include more detail from the article, especially focusing on the lines around the abstract. I’m not sure if it's necessary, but it could help clarify things further. I'll check to see if referencing them in more detail will provide added value.


Opening article lines around abstract for analysis


Scaling Managed Agents: Decoupling the brain from the hands \ Anthropic


Planning a detailed, cited answer with conceptual explanations


The user is asking for a deep, conceptual explanation, along with a blueprint. I’ll make sure to synthesize various ideas carefully. All factual claims will be supported by citations, mainly from official sources. I need to clearly distinguish between inferences and sourced knowledge. Maybe no need for file searches or bullet points, but sections and moderate headings will keep it organized. I'll likely compare the article’s concepts to an OS/DB model for clarity. An ASCII architecture diagram might be useful, without citations inside the code block. Features like agent packs, environment configuration, and permission policies will also need mention.


Building a comprehensive blueprint with citations


I’m aiming for a synthesis of a complete blueprint, including components like product layer, control vs. data plane, runtime primitives, and state/execution models. I’ll compare Anthropic’s offerings to what one might build in a self-hosted environment. I should also include "North Star design principles" while ensuring citations for each claim. For instance, I’ll back up the p50 TTFT and p95 latency drops with citations from the article.


Considering prompt caching and session statuses


I might need to mention the prompt caching TTL (5 minutes) from the events page as it could be relevant to cost, but I'll be careful about how I reference the TTL. I should also mention built-in features like prompt caching, compaction, and session statuses like idle/running—those could fit in with the state machine discussion. I'd cite docs for the relevant data. The search snippet I have should be good enough to use as a source.


Considering callable_agents, permissions, and skills


I might need an extra source for callable_agents. Research mentions them, but it might be safer to avoid details. I can cite a snippet from the search results, where callable_agents are described as a research preview. Also, I should cite mentions of skills and permission policies, focusing on custom tools and networking details.


Creating a clear blueprint structure


For citations, I think search result snippets might be enough to cover certain areas. I’ll mention vaults and workspace-scoped details if necessary, but probably not in this case. I’ll focus on highlighting key concepts like managed agents and infrastructure. The blueprint structure could include foundational principles and clearly defined planes separated into sections.


Thought for 1m 57s

下面我不再把它当成一篇“产品介绍文”读，而是把它当成一篇 Agent 操作系统设计文 来拆。


我的结论先放前面：


Managed Agents 的核心启发，不是“帮你托管一个 agent loop”，而是把 Agent 从一段脆弱的业务代码，升级成一套稳定的运行时抽象。 Anthropic 明确把它定义成一组会比具体 harness 更持久的接口：session、harness、sandbox。文章的原话是，harness 会随着模型进步而“go stale”，所以系统应该围绕稳定接口设计，而不是围绕某一代最优 harness 设计。官方文档则把产品接口进一步固化成 Agent、Environment、Session、Events 这些一等资源。Claude平台+4Anthropic+4Claude平台+4



一、这篇文章真正带来的概念跃迁


以前很多团队做 agent，本质还是在做一段“增强版聊天循环”：


prompt + tools

while loop

遇错 retry

上下文长了就 summarize

需要执行就开容器

容器里既跑模型控制逻辑，也存状态，也拿凭证


Anthropic 这篇文章真正推翻的是这套默认做法。它指出：harness 本身编码了“当前模型还不够强”的假设，这些假设会失效。 他们举的例子是，某代模型会出现接近上下文上限时提前收尾的“context anxiety”，于是 harness 加了 context reset；但换更强模型后，这个补丁就变成 dead weight。Anthropic+1


所以文章真正想说的是：


Agent 系统里最不应该被“写死”的部分，恰恰是大家最喜欢优化的那部分：harness。
应该稳定的是接口边界，不是当代最强 prompt loop。Anthropic+1



二、核心概念启发：把 Agent 当成“运行时”，不是“提示词工程”


1. Session 不是聊天记录，而是 durable state


Anthropic 把 session 定义成 append-only log，记录“发生过的一切”；官方产品里，Session 也是独立资源，引用 Agent 和 Environment，并在多轮交互中维护历史。会话驱动是事件式的：你发用户事件，系统返回 agent/session/span 事件。Anthropic+2Claude平台+2


这带来的启发是：


长时 Agent 的真状态，不应该藏在 prompt 里，也不应该绑在某个活着的进程里，而应该落在外部可恢复的事件流里。 这本质上是把 agent 做成一种 event-sourced runtime。这个表述是我的归纳，但它直接来自 Anthropic 对 session log、getSession()、emitEvent()、崩溃后 wake(sessionId) 恢复的描述。Anthropic


2. Harness 不是业务代码，而是可替换的编排器


官方 overview 直接说 Managed Agents 提供 harness 和 infrastructure；工程文则把 harness 定义为“调用 Claude、路由工具调用、组织上下文的 loop”。Anthropic 甚至把 Managed Agents 称作 meta-harness：不预设未来 Claude 需要哪种具体 harness，只保证周边接口稳定。Claude平台+2Anthropic+2


启发是：


你应该把 harness 当成策略层，而不是系统事实层。
事实层在 session；执行层在 sandbox / tools；harness 只是“当前版本的解释器”。


3. Sandbox 不是 agent 本体，而是一个“手”


文章里最有名的比喻是 “brain vs hands”。Anthropic 解释，brain 和 hands 解耦后，容器只在需要时通过一个类似 execute(name, input) -> string 的接口被调用；每个 hand 可以是容器、手机、甚至别的设备或系统。这样不但可以按需 provision，还能让一个 brain 对接多个 hands。Anthropic


启发是：


执行环境应是工具化资源，而不是 agent 身份的一部分。
这意味着“文件系统”“浏览器”“代码执行”“GitHub”“手机自动化”“ERP 操作”都应被统一看成 execution surface，而不是杂乱插件。


4. Context 不是整个 session，本质上只是 working set


Anthropic 说得很清楚：session 负责 durable / recoverable storage，harness 负责 arbitrary context management。可以从 session 抓取历史片段，再变换后放回模型窗口；这样把“可恢复历史”和“当前工作集”分开，避免把 prompt 直接当 source of truth。Anthropic


这对所有做长任务的团队都很关键：


上下文窗口只是 cache，不是数据库。


5. 安全不该建立在“模型暂时还不够聪明”上


Anthropic 明确批评了旧做法：把模型生成的非可信代码和凭证放在一个容器里，prompt injection 只要诱导模型读环境变量，就可能拿到 token。它的结构性修复，是让 token 永远不可从 sandbox 触达；同时官方产品又把 vaults 做成独立认证原语，在会话创建时按 ID 绑定用户凭证，而不是每次调用传 token。Anthropic+2Claude平台+2


启发是：


Agent 安全的主战场不是 prompt guardrail，而是 secret reachability。



三、构建 Managed Agents 的完整蓝图


下面这套蓝图，不是逐字复述 Anthropic 实现，而是基于文章和官方接口抽象出来的 vendor-neutral 版本。也就是说，哪怕你不直接用 Anthropic 的托管服务，自建时也应该朝这个方向收敛。Anthropic 官方已经把核心资源定成 Agent、Environment、Session、Events、Vaults、Permission Policies、Skills；我下面是在这个基础上补齐一个完整系统。Claude平台+5Claude平台+5Claude平台+5



四、蓝图总览：六层架构


第 1 层：Spec / Control Plane


这一层负责“定义”，不负责“运行”。


它至少应包含 4 类对象：


AgentSpec
定义模型、system prompt、工具集、MCP servers、skills、可调用的其他 agents、元数据、版本号。官方文档明确说 Agent 是可复用、带版本控制的配置资源。Claude平台+1


EnvironmentSpec
定义容器模板、预装包、网络策略、allowed hosts。官方文档说明 Environment 是容器配置模板，可复用；多个 session 共用同一环境定义，但各自拿到隔离容器实例。Claude平台+1


PolicySpec
定义工具权限、人工审批阈值、预算、审计、网络策略。Anthropic 已公开了 permission policies，区分 always_allow 和 always_ask，并支持对单个工具覆写策略。Claude平台


CredentialSpec / VaultRef
定义某个 end-user、租户或业务身份可访问的外部系统。Anthropic 的 vaults 就是这层抽象：凭证注册一次，在创建 session 时通过 vault_ids 绑定。Claude平台+1


设计原则： control plane 中所有对象都应可版本化、可回滚、可审计。Anthropic 已对 Agent 做了版本化支持，并允许在 session 启动时 pin 到特定 agent version；Environment 本身不版本化，所以如果你自建，最好自己补一层 environment revision。前半句是官方事实，后半句是我给你的设计建议。Claude平台+2Claude平台+2



第 2 层：Session / State Plane


这是整个系统的“真状态层”。


最小对象模型应包括：


Session

Event

Span

Artifact

Checkpoint

Usage


Anthropic 官方已经公开了 Session 和事件流：会话是状态机，常见状态包括 idle、running、rescheduling、terminated；通信通过事件完成；会话对象还可返回累计 usage，用于监控 token 消耗和预算。Claude平台+1


我的建议是把事件分成 6 大类：


User events：用户请求、补充约束、人工确认

Agent events：思考结果、工具调用、消息输出

Tool events：开始、结束、返回值、错误

Session events：状态变化、重调度、终止

Span events：子任务、阶段、性能分段

Governance events：审批、拒绝、预算触发、升级人工


这样做的原因是：Anthropic 已经证明“外置 durable log”是恢复和扩展的基础；你要进一步把它升级成能支撑审计、回放、评估、计费和训练数据沉淀的总线。前半句来自官方，后半句是架构延伸。Anthropic+1



第 3 层：Harness / Orchestration Plane


这一层是“大脑调度器”，但它必须是 无状态可替换 的。


Anthropic 的核心做法就是 harness 也做成 cattle：崩了就重拉，从 session log 读回历史继续跑，不必抢救旧进程。文章明确提到 harness 崩溃后可用 wake(sessionId) 和 getSession(id) 恢复，再通过 emitEvent 持续写回 durable event log。Anthropic


所以你自建时，harness 应至少拆成 5 个子模块：


Planner
决定当前该做什么：直接答复、提问、调用工具、拆任务、切 agent。


Context Manager
决定当前窗口要塞什么。Anthropic 明确把 context management 留在 harness，而不是 session。Anthropic


Tool Router
把调用路由到 sandbox、MCP、custom tool、另一个 callable agent。官方 Agent 配置里已经把 tools、mcp_servers、skills、callable_agents 列成能力面。Claude平台+1


Recovery Manager
处理中断、重试、继续执行、幂等补偿。


Policy Gate
在真正执行危险动作前做批准、预算、网络、租户权限检查。Anthropic 的 permission policies 已经给出最基础的形态。Claude平台


这里最关键的原则是：


harness 不能拥有任何不可恢复状态。
否则你会重新回到“单个 agent 进程挂了就全盘重来”的 demo 架构。



第 4 层：Hands / Execution Plane


Anthropic 的文章已经把这层说透了：hand 本质就是通过统一工具接口暴露的执行环境，brain 不应依赖 hand 的实现细节；这样既能 many hands，也能按需挂接。Anthropic


你应该把 hands 分成 4 类：


Cloud Sandboxes
临时代码执行、文件编辑、repo 操作、数据分析。官方 Environment 就是这层，支持预装包与网络配置。Claude平台+1


Remote MCP Services
标准化第三方能力，如 GitHub、Jira、Notion、内部服务。官方 Agent 支持配置 MCP servers 与 mcp toolsets。Claude平台+1


Custom Tools
由你的应用执行的业务动作。官方文档明确说 custom tools 由你的应用执行，不受 permission policies 约束，因为执行控制权在你这边。Claude平台


Callable Agents / Specialist Agents
把复杂任务分发给别的 agent。官方把 callable_agents 标成研究预览。Claude平台


我的建议是统一成这个接口思维：


Capability = {name, schema, auth_context, risk_level, executor_type, idempotency_key, timeout_policy}


这不是 Anthropic 文档原文，但它是把 Anthropic 的 hand 抽象工业化后的自然下一步。



第 5 层：Security / Trust Plane


这一层最不能省。


Anthropic 的文章和官方文档联合给了一个很清晰的安全模型：


非可信代码应运行在 sandbox 中，不应接触凭证

凭证应通过 vault / proxy / server-side 代表调用，而不是暴露给模型或容器

工具应可配置自动运行或人工批准

生产环境建议用 limited networking，并把域名列入 allowed_hosts，遵循最小权限原则。Claude平台+3Anthropic+3Claude平台+3


如果我把它翻译成一套可落地的安全蓝图，就是 7 条：


1. Secret unreachable
模型看不到 token，生成代码也拿不到 token。Anthropic+1


2. Tool-level authorization
授权发生在服务端工具入口，不在 prompt 里。Anthropic 的 permission policies 是最小实现。Claude平台


3. Network least privilege
sandbox 默认 limited network，只开必要域名。官方文档明确建议生产这样做。Claude平台


4. Human approval for high-risk effects
例如 bash、写生产库、发消息、转账、删数据。Anthropic 支持 always_ask，并通过 user.tool_confirmation 继续执行。Claude平台+1


5. End-user delegated identity
agent 是以谁的身份做事，要能绑定并审计。vaults 的设计就是为此服务。Claude平台+1


6. Full audit trail
谁触发、模型做了什么、批准了什么、外部系统写入了什么，都写 event log。


7. Blast radius control
每个 hand 独立故障域；一个 hand 挂了，不应把整场任务状态带走。Anthropic 把 hands 与 brains 解耦，本质就在降 blast radius。Anthropic



第 6 层：Observability / Cost / Ops Plane


Anthropic 的官方接口已经公开了 usage 聚合、事件流、状态流转、提示缓存和压缩优化；工程文还给了一个极强信号：brain/hands 解耦后，p50 TTFT 降约 60%，p95 降超 90%。Claude平台+2Claude平台+2


所以一个完整 Managed Agents 系统，至少要看 10 个指标：


TTFT

task completion rate

human handoff rate

tool success rate

retry rate

sandbox cold-start rate

average events per task

context fetch cost

token / cache hit ratio

unsafe action blocked rate


这些指标名称是我的建议，但它们直接对应 Anthropic 已经暴露的状态、usage、事件、prompt caching 与 performance 关注点。Claude平台+2Claude平台+2



五、最关键的设计：Session、Context、Memory 三者怎么分


这里最容易做错。


很多团队把“历史消息”“长期记忆”“工作上下文”混成一坨。Anthropic 的文章给了一个更好的分层。Anthropic


正确分法


Session Log
不可篡改事实流。发生过什么，都在这里。用于恢复、审计、重放。Anthropic+1


Working Context
当前这一轮让模型看到的工作集，由 harness 动态选择和变换。Anthropic


Memory
从大量 session 中抽取的、可复用的长期知识，比如用户偏好、项目背景、常用流程。Anthropic 这篇没展开 memory，但 skills 的“按需加载领域知识，只在相关时影响上下文窗口”给了一个很好的思路：memory 不应总是灌进 prompt，而应像 skill 一样渐进披露。 前半句基于 skills 文档，后半句是我的设计延伸。Claude平台


因此，推荐的上下文装配器应该长这样


每一轮模型调用前，Context Manager 做 5 件事：


取最近 N 个关键事件

加入当前任务计划与未完成阻塞项

加入相关 artifact 摘要

按需拉取 skill / memory 片段

依据缓存友好原则组织上下文


Anthropic 官方明确说 harness 支持 prompt caching、compaction 等优化；事件页也公开了 cache 读写 usage 字段和 5 分钟 TTL。Claude平台+1



六、一个真正能跑长任务的标准执行流


下面是我建议的 canonical flow。不是 Anthropic 文档原文，但和它的 Session / Events / Tool Confirmation / Vault / Environment 模型完全一致。Claude平台+5Claude平台+5Claude平台+5


阶段 1：创建定义


选 AgentSpec 版本

选 EnvironmentSpec

绑定 VaultRef

附上 permission policy


阶段 2：启动 Session


创建 session，引用 agent + environment

session 初始状态 idle

等待用户事件触发实际工作Claude平台


阶段 3：harness 唤醒


读取 session log

组装 working context

调模型生成下一步动作


阶段 4：执行动作


若是直接回复，发 agent message event

若是工具调用，发 agent.tool_use / agent.custom_tool_use / agent.mcp_tool_use

若工具需审批，session 进入 requires_action 停顿，等待 user.tool_confirmation

若是 custom tool，外部系统执行后发 user.custom_tool_result 回来Claude平台+1


阶段 5：回写状态


结果写回 event log

产物落 artifact store

usage 累加

判断继续、暂停、重调度或终止Claude平台+1


阶段 6：崩溃恢复


harness 挂了无所谓

重新 wake

从 session log 恢复

继续跑Anthropic


这条执行流的本质，是让 agent 不再依赖“有一个活着的主循环”。



七、如何构建 “many brains, many hands”


这是文章里最有未来感的一部分。


Anthropic 说，brain/hands 解耦后，不需要每个会话都先为一个容器付出冷启动；只有需要 hand 时才通过工具调用挂上执行环境，因此 TTFT 显著下降。同时 hands 是统一工具接口，brain 不需要关心它背后是容器还是别的系统；甚至 brains 之间还可以传 hand。Anthropic


把它变成工程方案，就是：


many brains


同一 Session 可被多个 stateless harness worker 抢占继续执行

同一任务可拆成多个 sub-session / sub-agent

Planner agent 负责任务分解

Specialist agent 负责局部执行

Supervisor agent 负责汇总与冲突消解


many hands


一个脑可以同时使用 shell、browser、sql、github、crm、internal api

hand 要有统一 schema、鉴权、超时、幂等与返回格式

hand 之间故障隔离

hand 可以按任务动态注入


Anthropic 官方已经把 callable_agents 放进 agent 能力面，虽是 research preview，但足以说明它也在朝多 agent 编排走。Claude平台


我自己的判断是：


many brains, many hands 不是“多接几个工具”这么简单，而是 Agent 从单线程工具使用，走向分布式任务编排。



八、你要自己补上的三个关键能力


Anthropic 这篇文很强，但它没把这三块展开。你自建时一定要补。


1. 幂等与副作用控制


工具接口不能只返回 string。工程里你至少要有：


effect_type: read / write / destructive

idempotency_key

retry_class

compensation_strategy


这是我对 execute(name, input) -> string 的工业级扩展。Anthropic 给的是最小抽象；生产系统必须在其上补 side effect discipline。Anthropic


2. Artifact 管理


会话里不只是消息，还有文件、diff、报告、截图、数据表。官方产品已经支持文件、容器和 Office/PDF 类 skills，说明 artifact 是一等对象，只是这篇工程文没细讲。Claude平台+1


3. Eval 与治理闭环


Managed Agents 不是“能跑就行”，而是要能持续变更 harness、模型、tools、skills 而不把线上搞坏。因此你需要：


replay eval

golden tasks

failure taxonomy

policy regression

cost regression

latency regression


这部分是我的建议，但正好对应 Anthropic 把 Agent、Environment、Policy、Version 做成独立对象的原因：为了让变更可控。Claude平台+2Claude平台+2



九、一个可落地的对象模型


你如果真要构建自己的 Managed Agents，我建议核心 schema 至少有这些：


AgentSpec


id, version, model, system, toolsets, mcp_servers, skills, callable_agents, metadata


这和官方 Agent 资源基本一致。Claude平台+1


EnvironmentSpec


id, runtime_type, packages, networking_mode, allowed_hosts, filesystem_profile


这和官方 Environment 基本一致，只是我额外补了 filesystem_profile。Claude平台+1


Session


id, agent_ref, environment_ref, vault_refs, status, usage, created_at, archived_at


Anthropic 的 session 文档里已有这些核心关系与状态。Claude平台


Event


id, session_id, type, actor, payload, processed_at, causal_parent_id


Anthropic 已公开事件类型、方向和 processed_at。causal_parent_id 是我建议补的。Claude平台


Capability


name, executor_type, schema, auth_scope, permission_policy, timeout, idempotency_class


其中 permission policy 来自官方，其他是工程增强。Claude平台


Vault


id, user_ref, provider, credential_refs, refresh_policy


官方 vaults 已公开“在 session 创建时引用 per-user credentials”的模式。Claude平台+1



十、分阶段建设路线图


第 0 阶段：先别做 Managed，先做可观测


只做：


单 agent

单 sandbox

event log

tool trace

usage trace

人工审批


目标不是高自治，而是先把“发生了什么”看清楚。Anthropic 的产品也把事件、usage、session 状态做成显式接口，说明这一步是基础。Claude平台+1


第 1 阶段：brain / hand 解耦


把：


运行状态从容器里拿出来

harness stateless 化

sandbox 按需 provision

credentials 移出执行环境


这一步是 Managed Agents 文章的精髓。Anthropic+1


第 2 阶段：引入 policy 与 vault


把高风险工具改成审批流，把 end-user identity 和第三方凭证独立管理。Anthropic 的 permission policies 和 vaults 正是这一步。Claude平台+1


第 3 阶段：引入 skills 与 context manager


把领域知识从 system prompt 挪出去，变成按需加载的 skill / memory。Anthropic 的 skills 就是这类渐进披露能力。Claude平台


第 4 阶段：many brains, many hands


开始做：


specialist agents

callable agents

sub-session

parallel execution

failure domain isolation


这一步才是真正的 agent platform，而不是“高级工具调用”。Anthropic 的文章和 agent setup 已释放出这个方向。Anthropic+1



十一、最值得记住的 8 条原则


状态在 session，不在进程。 Anthropic+1

harness 是可替换策略，不是系统事实。 Anthropic

context window 是 working set，不是数据库。 Anthropic

sandbox 是 hand，不是 brain。 Anthropic

secrets 必须对生成代码不可达。 Anthropic+1

权限控制应落在工具层，不落在 prompt 层。 Claude平台

扩展靠稳定接口，不靠当前最佳 harness。 Anthropic+1

Agent 平台最终竞争的是 runtime quality，不只是模型能力。 这句是我的判断，但它直接由 Anthropic “提供 harness and infrastructure” 与 “meta-harness” 的产品方向推出。Claude平台+1



最后一层判断


如果把这篇文章压缩成一句话，我会这么说：


Managed Agents 的本质，是把“AI 会不会做事”升级成“AI 如何被安全、可恢复、可扩展地托管做事”。 Anthropic 不是单纯在卖一个长时 agent，而是在定义 Agent Runtime 的最小稳定接口：可版本化的 Agent、可复用的 Environment、事件驱动的 Session、可隔离的 Hands、可外置的 Credentials、可插拔的 Skills。Claude平台+5Claude平台+5Claude平台+5


如果你愿意，我下一条可以继续直接给你一版：


“从 0 到 1 设计 Managed Agents 的系统架构图 + 核心数据表结构 + API 设计草案”。



Sources:


Scaling Managed Agents: Decoupling the brain from the hands \ Anthropic

Claude Managed Agents overview - Claude API Docs
