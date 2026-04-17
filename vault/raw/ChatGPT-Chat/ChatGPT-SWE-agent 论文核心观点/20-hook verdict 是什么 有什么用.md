# hook verdict 是什么 有什么用

> Source: SWE-agent 论文核心观点
> Time: 2026/4/15 11:23:16

## Question

hook verdict 是什么 有什么用

## Answer

我查一下 Claude Code hooks 里这个概念在官方文档中的具体语义，再给你一个工程上好用的解释。

搜索Claude Code钩子官方文档


Hooks 参考 - Claude Code Docs


已思考 15s

hook verdict 可以理解成：

hook 在收到事件输入后，返回给 Claude Code 的“处理结果/裁决”。

官方文档的表述是：当 hook 事件触发时，Claude Code 会把 JSON 上下文传给你的 hook 处理器；处理器可以检查输入、采取行动，并且可选地返回一个 decision。Claude+1



它本质上是什么


从工程角度看，hook verdict 就是 hook 对当前事件给出的控制信号。常见用途有三类：


第一类是放行。
也就是 hook 看完输入后，认为这次工具调用或当前流程可以继续。Claude+1


第二类是阻断。
例如在 PreToolUse 里，你可以在工具真正执行前检查输入；官方指南就给了阻止编辑受保护文件的例子，命中规则后 Claude 会收到“为什么被阻止”的反馈。Claude


第三类是附加上下文/反馈。
例如在 PostToolUse 里，你可以在编辑后自动运行格式化或验证逻辑，并把结果回灌给 Claude，影响它下一步怎么做。官方指南明确展示了 PostToolUse 配 Edit|Write，在每次编辑后自动执行命令。Claude



它有什么用


1. 把“希望 Claude 做”变成“系统确定会做”


官方 hooks 指南强调，hooks 提供的是对 Claude Code 行为的deterministic control，也就是确定性控制：某些动作会始终发生，而不是依赖 LLM 自己决定要不要做。Claude+1


这就是 hook verdict 最核心的价值。
没有 verdict，你只能“提示 Claude 应该先 lint 再 build”；
有 verdict，你可以真正表达：


这次 edit 可以继续

这次 edit 必须先修

这次 Bash 命令不允许执行

这段额外信息必须注入给 Claude


2. 把工具调用变成“可治理流程”


Claude Code 的 hook 事件覆盖了：


会话级事件

每轮事件

agentic loop 内每次工具调用事件


官方参考里明确列出了 SessionStart、UserPromptSubmit、PreToolUse、PostToolUse 等。Claude+1


所以 verdict 的作用其实是：

让你在这些生命周期点，对 Claude 的行为做显式治理。

3. 做状态机的“状态转移结果”


如果你在实现我们前面讨论的状态机，那么 hook verdict 就是最自然的状态转移输出。


比如：


PostToolUse(Edit) 后返回：EDIT_REJECTED_HARD

PostToolUse(Edit) 后返回：EDIT_ACCEPTED_LOCAL

PreToolUse(Bash) 时根据状态返回：允许或阻断


也就是说，verdict 就是状态机在每个事件点给出的裁决结果。
这是我对 hooks 机制的工程化解释，和官方的“可选返回 decision”是一致的。Claude+1



你可以把它理解成什么


最简单的类比是：


event：发生了什么

hook input：这次事件的上下文

hook verdict：系统看完后给出的裁决


例如：


例子 1：编辑受保护文件


event：PreToolUse(Edit)

input：Claude 想编辑 .env

verdict：block

用处：防止危险修改。官方指南就有这个模式。Claude


例子 2：编辑后自动格式化


event：PostToolUse(Edit|Write)

input：刚刚改了哪个文件

verdict：continue + 附加结果

用处：自动执行后处理。官方指南给了 Prettier 示例。Claude


例子 3：lint rejected edit


event：PostToolUse(Edit)

input：修改后的文件路径和工具上下文

verdict：
HARD_REJECT：本地状态坏了，必须修

SOFT_INCOMPLETE：局部健康，但任务没收敛

ACCEPTED：允许进入下一步

用处：把“验证结果”变成后续流程控制


这个第三类不是官方文档直接给的术语，而是把 hook 的 decision 能力用于你关心的 edit/validate 状态机。



为什么它很关键


因为如果没有 hook verdict，很多规则都只是“建议”：


Claude 也许会先 lint

也许会忽略 lint

也许 edit 已经坏了还继续 build

也许该阻断的时候没阻断


而有了 verdict，你能真正控制：


是否继续

是否阻断

需要向 Claude 注入什么反馈

当前状态应该怎么更新


所以一句话总结：

hook verdict 就是 hook 对某个生命周期事件给 Claude Code 发出的裁决结果；它的作用是把规则、验证和状态机，变成真正会生效的控制逻辑。 Claude+2Claude+2

你要的话，我下一条可以直接给你一个 hook verdict 的标准 JSON 结构模板。



Sources:


Hooks 参考 - Claude Code Docs
