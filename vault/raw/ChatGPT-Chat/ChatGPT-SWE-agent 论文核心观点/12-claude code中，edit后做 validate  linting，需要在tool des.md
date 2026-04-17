# claude code中，edit后做 validate / linting，需要在tool desctiption 还是 claude.md 或者其他层面进行

> Source: SWE-agent 论文核心观点
> Time: 2026/4/15 10:32:23

## Question

claude code中，edit后做 validate / linting，需要在tool desctiption 还是 claude.md 或者其他层面进行深度构造？

## Answer

我先核一下 Claude Code 官方文档里这几个层次分别是干什么的，再给你一个“放在哪里最合适、为什么”的设计结论。

浏览Anthropic官方文档关于Claude Code


Claude Code | Anthropic's agentic coding system
用了这套配置，Claude Code 终于不用我反复交代背景了 ...
Claude Code settings.json 详解（三）：hooks 钩子全解析
Hooks reference - Claude Code Docs
Claude Code Hooks 完全指南：自动格式化、自动测试等 ...


Opening official documentation from code.claude.com and anthropic


Hooks reference - Claude Code Docs
Claude Code | Anthropic's agentic coding system  \ Anthropic


搜索Claude.md文档和工具描述


Explore the .claude directory - Claude Code Docs
CLAUDE.md 使用指南 - 菜鸟教程
【Claude Code最新教程】CLAUDE.md详解与最佳实践 ...
CLAUDE.md 编写完全指南：项目配置最佳实践 | ClaudeCodeLab


寻找CLAUDE目录和工具参考


Explore the .claude directory - Claude Code Docs


查找LSP工具行为及钩子示例


Hooks reference - Claude Code Docs
Introducing advanced tool use on the Claude Developer Platform \ Anthropic


已思考 32s

我的判断是：


不要把 edit 后的 validate / linting 只放在一个层面。
在 Claude Code 里，最稳的做法是分层：


tool description / tool schema：定义“这个工具是什么、输入输出是什么、什么时候该用”

CLAUDE.md：定义“项目希望 Claude 遵守什么流程和偏好”

hooks / settings.json：定义“哪些检查必须自动触发、失败后怎么阻断或反馈”

LSP / built-in verification：提供“编辑后的即时代码智能反馈”


这样分工最清晰，也最接近 Claude Code 官方能力边界：CLAUDE.md 是每个会话都会加载的持久指令；settings.json 负责 permissions、hooks、env vars 等；PostToolUse/PostToolUseFailure 可以在工具调用后自动执行逻辑并把反馈给 Claude；而内建 LSP 工具会在每次文件编辑后自动报告 type errors 和 warnings。Claude+2Claude+2



先给结论：validate 放哪里最合适


最应该放在 hooks / settings.json 的内容


“凡是必须执行、需要自动触发、最好能阻断或回灌给模型的检查”，都应该放在 hooks。
原因很简单：PostToolUse 就是为“工具成功执行后立刻跑额外逻辑”设计的，而且可以把 additionalContext 或 decision: "block" 返回给 Claude；PostToolUseFailure 则能在工具失败时提供纠偏信息。官方还明确给了 PostToolUse 针对 Write 的输入 schema。Claude+1


对 edit/lint 这个问题，hooks 才是真正的执行层。
因为你要的不是“Claude 知道应该 lint”，而是“Claude 写完就真的会被触发 lint”。


最应该放在 CLAUDE.md 的内容


“项目级规范、优先级、策略偏好、验证顺序” 适合放 CLAUDE.md。
比如：


修改 Python 文件后优先看 LSP 诊断

只跑最小相关测试，不要先跑全量

formatter 可以自动修，但 typecheck 不通过不能提交

前端改动先跑 eslint + targeted test

migration / schema 变更时要补相应检查


这是因为 CLAUDE.md 是“每个会话都会加载的指令层”，适合放长期稳定的项目规则，而不是具体自动化机制。官方文档就把 CLAUDE.md 定义为 every session loaded 的 instructions。Claude


最应该放在 tool description / tool examples 的内容


“Claude 如何正确使用 validate 工具” 适合放在 tool description，最好再加 examples。
Anthropic 官方工程文章明确说过：agent 需要从示例中学习正确的 tool usage，仅靠 JSON schema 不够，因为 schema 只能表达结构合法性，表达不了“什么时候该用、哪些参数组合有意义、你们约定的使用惯例”。Anthropic


所以如果你有自定义 MCP 工具，比如：


run_lint

run_targeted_tests

validate_changed_files


那它们的 tool description 里要写清：


适用场景

输入粒度

失败输出格式

与 edit / LSP / Bash 的关系


但这层更像“教会 Claude 怎么用工具”，不是“强制一定会执行”。



为什么不能只靠 CLAUDE.md


因为 CLAUDE.md 主要是行为引导，不是强执行机制。
它会在会话里持续影响 Claude 的决策，但它本身不会自动在写文件后触发命令。官方分工也很清楚：CLAUDE.md 是 instructions；settings.json 才是 permissions / hooks / env vars 的位置。Claude


所以如果你把“每次 edit 后必须 lint”只写在 CLAUDE.md 里，会有三个问题：


第一，Claude 可能在复杂任务中“知道但漏做”。
第二，Claude 可能做了，但做法不一致，比如有时跑全量、有时跑单文件。
第三，失败时你拿不到结构化、自动回灌的反馈。


换句话说：

CLAUDE.md 能提高遵守概率，但不能替代自动化 enforcement。


为什么不能只靠 tool description


因为 tool description 决定的是“会不会正确调用”，不是“是不是必定会发生”。
尤其在 Claude Code 这种 agentic loop 里，Claude 会根据任务自己选择工具；官方文档也明确说 Claude 会根据 prompt 和沿途获得的信息决定用什么工具。Claude


所以如果你把 lint 逻辑全塞进某个自定义工具描述里，比如：

修改完文件后请调用 run_lint

这仍然是“软约束”。
Claude 大概率会做得更好，但它仍然可能：


先忘了调用

调错粒度

在多文件任务里只检查一个文件

没把失败当 blocker


tool description 更适合解决的是：

“Claude 应该怎么调用 validate 工具，返回值怎么看，什么时候升级到更重的检查。”


Claude Code 现成能力里，哪个层面最应该承接“edit 后 validate”


1. LSP：做即时、低延迟、编辑后自动反馈


官方 Tools reference 明确写了：LSP 工具提供 code intelligence；after each file edit, it automatically reports type errors and warnings，Claude 也可以直接调用它做 definition/reference/type info 等导航。Claude


所以如果你的问题是：

Claude Code 里 edit 后的第一层 validate 应该放哪？

答案其实是：

先吃内建 LSP 自动反馈。

它天然适合作为第一道快速反馈，因为它和 edit 紧耦合，而且不用你额外再教 Claude“写完后先去哪里看诊断”。


2. hooks：做强制触发的 lint / test / policy checks


如果你需要：


写完文件就跑 lint

某些文件改动后自动跑 targeted tests

改了 schema 文件就自动做 migration check

不通过时把结果立即反馈给 Claude 继续修


那就应该在 settings.json 的 hooks 里做。
PostToolUse 正适合 “Write/Edit 之后触发命令”；官方 hook lifecycle 也把 PreToolUse / PostToolUse 放在每次 agentic loop 的工具调用里。Claude+1


3. CLAUDE.md：做策略编排


CLAUDE.md 最适合写成这种规则：


优先读取 LSP 诊断，再决定是否跑 Bash 级 lint

修改单文件时优先单文件校验；多文件提交前再跑 changed-files 校验

不要在每次小 edit 后跑全量测试，除非用户明确要求

若 hook 返回 blocker，先修 blocker 再继续实现


这样 Claude 的策略会更稳定，但执行仍由 hooks/LSP 托底。



我建议的分层设计


A. 最佳实践：四层分工


第 1 层：tool description / examples
负责“会用”。


放这些内容：


run_lint(file_paths, scope) 的参数语义

scope=changed 和 scope=workspace 的区别

什么时候先用 LSP，什么时候再用 Bash lint

失败输出如何阅读


这层的重点不是硬约束，而是 Anthropic 强调的 usage patterns from examples。Anthropic


第 2 层：CLAUDE.md
负责“想这么做”。


放这些内容：


项目验证策略

最小检查原则

提交前门槛

特定目录/语言的额外规则


这层让 Claude 有稳定偏好。Claude


第 3 层：hooks / settings.json
负责“真的会做”。


放这些内容：


PostToolUse on Edit / Write

跑 eslint, ruff, mypy, pytest -k ...

返回 additionalContext

必要时 decision: "block" 阻断继续推进


这层是执行与 enforcement。Claude


第 4 层：LSP
负责“最快的即时反馈”。


放这些内容：


每次 edit 后自动出现的 type errors / warnings

直接导航到定义、引用、实现


这层应该是默认基础设施。Claude



一个更具体的建议


如果你问的是：

在 Claude Code 里，我要把 “edit 后 validate / linting” 的主逻辑放哪？

我的答案是：

主逻辑放 hooks，策略写 CLAUDE.md，工具用法放 tool description/examples，第一层即时诊断依赖 LSP。

也就是：


必须发生 的，放 hooks

希望 Claude 优先这么做 的，放 CLAUDE.md

自定义工具该怎么用 的，放 tool description + examples

编辑后的快速语义反馈，交给 LSP


这是最稳的组合。



一个常见误区


很多人会把所有规则都写进 CLAUDE.md，期待 Claude 记住：


写完就 lint

lint 失败就修

再跑 test

再检查 changed files


这在简单项目里可行，但一旦任务变长，就容易退化成“知道规则，但执行不稳定”。
Claude Code 官方把 hooks 单独做成生命周期自动化机制，本质上就是在告诉你：

重复、机械、必须执行的流程，不要只靠模型记忆，要下沉到生命周期自动化。 Claude+1


最后给你一个落地判断


如果你现在在做 Claude Code 项目的 edit-validate 体系，我建议：


第一步：先写一个简洁的 CLAUDE.md，定义“先 LSP、后 targeted lint、提交前再 widened checks”的策略。Claude

第二步：在 settings.json 里配 PostToolUse 钩子，匹配 Edit 或 Write，自动跑最轻量的 lint/check，并把结果回灌给 Claude。Claude+1

第三步：如果你有自定义 MCP validate 工具，再把“正确用法 + 示例”写进 tool description，而不是只写参数 schema。Anthropic

第四步：把 LSP 当作默认的第一道反馈，而不是自己重造一个“每次 edit 后先跑重型检查”的流程。Claude


一句话总结：

Claude.md 负责“理念”，tool description 负责“会用”，hooks 负责“执行”，LSP 负责“即时反馈”。edit 后 validate / linting 的主战场应该是 hooks，不该只靠 CLAUDE.md。


Sources:


Explore the .claude directory - Claude Code Docs

Introducing advanced tool use on the Claude Developer Platform \ Anthropic
