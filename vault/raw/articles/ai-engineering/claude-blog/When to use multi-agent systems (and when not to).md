---
title: "When to use multi-agent systems (and when not to)"
source: "https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them"
author:
published: 2001-01-23
created: 2026-04-16
description: "Most teams don't need multi-agent systems. Learn the three scenarios where they consistently outperform single agents—and how to implement them effectively."
tags:
  - "clippings"
---
A multi-agent system is an architecture where multiple LLM instances run with separate conversation contexts, coordinated through code. Multiple coordination patterns exist (agent swarms, capability-based systems, and message bus architectures), but this article focuses on the orchestrator-subagent pattern: a hierarchical model where a lead agent spawns and manages specialized subagents for specific subtasks. This pattern offers a straightforward coordination model and is a good starting point for teams new to multi-agent systems. We'll explore other patterns in detail in our next article.多智能体系统是一种架构，其中多个大语言模型（LLM）实例在独立的对话上下文下运行，并通过代码进行协调。该系统存在多种协调模式（智能体群、基于能力的系统以及消息总线架构），但本文重点探讨协调器-子智能体模式：这是一种分层模型，由主智能体生成并管理针对特定子任务的专用子智能体。该模式提供了一种直观的协调机制，是刚接触多智能体系统的团队的良好起点。我们将在下一篇文章中详细探讨其他模式。

Today, multi-agent systems are often applied in situations where a single agent would perform better, though this calculus continues to evolve as models improve. At Anthropic, we’ve seen teams invest months building elaborate multi-agent architectures only to discover that improved prompting on a single agent achieved equivalent results.如今，多智能体系统常被应用于单智能体表现会更优的场景，不过随着模型的不断优化，这一情况也在持续变化。在 Anthropic 公司，我们曾看到团队花费数月时间构建复杂的多智能体架构，最终却发现对单智能体进行优化提示工程就能达到同等效果。

After building multi-agent systems and working with teams deploying them in production, we've identified three situations where multiple agents consistently outperform a single agent: when context pollution degrades performance, when tasks can run in parallel, and when specialization improves tool selection or task focus. Outside these situations, the coordination costs typically exceed the benefits.在构建多智能体系统并与团队合作将其部署到生产环境后，我们发现了三种多智能体始终优于单智能体的情况：上下文污染导致性能下降时、任务可并行运行时，以及专业化能提升工具选择或任务聚焦度时。在这些情况之外，协调成本通常会超过其带来的收益。  
  
In this article, we share how to recognize single-agent limits, identify the three scenarios where multi-agent systems excel, and avoid common implementation mistakes. 在本文中，我们将分享如何识别单智能体的局限性，明确多智能体系统发挥优势的三种场景，并规避常见的实施错误。

## The case for starting with a single agent从单个智能体开始的理由

A well-designed single agent with appropriate tools can accomplish far more than many developers expect.一个设计精良、配备合适工具的单一智能体所能完成的任务，远超许多开发者的预期。

Multi-agent systems introduce overhead. Every additional agent represents another potential point of failure, another set of prompts to maintain, and another source of unexpected behavior. 多智能体系统会带来额外开销。每增加一个智能体，就意味着多一个潜在的故障点、多一套需要维护的提示词，也多一个意外行为的诱因。

We've observed teams build elaborate multi-agent systems with separate agents for planning, execution, review, and iteration, only to discover that they suffered from lost context at each handoff and spent more tokens coordinating than executing. In our testing, multi-agent implementations typically use 3-10x more tokens than single-agent approaches for equivalent tasks. This overhead stems from duplicating context across agents, coordination messages between agents, and summarizing results for handoffs.我们观察到，一些团队搭建了复杂的多智能体系统，为规划、执行、审核和迭代分别配备了智能体，结果却发现每次交接时都会出现上下文丢失的问题，且用于协调的令牌数量远多于执行任务本身的令牌数量。在我们的测试中，完成相同任务时，多智能体方案的令牌使用量通常是单智能体方案的3到10倍。这种额外开销源于智能体间上下文的重复传递、智能体之间的协调消息，以及为交接操作汇总结果所消耗的令牌。

## A decision framework for multi-agent systems多智能体系统的决策框架

Multi-agent architectures provide value when they address specific constraints that a single agent cannot overcome. This means multi-agent architectures should be reserved for cases where they provide clear benefits that justify the additional cost. 多智能体架构在解决单个智能体无法克服的特定约束时才能体现其价值。这意味着，只有当多智能体架构能带来明确的、足以抵消额外成本的优势时，才应采用这种架构。

The patterns below represent cases where we consistently observe positive returns on this investment.以下模式代表我们在这项投资上持续获得正收益的情况。

### Context protection 上下文保护

Large language models have finite context windows, and response quality can degrade as context grows. When an agent's context accumulates information from one subtask that is irrelevant to subsequent subtasks, context pollution occurs. Subagents provide isolation, with each operating in its own clean context focused on its specific task.大语言模型的上下文窗口有限，且随着上下文规模扩大，回复质量可能会下降。当智能体的上下文积累了来自某个子任务的、与后续子任务无关的信息时，就会发生上下文污染。子智能体提供了隔离机制，每个子智能体都在独立的干净上下文内运行，专注于自身的特定任务。

Consider a customer support agent that needs to retrieve order history while diagnosing technical issues. If every order lookup adds thousands of tokens to the context, the agent's ability to reason about the technical problem degrades.设想这样一个客户支持智能体：它需要在诊断技术问题时查询订单历史。如果每一次订单查询都会向上下文添加数千个标记，那么该智能体针对技术问题进行推理的能力就会下降。

**The single-agent approach: 单智能体方法：**

```javascript
# Single agent accumulates everything in context
conversation_history = [
    {"role": "user", "content": "My order #12345 isn't working"},
    {"role": "assistant", "content": "Let me check your order..."},
    # Tool result adds 2000+ tokens of order history
    {"role": "user", "content": "... (order details, past purchases, shipping info) ..."},
    {"role": "assistant", "content": "Now let me diagnose the technical issue..."},
    # Context is now polluted with order details the agent doesn't need
]
```

The agent must reason about the technical issue while maintaining 2000+ tokens of irrelevant order history in context, diluting attention and reducing response quality.智能体必须在推理技术问题的同时，在上下文中保留2000多个标记的无关订单历史，这会分散注意力并降低回复质量。

**The multi-agent approach: 多智能体方法：**

```javascript
from anthropic import Anthropic

client = Anthropic()

class OrderLookupAgent:
    def lookup_order(self, order_id: str) -> dict:
        # Separate agent with its own context
        messages = [
            {"role": "user", "content": f"Get essential details for order {order_id}"}
        ]
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            messages=messages,
            tools=[get_order_details_tool]
        )
        # Returns only essential information
        return extract_summary(response)

class SupportAgent:
    def handle_issue(self, user_message: str):
        if needs_order_info(user_message):
            order_id = extract_order_id(user_message)
            # Get only what's needed, not full history
            order_summary = OrderLookupAgent().lookup_order(order_id)
            # Inject compact summary, not full context
            context = f"Order {order_id}: {order_summary['status']}, purchased {order_summary['date']}"
        
        # Main agent context stays clean
        messages = [
            {"role": "user", "content": f"{context}\n\nUser issue: {user_message}"}
        ]
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2048,
            messages=messages
        )
        return response
```

The order lookup agent processes the full order history and extracts a summary. The main agent receives only the 50-100 tokens it actually needs, keeping context focused.订单查询代理处理完整的订单历史并提取摘要。主代理仅接收其实际需要的50-100个标记，确保上下文聚焦。

Context isolation is most effective when subtasks generate high context volume (more than 1000 tokens) but most of that information is irrelevant to the main task, when the subtask is well-defined with clear criteria for what information to extract, and for lookup or retrieval operations that require filtering before use.当子任务产生大量上下文（超过1000个标记）但其中大部分信息与主任务无关时，当子任务定义明确且有明确的信息提取标准时，以及对于需要在使用前进行过滤的查找或检索操作，上下文隔离的效果最为显著。

### Parallelization 并行化

Running multiple agents in parallel allows you to explore a larger search space than a single agent can cover. This pattern has proven particularly valuable for search and research tasks.并行运行多个智能体，能探索的搜索空间比单个智能体所能覆盖的范围更大。这种模式已被证明在搜索和研究类任务中具有特别重要的价值。

Our [Research feature](https://www.anthropic.com/engineering/multi-agent-research-system) uses this approach. A lead agent analyzes a query and spawns multiple subagents to investigate different facets in parallel. Each subagent searches independently, then returns distilled findings. Multi-agent search has shown substantial accuracy improvements over single-agent approaches by allowing exploration across larger information spaces.我们的 [研究功能](https://www.anthropic.com/engineering/multi-agent-research-system) 采用了这种方法。一个主智能体分析查询请求，并生成多个子智能体，以并行方式研究不同方面。每个子智能体独立进行搜索，然后返回提炼后的结论。多智能体搜索通过支持在更大的信息空间中进行探索，相比单智能体方法，已展现出显著的准确率提升。

The core implementation decomposes a question into independent facets, runs subagents concurrently, then synthesizes the results.核心实现将一个问题分解为独立的方面，并行运行子智能体，然后整合结果。

```javascript
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

async def research_topic(query: str) -> dict:
    # Lead agent breaks query into research facets
    facets = await lead_agent.decompose_query(query)
    
    # Spawn subagents to research each facet in parallel
    tasks = [
        research_subagent(facet) 
        for facet in facets
    ]
    results = await asyncio.gather(*tasks)
    
    # Lead agent synthesizes findings
    return await lead_agent.synthesize(results)

async def research_subagent(facet: str) -> dict:
    """Each subagent has its own context window"""
    messages = [
        {"role": "user", "content": f"Research: {facet}"}
    ]
    response = await client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        messages=messages,
        tools=[web_search, read_document]
    )
    return extract_findings(response)
```

This improved coverage comes at a cost. Multi-agent systems typically consume 3 to 10 times more tokens than single-agent approaches for equivalent tasks. This happens because each agent needs its own context, agents must exchange messages to coordinate, and results must be summarized when passed between agents. While parallelism helps reduce total execution time compared to running all that work sequentially, multi-agent systems often take longer overall than single-agent systems because of the sheer increase in total computation.这种覆盖范围的提升是有代价的。在完成相同任务时，多智能体系统消耗的 token 数量通常是单智能体方法的3到10倍。出现这种情况的原因是，每个智能体都需要自身的上下文，智能体之间必须交换消息来进行协调，且结果在智能体间传递时需要进行汇总。尽管与按顺序执行所有工作相比，并行处理有助于缩短总执行时间，但由于总计算量的大幅增加，多智能体系统的整体运行时间往往比单智能体系统更长。

The primary benefit of parallelization is thoroughness, not speed. When you need to search across a large information space or investigate many angles of a complex question, parallel agents can cover more ground than a single agent working within its context limits. The tradeoff is higher token usage and often longer total execution time in exchange for more comprehensive results.并行化的主要优势是全面性，而非速度。当你需要在庞大的信息空间中进行搜索，或是探究一个复杂问题的多个层面时，并行智能体能够比受上下文限制的单个智能体覆盖更广的范围。其代价是会消耗更多的 token，且整体执行时间通常更长，以此换取更全面的结果。

### Specialization 专业化

Different tasks sometimes benefit from different tool sets, system prompts, or domains of expertise. Rather than providing a single agent with access to dozens of tools, specialized agents with focused toolsets matched to their responsibilities can improve reliability.不同的任务有时需要不同的工具集、系统提示或专业领域的支持。与其让单个智能体拥有数十种工具的访问权限，不如让具备针对性工具集的专业智能体匹配其职责，这样能提升可靠性。

#### Tool set specialization 工具集专业化

When an agent has access to too many tools, performance suffers. Three signals indicate tool specialization would help:当一个智能体可使用的工具过多时，其性能会下降。有三个信号表明工具专业化会有所帮助：

1. **Quantity.** An agent with too many tools (often 20+) struggles to select the appropriate one.**数量。** 拥有过多工具（通常超过20种）的智能体难以选择合适的工具。
2. **Domain confusion.** When tools span multiple unrelated domains (database operations, API calls, file system operations), the agent confuses which domain applies to a given task.**领域混淆。** 当工具涉及多个不相关的领域（数据库操作、API 调用、文件系统操作）时，智能体会混淆哪个领域适用于给定任务。
3. **Degraded performance.** Adding new tools degrades performance on existing tasks, suggesting the agent has reached its capacity for tool management.**性能下降。** 添加新工具会降低现有任务的性能，这表明智能体已达到其工具管理的容量上限。

#### System prompt specialization 系统提示专业化

Different tasks sometimes require different personas, constraints, or instructions that conflict when combined. A customer support agent needs to be empathetic and patient; a code review agent needs to be precise and critical. A compliance-checking agent needs rigid rule-following; a brainstorming agent needs creative flexibility. When a single agent must switch between conflicting behavioral modes, separating into specialized agents with tailored system prompts produces more consistent results.不同的任务有时需要不同的角色设定、约束条件或指令，这些内容在组合时会产生冲突。客户支持代理需要富有同理心且有耐心；代码审查代理则需要精准且严谨。合规检查代理需要严格遵守规则；头脑风暴代理则需要具备创造性的灵活性。当单个代理必须在相互冲突的行为模式之间切换时，将其拆分为拥有定制系统提示的专业代理，能得出更一致的结果。

#### Domain expertise specialization 领域专业知识专业化

Some tasks benefit from deep domain context that would overwhelm a generalist agent. A legal analysis agent might need extensive context about case law and regulatory frameworks. A medical research agent might need specialized knowledge about clinical trial methodology. Rather than loading all domain context into a single agent, specialized agents can carry focused expertise relevant to their specific responsibilities.有些任务得益于深度领域上下文，而这会让通用智能体难以应对。法律分析智能体可能需要大量关于判例法和监管框架的上下文信息。医学研究智能体则可能需要有关临床试验方法的专业知识。与其将所有领域上下文加载到单个智能体中，不如让专业智能体携带与其具体职责相关的精准专业能力。

**Example: Multi-platform integration.** Consider an integration system where agents need to work across CRM, marketing automation, and messaging platforms. Each platform has 10-15 relevant API endpoints. A single agent with 40+ tools often struggles to select correctly, confusing similar operations across platforms. Splitting into specialized agents with focused toolsets and tailored prompts resolves selection errors.**示例：多平台集成。** 假设有一个集成系统，其中智能体需要在客户关系管理（CRM）、营销自动化和消息传递平台之间协同工作。每个平台都有10-15个相关的API端点。一个拥有40多种工具的单一智能体往往难以正确选择工具，会混淆不同平台间相似的操作。将智能体拆分为拥有专属工具集和定制提示词的专用智能体，就能解决选择错误的问题。

```javascript
from anthropic import Anthropic

client = Anthropic()

# Specialized agents with focused toolsets and tailored prompts
class CRMAgent:
    """Handles customer relationship management operations"""
    system_prompt = """You are a CRM specialist. You manage contacts, 
    opportunities, and account records. Always verify record ownership 
    before updates and maintain data integrity across related records."""
    tools = [
        crm_get_contacts,
        crm_create_opportunity,
        # 8-10 CRM-specific tools
    ]

class MarketingAgent:
    """Handles marketing automation operations"""
    system_prompt = """You are a marketing automation specialist. You 
    manage campaigns, lead scoring, and email sequences. Prioritize 
    data hygiene and respect contact preferences."""
    tools = [
        marketing_get_campaigns,
        marketing_create_lead,
        # 8-10 marketing-specific tools
    ]

class OrchestratorAgent:
    """Routes requests to specialized agents"""
    def execute(self, user_request: str):
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system="""You coordinate platform integrations. Route requests to the appropriate specialist:
- CRM: Contact records, opportunities, accounts, sales pipeline
- Marketing: Campaigns, lead nurturing, email sequences, scoring
- Messaging: Notifications, alerts, team communication""",
            messages=[
                {"role": "user", "content": user_request}
            ],
            tools=[delegate_to_crm, delegate_to_marketing, delegate_to_messaging]
        )
        return response
```

This pattern mirrors effective professional collaboration, where specialists with tools matched to their roles collaborate more effectively than generalists attempting to maintain expertise across all domains. However, specialization introduces routing complexity. The orchestrator must correctly classify requests and delegate to the right agent, and misrouting leads to poor results. Maintaining multiple specialized agents also increases prompt maintenance overhead. Specialization works best when domains are clearly separable and routing decisions are unambiguous.这种模式与高效的专业协作如出一辙：配备适配自身角色工具的专业人士，比试图在所有领域都保持专业能力的通才协作效果更好。不过，专业化会带来路由复杂性。协调者必须对请求进行正确分类并委派给合适的智能体，而错误路由会导致结果不佳。维护多个专业智能体还会增加提示维护的开销。当领域界限清晰可分且路由决策明确时，专业化的效果最佳。

## Outgrowing single-agent architectures 不再适用于单智能体架构

Beyond the general framework, certain concrete signals suggest that single-agent patterns have been outgrown:除了整体框架之外，一些具体信号表明单智能体模式已不再适用：

**Approaching context limits.**If an agent routinely uses large amounts of context and performance is degrading, context pressure may be the bottleneck. Note that recent advances in context management ([such as compaction](https://platform.claude.com/cookbook/tool-use-automatic-context-compaction)) are reducing this limitation, allowing single agents to maintain effective memory across much longer horizons.**上下文容量即将达到上限。** 如果智能体频繁使用大量上下文且性能出现下降，上下文压力可能是瓶颈所在。需注意，上下文管理方面的最新进展（ [如压缩技术](https://platform.claude.com/cookbook/tool-use-automatic-context-compaction) ）正在缓解这一限制，使单个智能体能够在更长的时间范围内维持有效的记忆能力。

**Managing many tools.** When an agent has 15-20+ tools, the model spends significant context and attention understanding its options. Before adopting a multi-agent architecture, consider using the [Tool Search Tool](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/tool-search-tool), which lets Claude dynamically discover tools on-demand rather than loading all definitions upfront. This can [reduce token usage by up to 85%](https://www.anthropic.com/engineering/advanced-tool-use) while improving tool selection accuracy.**管理众多工具。** 当一个智能体拥有15至20个及以上工具时，模型会消耗大量上下文和注意力来了解自身的可选工具。在采用多智能体架构之前，可以考虑使用 [工具搜索工具](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/tool-search-tool) ，该工具能让Claude按需动态发现工具，而非预先加载所有工具定义。这一方式可 [将令牌使用量降低高达85%](https://www.anthropic.com/engineering/advanced-tool-use) ，同时提升工具选择的准确性。

**Parallelizable subtasks.** When tasks naturally decompose into independent pieces (research across multiple sources, tests for multiple components), parallel subagents can provide substantial speedups.**可并行的子任务。** 当任务自然分解为独立部分（跨多个来源的研究、多个组件的测试）时，并行子智能体可以显著提升执行速度。

These thresholds will shift as models improve. Current limits represent practical guidelines, not fundamental constraints.随着模型的不断优化，这些阈值也会随之变化。当前的限制只是实用的指导原则，而非根本性约束。

## Context-centric decomposition 上下文感知分解

When adopting a multi-agent architecture, the most important design decision is how to divide work between agents. We've observed that teams frequently make this choice incorrectly, leading to coordination overhead that negates the benefits of multi-agent design.在采用多智能体架构时，最重要的设计决策是如何在智能体之间分配工作。我们发现，团队常常做出错误的选择，由此产生的协调开销会抵消多智能体设计带来的优势。

The key insight is to adopt a **context-centric view** rather than a problem-centric view when decomposing work.核心见解是，在拆解工作时应采用 **以情境为中心的视角** ，而非以问题为中心的视角。

**Problem-centric decomposition (often counterproductive).** Dividing by type of work (one agent writes features, another writes tests, a third reviews code) creates constant coordination overhead. Each handoff loses context. The test-writing agent lacks knowledge of why certain implementation decisions were made and the code reviewer lacks the context of exploration and iteration.**以问题为中心的拆分（通常适得其反）。** 按工作类型划分（一个智能体编写功能，一个编写测试，另一个审核代码）会产生持续的协调开销。每一次交接都会丢失上下文。编写测试的智能体不了解做出某些实现决策的原因，代码审核者也缺乏探索和迭代的上下文。

**Context-centric decomposition (usually effective).** Dividing by context boundaries means an agent handling a feature should also handle its tests, because it already possesses the necessary context. Work should only be split when context can be truly isolated.**基于上下文的拆分（通常效果良好）。** 按上下文边界进行拆分意味着处理某一功能的智能体也应处理其测试，因为它已具备必要的上下文。仅当上下文能够被真正隔离时，才应拆分工作。

This principle emerges from observing failure modes in multi-agent systems. When agents are split by problem type, they engage in a "telephone game," passing information back and forth with each handoff degrading fidelity. In one experiment with agents specialized by software development role (planner, implementer, tester, reviewer), the subagents spent more tokens on coordination than on actual work.这一原则源于对多智能体系统中故障模式的观察。当智能体按问题类型拆分时，它们会陷入一场“传话游戏”，每一次信息传递都会降低信息的保真度。在一项针对按软件开发角色（规划者、实施者、测试者、评审者）分工的智能体实验中，这些子智能体在协调上花费的代币比在实际工作上还多。

**Effective decomposition boundaries include:有效的分解边界包括：**

- **Independent research paths.** Investigating "market trends in Asia" versus "market trends in Europe" can proceed in parallel with no shared context.**独立的研究路径。** 调研“亚洲市场趋势”与“欧洲市场趋势”可并行开展，二者无共享背景。
- **Separate components with clean interfaces.** With a well-defined API contract, frontend and backend work can proceed in parallel.**用清晰的接口分离组件。** 凭借定义明确的API契约，前端和后端的开发工作可以并行推进。
- **Blackbox verification.** A verifier that only needs to run tests and report results does not require implementation context.**黑盒验证。** 仅需运行测试并报告结果的验证器不需要实现上下文。

**Problematic decomposition boundaries include:存在问题的拆分边界包括：**

- **Sequential phases of the same work.** Planning, implementation, and testing of the same feature share too much context.**同一工作的连续阶段。** 同一功能的规划、实施与测试共享了过多的上下文信息。
- **Tightly coupled components.** Components requiring constant back-and-forth belong in the same agent.**紧耦合组件。** 需要频繁交互的组件应归属于同一个智能体。
- **Work requiring shared state.** Agents that would need to frequently synchronize understanding should remain together.**需要共享状态的工作。** 需要频繁同步认知的智能体应保持在一起。

## The verification subagent pattern 验证子智能体模式

One multi-agent pattern that consistently works well across domains is the **verification subagent**. This is a dedicated agent whose sole responsibility is testing or validating the main agent's work.一种在各个领域都持续表现良好的多智能体模式是 **验证子智能体** 。这是一个专用智能体，其唯一职责是测试或验证主智能体的工作成果。

It's worth noting that more capable orchestrator models (like Claude Opus 4.5) are increasingly able to evaluate subagent work directly without a separate verification step. However, verification subagents remain valuable when using less capable orchestrators, when verification requires specialized tools, or when you want to enforce explicit verification checkpoints in your workflow.值得注意的是，能力更强的协调器模型（如 Claude Opus 4.5）已越来越能直接评估子智能体的工作，无需单独的验证步骤。不过，在使用能力较弱的协调器、验证需要专用工具，或希望在工作流中设置明确的验证检查点时，验证子智能体仍具有重要价值。

Verification subagents succeed because they sidestep the telephone game problem. Verification requires minimal context transfer by nature, so a verifier can blackbox-test a system without needing the full history of how it was built.验证智能代理之所以能成功，是因为它们避开了“传话游戏”的问题。验证本质上只需要最少的上下文传递，因此验证者可以对系统进行黑盒测试，而无需了解系统构建的完整历史。

### Implementation 实施

The main agent completes a unit of work. Before proceeding, it spawns a verification subagent with the artifact to verify, clear success criteria, and tools to perform verification.主智能体完成一个工作单元。在继续执行之前，它会生成一个验证子智能体，该子智能体携带待验证的工件、明确的成功标准以及执行验证所需的工具。

The verifier does not need to understand why the artifact was built as it was. It only needs to determine whether the artifact meets the specified criteria.验证者无需理解该工件为何被构建为当前样式，只需判断其是否符合指定标准。

```javascript
from anthropic import Anthropic

client = Anthropic()

class CodingAgent:
    def implement_feature(self, requirements: str) -> dict:
        """Main agent implements the feature"""
        messages = [
            {"role": "user", "content": f"Implement: {requirements}"}
        ]
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            messages=messages,
            tools=[read_file, write_file, list_directory]
        )
        return {
            "code": response.content,
            "files_changed": extract_files(response)
        }

class VerificationAgent:
    def verify_implementation(self, requirements: str, files_changed: list) -> dict:
        """Separate agent verifies the work"""
        messages = [
            {"role": "user", "content": f"""
Requirements: {requirements}
Files changed: {files_changed}

Run the test suite and verify:
1. All existing tests pass
2. New functionality works as specified
3. No obvious errors or security issues

You MUST run the complete test suite before marking as passed.
Do not mark as passing after only running a few tests.
Run: pytest --verbose
Only mark as PASSED if ALL tests pass with no failures.
"""}
        ]
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            messages=messages,
            tools=[run_tests, execute_code, read_file]
        )
        return {
            "passed": extract_pass_fail(response),
            "issues": extract_issues(response)
        }

def implement_with_verification(requirements: str, max_attempts: int = 3):
    for attempt in range(max_attempts):
        result = CodingAgent().implement_feature(requirements)
        verification = VerificationAgent().verify_implementation(
            requirements,
            result['files_changed']
        )
        
        if verification['passed']:
            return result
        
        requirements += f"\n\nPrevious attempt failed: {verification['issues']}"
    
    raise Exception(f"Failed verification after {max_attempts} attempts")
```

### Applications 应用场景

Verification subagents are effective for:验证子智能体适用于以下场景：

- **Quality assurance.** Running test suites, linting code, validating outputs against schemas.**质量保证。** 运行测试套件、对代码进行语法检查、根据模式验证输出。
- **Compliance checking.** Verifying documents meet policy requirements, checking outputs against rules.**合规性检查。** 验证文件是否符合政策要求，对照规则检查输出结果。
- **Output validation.** Confirming generated content meets specifications before delivery.**输出验证。** 在交付前确认生成的内容符合规范。
- **Factual verification.** Having a separate agent verify claims or citations in generated content.**事实核查。** 由独立的智能体核查生成内容中的主张或引用。

### The early victory problem 早期胜利问题

The most significant failure mode for verification subagents is marking outputs as passing without thorough testing. The verifier runs one or two tests, observes them pass, and declares success.验证子智能体最主要的故障模式是在未进行全面测试的情况下就将输出标记为通过。验证器只运行一两次测试，观察到测试通过后就宣布成功。

Mitigation strategies include: 缓解策略包括：

- **Concrete criteria.** Specify "Run the full test suite and report all failures" rather than "make sure it works." **具体标准。** 明确说明“运行完整的测试套件并报告所有失败情况”，而非“确保其正常工作”。
- **Comprehensive checks.** Require the verifier to test multiple scenarios and edge cases.**全面检查。** 要求验证人员测试多种场景和边界情况。
- **Negative tests.** Direct the verifier to attempt inputs that should fail and confirm they do.负面测试。</b>指导验证者尝试那些预期会失败的输入，并确认它们确实失败了。
- **Explicit instructions.** The instruction "You MUST run the complete test suite before marking as passed" is essential. Without explicit requirements for comprehensive validation, verification agents take shortcuts.**明确的指令。** 指令“你必须在标记为通过之前运行完整的测试套件”至关重要。如果没有针对全面验证的明确要求，验证智能体就会走捷径。

## Moving forward 后续步骤

Multi-agent systems are powerful, but not universally appropriate. Before adding the complexity of multiple coordinated agents, confirm that:多智能体系统功能强大，但并非适用于所有场景。在引入多个协同智能体带来的复杂性之前，请确认以下几点：

1. **Genuine constraints exist** that multi-agent solves, such as context limits, parallelization opportunities, or need for specialization.**确实存在一些真实的约束** ，多智能体系统需要解决这些约束，比如上下文限制、并行化机会，或是对专业化的需求。
2. **Decomposition follows context, not problem type.** Group work by what context it requires, not by what kind of work it is.**分解遵循上下文，而非问题类型。** 按所需上下文对工作进行分组，而非按工作类型划分。
3. **Clear verification points exist** where subagents can validate work without requiring full context.**存在明确的验证点** ，子智能体可在这些点验证工作，且无需完整上下文。

Our advice? Start with the simplest approach that works, and add complexity only when evidence supports it.我们的建议是什么？从最有效的简单方法入手，只有有证据支持时再增加复杂程度。

*This is the first in a series of posts on multi-agent systems. For more on single-agent patterns, see* [*Building effective agents*](https://www.anthropic.com/engineering/building-effective-agents)*. For context management strategies, see* [*Effective context engineering for AI agents*](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)*. For a deep dive into how we built our multi-agent research system, see* [*How we built our multi-agent research system*](https://www.anthropic.com/engineering/multi-agent-research-system)*.**这是关于多智能体系统系列文章的第一篇。有关单智能体模式的更多内容，请参阅* [*构建高效能智能体*](https://www.anthropic.com/engineering/building-effective-agents) *。有关上下文管理策略的内容，请参阅* [*AI 智能体的高效上下文工程*](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) *。若想深入了解我们如何构建多智能体研究系统，请查看* [*我们如何构建多智能体研究系统*](https://www.anthropic.com/engineering/multi-agent-research-system) *。*

## Acknowledgements 致谢

Written by Cara Phillips, with contributions from Paul Chen, Andy Schumeister, Brad Abrams, and Theo Chu.由卡拉·菲利普斯撰写，保罗·陈、安迪·舒迈斯特、布拉德·艾布拉姆斯和西奥·朱参与撰稿。