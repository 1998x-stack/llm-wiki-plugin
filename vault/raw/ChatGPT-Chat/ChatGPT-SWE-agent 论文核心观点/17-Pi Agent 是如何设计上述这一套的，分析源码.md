# Pi Agent 是如何设计上述这一套的，分析源码

> Source: SWE-agent 论文核心观点
> Time: 2026/4/15 11:03:37

## Question

Pi Agent 是如何设计上述这一套的，分析源码

## Answer

调查 Pi Agent 设计及源代码


用户可能在问关于 Pi Agent 的设计问题。为了分析源代码，我需要通过搜索引擎查找公开的最新源代码，可能是 GitHub 上的相关资源。由于概念可能有些模糊，我觉得需要进一步查找以澄清细节。

可以把 Pi Agent 理解成：

不是内建一套固定的 Claude Code 式“hooks + LSP + local validate 状态机”，
而是把这套能力拆成 agent-core 的循环 + coding-agent 的扩展事件系统 + 会话持久化，然后让你用 extension 自己拼出来。

也就是说，Pi 的核心设计不是“内置一条唯一正确流程”，而是 把工作流做成可编程 runtime。这一点从仓库结构、pi-agent-core 的 hook、coding-agent 的 extension 事件、以及示例 extension 的写法都很明显。GitHub+2GitHub+2



Pi Agent 的底层设计：先有 loop，再有 policy



Pi monorepo 把能力拆成三层：


pi-ai：统一模型接口

pi-agent-core：agent runtime

pi-coding-agent：面向 coding 场景的 CLI / SDK。GitHub+1


其中真正关键的是 pi-agent-core。它已经提供了你做“状态机”所需的几个核心原语：


事件流：agent_start、turn_start、message_*、tool_execution_*、agent_end

工具执行模式：parallel 或 sequential

beforeToolCall：工具执行前的 preflight，可阻断

afterToolCall：工具执行后、结果发出前的后处理。GitHub


这意味着 Pi 的基本哲学是：

先把“LLM + tools + loop”做得最小，然后把 guardrail / plan mode / permissions / stateful workflow 往上层 extension 挪。

这和 Claude Code 那种更“产品内建”的路径不一样。Pi README 也直接说了：它是一个 minimal terminal coding harness，默认只给 4 个工具：read、write、edit、bash；像 sub agents、plan mode 这些都不是硬编码内置，而是让你通过 extension / package 自己加。GitHub



Pi 的“hooks”设计：不是 settings.json hooks，而是 extension event bus



如果把 Claude Code 的 PreToolUse / PostToolUse 类比到 Pi，Pi 对应的机制其实是 extension 事件系统。


coding-agent/docs/extensions.md 里把生命周期画得很清楚：


input

before_agent_start

context

before_provider_request

tool_call（can block）

tool_result（can modify）

turn_end

agent_end

session_start / session_switch / session_compact 等。GitHub+1


这里最重要的是两个点：


tool_call


在工具真正执行前触发，可直接返回 { block: true, reason: ... } 阻断。
官方文档和 permission-gate.ts / protected-paths.ts 示例都这么做：对危险 bash 或受保护路径的 write/edit，直接 block。GitHub+2GitHub+2


tool_result


在工具执行后、最终 tool result 发给模型前触发，可修改结果。
文档明确写了 tool_result 是 middleware 式链路：可以 patch content、details、isError。GitHub


所以从源码/文档看，Pi 的答案不是“把规则写在某个配置文件里”，而是：

把策略放进 extension，对 runtime 事件做拦截、变换、阻断和状态更新。


Pi 的“状态机”不是隐藏在框架里，而是由 extension 显式实现



这一点最好的源码例子不是 lint，而是 plan-mode 扩展。
它几乎就是一个完整的状态机实现样板。


它怎么做状态


plan-mode/index.ts 里直接维护：


planModeEnabled

executionMode

todoItems


并且用 pi.appendEntry() 持久化，再在 session_start 时从 session entries 里恢复。GitHub+1


它怎么做状态转移


开启 plan mode 时，调用 pi.setActiveTools() 把可用工具切成只读集合

tool_call 上拦截 bash，不在 allowlist 就 block

before_agent_start 注入隐藏上下文消息，告诉模型当前处于 [PLAN MODE ACTIVE]

turn_end 根据 [DONE:n] 标记推进 todo

agent_end 决定下一步是继续计划、执行计划，还是恢复正常模式。GitHub


这说明 Pi 的设计非常明确：

状态机 = extension 里的显式状态变量 + session 持久化 + lifecycle events + tool set switching + hidden context injection。

而不是框架里偷偷有一个统一的“task_state / edit_state / verification_state”对象。



Pi 对你前面那套“edit → validate → rejected/accepted → repair”是怎么设计的？



直接说结论：


Pi 没有看到内建的：


每次 edit 后自动 LSP

每次 edit 后自动 lint/typecheck

lint rejected edit 后自动禁止 build/test 的默认主流程


我在 pi-coding-agent README、extensions 文档、以及 examples 里能明确看到的是：


默认工具只有 read/write/edit/bash

可通过 extension 拦截 tool_call

可通过 extension 修改 tool_result

可通过 extension override built-in tools

可通过 extension 维护状态和切换工具集。GitHub+2GitHub+2


但我没有在这些公开文档/示例里看到 Pi 自带一个 Claude Code 那样的“edit 后自动 LSP + 本地 gate + 阻断 build”的默认实现。更准确地说，Pi 公开表达出来的是一种框架立场：

这套策略不是默认 baked in，而是应该由 extension 来实现。

这一点和它的 README 里“minimal harness、powerful defaults but skips features like sub agents and plan mode”是一致的。GitHub



也就是说，Pi 的“上述这一套”是怎么做的？



如果把你前面一直在问的那套系统拆开，Pi 的设计对应关系大概是这样：


A. CLAUDE.md / AGENTS.md 对应物


Pi 会在启动时加载 AGENTS.md 或 CLAUDE.md，从全局目录、父目录、当前目录一路拼接。
这层就是项目规则 / 常用命令 / 约定的入口。GitHub


B. hooks 对应物


不是 settings.json hooks，而是 extension events：


tool_call = PreToolUse

tool_result = PostToolUse

before_agent_start = 预注入 system/context

context = 上下文变换

turn_end/agent_end/session_start = 收尾、持久化、恢复。GitHub+1


C. 状态机


不是框架强内置，而是 extension 自己维护：


内存变量

appendEntry() 落 session

session_start 重建状态

setActiveTools() 或 hidden message 调整行为。GitHub+1


D. tool-level guardrail


靠：


tool_call block

tool_result rewrite / mark error

override built-in tools。GitHub+2GitHub+2



这对 “lint rejected edit 重新设计” 意味着什么



如果你要在 Pi 里做你前面那套设计，最自然的做法不是去找“Pi 内置哪个配置项”，而是直接写 extension，把它做成显式状态机。


我会建议这样映射：


tool_call：拦截 edit / write / bash


edit/write 后把状态设成 EDIT_PROPOSED

如果当前状态还是 EDIT_REJECTED，就 block bash build/test

如果路径敏感，直接 block
这和 protected-paths.ts / permission-gate.ts 的写法完全同构。GitHub+1


tool_result：做 validate verdict 汇总


对 edit/write 的结果，不直接让模型自由发挥

在 tool_result 里跑 lint/typecheck/LSP wrapper

如果有 blocker，就把结果改写成：
isError: true

details: { editState: "EDIT_REJECTED", diagnostics: [...] }

content 写清楚“先修复本地错误，再继续”
因为 tool_result 明确支持修改 content/details/isError。GitHub


session_start + appendEntry


保存最近一次 edit verdict

恢复 EDIT_REJECTED / EDIT_ACCEPTED

让状态能跨 branch / resume 持续
Pi 官方明确建议 extension 的 state 存在 tool result details 里，便于 branching；也支持用 appendEntry() 存自定义状态。GitHub+1


before_agent_start / context


注入隐藏控制消息，例如：
“当前 edit 被 rejected，只允许 Read/Edit/LSP”

“当前只允许 targeted verify”

或过滤掉过时状态消息
这和 plan-mode 的实现方式完全一致。GitHub


setActiveTools()


如果你想更硬一点，可以像 plan-mode 那样：


EDIT_REJECTED 时只开放 read/edit/write/bash-validate

禁用普通 bash build/test

EDIT_ACCEPTED 后再恢复正常工具集。GitHub



Pi 相比 Claude Code 的关键区别



我觉得最本质的差异有 3 个：


1. Pi 更像“可编程 runtime”，Claude Code 更像“内置产品流程”


Pi 没有把这套验证-阻断-修复闭环做成默认产品功能，而是把可编程点暴露给 extension。
Claude Code 更偏“现成 lifecycle + LSP + rules + hooks”的产品形态。
Pi 则更像“你自己写 extension，把工作流装进去”。GitHub+2GitHub+2


2. Pi 的状态更强调“会话日志可重建”


Pi session 是 JSONL tree，支持 branching、fork、compaction，并建议 extension 把 state 存在 tool result details 或 custom entries 里，这样状态能跨分支恢复。GitHub+2GitHub+2
这点对你要做 trajectory / failure attribution 很有价值。


3. Pi 默认没有把 “post-edit local validate” 产品化


默认只有 read/write/edit/bash 四工具；guardrail、plan mode、path protection、tool override 这些都通过 extension 实现。GitHub+1
所以你要的 “lint rejected edit loop” 在 Pi 里不是“打开某个内置开关”，而是“写一个 extension”。



最终判断



如果一句话总结 Pi Agent 是如何设计你前面这整套的：

Pi 不是把“edit → validate → reject/accept → repair → verify”做成固定内置状态机；它把这套东西拆成 agent-core 的 hook 点和 coding-agent 的 extension 事件，再让你用 extension 自己实现状态、拦截、验证、工具切换和持久化。 GitHub+2GitHub+2

所以如果你是要借鉴 Pi 的思路，最值得学的不是“它默认怎么做 lint gate”，而是这三件事：


事件点够全：tool_call、tool_result、context、before_agent_start、turn_end、session_start

状态能持久化：details / appendEntry() / session tree

工具集可动态切换：setActiveTools() + tool override + block/modify middleware。GitHub+3GitHub+3GitHub+3


如果你要，我下一条我可以直接给你两样东西中的一个：
A. 按 Pi extension API 写一版 lint-rejected-edit 扩展示例
或者
B. 把 Pi 的事件流翻译成你前面那套 task_state/edit_state/verification_state 的完整映射表。
