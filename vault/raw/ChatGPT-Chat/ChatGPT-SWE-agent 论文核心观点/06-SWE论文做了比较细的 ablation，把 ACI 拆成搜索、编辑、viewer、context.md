# SWE论文做了比较细的 ablation，把 ACI 拆成搜索、编辑、viewer、context 等模块分别对比。

> Source: SWE-agent 论文核心观点
> Time: 2026/4/13 11:35:49

## Question

SWE论文做了比较细的 ablation，把 ACI 拆成搜索、编辑、viewer、context 等模块分别对比。
详细展开 具体哪些 Ablation，如何设计，结果是什么？最终证明了什么观点？

## Answer

我把消融表和对应正文解释一起拆开讲：会先列“做了哪些 ablation”，再讲每个 ablation 的设计意图、数值结果、作者怎么解释，以及这些结果共同支持了什么结论。

在arXiv和NeurIPS搜索论文及引用


proceedings.neurips.cc


查找并添加表3周围的线条和解释


proceedings.neurips.cc


分析并解释指定段落内容


proceedings.neurips.cc


已思考 13s

SWE-agent 这组 ablation 很值得细看，因为它不是泛泛地说“我们做了个更好的 agent”，而是把 ACI（Agent-Computer Interface） 真的拆成几个部件来验证：搜索怎么做、编辑怎么做、文件窗口开多大、历史保留多少，这些具体设计会不会显著改变最终解题率。论文是在 SWE-bench Lite（300 个样本） 上，对 SWE-agent with GPT-4 Turbo 的 ACI 做消融分析，主结果汇总在 Table 3。NeurIPS 论文集+1


先给结论版：


他们一共做了 4 大类 ablation：


Editor：有没有专门 edit 动作，edit 是否带 linting

Search：总结式搜索、迭代式搜索、无专门搜索

File Viewer：一次给 30 行、100 行、整文件

Context：保留最近 5 条 observation、保留全部历史、去掉 demonstration


对应的最好配置恰好都是当前 SWE-agent 采用的配置：
w/ linting、Summarized search、100 lines、Last 5 observations。 这些最优项全部拿到 18.0% resolved；而替代设计会带来 1.7 到 7.7 个点不等的下降。NeurIPS 论文集+1



1. 这组 ablation 是怎么设计的


论文的思路不是一次改很多东西，而是以当前最佳的 SWE-agent 配置为基准，然后每次只替换一个 ACI 组件，看性能变化。Table 3 明确说，这些消融针对的是 SWE-agent interface，考虑了不同的 searching / editing / file viewer window size / context management。这意味着它的实验目标不是比模型、比 prompt，而是比 interface design choice。NeurIPS 论文集


换句话说，论文想回答的是：


搜索工具应该怎么呈现给 agent？

编辑能力应该是 shell 原生，还是专门设计动作？

agent 看文件时，窗口越大越好吗？

历史越完整越好吗？

demo 到底有没有帮助？


这组 ablation 的价值就在于，它把“agent 工程经验”变成了可以定量比较的设计变量。NeurIPS 论文集+1



2. Editor ablation：编辑接口怎么设计


2.1 比了哪三种


论文比较了三种编辑设置：


w/ linting：专门的 edit 动作，并且带 lint / syntax checking

edit action：有专门 edit 动作，但不带 linting

No edit：没有专门 edit 接口，只能依赖 shell 方式改文件，比如重定向整文件或用 sed 做单行 / 搜索替换。NeurIPS 论文集+2NeurIPS 论文集+2


2.2 结果是什么


数值如下：


w/ linting：18.0

edit action：15.0，比最佳低 3.0

No edit：10.3，比最佳低 7.7。NeurIPS 论文集+1


2.3 为什么这样设计


论文在正文里解释得很明确：
SWE-agent 的 file editor + viewer 被设计成把编辑过程压缩成一个命令，支持方便的多行修改，并且修改后会自动更新文件视图。而在 No edit 设置里，模型只能用很笨重的方式改文件：要么整文件重写，要么用 sed 这种不适合复杂局部修改的工具，既低效又容易出错。NeurIPS 论文集+1


同时，带 linting 的版本会在编辑后做语法检查；如果新编辑引入了语法错误，系统会把错误和前后代码片段反馈给 agent，无效编辑会被丢弃，agent 需要重新编辑。论文直接写到：Invalid edits are discarded, and the agent is asked to try editing the file again. NeurIPS 论文集


2.4 这组结果说明什么


这组 ablation 证明了两个点。


第一，编辑接口本身极其关键。
从 18.0 到 10.3，差了 7.7 个点，是 Table 3 里降幅最大的模块之一。也就是说，软件工程 agent 的瓶颈并不只是“会不会想对”，而是“能不能稳定执行修改”。NeurIPS 论文集


第二，guardrail 是实打实有收益的。
同样都是专门 edit 接口，带 linting 比不带 linting 高 3.0 个点。这说明论文不是空泛地说“加护栏更稳”，而是证明确实减少了错误传播、提升了恢复能力。论文在设计原则里也明确把这点写成：Guardrails mitigate error propagation and hasten recovery。NeurIPS 论文集+1



3. Search ablation：搜索接口怎么设计


3.1 比了哪三种


论文比较了三种搜索方式：


Summarized：总结式搜索

Iterative：迭代式搜索

No search：没有额外搜索接口，只用 shell-only 风格的基本命令。NeurIPS 论文集+2NeurIPS 论文集+2


3.2 结果是什么


数值如下：


Summarized：18.0

Iterative：12.0，比最佳低 6.0

No search：15.7，比最佳低 2.3。NeurIPS 论文集+1


3.3 这三种接口分别是什么


论文解释得很具体：


Iterative search 是模仿传统人类界面的做法：
一次显示一个搜索结果，agent 可以用 next / prev 看下一个匹配项，每个结果带一小段上下文。优点是 agent 在看到结果后可以立刻开始编辑。NeurIPS 论文集


Summarized search 则是一次给出完整结果摘要，而且在 query 不够具体时会提示 agent 如何 refine 搜索。Figure 5 说明 summarized search 会展示 exhaustive list of results，并提供 refining guidance。NeurIPS 论文集


3.4 为什么 iterative 反而更差


这是整篇论文里最有启发的发现之一。
论文说，当匹配结果很多时，agent 往往会机械地把每个 match 都翻一遍，不断调用 next，直到所有结果都被检查过。这种行为会耗尽 cost budget 或 context window，结果甚至比“没有额外搜索工具”还差：No search 15.7，高于 Iterative 12.0。 NeurIPS 论文集


这点特别重要，因为它说明：

对人类自然的 UI，不一定对 LM 自然。

对人类来说，next / prev 看搜索结果很合理；
但对 agent 来说，这种设计会诱导出低效遍历行为。
所以 summarized search 的优势不只是“信息更全”，而是它阻止了 agent 进入穷举式局部策略。NeurIPS 论文集+1


3.5 这组结果说明什么


这组 ablation 证明的核心不是“搜索工具有用”，而是更细的判断：


搜索接口的“呈现方式”决定了 agent 是否高效。
同样是帮 agent 搜，总结式搜索优于迭代式搜索，甚至优于没有额外搜索时的自然 shell 探索。这直接支持了论文在第 2 节提出的设计原则：动作应该 compact and efficient，而不是由很多小动作跨多轮拼成高阶操作。NeurIPS 论文集+1



4. File Viewer ablation：文件窗口应该多大


4.1 比了哪三种


论文比较了 file viewer 的三种窗口大小：


30 lines

100 lines

Full file。NeurIPS 论文集


4.2 结果是什么


数值如下：


100 lines：18.0

30 lines：14.3，比最佳低 3.7

Full file：12.7，比最佳低 5.3。NeurIPS 论文集+1


4.3 为什么这样比


这里背后在测试一个很核心的问题：
给 agent 看代码时，是不是越多越好？


30 行代表局部上下文较少；
100 行代表中等窗口；
整文件代表理论上上下文最完整。NeurIPS 论文集


4.4 结果怎么理解


结果很明确：不是越多越好。
100 行最好，整文件反而最差之一。
这说明对 agent 来说，文件查看不是“尽可能暴露所有信息”，而是要给一个既够定位、又不淹没上下文的窗口。NeurIPS 论文集


这和论文在设计原则里说的“Environment feedback should be informative but concise”完全一致。LM 不像人类那样能轻松忽略不重要内容；上下文里多余的信息会占 token、扰乱注意力。NeurIPS 论文集


4.5 这组结果说明什么


它证明了一个很反直觉但很关键的点：

对 agent 来说，信息总量和信息可用性不是一回事。

整文件虽然信息最全，但不是最可用；
30 行虽然紧凑，但可能不够支撑局部推理；
100 行提供了一个最佳平衡。NeurIPS 论文集+1



5. Context ablation：历史怎么管理


5.1 比了哪三种


论文比较了三种 context 管理方式：


Last 5 Obs.

Full history

w/o demo.（不带 demonstration）。NeurIPS 论文集


5.2 结果是什么


数值如下：


Last 5 Obs.：18.0

Full history：15.0，比最佳低 3.0

w/o demo.：16.3，比最佳低 1.7。NeurIPS 论文集+1


5.3 系统具体怎么做


论文正文解释了当前最佳做法：


早于最近 5 条的 observation 会被压缩成单行

没有输出的命令会返回专门的成功说明

malformed generation 会收到错误提示，且旧错误消息大多会被删掉

这样做是为了保持上下文“concise and informative”。NeurIPS 论文集


5.4 为什么 Full history 更差


这说明上下文不是越全越好。
保留完整历史，会把很多已经过时、低相关、重复性的 observation 继续带入 prompt，增加噪声和 token 占用；而只保留最近 5 条，让 agent 主要基于当前工作集决策，反而更有效。NeurIPS 论文集+1


5.5 demo 的作用有多大


去掉 demonstration 后性能下降 1.7 个点，说明它有帮助，但不是决定性来源。它更多像是帮助 agent 学会正确使用命令和格式，而不是主要知识来源。论文附录也提到 demonstration 会 slightly help agents with understanding proper command usage and reduce errant responses。NeurIPS 论文集+1


5.6 这组结果说明什么


这组 ablation 证明：

context management 是 ACI 的一部分，而不是简单把所有历史都喂回去。

最好的 agent 不是“记住一切”，而是“只保留还有决策价值的最近状态”。这正好呼应论文对 ACI 的定义：ACI 不只规定命令，也规定环境状态怎样组织、格式化、组合成 LM 的输入。NeurIPS 论文集+1



6. 这些 ablation 最终共同证明了什么


如果把 Table 3 的四类结果放在一起看，论文最终证明的不是某个局部技巧，而是一个整体观点：


6.1 证明一：性能提升来自 ACI 设计，而不只是模型本身


同一个 GPT-4 Turbo，
只是换搜索接口、编辑接口、viewer 大小、history 管理，解题率就能从 10.3 / 12.0 / 12.7 / 15.0 这类水平，提升到 18.0。
这说明模型权重没变，但interface design choice 本身就足以显著改变 agent 行为和结果。NeurIPS 论文集+1


6.2 证明二：对人类友好的界面，不一定对 LM 友好


最典型就是 Iterative search。
它借鉴了 Vim / VSCode 这种人类熟悉的 next / prev 搜索体验，但对 agent 来说反而更差，因为会诱导穷举式浏览。论文直接说它是 inspired by traditional user interfaces，但表现比 summarized search 低很多，甚至比 no search 还差。NeurIPS 论文集


6.3 证明三：高性能 agent 依赖“简单动作 + 紧凑反馈 + 护栏 + 受控上下文”


四类消融分别对应论文第 2 节提出的设计原则：


simple / efficient actions：专门 edit 动作、总结式搜索更优

informative but concise feedback：100-line viewer 最优

guardrails：linting 显著有益

history management：last 5 observations 优于 full history。NeurIPS 论文集+2NeurIPS 论文集+2


6.4 证明四：软件工程 agent 的问题是系统设计问题，不只是推理问题


这组 ablation 最深的含义是：
SWE agent 的成败不只取决于“模型会不会想到正确 patch”，也取决于：


能不能高效找到地方

能不能稳定改进去

能不能看到正确反馈

能不能不被历史噪声淹没

能不能在犯错时被及时拉回来


而这些都属于 ACI / workflow / interface design。NeurIPS 论文集+1



7. 一句话总结 Table 3


如果压成一句话，Table 3 证明的是：

SWE-agent 的优势不是“多了点工具”这么简单，而是这些工具、反馈和历史管理被按 LM 的特点重新设计过；一旦沿用人类习惯或默认 shell 方式，性能会明显退化。 NeurIPS 论文集+2NeurIPS 论文集+2

你要的话，我下一条可以继续把 Table 3 逐行改写成“汇报口径”，也就是你拿去给老板或同事讲时，每一行该怎么说。



Sources:
