# 这里我有一个疑问, 局部编辑会不会有一定验证不通过的情况, 比如LLM打算修改一个变量的类型, 它一定会一个 multiedit 把所有地方都改完吗?  如果做

> Source: SWE-agent 论文核心观点
> Time: 2026/4/15 11:13:22

## Question

这里我有一个疑问, 局部编辑会不会有一定验证不通过的情况, 比如LLM打算修改一个变量的类型, 它一定会一个 multiedit 把所有地方都改完吗?  如果做不到那中间修改的每一步都可能会引发lint error 
以及编辑验证的周期颗粒度是每次编辑, 还是end turn来一次

## Answer

已思考 7s

这是个非常关键的问题，而且你问到了这类系统里最容易设计错的地方。


结论先说：


会。局部编辑完全可能暂时不通过验证。
尤其当修改是“跨文件、跨符号、跨调用链”的时候，LLM 不一定能在一次 edit 里把所有地方一起改完。
所以如果你把“每次 edit 后必须 100% lint/typecheck 通过”当成硬门槛，系统很容易被卡死。


因此更合理的做法不是：

每次 edit 后都要求“仓库局部完全健康”

而是：

每次 edit 后区分“暂时性中间态” vs “明显坏状态”，再决定是否阻断。

你第二个问题也一样重要：


验证周期不应该只有一种。
一般要分层：


每次编辑后：做快速、局部、低成本验证

end turn / 一个小批次编辑后：做中等粒度验证

阶段完成后：做 targeted verify

提交前：再做更大范围验证


也就是说，不是 edit 粒度和 end-turn 粒度二选一，而是都要有，只是承担的职责不同。



1. 为什么局部编辑天然会有“中间不通过”的情况


你举的例子非常典型：

LLM 想把一个变量的类型改掉，但不一定一次把所有引用都改完。

这类改动常见于：


类型签名修改

函数参数重命名

返回值结构变化

类字段改名

接口拆分

异步/同步切换

schema 迁移

调用链层层传递的改动


在这些场景里，“最终正确”往往必须经过“中间暂时不一致”。
也就是说，存在一种合法的开发路径：


先改定义

再改直接调用点

再改深层使用方

最后补测试/适配逻辑


在第 1、2 步之间，lint/typecheck 很可能短暂报错。
这不是 agent 失控，而是增量修改天然产生的过渡态。


所以如果你的 gate 是：

每一次 edit 后都必须零错误

那系统会迫使 agent 只能做：


超大原子 edit

或者永远不敢做跨文件改动


这两者都不好。



2. 为什么“每次 edit 必须全通过”会有问题


问题一：会逼迫模型做过大的原子编辑


为了避免中间态报错，模型会倾向于一次改很多地方。
但一次改太多地方，又会带来：


diff 过大

定位难

恢复难

出错后不好修

observation 过载


结果就是你本来想通过“严格 validate”提升稳定性，反而把 agent 推向更危险的大步编辑。


问题二：会错误惩罚“合理过渡态”


有些错误不是“编辑错了”，只是“还没改完”。
如果把这种状态直接判成 rejected，Claude/agent 会被迫回滚一个其实方向正确的改动。


问题三：会让 repair loop 变成无意义来回


系统会一直说：


edit rejected

edit rejected

edit rejected


但真正需要的不是“修这个局部 lint”，而是“继续完成剩余迁移”。


这时 repair loop 就变成了假问题。



3. 所以关键不是“验不验”，而是“验什么”


这里最重要的设计原则是：

把验证分成“局部结构健康检查”和“任务完整性检查”两类。

A. 局部结构健康检查


回答的是：


这次 edit 有没有把代码写坏到不应该继续？


这类检查适合每次 edit 后做，典型包括：


语法错误

parser failure

非法缩进

文件损坏

明显格式破坏

edit 命令写坏文件边界

不可解析 AST


这些问题一旦出现，基本可以确定：

这不是“合理中间态”，而是“坏状态”。

所以这类应该是 硬阻断。



B. 任务完整性检查


回答的是：


当前整个改动链是否已经收敛完成？


这类检查更适合在 end turn、batch end、阶段结束、submit 前做。典型包括：


typecheck 全通过

changed-files lint 全通过

相关单测通过

调用链一致

迁移是否完整


这些失败不一定意味着当前 edit 错了，可能只是：

还没改完。

所以这类一般不该在每次 edit 后直接强阻断，至少不能一刀切。



4. 怎么区分“合理中间态”与“明显坏状态”


这是设计状态机时最核心的一刀。


我建议把 edit 后的结果分成三类，而不是两类。


类别 1：HARD_REJECT


必须立刻阻断并进入 repair。


典型包括：


syntax error

parser failure

文件被写坏

非法 patch / 不可解析

严重局部 lint 失败（比如 Python 缩进炸了）

工具执行异常导致状态不可信


这类说明：

当前文件已经不处于可继续工作的健康状态。

所以要回 repair loop。



类别 2：SOFT_INCOMPLETE


允许继续，但要显式记录“当前任务还未收敛”。


典型包括：


改了类型定义，调用点还没全改

新接口已写，但旧调用还存在

changed-files typecheck 还有若干可解释错误

测试尚未更新

repo 级 build 暂时失败，但失败原因与预期迁移一致


这类说明：

当前 edit 本身可以接受，但任务尚未完成。

所以不能 submit，但可以继续下一步 edit。



类别 3：ACCEPTED


局部健康，且当前阶段的预期验证已通过。


这时允许进入：


下一文件

targeted verify

submit path



5. 你的例子里，类型迁移应该怎么处理


假设 agent 要把：


type UserId = string


改成：


type UserId = { value: string }


而项目里几十处都在用 UserId。


如果你要求每次 edit 后必须零错误，那它必须一次改完所有引用。
这对 agent 很难，也不稳。


更合理的方式是：


第一步：进入“迁移模式”


状态机知道这是一类跨文件迁移，不应该把中间 type errors 全当 hard reject。


第二步：局部 edit 后只检查“文件是否健康”


例如：


语法是否正确

AST 是否可解析

当前 edit 是否引入明显局部错误


如果健康，就允许继续。


第三步：在 end turn / batch end 做“迁移进度检查”


例如：


当前 changed files 里还有多少相关 type errors

错误是否集中在预期调用点

是否符合迁移路径


如果错误是“预期中的未完成迁移”，标为 SOFT_INCOMPLETE，而不是 HARD_REJECT。


第四步：当相关调用链改完后，再做 stricter verify


这时再要求：


changed-files typecheck 通过

targeted tests 通过



6. 所以验证颗粒度到底是“每次编辑”还是“end turn”？


答案是：

两者都要，但目的不同。


每次编辑后：做“局部健康验证”


目标是判断：


这次 edit 有没有把当前文件/局部状态写坏

是否应该立刻 repair


适合做：


syntax

parser

轻量 LSP

单文件 lint

局部 AST/format 健康检查


不适合在这一步强行做：


全项目 typecheck

全项目 test

大范围 build


因为这些太重，而且会把“未完成迁移”误判成“坏 edit”。



End turn / 小批次结束：做“阶段收敛验证”


目标是判断：


这一轮做完后，当前子目标是否接近完成

当前错误是“坏状态”还是“还没改完”


适合做：


changed-files typecheck

相关符号/调用链检查

轻量 targeted lint

migration completeness heuristic


这一步最适合识别 SOFT_INCOMPLETE。



阶段结束 / 准备提交前：做“严格验证”


目标是判断：


是否真的可以 submit


适合做：


targeted tests

changed-files strict validation

必要的 build / integration check



7. 最推荐的验证分层


我建议你直接这样设计。


Layer 1：After Edit


强制执行，快，硬 gate


输出：


HARD_REJECT

PROVISIONALLY_ACCEPTED


检查：


syntax

parser

file integrity

局部 LSP


如果失败：进入 repair
如果通过：允许继续，但不代表任务完成



Layer 2：End Turn / End Batch


阶段性判断，识别中间态


输出：


SOFT_INCOMPLETE

BATCH_ACCEPTED

HARD_REJECT


检查：


changed-files validation

迁移相关错误是否仍集中在预期范围

是否出现新的非预期扩散错误


这一步最关键，因为它解决你提的那个问题：

不要把“合理未完成”误判成“必须回滚”。


Layer 3：Pre-Submit


严格 gate


输出：


READY_FOR_SUBMIT

NEEDS_MORE_WORK


检查：


targeted tests

stricter changed-files checks

必要时 broader verification



8. 状态机应该怎么表达这个问题


我建议把你之前的 EDIT_ACCEPTED / EDIT_REJECTED 再细化成：


EDIT_REJECTED_HARD

EDIT_ACCEPTED_LOCAL

EDIT_INCOMPLETE_EXPECTED

EDIT_ACCEPTED_STAGE

EDIT_READY_FOR_SUBMIT


对应含义：


EDIT_REJECTED_HARD


当前 edit 本身坏了，必须修。


EDIT_ACCEPTED_LOCAL


当前 edit 局部健康，可以继续下一步。


EDIT_INCOMPLETE_EXPECTED


当前 edit 局部健康，但任务级验证显示还有预期中的未完成迁移。


EDIT_ACCEPTED_STAGE


当前这一小批改动已经阶段性闭合。


EDIT_READY_FOR_SUBMIT


所有必要验证通过。


这样就不会只有“通过/不通过”两个粗糙状态。



9. 一个很实用的判定标准


当 edit 后出现错误时，不要先问：

“是否有错误？”

先问两个问题：


问题 1


这个错误是否说明当前文件/局部状态已经不可继续？


如果是，就是 HARD_REJECT。


问题 2


这个错误是否只是说明跨文件迁移还没完成？


如果是，就是 SOFT_INCOMPLETE，允许继续下一步 edit。


这个区分比“每次 edit 后过不过 lint”重要得多。



10. 工程上怎么落地


如果你在 Claude Code / Pi / 自己的 agent 里实现，我会建议：


edit 后 hook 只做硬 gate


只拦：


syntax

parser

file corruption

obvious local blocker


end turn hook / orchestrator 做阶段判断


判断：


当前 changed-files 的错误是否可解释为未完成迁移

是否允许继续 edit

是否需要提醒 Claude “先完成剩余引用修改”


submit 前再严格 gate


要求：


changed-files strict clean

targeted tests pass



11. 最终回答你的两个问题


问题 1


局部编辑会不会有一定验证不通过的情况？


会，而且这是正常现象。
尤其是跨文件、跨调用链、类型迁移类改动，LLM 不一定能一次 multiedit 全改完。
所以不能把所有 edit 后的验证失败都当成“edit 错了”；要区分：


坏状态：必须立刻修

过渡态：允许继续完成剩余迁移



问题 2


编辑验证的周期颗粒度是每次编辑，还是 end turn 来一次？


最合理的是分层组合：


每次编辑后：做快速局部硬 gate，防止坏状态扩散

end turn / batch end：做阶段性判断，识别“合理未完成”

阶段结束 / submit 前：做严格验证


所以不是二选一，而是：

after-edit 用来防坏，end-turn 用来判断是否收敛。


如果你愿意，我下一条可以直接给你一版：


“支持中间态的状态机 JSON Schema 升级版”
也就是把 HARD_REJECT / SOFT_INCOMPLETE / ACCEPTED 这三类正式编码进去。
