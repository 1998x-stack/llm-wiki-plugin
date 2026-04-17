# SWE agent 有哪些图表，每个图表核心内容和核心观点是什么？

> Source: SWE-agent 论文核心观点
> Time: 2026/4/13 11:13:55

## Question

SWE agent 有哪些图表，每个图表核心内容和核心观点是什么？

## Answer

我去把论文里的图表目录和正文对上，按“图/表编号 → 讲什么 → 想证明什么”给你整理成一版可直接复述的说明。

搜索相关论文PDF和表格截图


SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering
SWE-agent: Agent-Computer Interfaces Enable Automated ...
SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering
SWE-agent: Agent-Computer Interfaces Enable Automated Software ...
SWE-agent：让AI自主完成软件工程任务的突破性进展
Paper page - SWE-agent: Agent-Computer Interfaces Enable Automated ...
SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering
NeurIPS 2024 Papers
SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering
SWE-agent: Agent-Computer Interfaces Enable Automated ...


检查PDF文本并提取图表描述


我需要检查PDF文本，查看有关图表或表格的部分。可以尝试打开PDF文件并提取其中的文字，特别是可能带有“Figure”等描述的文字。这样可以帮助我找到相关的内容和说明。


检查PDF文本并提取图表周围的内容


proceedings.neurips.cc


汇总图表与表格并提取关键信息


我需要找出所有提到“Figure”和“Table”的位置，可能会用查找功能来枚举这些出现。但是，如果文献比较大，查找结果会很庞大。也许可以通过打开含有说明的页面并分析文本，或者截图包含图表的页面。用户问关于“图表”的问题，可能意味着包括正文和附录中的图表。我得尽量总结所有图表，也许从主要部分和附录中收集。


分析PDF图表并确定范围


系统要求在分析PDF时必须使用截图。我想做的是，截取包含主要图表的页面，可能足够了。接下来，我需要列出主文献和附录中的所有图表和表格编号，可以从“Figure 27”开始查找，也许会有27个图表和4个表格。用查找功能找图表编号，比如“Figure 10”和"Table 4"。


查找并列举论文中的所有图表


proceedings.neurips.cc


截取包含主要图表的页面


我考虑截取第0至7页的截图，可能还要包括第15页。页面0-7包含了图表1-8以及表格1-3，而第15页包含了图表9和表格4。这样可以确保主要图表和表格都被收集到。


截图提取主要图表内容


已思考 31s

如果你问的是论文正文（main paper）里的图表，SWE-agent 主要有 8 个图（Figure 1–8）和 3 个表（Table 1–3）；如果把附录也算上，还会有 Figure 9、Table 4，以及更多补充分析图表。正文里的这些图表基本已经把论文的核心论点讲完了：LM 做软件工程，关键不只是模型，而是 ACI 这种为 agent 定制的交互界面。 NeurIPS Proceedings+2NeurIPS Proceedings+2



一、正文里的所有图（Figure 1–8）


Figure 1：SWE-agent 的总系统图


图里讲什么
Figure 1 画的是整个系统结构：LM Agent 不直接面对计算机，而是通过一个 ACI（Agent-Computer Interface） 与计算机交互；ACI 一边提供 LM-friendly commands，一边把环境反馈整理成 LM-friendly environment feedback。NeurIPS Proceedings+1


核心观点
这张图要证明的不是“SWE-agent 会写代码”，而是：
真正的研究对象是 interface。
也就是，软件工程 agent 的表现高度依赖它怎么和计算机交互，而不是只看底层模型本身。NeurIPS Proceedings



Figure 2：ACI 和人类 IDE 的类比图


图里讲什么
Figure 2 把 LM Agent : ACI 和 Human : IDE/GUI 做了类比。对人类程序员，VSCode/PyCharm 这类 IDE 会显著提高效率；对 LM agent，也应该设计一个对应的、适合它的专用界面。NeurIPS Proceedings+1


核心观点
这张图想强调：
ACI 对 agent 的意义，类似 IDE 对人类工程师的意义。
所以论文不是把 agent 当“更强的代码补全器”，而是把它当成一种新的“计算机使用者”。NeurIPS Proceedings



Figure 3：File Viewer 和 Edit 的一体化设计


图里讲什么
Figure 3 分成两部分：
左边是 file viewer，展示打开文件的局部内容和行号；右边是 edit action，直接基于这些行号做替换。编辑后，viewer 会自动显示更新后的文件内容。NeurIPS Proceedings+1


核心观点
这张图想说明：
高效编辑不是“让 agent 自己拼很多 shell 命令”，而是提供一个与 viewer 对齐的局部编辑动作。
也就是把“看文件 → 定位行号 → 修改 → 再确认”的链路压缩成一个连续、可解释的工作流。NeurIPS Proceedings+1



Figure 4：Pass@k 曲线


图里讲什么
Figure 4 展示的是 SWE-agent with GPT-4 Turbo 在 SWE-bench Lite 上跨 6 次运行的 pass@k / % resolved 曲线。随着 k 从 1 提高到 6，解决率从大约 18% 继续升高到 30%+。论文同时指出，平均方差不高，但具体到单个样本，是否解决会有明显波动。NeurIPS Proceedings+1


核心观点
这张图不是在说“多采样就一定更强”，而是在说明两件事：
第一，SWE-agent 结果具有一定稳定性，但单题波动仍然明显；
第二，当前 agent 还不是“确定性系统”，同一个任务不同 run 仍有较大随机性。NeurIPS Proceedings



Figure 5：三种 Search Interface 对比


图里讲什么
Figure 5 对比了三种搜索方式：


No Search：只用 shell/basics 自己找

Iterative Search：一条条翻搜索结果

Summarized Search：一次返回压缩后的搜索结果，并在 query 太泛时提示 refine


图里展示的是一个具体任务实例下，这三种搜索界面的交互差异。NeurIPS Proceedings+1


核心观点
这张图的核心不是“有搜索比没搜索强”，而是更细的一点：
总结式搜索比迭代式搜索更适合 LM agent。
因为 iterative search 容易诱导模型把结果一个个翻完，耗掉上下文和成本；summarized search 更有助于快速缩小定位范围。NeurIPS Proceedings+2NeurIPS Proceedings+2



Figure 6：三种 Edit Interface 对比


图里讲什么
Figure 6 对比了三种编辑方式：


No edit：靠普通 bash / shell 方式改文件

edit w/o linting：有专门 edit 动作，但没有 lint/syntax 检查

edit w/ linting：既有 edit 动作，又有 linting / syntax guardrail


图中直接展示了这三种编辑界面的差别，尤其是 linting 会阻止坏编辑被应用。NeurIPS Proceedings+1


核心观点
这张图要证明的是：
编辑能力的关键不是“能不能改”，而是“能不能稳定地改”。
尤其是 linting guardrail 很重要，因为它可以阻断 agent 自己引入的 syntax/compile error，防止错误级联。NeurIPS Proceedings+2NeurIPS Proceedings+2



Figure 7：成功轨迹里的动作分布


图里讲什么
Figure 7 统计了 SWE-agent 在成功解决的 SWE-bench 全测试集任务中，各个 turn 上不同动作被调用的频率。图里能看到早期更多是 find_file、search_dir、open 这类定位动作，后期更多是 edit、python、pytest 这类修改和验证动作。NeurIPS Proceedings+1


核心观点
这张图在讲一个“行为模式”：


前几轮主要是 reproduction / localization

后几轮主要是 edit → execute 循环


也就是说，成功的 SWE-agent 轨迹不是一上来就改代码，而是先定位，再进入编辑-验证闭环。NeurIPS Proceedings+1



Figure 8：失败模式分布图


图里讲什么
Figure 8 把未解决任务按失败类型做了分布统计。最大的几类包括：


Incorrect Implementation

Overly Specific Implementation

Failed to Recover from Edit

Failed to Find Edit Location

Failed to Find Relevant File 等。NeurIPS Proceedings+1


论文正文特别指出，大约 52.0% 的未解决样本属于 Incorrect Implementation 或 Overly Specific Implementation，另有 23.4% 和编辑失败后的恢复有关。NeurIPS Proceedings


核心观点
这张图说明：
SWE-agent 的主要瓶颈已经不只是“找不到文件”，而是“方案本身不够对”或“改坏后恢复不了”。
也就是说，接口设计虽然解决了不少导航/编辑问题，但真正的功能性推理和泛化实现仍然是主要难点。NeurIPS Proceedings



二、正文里的所有表（Table 1–3）


Table 1：主结果表


表里讲什么
Table 1 比较了 SWE-agent、Shell-only agent、RAG 在 SWE-bench full 和 SWE-bench Lite 上的结果，以及平均成本。核心数字包括：


SWE-agent w/ GPT-4 Turbo：12.47% resolved on full，18.00% on Lite

Shell-only agent w/ GPT-4 Turbo：Lite 上 11.00%

RAG w/ GPT-4 Turbo：full 上 1.31%，Lite 上 2.67%。NeurIPS Proceedings+1


核心观点
这个表最想证明两件事：
第一，交互式 agent 明显优于非交互式 RAG；
第二，专门设计的 ACI 明显优于直接用 shell 的 agent。
换句话说，表 1 是整篇论文“ACI 有效”的最核心实证证据。NeurIPS Proceedings+1



Table 2：HumanEvalFix 结果表


表里讲什么
Table 2 对比不同模型在 HumanEvalFix 上的 pass@1，按 Python / JS / Java 三种语言列出。SWE-agent w/ GPT-4 Turbo 的结果是：


Python：87.7

JS：89.7

Java：87.9。NeurIPS Proceedings+1


核心观点
这个表的作用更像“补充证明”：
SWE-agent 不只在 repo-level 的 SWE-bench 上有效，在程序修复任务上也很强。
但从论文主线看，Table 2 的重要性低于 Table 1，因为论文最关键的命题还是“ACI 对真实软件工程任务有效”。NeurIPS Proceedings



Table 3：ACI 消融实验表


表里讲什么
Table 3 是整篇论文最重要的分析表之一。它把 interface 拆开来做消融：


Editor：edit action / w linting / no edit

Search：summarized / iterative / no search

File Viewer：30 lines / 100 lines / full file

Context：last 5 obs / full history / w/o demo.。NeurIPS Proceedings+1


主要结论包括：


summarized search 最好，iterative search 最差

有 linting 的 edit 最好

100-line viewer 最好

最近 5 条 observation 比 full history 更好。NeurIPS Proceedings+1


核心观点
这张表真正要证明的是：
SWE-agent 的提升不是“碰巧系统堆起来更强”，而是 ACI 的具体设计选择本身在起作用。
也就是说，搜索怎么做、编辑怎么做、viewer 开多大、历史留多少，都会显著影响 agent 表现。NeurIPS Proceedings+1



三、附录里还值得看的两个图表


如果你也想把附录里最有价值的图表一起看进去，最值得加上的就是下面两个。


Figure 9：轨迹结构图


讲什么
Figure 9 把一条完整 trajectory 的消息结构画出来：system prompt、demonstration、issue statement、thought/action、environment response、collapsed observations、最终 submit patch。NeurIPS Proceedings+1


核心观点
它说明 SWE-agent 不是简单工具调用，而是一个经过精心设计的 prompt + action + feedback + history collapse 的轨迹系统。NeurIPS Proceedings


Table 4：工具命令表


讲什么
Table 4 列出了 ACI 的核心命令，包括 open、goto、scroll_down、scroll_up、search_file、search_dir、find_file、edit、create、submit。NeurIPS Proceedings+1


核心观点
它直接落地了论文的方法论：
给 agent 一小组简单、清晰、参数少、互相配合的专用动作，比让它裸用 shell 更有效。 NeurIPS Proceedings+1



四、把所有图表压成一句话


如果把这些图表串起来，论文在用它们讲一个完整故事：


Figure 1–2：先提出 ACI 这个研究对象

Figure 3 / Table 4：再说明 ACI 具体长什么样

Table 1–2：证明它确实有效

Table 3 / Figure 5–6：证明有效来自具体 interface design choice

Figure 7–8：进一步分析 agent 成功和失败的行为模式

Figure 9：补充解释系统轨迹是如何组织起来的。 NeurIPS Proceedings+9NeurIPS Proceedings+9NeurIPS Proceedings+9


如果你愿意，我下一条可以直接给你整理成一版：“每张图表适合怎么讲给老板/同事听”的汇报话术版。



Sources:
