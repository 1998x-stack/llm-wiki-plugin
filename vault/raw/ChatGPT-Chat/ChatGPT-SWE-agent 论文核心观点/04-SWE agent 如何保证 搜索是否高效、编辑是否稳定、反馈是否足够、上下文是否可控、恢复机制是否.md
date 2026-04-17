# SWE agent 如何保证 搜索是否高效、编辑是否稳定、反馈是否足够、上下文是否可控、恢复机制是否存在。

> Source: SWE-agent 论文核心观点
> Time: 2026/4/13 11:09:30

## Question

SWE agent 如何保证 搜索是否高效、编辑是否稳定、反馈是否足够、上下文是否可控、恢复机制是否存在。

如何设计环境反馈，保证specific concise？

设计了哪些tool/动作，保证simple and easy to understand for agents?

模型感知状态变化具体包含哪些模块，如何设计状态变化？

Guardrails 具体包含哪些，如何设计分析，进行深度思考，撰写所有的 Guardrails 设计，并且给出补充

## Answer

我先把论文正文和公开仓库里和 ACI / tools / guardrails 直接相关的部分对齐一下，再按你这 5 个问题逐条展开，尽量把“论文原文有的”和“我补充设计的”分层写清楚。

搜索SWE-agent论文和GitHub文档详细信息


SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering
SWE-agent工具系统全解析：从文件映射到代码审查的完整生态
SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering
Command line basics - SWE-agent documentation
sweagent · PyPI
SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering
File Editing Tools | scaleapi/SWE-agent | DeepWiki
GitHub - miaoow/ECHO-SWE-agent: SWE-agent takes a GitHub issue and ...
SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering
Imad Dabbura - SWE-agent: Agent-Computer Interfaces Enable Automated ...
SWE-agent: Agent-Computer Interfaces Enable Automated ...
[AI SWE-agent] 帮你解决Github中的bug和issue - 知乎


查找设计原则相关PDF和表格内容


proceedings.neurips.cc


查找设计原则和模式分析


proceedings.neurips.cc


查找设计原则 118-136 行内容


proceedings.neurips.cc


编辑和优化搜索策略及输出


proceedings.neurips.cc


查找上下文管理相关细节


proceedings.neurips.cc


搜索特定消息并截断输出


proceedings.neurips.cc


已思考 34s

下面我按你 5 个问题逐条拆。
我会分成两层：


第一层：论文里实际做了什么。
第二层：如果把它当成今天做 SWE agent 的设计原则，我会怎么补全。


先给一句总判断：

SWE-agent 的做法不是“把模型变聪明”，而是把失败高发的环节结构化：搜索做成总结式、编辑做成单步多行替换、反馈做成状态差异回显、上下文做成最近窗口、恢复做成错误即拦截。 论文里最强的不是某个单点技巧，而是这几个点连成闭环。NeurIPS Proceedings+4NeurIPS Proceedings+4NeurIPS Proceedings+4


1. SWE-agent 如何保证：搜索高效、编辑稳定、反馈足够、上下文可控、恢复机制存在


1.1 搜索是否高效：它不是“多搜”，而是“减少低效遍历”


论文明确比较了三种搜索接口：No search、Iterative search、Summarized search。结果是 Summarized search 最好（18.0），Iterative search 明显更差（12.0）。作者解释得很直接：迭代式搜索会诱导 agent 把搜索结果一个个翻完，容易耗尽成本预算和上下文窗口；总结式搜索则一次给出完整结果摘要，并在查询不够具体时给出 refinement guidance。也就是说，它保证“搜索高效”的方法不是给更多按钮，而是防止 agent 落入机械翻页式局部最优。NeurIPS Proceedings+1


这里的关键洞察是：
对人类来说，next/prev 看结果很自然；
但对 LM 来说，这种 UI 很容易变成“无脑枚举所有匹配项”。
所以 SWE-agent 不是把搜索设计成“看得更细”，而是设计成“让 agent 更快收缩搜索空间”。这是非常 agent-native 的想法。NeurIPS Proceedings+1


我把它抽象成一句话：
高效搜索 = 不是提高 recall，而是减少 agent 在无价值结果上的 turn 消耗。
这也是为什么 summarized search 比 iterative search 更符合论文的 ACI 原则：动作要 compact，反馈要 informative but concise。NeurIPS Proceedings+1


1.2 编辑是否稳定：它把“改文件”从多步 shell 流程压缩成一个受约束动作


SWE-agent 没有让模型靠 shell 去 sed、重定向、整文件重写来改代码，而是提供了一个专门的 edit 动作：指定起止行 + replacement_text，一次完成多行替换。论文强调这件事的本质是“compact, efficient file editing is critical to performance”，并且消融里 有 edit 但无 linting 为 15.0，带 linting 升到 18.0，而 No edit 降到 10.3。NeurIPS Proceedings+1


为什么这会让编辑更稳定？因为它同时解决了三类问题：


第一，动作原子化。
原本 shell 编辑需要多步组合，模型很容易中间某步做错；edit 把高频编辑压缩成一个动作。NeurIPS Proceedings+1


第二，编辑后立即看到结果。
编辑应用后，file viewer 会自动展示更新后的内容，agent 不用再发额外命令确认“刚才到底改没改进去”。NeurIPS Proceedings


第三，非法编辑直接丢弃。
如果 linting / syntax check 发现新错误，修改不会落盘，而是把错误和局部 before/after 片段反馈给 agent，再让它重试。这样坏状态不会污染后续轨迹。NeurIPS Proceedings+2NeurIPS Proceedings+2


所以它保证“编辑稳定”的核心不是更会改代码，而是：

先把编辑动作做小、做原子、做可验证，再谈模型会不会改对。 NeurIPS Proceedings+2NeurIPS Proceedings+2

1.3 反馈是否足够：足够不是“多给”，而是“刚好能驱动下一步动作”


论文一开始就写到，SWE-agent 给 agent 的是 specific, concise feedback about a command’s effects at every turn。具体做法包括：


编辑后自动显示更新后的文件内容

对无输出命令，明确返回 “Your command ran successfully and did not produce any output”

lint 失败时返回错误类型，以及错误前后的代码片段

file viewer 显示当前打开文件路径、总行数、窗口前后省略行数、可见行号 NeurIPS Proceedings+3NeurIPS Proceedings+3NeurIPS Proceedings+3


这套设计的共同点是：
每条反馈都在回答 agent 下一步最需要知道的那个问题。


比如 shell 里很多命令成功时没有输出。
对人类来说，这没问题；
对模型来说，这会产生歧义：是成功了、没权限、没生效、还是没命中？
所以 SWE-agent 特地把“无输出但成功”显式语言化。NeurIPS Proceedings


换句话说，论文里“反馈足够”的标准不是日志完整，而是：

是否足以让 agent 在下一步少猜一次。 NeurIPS Proceedings+1

1.4 上下文是否可控：它不是保存全部历史，而是只保留“最近有效工作记忆”


论文的消融结果很清楚：Last 5 Observations = 18.0，Full history = 15.0。系统实现上，早于最近 5 条的 observations 会被折叠成单行摘要；格式错误消息会在模型恢复正常后被去噪，除了第一条外其余都删掉。NeurIPS Proceedings+3NeurIPS Proceedings+3NeurIPS Proceedings+3


这说明 SWE-agent 对“上下文可控”的理解非常成熟：
上下文管理不是“留多少”，而是“留哪些状态对下一步还有决策价值”。论文明确说这样做是为了减少不必要上下文、避免展示过时文件信息，并支持更多交互轮次。NeurIPS Proceedings+1


这里有个很重要的隐含原则：


过去的搜索结果，经常已经失效

过去的打开窗口，经常已经不是当前工作面

过去的格式错误，多数只是噪声

最近几步的动作-反馈链，才是 agent 的真正工作记忆


所以它不是在做“完整日志系统”，而是在做“LM 的短时任务记忆系统”。NeurIPS Proceedings+1


1.5 恢复机制是否存在：存在，而且是“早恢复、局部恢复、自动恢复”


论文对 recovery 讲得其实很具体。
他们把 failed edit 定义为触发 linting error 的 edit，然后分析 agent 是否会在后续 edit 中恢复。结果是：在已解决轨迹里，出现过至少 1 次 failed edit 的情况并不少见，但 agent 在 135 次出现 1+ failed edit 的情形里成功恢复了 104 次。NeurIPS Proceedings


这说明恢复不是补充逻辑，而是主流程的一部分。
SWE-agent 的恢复机制主要有三层：


第一层，编辑失败不提交。
坏修改直接丢弃。NeurIPS Proceedings+1


第二层，失败原因回显。
返回 lint 错误类别和局部代码差异。NeurIPS Proceedings+1


第三层，格式错误重试 + 历史去噪。
模型输出不合 thought/action 格式时，系统给标准错误模板要求重试；若后续恢复，则把 malformed generation 相关历史移除，避免污染后文。连续 3 次 malformed response 则提前终止。NeurIPS Proceedings+1


所以它的恢复机制不是传统意义上的“rollback system”，而是：

在每个高风险动作点建立局部回退与重试机制，把长轨迹错误限制在局部。 NeurIPS Proceedings+2NeurIPS Proceedings+2


2. 如何设计环境反馈，保证 specific concise


我先给一个我认为最准确的抽象：

specific = 明确告诉 agent“这一步发生了什么变化”； concise = 只给能决定下一步动作的信息，不把原始环境噪声完整灌进去。

论文里这个原则写得很清楚：反馈应该提供关于当前环境状态和最近动作效果的“substantive information”，但不要带不必要细节。NeurIPS Proceedings


2.1 论文里已经落地的反馈设计


A. 命令结果要有“语义结论”


比如命令成功但没有 stdout 时，系统不会沉默，而是明确写：
“Your command ran successfully and did not produce any output.”
这就是 specific。因为它消除了“到底有没有生效”的歧义。NeurIPS Proceedings


B. 编辑反馈要回到“状态差异”


编辑后自动展示修改后的 file viewer；如果编辑非法，则展示 lint 错误以及 before/after snippet。
这就是 concise，因为它不是把整文件再 dump 一遍，而是只把 agent 最需要核对的局部状态返回。NeurIPS Proceedings+1


C. 搜索反馈要回到“候选空间”


总结式搜索不让 agent 一条一条翻，而是一次给出匹配概览，并对 query 过泛时给 refinement guidance。
这就是 concise，因为它把“海量搜索结果”压缩成“接下来该往哪个文件/关键词收缩”。NeurIPS Proceedings+1


D. 文件查看反馈要稳定暴露定位坐标


路径、总行数、当前窗口范围、前后省略量、行号，这些都是状态坐标。
specific 的关键并不是显示更多代码，而是让 agent 知道“我现在看的是哪一块”。NeurIPS Proceedings


2.2 我补充的反馈设计方法论


如果今天让我做一个 SWE-agent 级别的反馈系统，我会要求每条 observation 都满足四个字段：


1）Outcome：动作是否成功
2）Delta：如果成功，状态变化了什么
3）Anchor：变化发生在什么对象/范围
4）Next-step hint：如果失败，建议下一步缩小到什么重试空间


例如不要返回：

command finished

而要返回：

edit rejected: Python syntax error E999 at lines 1058-1059 in sympy/parsing/mathematica.py. Your changes were not applied. See original and proposed snippets below.

这种写法的好处是，agent 下一步几乎天然会继续 edit，而不是跑偏去做别的事。这个模板化设计是我基于论文原则做的扩展，不是论文原文直接给出的字段结构。论文支持“specific, concise”和“show error + snippet + reject invalid edits”这部分基础。NeurIPS Proceedings+1


2.3 一个判断标准


判断一条环境反馈是否合格，可以问两个问题：


第一，agent 看完能不能少发一个确认命令？
第二，agent 看完会不会知道下一个动作类型是什么？


如果答案都是“不能”，那这条反馈大概率不够 specific；
如果答案是“可以，但用了半页日志”，那这条反馈大概率不够 concise。
这是我对论文原则的工程化改写。NeurIPS Proceedings+1



3. 设计了哪些 tool / 动作，保证 simple and easy to understand for agents


论文和附录列得比较明确。SWE-agent 在普通 bash 之外，提供了几类专门动作：


文件查看


open <path> [<line_number>]

goto <line_number>

scroll_down

scroll_up


搜索工具


search_file <search_term> [<file>]

search_dir <search_term> [<dir>]

find_file <file_name> [<dir>]


文件编辑


edit <n>:<m> <replacement_text> end_of_edit


另外在轨迹分析里还会看到 create、python、pytest、submit 等动作。论文把 Localization / Editing / Testing 作为关键子任务，其中 Testing 对应写脚本或改测试来复现和验证问题。NeurIPS Proceedings+2NeurIPS Proceedings+2


3.1 为什么这些动作算 simple


因为它们都满足三个条件：


A. 单一职责明确


find_file 找文件名，search_dir 找目录内内容匹配，search_file 做文件内搜索，open/goto/scroll 做窗口导航，edit 做局部替换。
每个动作的语义边界都很清楚。NeurIPS Proceedings


B. 参数很少


论文明确说，simple commands with a few options and concise documentation are easier for agents to use。SWE-agent 的动作基本都只带 1-2 个核心参数，远比 bash 那种几十个 flags 的命令族更适合模型。NeurIPS Proceedings+1


C. 和返回格式互相补


论文附录特别强调 file viewer 里的命令是“complementary and grounded in the File Viewer standard output”。也就是说，open 输出的窗口信息能直接服务于 goto / scroll / edit。这减少了 agent 在动作之间做额外心智转换。NeurIPS Proceedings


3.2 为什么它们也算 compact and efficient


论文的第二条设计原则就是动作要 compact and efficient。
所以 SWE-agent 不是只追求“简单”，而是追求“简单但能完成更高阶操作”。最典型的就是 edit：单个动作就能完成多行替换，而不用模型先定位、复制、重写整文件、再验证。NeurIPS Proceedings+2NeurIPS Proceedings+2


3.3 我补充：什么动作不该设计进去


如果沿着这篇论文的原则往前推，我会说下面三类动作不应该成为主动作：


第一类，语义过泛的万能动作，比如让 agent 直接写任意 shell pipeline。
第二类，参数自由度太高的动作，比如一个命令兼容几十种 flags。
第三类，执行成功与失败差异不明显的动作，因为它们会制造 observation 歧义。


bash 不是不能开放，而是不应该成为主路径。SWE-agent 也是 built atop Linux shell，但把主要软件工程操作收敛到了更窄的 LM-friendly 工具集上。NeurIPS Proceedings+1



4. 模型感知状态变化具体包含哪些模块，如何设计状态变化


论文有一句很关键：
一个好的 ACI 应该帮助 agent understand the state of the application given previous changes，并把 commands 与 environment state communication 一起设计。NeurIPS Proceedings


我把它拆成 4 个状态模块。


4.1 文件状态


这是最核心的一层。
SWE-agent 通过 file viewer 让模型始终知道：


当前打开的是哪个文件

文件总共有多少行

当前窗口显示哪一段

每一行的行号是多少

前后还有多少内容被省略 NeurIPS Proceedings


编辑后它又自动显示更新后的窗口。
这意味着模型感知的不是“代码文本本身”，而是“代码文本 + 坐标系 + 刚刚发生的变更”。NeurIPS Proceedings


4.2 搜索状态


搜索不只是返回匹配项，而是帮助模型理解：


当前 query 是否足够具体

候选文件集合是否已收缩

当前下一步应该 open 哪个文件或 refine 哪个关键词 NeurIPS Proceedings+1


也就是说，搜索反馈其实是在维护一个“问题定位状态”。
这对 localization 很重要。论文附录也明确把 localization 分成 file-level 和 line-level 两层。NeurIPS Proceedings


4.3 执行状态


执行状态主要来自 python / pytest / shell 命令的 observation。
论文虽然没把这一块展开成最复杂的状态机，但至少做了两件事：


对有输出的命令按统一模板显示

对无输出但成功的命令给显式成功语句 NeurIPS Proceedings+1


这让模型知道“命令结果是空”与“命令无效/异常”不是一回事。


4.4 交互协议状态


这层很容易被忽略，其实也很关键。
SWE-agent 要求每步输出 thought + action；若格式错误，就返回固定的 format error message；恢复后会把 malformed 相关历史去噪。也就是说，系统不只维护“仓库状态”，还维护“交互是否仍在有效协议内”。NeurIPS Proceedings+1


4.5 如何设计状态变化


我会把 SWE-agent 的状态变化设计总结成一句话：

每个动作都必须返回“对象状态的最小充分差异”，而不是原样转储整个环境。

更具体地说：


open 改变当前 file window 状态

scroll/goto 改变当前 file viewport 状态

search_* 改变候选定位状态

edit 改变文件内容状态

pytest/python 改变验证状态

format_error 改变协议状态


好的 agent 环境不是“命令执行器”，而是“显式状态转移系统”。
这部分表述是我对论文的抽象，但它和论文把 ACI 定义成 commands + state communication 是一致的。NeurIPS Proceedings+2NeurIPS Proceedings+2



5. Guardrails 具体包含哪些，如何设计分析，并给出完整 Guardrails 设计与补充


这是你问得最值的一部分。
因为 Guardrails 才是 SWE-agent 从“可跑”走向“可恢复”的关键。


先说论文里明确存在的 guardrails，再给我认为应该补充的完整设计。



5.1 论文里明确存在的 Guardrails


Guardrail 1：编辑语法检查 / linting gate


这是论文最明确、最重要的 guardrail。
Python 文件 edit 后会做 syntax check；若发现错误，edit 不会被应用，系统会返回 lint 错误，以及错误前后的文件片段，然后要求 agent 重试。论文的编辑消融表明：w/ linting = 18.0，edit w/o linting = 15.0。NeurIPS Proceedings+3NeurIPS Proceedings+3NeurIPS Proceedings+3


这类 guardrail 的本质是：


把错误从“晚一点才爆炸”变成“立刻暴露”

把错误从“全局污染”变成“局部拒绝提交”

把错误从“silent corruption”变成“可解释 observation”


这是 SWE-agent guardrails 的核心。NeurIPS Proceedings+2NeurIPS Proceedings+2


Guardrail 2：格式约束 + 格式错误重试


每一轮必须输出 thought/action 的约定格式。
若模型输出 malformed response，环境会发固定错误模板，要求重试；连续 3 次 malformed response 则提前终止。恢复成功后，还会把 malformed 相关历史移除，减少未来污染。NeurIPS Proceedings+1


这类 guardrail 保护的是交互层而不是代码层。
没有它，轨迹可能在“会改代码”之前就先死于“不会按协议说话”。


Guardrail 3：无输出命令的显式成功说明


这看起来不像 guardrail，但我认为它本质上就是。
因为 shell 的 silent success 很容易诱导 agent 重复确认或错误归因。系统专门把它变成显式 observation，实际是在防止 interpretation error。NeurIPS Proceedings


Guardrail 4：历史去噪


过去错误消息只保留第一条，旧 observation 折叠成单行摘要，恢复后删除 malformed generation 对应历史。
这也是 guardrail，因为它防止的是 错误上下文累积污染。NeurIPS Proceedings+2NeurIPS Proceedings+2



5.2 论文里隐含但很重要的 Guardrail 思路


论文虽然没有把它们都命名成 guardrail，但从 ACI 设计看，下面这些其实都在发挥 guardrail 作用。


A. 小动作空间本身就是 guardrail


动作越少、语义越窄，模型出错面越小。
这是一种“通过 interface restriction 降低错误率”的 guardrail。NeurIPS Proceedings+1


B. 100-line viewer 是上下文 guardrail


不是越多越好，而是把模型看到的窗口限制在局部最有用范围。Full file 反而更差。NeurIPS Proceedings+1


C. Summarized search 是探索 guardrail


它限制 agent 不要在 next/prev 结果里机械穷举。NeurIPS Proceedings+1



5.3 我会如何系统化设计一套“完整 Guardrails”


如果今天让我基于 SWE-agent 思想写一套完整的 guardrail 体系，我会分成 6 层。


第一层：Protocol Guardrails（协议护栏）


保护 agent 不要偏离交互协议。


包括：


单回合必须只有一个 thought/action 对

command schema 校验

参数类型校验

非法输出重试

连续多次非法输出终止

恢复后对 malformed history 去噪


这是论文已有实现最接近完整的一层。NeurIPS Proceedings+1


第二层：Action Guardrails（动作护栏）


保护单个动作不要把环境推入不可解释状态。


包括：


edit 只允许改打开文件中的显式行段

open/goto/scroll 必须作用于有效范围

search_* 限制返回格式和最大结果量

命令无输出时必须返回显式 success marker


论文已实现其中大部分方向，但并未完整枚举成一套体系。edit、viewer、search 的窄接口都属于这里。NeurIPS Proceedings+2NeurIPS Proceedings+2


第三层：State Guardrails（状态护栏）


保护 agent 始终能解释“现在是什么状态”。


包括：


当前打开文件、当前窗口、当前目录显式回显

编辑后自动回显变更区域

搜索后显式回显匹配概览与 refine 建议

测试后回显失败/通过摘要，而不是整页日志


论文对 file viewer、edit feedback、search summary 已经做了大半。NeurIPS Proceedings+2NeurIPS Proceedings+2


第四层：Semantic Guardrails（语义护栏）


保护“代码没有写坏”，不是只保护“格式合法”。


论文目前主要做到 syntax / lint 这一层。它自己也承认未来可加入 static analysis、fault localization、test generation、web browsing 等更强工具。若扩展成更完整语义 guardrails，可以包括：


type checker

import resolution / build validation

unit-test subset rerun

changed-function smoke tests

static analyzer warnings

diff risk scoring


这部分是我的补充设计，论文只明确提出过“可以加入 static analysis 等工具”的未来方向。



Sources:
