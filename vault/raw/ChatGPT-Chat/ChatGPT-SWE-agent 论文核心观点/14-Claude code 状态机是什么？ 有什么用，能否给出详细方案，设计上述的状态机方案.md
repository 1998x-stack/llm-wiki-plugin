# Claude code 状态机是什么？ 有什么用，能否给出详细方案，设计上述的状态机方案

> Source: SWE-agent 论文核心观点
> Time: 2026/4/15 10:50:38

## Question

Claude code 状态机是什么？ 有什么用，能否给出详细方案，设计上述的状态机方案

## Answer

查找Claude Code相关资料


我需要查询Claude Code的最新官方文档，因为它可能已经有所更新，产品的细节和功能也可能有所变化。虽然不是公司内部的内容，但需要确保准确、简洁地引用当前信息。所以，我会通过web查询，获取所有相关的官方资料。


搜索Claude Code官方文档及相关信息


Hooks 参考 - Claude Code Docs
ClaudeCode Hook 中文文档 | 蛤布斯堡
用了这套配置，Claude Code 终于不用我反复交代背景了 ...
Claude Code Hooks Guide


已思考 11s

可以。先把最关键的一句话说清：


Claude Code 官方没有一个现成名叫“状态机”的产品功能。
这里说的“Claude Code 状态机”，更准确地说，是基于 Claude Code 的生命周期、工具、LSP、hooks、CLAUDE.md 之上，给 agent 工作流加的一层显式控制逻辑。Claude Code 已经提供了足够的底层能力：Edit/Write 工具、LSP 在每次编辑后自动报告类型错误和警告、PreToolUse/PostToolUse hooks、以及会话级指令文件 CLAUDE.md。状态机就是把这些能力组织成一个可控、可恢复、可阻断的执行流程。Claude+1


我建议你把“状态机”理解成：

一套显式的任务阶段、状态转移条件、阻断条件、恢复路径。

它的作用不是让 Claude 更会写代码，而是让 Claude 不容易在错误状态上继续前进。这对你前面一直关心的 lint rejected edit 特别重要。因为没有状态机时，Claude 容易出现这种行为：


edit 失败了

但它还想继续 build / test

或者开始改别的文件

最后把局部错误扩散成全局混乱


而有了状态机，系统会明确规定：


这次 edit 现在属于什么状态

哪些动作被允许

哪些动作必须阻断

下一步只能走哪条恢复路径



一、Claude Code 状态机是什么


Claude Code 本身已经有很清楚的“事件点”：


用户提交提示

工具调用前

工具调用后

会话开始/结束

Claude 自动使用 LSP、Edit、Write、Bash 等工具。Claude+1


所以“状态机”不是凭空发明的，而是在这些事件点上加一层逻辑：


当前任务是不是还在 定位阶段

当前 edit 是不是 待验证

当前文件是不是 验证失败

当前任务是不是 允许升级到 build/test

当前任务是不是 可以提交


它是一个 control plane。
Claude 仍然负责推理和执行；状态机负责“交通规则”。



二、它有什么用


1. 防止“错误状态继续传播”


这是最核心的用处。
官方文档明确说，LSP 会在每次文件编辑后自动报告类型错误和警告，让 Claude 可以不用先 build 就知道问题。Claude+1
如果没有状态机，这些诊断只是“信息”；Claude 仍然可能忽略它们继续 build。
有状态机后，这些诊断会变成 状态转移条件：


无 blocking 错误 → 进入 accepted

有 blocking 错误 → 进入 rejected，禁止 build/test


这样错误不会继续往下传。


2. 把“希望 Claude 遵守”变成“Claude 必须遵守”


CLAUDE.md 能提供项目规则，但它主要是行为引导；hooks 才能在生命周期里自动执行并决定是否阻断。官方 hooks 文档明确支持在事件触发时执行命令、检查输入，并返回决定。Claude
状态机把两者结合起来：


CLAUDE.md 规定原则

hook 执行验证

状态机决定下一步是否允许


3. 让 repair loop 变得稳定


没有状态机时，Claude 修错往往是“想到哪改到哪”。
有状态机后，repair loop 会很清晰：


edit 被拒绝

收到结构化 diagnostics

只允许 Read/Edit/LSP

修好后重新验证

通过后才允许进入 build/test


这会显著减少轨迹漂移。


4. 支持多文件、多阶段任务


Claude Code 不是只能改单文件。它有 Edit、Write，Claude 也能调用 Bash、LSP、Glob、Grep 等工具。Claude
所以状态机还可以管理：


单文件 edit 状态

多文件任务整体状态

changed-files 验证状态

submit readiness


也就是说，状态机既能管局部 edit，也能管全局任务。



三、状态机应该分几层


我建议至少分三层。


第一层：Task-level 状态机


管理整个任务当前走到哪一步。比如：


task_initialized

task_localizing

task_editing

task_validating

task_ready_for_submit

task_blocked

task_completed


这层回答的是：


整个任务现在在干什么。


第二层：File-level / Edit-level 状态机


管理某个具体 edit 的状态。比如：


edit_proposed

edit_validating

edit_accepted

edit_rejected

edit_repairing


这层回答的是：


这次 edit 现在能不能算有效。


第三层：Verification-level 状态机


管理验证的范围和级别。比如：


lsp_checked

local_lint_checked

changed_files_checked

targeted_tests_checked

broad_verification_checked


这层回答的是：


现在应该跑哪一层检查，而不是盲目全量 build。



四、最推荐的核心状态机方案


下面是我建议你直接采用的主状态机。



A. Task-level 状态机


状态列表


1）TASK_INIT


任务刚开始，Claude 还没定位问题。


允许动作：


Read

Glob

Grep

LSP

Bash（只读类）

Edit/Write 一般不建议立刻做


转移条件：


找到相关文件 / 形成初步修改计划 → TASK_LOCALIZED



2）TASK_LOCALIZED


已经定位到相关文件、符号、测试入口。


允许动作：


Read

LSP

Edit

Write

少量 Bash


转移条件：


产生第一个 edit → TASK_EDITING



3）TASK_EDITING


Claude 正在做局部修改。


允许动作：


Edit

Write

Read

LSP


禁止动作：


大范围 build/test

submit


转移条件：


一个 edit 完成并进入验证 → TASK_LOCAL_VALIDATE



4）TASK_LOCAL_VALIDATE


局部 edit 已完成，正在做第一层验证。


这一步应该由：


LSP 自动诊断

PostToolUse(Edit|Write) hook 触发的 lint / parser / local typecheck


共同决定。Claude+1


转移条件：


无 blocker → TASK_EDIT_ACCEPTED

有 blocker → TASK_EDIT_REJECTED



5）TASK_EDIT_REJECTED


局部 edit 被拒绝。


允许动作：


Read

LSP

Edit

Write


禁止动作：


Bash build

全量 test

submit

扩散到不相关文件


转移条件：


修复后重新进入 TASK_LOCAL_VALIDATE


这就是你最关心的 lint rejected edit 核心状态。



6）TASK_EDIT_ACCEPTED


这次 edit 已被接受，可以向下推进。


允许动作：


下一个 file edit

changed-files validate

targeted tests

必要的小范围 Bash 验证


转移条件：


需要更多文件修改 → 回 TASK_EDITING

所有必要 edit 都完成 → TASK_TARGETED_VERIFY



7）TASK_TARGETED_VERIFY


所有关键 edit 已通过局部检查，现在跑最小相关验证。


允许动作：


targeted test

changed-files lint/typecheck

reproduction script

focused build step


转移条件：


失败 → 回到 TASK_EDITING

通过 → TASK_READY_FOR_SUBMIT



8）TASK_READY_FOR_SUBMIT


任务看起来完成，准备提交。


允许动作：


final summary

optional final check

submit


转移条件：


submit → TASK_COMPLETED



9）TASK_COMPLETED


终态。



五、Edit-level 状态机


这是最关键的一层，因为它直接解决 “rejected edit 继续 build” 的问题。



状态列表


1）EDIT_PROPOSED


Claude 刚写完一个 edit，但还没验证。


构造来源：


Edit / Write 成功返回后

diff 已产生

还没判定是否可接受



2）EDIT_VALIDATING


触发局部验证：


LSP diagnostics

syntax/parser

local lint

可选 local typecheck


这一步最好由 PostToolUse hook 自动执行。Claude



3）EDIT_ACCEPTED


通过条件：


没有 blocking diagnostics

没有 parse/syntax failure

没有项目规则定义的 blocker


允许转移：


next edit

targeted verify



4）EDIT_REJECTED


失败条件：


LSP error 达到 blocker 等级

syntax error

parser failure

local lint hard failure

policy hook 返回 block


这时系统必须做两件事：


记录 rejected reason

限制下一步动作集合



5）EDIT_REPAIRING


Claude 正在针对 rejected diagnostics 修复。


允许：


再次 Read

再次 LSP

再次 Edit


不允许：


build

broad tests

submit


修复成功后回 EDIT_VALIDATING。



六、Verification-level 状态机


这层用来避免“每次 edit 后就跑全量 build”。


状态等级


VERIFY_NONE


还没做验证


VERIFY_LSP_ONLY


只拿到 LSP 自动诊断


VERIFY_LOCAL


做了本文件 lint / parser / local typecheck


VERIFY_CHANGED_FILES


对变更文件集做了验证


VERIFY_TARGETED_TESTS


跑了最小相关测试


VERIFY_BROAD


做了更广的集成验证


核心策略：


edit 后默认先到 VERIFY_LSP_ONLY / VERIFY_LOCAL

不要一上来就 VERIFY_BROAD

只有在 edit accepted 后才允许升级验证范围



七、具体怎么落在 Claude Code 各层


1. CLAUDE.md


这里写状态转移规则和原则。


适合写：


所有 Edit/Write 后必须先看 LSP 和 local validation 结果

blocking diagnostics 未清除前，禁止 build/test/submit

多文件任务逐文件收敛，最后再做 changed-files 验证

targeted tests 优先于 broad verification

repair loop 优先最小修复，不做额外重构


这是策略层。Claude



2. hooks


这里写状态机执行器。


推荐至少配置：


PostToolUse matcher: Edit|Write

运行 local validator

汇总 LSP + lint + parser 结果

输出统一 verdict


Claude Code hooks 可以在生命周期点触发，并接收 JSON 上下文、返回决定。Claude



3. LSP


这里是第一层即时诊断源。
Claude Code 官方已经自动在每次文件编辑后报告 type errors 和 warnings。Claude+1


所以状态机设计时，不要忽略它，应该把它当成：


最低延迟

最局部

最常驻


的验证来源。



4. tool descriptions


这里写如何调用验证工具，以及失败时如何解释返回结果。


比如：


run_local_validate

run_changed_validate

run_targeted_test


并给示例。Anthropic 官方强调，工具除了 schema，最重要的是 usage examples。Claude



八、一个推荐的 verdict 数据结构


为了让状态机稳定工作，hook / validator 返回值不要只是文本，要结构化。


{
  "task_state": "TASK_LOCAL_VALIDATE",
  "edit_state": "EDIT_REJECTED",
  "verification_state": "VERIFY_LOCAL",
  "blocking": true,
  "file": "src/foo.ts",
  "changed_ranges": [
    {"start_line": 42, "end_line": 49}
  ],
  "diagnostics": [
    {
      "source": "lsp",
      "severity": "error",
      "code": "TS2339",
      "message": "Property 'bar' does not exist on type 'Baz'.",
      "range": {"start_line": 44, "end_line": 44}
    }
  ],
  "allowed_next_tools": ["Read", "Edit", "LSP"],
  "disallowed_next_tools": ["Bash", "Submit"],
  "repair_instruction": "Fix blocking diagnostics in the edited file before any build or broader verification."
}


这个结构的核心价值是：


Claude 不需要猜“我现在是什么状态”

Claude 不需要猜“我接下来能做什么”

Claude 不需要猜“是不是还能继续 build”



九、一个完整的转移逻辑


你可以把主路径理解成：


TASK_INIT
→ TASK_LOCALIZED
→ TASK_EDITING
→ EDIT_PROPOSED
→ EDIT_VALIDATING
→
如果通过：EDIT_ACCEPTED
→ TASK_TARGETED_VERIFY
→ TASK_READY_FOR_SUBMIT
→ TASK_COMPLETED


如果失败：
EDIT_REJECTED
→ EDIT_REPAIRING
→ EDIT_VALIDATING
→ 再次判断


这就是完整闭环。



十、为什么这套方案有效


因为它把 Claude Code 现有能力真正用起来了：


CLAUDE.md 负责规则与偏好加载。Claude

hooks 负责在工具调用后自动做 deterministic checks。Claude

LSP 负责 edit 后自动给即时诊断。Claude+1

工具描述负责把“怎么调用验证工具”讲清楚。Claude


所以状态机不是额外负担，而是把这些零散能力变成一个统一工作流。



十一、最简落地版


如果你想先做 MVP，我建议先做三条规则就够了：


Edit|Write 后自动跑 PostToolUse local validate。Claude

如果有 blocking diagnostics，状态进入 EDIT_REJECTED，禁止 Bash/Submit。

只有 EDIT_ACCEPTED 后，Claude 才能跑 targeted tests 或更广验证。


这三条就已经能把你图里那类问题基本消掉。



十二、一句话总结


Claude Code 状态机，不是 Claude Code 官方单独的产品模块，而是你基于 CLAUDE.md + hooks + LSP + tools 设计出来的一层显式控制系统。它的核心价值是把“Claude 应该怎么做”升级成“Claude 现在处于什么状态、只能怎么做”，从而把 lint rejected edit 这类局部错误困在局部修复闭环里，而不是继续扩散到 build/test/submit。Claude+2Claude+2


你要的话，我下一条可以直接给你两样东西中的任意一个：
一份 可直接落地的 CLAUDE.md + hooks 模板，或者一份 完整状态机 JSON Schema / YAML 配置草案。



Sources:


Tools reference - Claude Code Docs
