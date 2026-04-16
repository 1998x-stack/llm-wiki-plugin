# claude code中，edit后做 validate / linting，需要在tool desctiption 还是 claude.md 或者其他层面进行

> Source: SWE-agent 论文核心观点
> Time: 2026/4/15 10:34:51

## Question

claude code中，edit后做 validate / linting，需要在tool desctiption 还是 claude.md 或者其他层面进行深度构造？
关键是 根据linting，Agent纠正 错误，如何以及在什么层面深度构造，对于lint rejected edit 重新设计

## Answer

Searching for Claude Code documentation


这是一个关于Claude Code的工作相关问题，因此我应该先考虑查找最新的文档。信息可能已经发生变化，所以我打算通过网络搜索最新的Claude文档来获取相关数据，尤其是关于钩子、LSP、工具描述等部分。


搜索Claude Code官方文档和工具描述


尝试使用一般网络搜索


搜索失败可能是因为域名的原因。为了补充信息，我会尝试用更广泛的网络搜索方法，看看能否找到相关的资料。


搜索与Claude工具使用相关文档


Hooks 参考 - Claude Code Docs
Introducing advanced tool use on the Claude Developer Platform
02-项目配置：CLAUDE.md、MCP、Skill与Hooks - 博客园
Claude Code Hooks 2026：全部事件列表 + 12个即用配置


查找官方文档


我要参考官方文档，可能需要查看来自搜索结果的code.claude.com文档。我会进一步寻找CLAUDE.md页面以及工具参考页面，确保获取准确的资料。


搜索Claude官方文档和工具参考


Explore the .claude directory - Claude Code Docs
CLAUDE.md 使用指南 - 菜鸟教程


已思考 30s

关键结论：


lint rejected edit 的“纠错闭环”主逻辑，不该放在 tool description，也不该只放在 CLAUDE.md。
最稳的设计是：


LSP / validate engine 负责发现问题，
hooks 负责强制触发与状态机控制，
CLAUDE.md 负责策略与优先级，
tool description 负责让 Claude 正确理解怎么调用工具、怎么看返回。


Claude Code 官方能力本身就是这么分层的：CLAUDE.md 是会话加载的持久指令；hooks 可以在 PreToolUse / PostToolUse 等生命周期点自动运行并把结果回灌给 Claude；LSP 会在每次文件编辑后自动报告 type errors 和 warnings。Claude+2Claude+2



先回答你最关心的点


你图里这句话：

“The edit was rejected by the linter, but I need to build anyway…”

这其实暴露了一个设计错误：


把 “edit-level guardrail” 和 “task-level verification” 混在了一起。


也就是系统没有明确区分：


这次编辑是否可以被接受

整个任务是否需要继续 build / test 验证


正确做法不是让 Claude 在被拒后自己辩论“要不要继续 build”，而是把它设计成一个明确状态机：


Edit proposed

Edit validated

Edit accepted 或 Edit rejected

如果 rejected，进入 repair loop

只有 accepted 的代码，才允许进入 build / test verification


也就是说：

被 lint reject 的 edit，不应该继续作为工作副本往后流。
应该回到“修这次 edit”的局部闭环，而不是升级到全局 build。

这和 Claude Code 的 hooks 能力非常契合，因为 hooks 可以在工具执行后自动运行验证逻辑，并返回额外上下文或直接阻断。Claude



应该放在哪一层


1. tool description：只负责“会不会用”


这一层适合写：


Edit 后通常会触发哪些检查

run_lint / run_typecheck / run_targeted_test 这些工具怎么选

返回结果里的字段是什么意思

遇到 lint_rejected 时应该进入 repair，而不是直接 build


但这一层不能承担强约束。
原因是 tool description 只能提高 Claude 的调用质量，不能保证它每次都真的执行这套流程。Anthropic 官方工程文章也强调，工具定义里除了 schema，还应该给具体 usage examples，因为 schema 本身不够表达正确使用模式。Anthropic


所以这一层的职责是：

教 Claude“怎么用验证工具”，不是保证验证一定发生。


2. CLAUDE.md：负责“策略与原则”


这一层最适合写成项目规则，例如：


每次 Edit/Write 后先读 LSP 诊断

单文件改动优先单文件 lint / typecheck

只有 edit accepted 才能进入 build / test

lint rejected edit 必须先修，不允许把 rejected edit 当成当前真状态

多文件修改时，先局部修复，再做 changed-files 级验证

不要把 build 当成替代 lint 的手段


因为 CLAUDE.md 会在会话中自动加载，适合承载这种长期、稳定的项目级决策规则。Claude


但它的问题也很明显：


它是“行为引导层”，不是“执行引擎层”。
所以它必须有，但不能单独承担 lint rejected edit 的闭环。



3. hooks：这是主战场


如果你问我 “lint rejected edit 重新设计”最应该深构在哪一层，我的答案是：

hooks + validator state machine。

Claude Code 的 hooks 本来就是在生命周期里自动执行的，PostToolUse 尤其适合在 Edit / Write 后立刻触发验证。hook 能做三件特别关键的事：


自动跑 lint / typecheck / targeted checks

把结果结构化回灌给 Claude

必要时直接 block 后续推进 Claude


这一层才是真正能把“知道该修”变成“必须先修”的地方。



4. LSP：做第一道即时反馈


Claude Code 官方写得很清楚：LSP 在每次文件编辑后会自动报告 type errors 和 warnings。Claude


所以 lint rejected edit 的重构，不应该从零开始自造一套“编辑后马上检查”的系统，而应该先承认：

Claude Code 已经有一层天然的 edit-after diagnostics。

你要做的不是替代它，而是围绕它设计：


哪些 LSP diagnostics 只是 warning

哪些 diagnostics 会把 edit 判成 rejected

rejected 后 Claude 应该怎么 repair

repair 成功前是否允许继续其他工具



真正需要深构的，不是“写在哪里”，而是“状态机怎么设计”


我建议把 edit → validate → repair 设计成一套显式状态机，而不是一句模糊规则。



推荐状态机


状态 1：proposed_edit


Claude 提出一个 edit，还没有被接受。


这里记录：


file path

changed ranges

diff summary

edit intent


状态 2：local_validate


系统自动触发局部验证：


LSP diagnostics

单文件 lint

syntax / parser checks

必要的 formatter safety checks


这一步最好由 PostToolUse(Edit|Write) hook 驱动。Claude+1


状态 3A：accepted_edit


条件是：


没有 blocking diagnostics

没有 syntax errors

没有被项目规则定义为 blocker 的 lint/type errors


此时 Claude 才能进入：


build

targeted test

next file edit

submit path


状态 3B：rejected_edit


条件是：


syntax / parse failure

blocking lint

blocking typecheck

hook policy reject


这时不能把工作副本当作已生效状态继续下去。
应该进入：


状态 4：repair_loop


Claude 收到结构化反馈后，只做这几件事之一：


revise same file edit

revert and re-edit

ask for clarification（极少数）

escalate to broader change only if local fix impossible


repair 成功后重新回到 local_validate。



最重要的设计点：反馈要结构化，不要只是“被拒绝了”


如果 hook 或 validator 只是返回一句：

lint rejected

Claude 很容易进入你图里那种错误心态：
“虽然被拒了，但我还是先 build 看看吧。”


所以你需要的不是简单报错，而是结构化 rejection。


建议返回这种结构：


{
  "edit_status": "rejected",
  "blocking": true,
  "scope": "single_file",
  "file": "src/foo.ts",
  "diagnostics": [
    {
      "source": "tsserver",
      "severity": "error",
      "code": "2339",
      "range": {"start": [42, 10], "end": [42, 25]},
      "message": "Property 'bar' does not exist on type 'Baz'."
    }
  ],
  "repair_instruction": "Fix the blocking diagnostics in this file before running build or broader tests.",
  "next_allowed_actions": ["Edit", "Read", "LSP"],
  "disallowed_actions": ["Bash(build)", "Bash(test:full)", "Submit"]
}


这样 Claude 不再需要“猜接下来该干嘛”，而是会被明确推回 repair loop。



lint rejected edit 该怎么重新设计


我建议你不要用“reject by linter”这个概念做唯一入口，而是做成三层 gate。


第一层：soft warnings


不阻断，只回灌。
例如：


formatting suggestions

non-critical style issues


Claude 可以继续，但需要优先修。


第二层：blocking local diagnostics


阻断当前 edit 进入 build/test。
例如：


syntax error

unresolved symbol

obvious type error

parse failure


这是 lint rejected edit 的主集合。
它们应该把 Claude 推回 repair_loop。


第三层：task-level verification failures


这是 edit accepted 之后才会发生的。
例如：


unit tests failed

build failed

regression introduced


这时候 Claude 才应该做你图里那种“继续 build/test 验证”的事。
也就是说：

build 是验证 accepted edit 的，不是用来给 rejected edit 兜底的。


具体该写什么


在 CLAUDE.md 里写


写原则，不写脚本细节：


所有文件修改后先读取 LSP / local validation 结果

blocking diagnostics 未清除前，不要运行 build 或扩大验证范围

对 rejected edit，优先最小修复，不要引入额外重构

多文件任务逐文件收敛，最后再做 changed-files 验证


这样 Claude 的策略会更稳定。Claude



在 hooks 里写


这里写真正自动化逻辑：


PostToolUse(Edit)

PostToolUse(Write)


执行：


run local linter / typecheck / parser

merge with LSP diagnostics

classify into soft/blocking

return structured result

blocking 时直接阻止继续进入 build/test 分支


这部分是核心。Claude



在 tool description 里写


写清楚工具语义和例子：


run_local_validate(file, changed_ranges)

run_changed_files_validate(files)

run_targeted_test(test_ids)

accept_edit / reject_edit / repair_edit


尤其要给例子。
Anthropic 官方对工具使用的建议很明确：
工具示例能显著提高正确使用率，schema 本身不够。 Anthropic



一个推荐架构


最稳的分工是：


LSP
发现 edit 后即时错误。Claude


Hook validator
把 LSP + lint + parser 合成统一 verdict。Claude


CLAUDE.md
规定 rejected edit 必须 repair，accepted edit 才能 broaden verification。Claude


Tool descriptions + examples
教 Claude 如何调用局部验证、扩大验证、修复验证失败。Anthropic



最后的结论


你这个问题的核心不是“放在 tool description 还是 CLAUDE.md”，而是：

lint rejected edit 必须从“提示词规范”升级成“生命周期状态机”。

真正应该深构的层面是：


主逻辑在 hooks，策略在 CLAUDE.md，工具语义在 tool descriptions，第一层即时诊断依赖 LSP。


如果只写在 CLAUDE.md，它会变成“希望 Claude 记住”；
如果只写在 tool description，它会变成“希望 Claude 会用”；
只有把它下沉到 hooks + structured validator result，Claude 才会真的进入：


edit → validate → reject/accept → repair/retest


而不是出现图里那种：


“虽然 edit 被拒了，但我还是想先 build 一下。”


我可以下一条直接给你一版 Claude Code 的 lint rejected edit 状态机 JSON schema，或者给你一份 CLAUDE.md + hooks 配置模板。



Sources:


Explore the .claude directory - Claude Code Docs

Introducing advanced tool use on the Claude Developer Platform
