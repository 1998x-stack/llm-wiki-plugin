# SWE-agent 论文的所有核心概念 展开详细分析 一个一个

> Source: SWE-agent 论文核心观点
> Time: 2026/4/13 11:00:53

## Question

SWE-agent 论文的所有核心概念 展开详细分析 一个一个

## Answer

我会按“概念词条”的方式拆开：先把论文里真正重要的概念列全，再逐个讲定义、它为什么重要、论文怎么用它、它的边界是什么。

搜索SWE-agent相关文献与资源


SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering
SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering
GitHub - SWE-agent/SWE-agent: SWE-agent takes a GitHub issue and tries ...
SWE-agent: Agent-Computer Interfaces Enable Automated ...
Agent tools - SWE-agent documentation
SWE-agent：让AI自主完成软件工程任务的突破性进展
Downloads 2024 - NeurIPS


分析PDF并截取关键部分截图


proceedings.neurips.cc


考虑设计方法论和表格结构


我需要考虑包括设计方法论和表格的部分，可能的关键概念包括本地化、上下文管理等。也许可以从第三部分开始，专注于设计原则。这个方向有很多值得思考的内容，需要进一步明确每一部分的框架和重点。


寻找设计方法论和关键概念


proceedings.neurips.cc


考虑截取关键数据页面内容


我在想，也许需要截取第0到第5页中关键数据的截图，以便更好地展示重点或支撑分析。这样一来，把重要数据集中展示应该能帮助理清思路，进一步确保关键内容清晰可见。


寻找关键图表截图（页面0-5）

下面我按 “核心概念词条” 来拆这篇 SWE-agent 论文。不是泛泛总结，而是把论文里的关键概念一个一个展开：
它是什么、为什么重要、论文里怎么定义/怎么实现、实验怎么支持、它的边界在哪里。
我会尽量把“论文原意”和“我的分析”分开。(arxiv.org , NeurIPS Proceedings+1)



1. Language Model Agent


1.1 概念是什么


论文先把 LM agent 定义成：一个语言模型在环境中反复采取动作并接收反馈的系统。这点很关键，因为它把模型从“回答问题的文本系统”变成了“在环境中行动的决策体”。论文在第 2 节直接说，LM acts as an agent when it iteratively takes actions and receives feedback。NeurIPS Proceedings


1.2 为什么重要


这一定义决定了整篇论文的视角：
SWE-agent 不是在研究“代码生成”，而是在研究“模型如何在软件工程环境里完成任务”。这就意味着，重点不再只是 prompt 和代码 token 预测，而是 动作空间、反馈格式、状态表示、错误恢复。NeurIPS Proceedings+1


1.3 我的理解


这是论文最底层的范式转换。只要你接受“LM 是 agent”，后面 ACI、guardrails、context management 这些概念才成立。否则你会一直把 SWE-agent 误解成“一个会自动改代码的 prompt workflow”。这不是论文的真正主张。这个判断是我基于论文整体结构做的归纳。NeurIPS Proceedings+1



2. Agent-Computer Interface（ACI）


2.1 概念是什么


ACI 是这篇论文最核心的概念。论文把它定义成：LM agent 与计算机交互时所使用的接口，包括两部分：
一部分是 agent 可以调用的命令/动作，另一部分是 环境把状态和反馈返回给 agent 的方式。论文明确写到，ACI specifies both the commands available to the LM and how the environment state is communicated back to the LM。NeurIPS Proceedings


2.2 为什么重要


论文的核心观点是：对 agent 来说，接口不是附属品，而是能力的一部分。
人类写代码会借助 IDE、terminal、search、lint、test runner；同样，LM agent 也需要一个专门为它设计的工作界面。论文甚至把 LM agent 当成“a new category of end user”，意思是：模型是一类新的“计算机使用者”，因此不该直接复用为人类设计的 UI。NeurIPS Proceedings+1


2.3 论文真正想证明什么


论文真正要证明的不是“我们做了一个 agent”，而是：
只要接口设计得更贴合 LM 的特点，agent 性能就会显著提高，即使不改模型权重。 第 1 页和第 2 页都明确在强调这一点。NeurIPS Proceedings+2NeurIPS Proceedings+2


2.4 我的理解


ACI 是这篇论文最“可迁移”的概念。
SWE-agent 作为系统会过时，具体命令集也会演化，但 “agent performance depends on interface design” 这个命题不会轻易过时。以后不只是软件工程，浏览器 agent、数据分析 agent、研究 agent 都会沿着这个逻辑走。这个扩展是我的推论，但和论文讨论“ACI principles may transfer to other domains”一致。NeurIPS Proceedings+1



3. 软件工程是“交互式任务”，不是“静态生成任务”


3.1 概念是什么


论文默认把软件工程任务看成一种 iterative interaction problem：
读 issue、找文件、读代码、修改、跑测试、看失败、再修改。论文在摘要和引言里都强调，SWE-agent 的能力体现在 create/edit code files, navigate repositories, execute tests and programs。NeurIPS Proceedings+1


3.2 为什么重要


如果你把软件工程当成“读题直接输出 patch”，你自然会关注 patch quality；
但如果你把它当成“交互式任务”，你就要关注：
搜索是否高效、编辑是否稳定、反馈是否足够、上下文是否可控、恢复机制是否存在。
这就是整篇论文的问题重定义。NeurIPS Proceedings+1


3.3 我的理解


这篇论文的很多创新其实都建立在这个前提上。
换句话说，SWE-agent 不是说“生成更好的代码”，而是说“让模型在代码环境里更像一个操作者”。这是它和很多纯 patch-generation 工作最本质的区别。NeurIPS Proceedings+1



4. ACI 的设计原则（Design Principles）


论文第 2 节非常重要，因为它不是只给系统结果，还总结了一组 ACI 设计原则。这些原则才是论文最有方法论价值的部分。NeurIPS Proceedings


4.1 原则一：动作要简单、容易理解


论文说，动作应该 simple and easy to understand for agents。很多 bash 命令太灵活、太开放、语义负担太重，对 LM 不友好。相反，少量、清晰、功能边界明确的动作更好。NeurIPS Proceedings+1


分析：
这背后的逻辑是，语言模型对“语义上明确的工具”更容易形成稳定使用模式，而对一个几乎无限制的 shell，容易出现动作选择混乱、命令格式错误、探索成本过高的问题。论文后面的 shell-only 对比就是这个观点的实验化支撑。NeurIPS Proceedings+1


4.2 原则二：反馈要简洁、信息密度高


论文强调，环境反馈要 specific, concise。模型不像人一样能轻松忽略大量无关信息；对 LM 来说，所有上下文都有 token 成本和干扰成本。论文明确说 humans can ignore irrelevant information, whereas all content has fixed cost for LMs。NeurIPS Proceedings+1


分析：
这说明 ACI 的反馈设计本质上是“压缩状态表示”。你不是把环境原样倒给模型，而是要把它加工成 足够行动、又不至于淹没上下文窗口 的观察。这个点对今天所有 agent 仍然成立。NeurIPS Proceedings+1


4.3 原则三：要帮助模型感知状态变化


论文说，一个好的 ACI 应该帮助 agent 理解应用的当前状态、此前改动的后果，以及最近动作的结果。编辑后给出更新后的文件片段，就是这种“状态可见性”的例子。NeurIPS Proceedings+1


分析：
本质上，这是把软件工程从“token continuation”变成“stateful control”。如果 agent 看不到自己的操作后果，它就无法形成闭环。NeurIPS Proceedings


4.4 原则四：要有 Guardrails


论文明确提出，guardrails 可以减少错误传播、加速恢复，例如在编辑动作中加入 syntax checker。NeurIPS Proceedings+1


分析：
这不是锦上添花，而是 agent 系统稳定性的核心。因为 LM 很容易在早期引入小错误，然后整条轨迹被污染；guardrail 的作用就是在“错误刚出现时”把它截断。这个思路后来影响了很多 agent 系统。NeurIPS Proceedings+1



5. Shell-only Baseline


5.1 概念是什么


论文专门拿了一个 Shell-only agent 做基线，也就是让模型更直接地面对 Linux shell 这类传统工具，而不提供专门设计的 LM-friendly ACI。NeurIPS Proceedings+1


5.2 为什么重要


这个基线的作用，是证明“不是因为你用了交互就强，而是因为你用了更合适的交互接口才强”。
如果没有 shell-only baseline，论文很难证明 ACI 的增益来自界面设计本身。NeurIPS Proceedings


5.3 论文结论


在 SWE-bench Lite 上，shell-only agent 的 resolved rate 明显低于 SWE-agent；论文摘要和引言里还提到，SWE-agent 比默认 Linux shell baseline 高出 10.7 个百分点。NeurIPS Proceedings+1


5.4 我的理解


这组对比非常关键，因为它直接支撑了论文最核心的论断：
为人设计的 UI，不一定适合 LM；LM 需要自己的 interface abstraction。
这几乎是整篇论文最重要的因果链。NeurIPS Proceedings+1



6. LM-friendly Commands


6.1 概念是什么


论文强调，SWE-agent 的 ACI 提供的是一小组 LM-friendly commands，用来完成仓库浏览、文件查看、搜索、编辑等高频动作，而不是把模型扔进一个高度可配置、动作空间几乎无限的 shell。NeurIPS Proceedings+1


6.2 为什么重要


命令本身就是 动作空间设计。
动作空间过大，模型容易迷航；动作空间过小，模型又做不成事。SWE-agent 的贡献之一，就是在软件工程任务上找到一个“小而有效”的动作集合。论文还说 final configuration has a small toolkit, albeit highly effective。NeurIPS Proceedings


6.3 我的理解


这是 reinforcement learning / planning 视角里很经典的问题：
能力上限不只取决于 policy，本身也取决于 action space 的设计。
SWE-agent 把这个问题落到了软件工程 agent 上。NeurIPS Proceedings



7. Search / Navigation


7.1 概念是什么


论文把 search/navigation 视为 ACI 的核心组件之一。agent 要想修复 issue，首先得能在 repo 里定位相关文件、相关类、相关行。论文后文把这类子任务称为 Localization。NeurIPS Proceedings+1


7.2 为什么重要


真实软件工程最难的往往不是“最后改那几行代码”，而是先 找到该改哪里。
因此，仓库级搜索能力实际上决定了 agent 是否能把问题缩到可操作范围。NeurIPS Proceedings+1


7.3 论文里的发现


Table 3 显示，不同搜索接口差异明显：
Summarized search 的效果比 Iterative search 更好，而 No search 虽然不是最差，但也不如总结式搜索。论文解释说，iterative search 让 agent 容易把每个结果都看一遍，导致成本和上下文被耗尽。NeurIPS Proceedings


7.4 我的理解


这说明“搜索能力”不是简单加个 grep 就行，关键在 结果呈现方式。
同样是搜，给模型一个“每次一个结果、一直 next”的浏览器式界面，可能反而诱导它陷入机械遍历；而把结果总结压缩后返回，更符合 LM 的使用方式。这个发现非常有启发性。NeurIPS Proceedings+1



8. Localization


8.1 概念是什么


论文把软件工程中的一个关键子任务称为 Localization，包括两层：
一层是 file-level localization，找到相关文件；
一层是 line-level localization，找到更精确的修改位置。论文附录里对行为模式分析时，多次把动作序列标注为 “Localization (File)” 和 “Localization (Line)”。NeurIPS Proceedings


8.2 为什么重要


Localization 是整个软件工程 agent 的第一道门槛。
找不到正确位置，再强的编辑能力也没有意义；找错位置，后续动作都会建立在错误假设上。NeurIPS Proceedings+1


8.3 我的理解


这篇论文虽然没把 localization 当成唯一主题，但它实际上在告诉我们：
SWE agent 的本质瓶颈之一，是 “从 issue 文本到代码位置”的映射能力。
因此，后续很多工作才会更关注 repository maps、symbol index、static analysis、call graph 等能力。这个延伸是我的推论，但与论文在 limitations 中提到可加入 static analysis 等工具一致。NeurIPS Proceedings



9. File Viewer


9.1 概念是什么


File viewer 是 ACI 的另一个核心组件。它决定 agent 如何查看文件内容，尤其是一次给多少行、是否支持滚动、如何定位。NeurIPS Proceedings+1


9.2 为什么重要


给太少，agent 看不全上下文；
给太多，token 浪费且噪声增加。
所以文件查看不是简单“cat 一下文件”，而是一个典型的 interface design 问题。NeurIPS Proceedings+1


9.3 论文结果


在 SWE-bench Lite 的 ablation 里，100 lines 的 viewer 表现最好，优于 30 lines，也优于直接给 full file。NeurIPS Proceedings


9.4 我的理解


这个结果特别说明，LM 不一定“上下文越多越好”。
全文件虽然信息最全，但对模型来说并不等于最可用；一个适中的窗口往往更利于局部推理和状态跟踪。这个现象和很多长上下文工作中的结论一致，但这里是在软件工程交互场景里被具体验证了。NeurIPS Proceedings+1



10. File Editor / Edit Action


10.1 概念是什么


论文把 file editor 设计成 ACI 的核心，因为实际修 bug 必须有稳定编辑能力。SWE-agent 不是让模型随意用 shell 改文件，而是提供更紧凑的编辑命令，并在编辑后同步更新 agent 对文件状态的认知。NeurIPS Proceedings+1


10.2 为什么重要


编辑动作如果笨重、脆弱、难以验证，agent 很容易在执行阶段而不是推理阶段失败。
论文甚至在第 6 页直接写：“Compact, efficient file editing is critical to performance.” NeurIPS Proceedings


10.3 论文结果


Table 3 中，带有专门 edit action 的设置优于 No edit；而 edit action + linting 又优于只有 edit action。NeurIPS Proceedings


10.4 我的理解


这说明工程 agent 的失败，很多时候不是“不会想”，而是“不会稳地做”。
换句话说，执行层的微小不稳定，会吞掉推理层的收益。这对今天做 coding agent 产品仍然极其现实。NeurIPS Proceedings+1



11. Linting


11.1 概念是什么


论文在 edit function 里集成了 code linter。当模型编辑后引入语法错误时，系统会把相关错误反馈给 agent，并丢弃无效编辑，让它重新尝试。NeurIPS Proceedings


11.2 为什么重要


Linting 是一种典型的 局部验证器。
它不负责判断问题是否最终修好，但它能快速判断“这次编辑是不是把代码直接写坏了”。这种局部验证非常适合 agent 场景。NeurIPS Proceedings+1


11.3 论文证据


带 linting 的编辑设置效果优于不带 linting 的 edit action。NeurIPS Proceedings


11.4 我的理解


linting 在这里不是“辅助功能”，而是一种 低成本、高收益的即时纠错机制。
它本质上是在 agent loop 里插入一个 cheap critic。以后你也可以把单元测试、类型检查、静态分析都视为这种 critic 的扩展。后半句是我的延伸，但和论文 limitations 里讨论加入 static analysis 等工具一致。NeurIPS Proceedings+1



12. Context Management


12.1 概念是什么


论文把 context management 单独作为 ACI 组件。它不只是“保存历史”，而是决定：
哪些历史要保留、哪些要删、错误格式怎么处理、哪些 observation 更值得进入 prompt。NeurIPS Proceedings


12.2 为什么重要


LM 不是外部记忆无限的系统。每条历史都占用上下文预算，而且错误、冗余、过时信息会污染后续决策。因此，context management 本质上是 agent 的“工作记忆管理”。NeurIPS Proceedings+1


12.3 论文结果


在 Table 3 中，Last 5 observations 的效果优于 Full history。另外，去掉 demonstration 后也会略有下降。NeurIPS Proceedings


12.4 我的理解


这是一个很强的信号：
不是历史越多越好，而是最近、相关、结构化的历史更好。
这和人类工作记忆很像：解决当前 bug，最有用的是最近几步的操作与反馈，而不是完整人生回放。NeurIPS Proceedings+1



13. Demonstration


13.1 概念是什么


论文给 agent 提供了一个 demonstration，也就是演示轨迹，用来展示如何正确使用接口。论文附录给出了示例模板，说明它是为了让模型学会 ACI 的正确用法，而不是照抄任务内容。NeurIPS Proceedings+1


13.2 为什么重要


这其实不是传统意义上的 few-shot “给答案”，而更像是 教模型怎么操作工具。
也就是：重点不在 domain knowledge，而在 interaction protocol learning。NeurIPS Proceedings


13.3 论文结论


去掉 demonstration 后，性能会小幅下降，说明它有帮助，但不是决定性因素。NeurIPS Proceedings


13.4 我的理解


demonstration 在这篇论文里更像“接口 onboarding”。
这说明 agent 系统里 few-shot 的价值，很多时候不是“提供更强知识”，而是“提供更稳的行为模板”。NeurIPS Proceedings+1



14. ReAct-style Loop


14.1 概念是什么


论文明确说，SWE-agent 每一步都会生成一个 thought 和一个 command，然后再接收命令执行结果。这就是典型的 ReAct 结构。NeurIPS Proceedings


14.2 为什么重要


这让 agent 的推理与行动形成显式耦合：
不是先想完一切再一次输出，而是 想一点、做一点、看反馈、再想一点。
对于软件工程这种高反馈密度任务，这种循环天然更合适。NeurIPS Proceedings+1


14.3 我的理解


ReAct 在这篇论文里不是创新点本身，但它是 ACI 能发挥作用的运行框架。
没有这个循环，ACI 就只是静态工具集；有了这个循环，ACI 才变成动态工作环境。NeurIPS Proceedings



15. Environment Feedback


15.1 概念是什么


论文一直强调 LM-friendly environment feedback。环境不只是执行命令，还会把结果以更适合 LM 消化的格式反馈回来。图 1 就把 ACI 分成了 “LM-friendly commands” 和 “LM-friendly environment feedback” 两块。NeurIPS Proceedings


15.2 为什么重要


动作只是半个接口；另一半是观察。
一个 agent 是否能有效迭代，取决于它看到的是“原始噪声”还是“加工过的任务相关反馈”。NeurIPS Proceedings+1


15.3 我的理解


很多 agent 系统只重视 tool calling，不重视 observation design。
SWE-agent 很可贵的一点，是它把 反馈格式 提升到和 动作设计 同等重要的位置。这个思路非常值得记。NeurIPS Proceedings+1



16. Guardrails


16.1 概念是什么


Guardrails 是论文提出的重要设计原则之一，用于减少 error propagation。除了 linting 以外，guardrails 还体现在错误命令、格式不合法、编辑失败时的恢复逻辑上。NeurIPS Proceedings+1


16.2 为什么重要


agent 最大的问题之一不是犯错，而是 犯错后继续在错的状态上推进。
Guardrails 的作用是把错误显式化、局部化、可恢复化。NeurIPS Proceedings


16.3 我的理解


如果说 ACI 是 agent 的“工作台”，那么 guardrails 就是“工作台上的护栏”。
它不是为了让 agent 更聪明，而是为了让 agent 没那么容易把自己搞崩。这在长轨迹任务里尤为重要。NeurIPS Proceedings+1



17. SWE-bench


17.1 概念是什么


SWE-bench 是论文的核心评测集，目标是评估系统是否能解决真实仓库中的 issue。论文在 full test set 上报告 GPT-4 Turbo 版 SWE-agent 解决了 12.47% 任务。NeurIPS Proceedings+1


17.2 为什么重要


SWE-bench 和普通 code generation benchmark 不同，它更接近真实软件工程任务，因为它要求在仓库上下文中定位、修改并通过测试。NeurIPS Proceedings


17.3 我的理解


这也是为什么这篇论文影响力大。
它不是在 HumanEval 这种相对“封闭”的任务里刷分，而是在更接近真实工程的 benchmark 上证明交互式 agent 的价值。NeurIPS Proceedings+1



18. HumanEvalFix


18.1 概念是什么


HumanEvalFix 是另一个评测集，用于衡量修复任务能力。论文在这个 benchmark 上报告了 87.7% 的 pass@1。NeurIPS Proceedings+1


18.2 为什么重要


它让论文不仅在 repo-level 软件工程任务上有结果，也在更经典的程序修复任务上展示出强表现。NeurIPS Proceedings


18.3 我的理解


HumanEvalFix 更像“补充证明”：
证明 SWE-agent 的交互式设计并不只在 SWE-bench 这种超复杂场景有效，在程序修复上也有竞争力。只是从论文思想上说，SWE-bench 才是更关键的舞台。NeurIPS Proceedings+1



19. Pass@1 / % Resolved


19.1 概念是什么


论文用了两类关键指标：
在 HumanEvalFix 用 pass@1；
在 SWE-bench 用 % Resolved。NeurIPS Proceedings


19.2 为什么重要


这两个指标分别对应两种任务设定：
一个更像单题修复是否一次成功，另一个更像真实 issue 是否被完整解决。NeurIPS Proceedings+1


19.3 我的理解


论文其实想说的是：
SWE-agent 不只是“会生成像样的 patch”，而是“更有机会把真实任务走到完成态”。
所以 % Resolved 比单纯 patch similarity 更符合它的价值主张。NeurIPS Proceedings



20. Ablation Study


20.1 概念是什么


论文做了比较细的 ablation，把 ACI 拆成搜索、编辑、viewer、context 等模块分别对比。NeurIPS Proceedings


20.2 为什么重要


没有 ablation，这篇论文就更像一个系统报告；
有了 ablation，它才真正证明“性能增益来自哪些界面设计选择”。NeurIPS Proceedings+1


20.3 论文给出的重要信号


几个最关键的结论是：
总结式搜索优于迭代式搜索；
100-line viewer 优于太小或全文件；
edit + linting 优于无 linting；
最近 5 条 observation 优于 full history。NeurIPS Proceedings


20.4 我的理解


这组消融的价值在于，它把 agent 设计从“玄学调 prompt”变成了“可以分部件优化的 interface engineering”。这件事很重要。NeurIPS Proceedings+1



21. Portability Across Models


21.1 概念是什么


论文不只在 GPT-4 Turbo 上做，还在 Claude 3 Opus 上展示了 ACI 的可迁移性；Claude 版在 SWE-bench 上也能解决 10.46% 的任务。NeurIPS Proceedings+1


21.2 为什么重要


这说明论文想证明的不是“某个模型恰好很强”，而是“ACI 作为系统层设计，本身具有跨模型价值”。NeurIPS Proceedings


21.3 我的理解


这让 ACI 更像一个“中间层创新”，而不是单模型特调。
从产品视角看，这种东西通常比单一 prompt 更值钱，因为它更可复用。NeurIPS Proceedings



22. Cost / Efficiency


22.1 概念是什么


论文在主结果表里也报告了平均成本。不同系统不仅效果不同，成本也不同。NeurIPS Proceedings


22.2 为什么重要


agent 系统不是只比准确率，还要比交互成本。
尤其搜索方式和历史管理会直接影响 token 消耗与轨迹长度。NeurIPS Proceedings


22.3 我的理解


这说明 ACI 设计不只是“提升成功率”，也是“控制无效探索”。
总结式搜索比迭代式搜索好的一个隐含原因，就是它更不容易把轨迹拖长。这个解释与论文文本一致，但这里是我做的因果强调。NeurIPS Proceedings



23. Open Source / Reproducibility


23.1 概念是什么


论文强调他们把交互流程、命令实现、接口设计、上下文逻辑、轨迹与评测工件都开源了。NeurIPS Proceedings+1


23.2 为什么重要


因为这篇论文的核心价值在“系统设计”，而系统设计如果不开源，很难被真正复现和迭代。NeurIPS Proceedings


23.3 我的理解


SWE-agent 之所以后来影响大，不只是论文写得好，也因为它把“ACI 作为可实验对象”公开出来了。这样后续工作才能在它上面继续迭代。NeurIPS Proceedings+1



24. Limitations


24.1 论文自己承认的限制


论文在附录里明确说，当前 toolkit 仍然小，未来还可以加入 web browsing、static analysis、fault localization、test generation 等工具；同时 ACI 设计过程目前仍以人工观察和手工迭代为主。NeurIPS Proceedings


24.2 为什么重要


这说明作者并没有声称“问题已解决”，而是在说：
我们证明了 ACI 这条路线重要，但远没走完。 NeurIPS Proceedings


24.3 我的理解


这篇论文最正确的阅读方式不是“它做出了终局系统”，而是“它确定了一个正确研究对象”。
终局系统可能会不断变，但 ACI / interaction design 会一直是核心议题。NeurIPS Proceedings+1



最后一层总结：这篇论文所有核心概念之间的关系


如果把整篇论文的概念关系压成一条链，就是：


LM Agent
→ 不是静态文本生成器，而是在环境中行动的 agent
→ 因此需要 ACI
→ ACI 包括 动作设计 + 反馈设计 + 上下文管理 + 护栏机制
→ 在软件工程里，这些能力具体表现为 搜索/定位、查看文件、编辑文件、运行测试、恢复错误
→ 好的 ACI 能显著提升 % Resolved / pass@1
→ 所以软件工程 agent 的竞争，本质上是 模型能力 × 接口设计 × 工作流闭环 的竞争，而不是只比模型参数。NeurIPS Proceedings+3NeurIPS Proceedings+3NeurIPS Proceedings+3


如果你愿意，我下一条我可以继续给你做两版中的任意一版：
A. “SWE-agent 论文概念图谱版”，把这些概念画成一张逻辑树；
B. “每个概念对应到今天 Devin / OpenHands / Cursor agent 的现实映射版”。



Sources:
