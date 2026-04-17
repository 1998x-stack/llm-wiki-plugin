# https://www.anthropic.com/engineering/managed-agents

> Source: 文章解读 Anthropic Agent
> Time: 2026/4/16 12:38:54

## Question

https://www.anthropic.com/engineering/managed-agents


详细分析解读这篇文章

## Answer

我先把原文读透，然后按“核心观点—技术架构—隐含前提—适用边界—对国内团队的启发”来拆。最后我会补一段我自己的判断，不只复述。


我已经拿到原文，也顺手对照了官方文档里的产品抽象，能看出这篇不是“技术博客式分享经验”，而是在替 Anthropic 的 Agent 平台定义一套长期接口哲学。下面我会把“文章表层说了什么”和“它真正想押注什么”分开讲。

浏览网页以获取和引用文章内容


Scaling Managed Agents: Decoupling the brain from the hands \ Anthropic


考虑是否需要查找文档


我可能需要检查一下文档，或者直接进行详细分析。或许找一个官方文档链接会有帮助，但不一定必须。考虑到用户要求的是文章分析，这样做可能有助于更好理解“托管代理”产品的结构。我要做的就是深入分析。


搜索关于管理代理的官方文档


海通国际：Anthropic正式公测Claude Managed Agents 大模型厂商加速布局Harness层
开发Agent苦日子熬到头了！Anthropic重磅发布Claude Managed Agents：速度 ...
Anthropic Launches Managed Agents to Run Enterprise AI Workloads
Mythos造假/Opus降智/Agent新平台，Anthropic所有更新一次性看懂
Claude Cowork is now available for enterprise use, adds analytics, access controls and more
开始使用 Claude Managed Agents - Claude API Docs
Scaling Managed Agents: Decoupling the brain from the hands
Claude Managed Agents 深度解读：Agent 开发的范式转移来了
Claude Managed Agents – Anthropic 推出的全托管 Agent 平台
Anthropic says Claude subscriptions will no longer support OpenClaw because it puts an 'outsized strain' on systems
Anthropic's New Product Aims to Handle the Hard Part of Building AI Agents


已思考 24s

这篇文章表面上是在讲 Anthropic 怎么做 Managed Agents，但更深一层，它其实是在回答一个更大的问题：


当模型能力快速变强、Agent harness 很快过时的时候，平台层到底应该固定什么，放开什么？


Anthropic 的答案是：不要把“当前这代模型需要什么样的 harness”固化进系统，而要把 Agent 系统拆成几个尽可能稳定的接口——session、harness、sandbox——让底层实现持续替换。 这正是文章标题里 “Decoupling the brain from the hands” 的含义。Anthropic+1



一句话总结这篇文章


这不是一篇“怎么写 agent prompt/harness”的文章，而是一篇Agent 基础设施设计宣言：

随着模型进步，harness 会变；所以真正该产品化的不是某个 harness，而是能容纳未来不同 harness 的接口层。 Anthropic


文章主线：它在解决什么问题


Anthropic 先抛了一个很关键的观察：harness 本质上编码了很多“模型现在还做不到什么”的假设，而这些假设会随着模型升级迅速过时。 他们举的例子是，之前为 Claude Sonnet 4.5 加的 context reset，是为了解决接近上下文上限时过早收尾的“context anxiety”；但换到 Claude Opus 4.5 后，这个问题消失了，原先的补丁反而成了负担。Anthropic


这点很重要，因为它把 Agent 工程里的一个常见误区说透了：


很多人把当前最好用的 agent loop、memory 策略、context compression、tool routing，当成“长期架构”

Anthropic 认为这些都更像阶段性补丁

所以平台层不该围绕“今天最优的 harness”设计，而要围绕“未来未知 harness 也能接入”设计。Anthropic


换句话说，这篇文章真正的目标不是证明某个 loop 更好，而是证明：应该把 agent 平台设计成 meta-harness。 Anthropic 在结论部分甚至直接用了这个词。Anthropic



核心抽象：把 Agent 虚拟化成 3 个部件


Anthropic 把 Agent 系统抽象成三个可分离部分：


Session：事件日志，记录一切发生过的事

Harness：调用 Claude、接工具、组织上下文的控制循环

Sandbox：执行代码、编辑文件、访问环境的“手” Anthropic


这跟操作系统历史上的抽象思路很像。文章专门引用了“programs as yet unthought of”这个经典命题：操作系统之所以能活几十年，不是因为它绑定了某代硬件，而是因为它把底层抽象成像 process、file、read() 这种长期稳定接口。Anthropic 试图对 Agent 复制这套方法。Anthropic


这里最值得注意的一点是：


他们不是在虚拟化“模型”，而是在虚拟化“agent 的运行时”。


这意味着 Anthropic 的产品边界已经明显从 model API 上移到 agent runtime / agent infra 这一层。官方文档里也能看到这种产品化痕迹：Managed Agents 的核心概念已经是 Agent、Environment、Session、Events，而不是单纯 messages/completions。Claude平台



为什么要“brain 和 hands 解耦”


1) 从“宠物容器”变成“牛群容器”


文章说，他们最开始把 session、harness、sandbox 都塞在一个 container 里。好处是简单，文件编辑也很直接；但坏处是你养出了一只“pet”——一个不能轻易挂掉、挂了就得人工救火的实例。容器一挂，会话丢失；容器卡死，很难定位是 harness bug、WebSocket 问题还是容器自己坏了。Anthropic


所以他们把 harness 移出了容器。这样 sandbox 只是一个被调用的执行环境，失败时只会表现成 tool-call error；Claude 如果判断可重试，可以重新 provision 一个新容器。也就是说，状态不再绑定在执行器上，而绑定在 session log 上。 Anthropic


这背后的架构思想很经典，但在 agent 世界里特别关键：


有状态的东西尽量外置

执行器尽量无状态、可重建

恢复依赖 event log，而不是依赖活着的进程


这是把 agent 系统从“能跑”升级到“能运维”的第一步。Anthropic



2) 真正把“恢复能力”做成架构特性


文章里一个容易被忽略、但很本质的点是：harness 自己也被做成 cattle 了。 因为 session log 放在外部，harness 崩了也不需要保活；新 harness 通过 wake(sessionId) 和 getSession(id) 就能从事件流里恢复，再继续 agent loop。Anthropic


这意味着 Anthropic 不是在做“长连接 agent”，而是在做一种更接近 event-sourced agent orchestration 的系统。虽然文章没用这个词，但从设计上很像：


durable event log 是事实来源

harness 是可替换的解释器

sandbox 是可替换的执行器


这比“一个进程里 while loop 跑到天荒地老”的常见 agent 实现高了一个层级。因为后者本质上仍然是 demo 架构，不是大规模托管架构。



3) 安全边界终于不是“相信模型别乱拿 token”


安全那一段其实含金量很高。Anthropic 明确指出：在旧架构里，Claude 生成的非可信代码和凭证在同一个容器里运行。这样 prompt injection 一旦诱导模型读环境变量，攻击者拿到 token 后就能开新 session、继续横向扩张。Anthropic


他们给的解决方案不是“缩 scope”“多加规则”，而是更结构性的：


Git token 在 sandbox 初始化时直接绑定进 repo remote，agent 本身不接触 token

MCP / 自定义工具的 OAuth token 存在 vault

Claude 调 MCP 通过 proxy，proxy 再拿 session 关联的凭证去外部服务调用

harness 也不直接知道这些凭证 Anthropic


这体现了 Anthropic 一个很成熟的判断：

不要把安全建立在“模型暂时没那么聪明”上。

文章甚至明确说，窄权限 token 只是缓解，而那仍然编码了“Claude 还做不到什么”的假设；随着模型变强，这种假设也会变旧。Anthropic


这是全文里我最认同的一句潜台词：
面向模型能力持续上升的系统，安全设计必须尽量从“行为约束”转向“结构隔离”。



文章最有价值的一段：Session 不是上下文窗口


这是全文最深的一层，不只是 infra 问题，而是 LLM runtime 设计问题。


Anthropic 说，长时任务经常超出上下文窗口。常见做法比如 compaction、summary、memory tool、trimming，都会涉及不可逆的信息保留/丢弃决策；而真正的问题在于，你无法提前知道未来哪段 token 会有用。Anthropic


所以他们把 session 设计成一个外置的、可查询的上下文对象：


Claude 当前窗口里只放一部分内容

完整历史在 session log 里

harness 可以用 getEvents() 按位置取片段、回看前文、从某个点继续读

再把取回来的事件经过变换后塞进 Claude 当前上下文 Anthropic


这意味着它不再把“上下文”理解为 prompt 字符串，而理解为：

一个可持久化、可切片、可重放、可变换的外部状态对象。 Anthropic

这点很先进，因为它把 memory/context engineering 从“prompt 技巧”提升成了“runtime 访问模式”。


也是为什么 Anthropic 特别强调：
session 负责 durable/recoverable storage，harness 负责 arbitrary context management。 两者故意分开，因为他们不想预设未来模型需要什么 context engineering。Anthropic


我的理解是，这里其实在说：


Session = source of truth

Context window = working set

Harness = cache manager + state selector


这个分层非常像数据库/操作系统的味道。它不是在做更复杂的 prompt，而是在做 LLM operating model。



“Many brains, many hands” 到底意味着什么


这一节表面上是性能和扩展性，实际上讲的是 Agent 从单体执行器变成分布式工作流节点。


Anthropic 说，brain 从 container 里拆出来之后：


不需要每个 session 先等容器启动

只有真需要 sandbox 时才 provision

因此 p50 TTFT 降了约 60%，p95 降了 90% 以上 Anthropic


这说明旧架构最大的问题之一，不是推理本身，而是把昂贵、慢启动的执行环境前置绑定给每个会话。一旦拆开，推理可以先跑，动作环境按需挂接。


更重要的是“many hands”那部分。Anthropic 说现在每个 hand 都只是 execute(name, input) -> string 这样的工具接口，harness 不关心它背后是容器、手机还是 Pokémon emulator；不同 brain 之间还可以传 hand。Anthropic


这句话的信息量很大。它其实在押注三件事：


工具/执行环境会高度异构

一个任务会跨多个执行环境协同

未来甚至会是多 agent / 多 brain 协作，而不是单 agent 单 shell Anthropic


这已经不是“让模型会用 bash”了，而是在往 通用 agent fabric 的方向走。



这篇文章真正的战略信号


我觉得这篇文章最值得重视的，不是几个接口名，而是 Anthropic 释放出的战略信号：


1) 大模型厂商正在往 harness / runtime 层上移


Managed Agents 已经不是单纯卖模型，而是托管 agent loop、sandbox、event stream、credential isolation、long-horizon orchestration。官方 quickstart 里也能看到，它把 Agent、Environment、Session 都变成一等 API 资源。Claude平台+1


这意味着行业竞争正在从：


“谁的 model API 更强”


转向：


“谁能提供更完整、更可靠的 agent runtime”



2) “Big Model vs Big Harness” 的答案越来越像：两者一体化


这篇文章并没有否认 harness 的重要性，恰恰相反，它说 harness 非常重要；只是 harness 本身会变，所以平台应该产品化 harness 外面的接口层。Anthropic


这其实比“模型重要还是工程重要”那种二元争论更成熟：


模型变强，旧 harness 会死

但没有 harness/runtime，模型也落不了地

真正的护城河不是写死一个 harness，而是做出能容纳未来 harness 的系统层



3) Agent 产品化的重心，正在从“能力演示”转向“可运营性”


全文讨论最多的不是“Claude 多聪明”，而是：


crash 后怎么恢复

凭证怎么隔离

context 怎么外置

VPC 怎么接

TTFT 怎么降

多执行环境怎么接入 Anthropic


这说明 Anthropic 已经把 Agent 看成生产基础设施问题，而不是实验室玩法。



文章没讲、但你读的时候必须补上的部分


这篇文章很强，但也有明显“故意没展开”的地方。


1) 它解决的是运行时架构，不是任务正确率


文章解决了 durability、security、latency、extensibility，但没有真正展开：


agent 如何规划

任务分解如何评估

工具选择如何校验

错误恢复何时自动、何时人工介入

长链路成本如何控制


也就是说，它解决的是 agent 能长期稳定跑，不是 agent 一定能把事做对。



2) execute(name, input) -> string 很优雅，但现实里会碰到结构化结果与幂等性问题


文章把 hand 抽象成工具接口，这很干净；但真实生产里，工具调用往往需要：


结构化 schema

可重试语义

side effects 标记

幂等键

权限边界

可审计 trace


这些在文中没有展开。不是说 Anthropic 没做，而是这篇文章更偏架构哲学，不是完整设计文档。



3) Session log 外置后，新的难题会变成“怎么读历史”


把历史都放 session 很合理，但会带来另一个难点：


哪些事件要回放

取多少窗口最划算

如何避免读历史变成新的 latency/cost 黑洞

如何做事件压缩又不丢可恢复性


Anthropic 说 harness 可以灵活变换 fetched events，这给了未来优化空间；但也意味着context engineering 的复杂度只是从 prompt 内部移动到了 runtime 层。Anthropic



对产品/平台团队最有启发的几点


如果把这篇文章翻成更务实的工程建议，我觉得是这几条：


1) 不要把“当前模型的缺点补丁”误当成长期平台能力


今天有效的 summary、reset、memory、retry 策略，半年后可能都是 dead weight。Anthropic 用 Sonnet 4.5 vs Opus 4.5 的例子，就是在提醒你这一点。Anthropic


2) 长时 Agent 的核心不是更长 prompt，而是外置状态


要把“历史”从模型 context 里拆出来，变成可查询、可恢复、可重放的对象。Anthropic 的 session/event 思路，值得几乎所有做 agent 的团队重看。Anthropic


3) 安全不要赌模型暂时不够聪明


凭证、工具权限、执行环境，最好结构隔离，而不是只靠 prompt 约束和 scoped token。Anthropic


4) 真正可扩展的 Agent 系统，一开始就别把 brain 和 hands 绑死


否则你后面接 VPC、接 MCP、接更多执行环境、做多 agent 协作时，都会被早期单体设计反噬。Anthropic



我的总体判断


我对这篇文章的评价很高，原因不是它讲了多新奇的分布式思想，而是它把 Agent 系统里最容易被忽略的一点讲清楚了：

在 Agent 时代，真正会快速过时的是“具体做法”；真正该长期稳定的是“接口边界”。

Anthropic 这次不是在卖一个“更会干活的 agent demo”，而是在试图定义：
模型厂商应该提供怎样的 agent runtime primitive。 Anthropic+1


如果这个方向成立，未来平台竞争会越来越像：


模型能力

agent runtime

tool / MCP / connector 生态

安全与可审计

长时任务状态管理


一起打包竞争，而不是单比模型分数。


所以这篇文章最重要的价值，不在“brain/hands”这个比喻本身，而在它明确宣告了一件事：


Anthropic 正在从“提供一个强模型”走向“提供一整套托管 agent 操作系统”。 Anthropic+1


如果你愿意，我下一条可以继续帮你做一版：站在 OpenAI / Google / 国内大模型公司的视角，对这篇文章做横向对比解读。



Sources:


Scaling Managed Agents: Decoupling the brain from the hands \ Anthropic

开始使用 Claude Managed Agents - Claude API Docs
