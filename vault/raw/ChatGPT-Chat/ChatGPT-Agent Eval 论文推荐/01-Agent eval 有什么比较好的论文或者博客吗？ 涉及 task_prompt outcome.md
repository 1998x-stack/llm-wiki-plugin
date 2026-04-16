# Agent eval 有什么比较好的论文或者博客吗？ 涉及 task_prompt: outcomes; 或者 init_prompt, multi-commi

> Source: Agent Eval 论文推荐
> Time: 2026/4/14 16:42:23

## Question

Agent eval 有什么比较好的论文或者博客吗？ 涉及 task_prompt: outcomes; 或者 init_prompt, multi-commits, final outcomes;

## Answer

我先帮你筛一版更贴近你这个问题的材料：重点找“Agent eval / harness / transcript / outcomes”以及“持续演化、多轮提交、最终结果”这两类，而不是泛泛的 benchmark 汇总。

浏览AI代理评估相关博客和论文


SWE-CI: Evaluating Agent Capabilities in Maintaining Codebases via ...
GitHub - SKYLENAGE-AI/SWE-CI: SWE-CI: Evaluating Agent Capabilities in ...
AgentBoard: An Analytical Evaluation Board of Multi-turn LLM Agents
EvoClaw: Evaluating AI Agents on Continuous Software Evolution
AgentBoard: An Analytical Evaluation Board of Multi-turn LLM Agents
EvoClaw: Evaluating AI Agents on Continuous Software Evolution
AgentBoard: An Analytical Evaluation Board of Multi-Turn LLM Agents
EvoClaw: Evaluating AI Agents on Continuous Software Evolution
WebGraphEval: Multi-Turn Trajectory Evaluation for Web ...
LLMs for Commit Messages: A Survey and an Agent-Based Evaluation ...
AgentBoard: Evaluating Multi-turn LLM Agents - Emergent Mind
EvoClaw: Evaluating AI Agents on Continuous Software Evolution
EvoClaw: Evaluating AI Agents on Continuous Software Evolution ...
Most Coding Agents Break 75%+ of Their Own Fixes Over Time


搜索OpenAI/Anthropic博客及评估相关内容


Demystifying evals for AI agents \ Anthropic
Harness engineering: leveraging Codex in an agent-first world
SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?
Measuring AI Ability to Complete Long Tasks - METR
长周期评估鸿沟：为什么你的智能体通过了所有基准测试却仍 ...


已思考 21s

有，而且你提到的这两种结构，其实对应的是 两类不同的 agent eval 设计：


单任务型：task_prompt -> trajectory -> outcome

连续演化型：init_prompt -> commit_1 / commit_2 / ... / commit_n -> final outcome，同时还要看每一步是否引入回归、是否破坏之前成果


我建议你优先看下面这些，按“和你问题的贴合度”排序。


一、最贴近你问题的


1) EvoClaw（2026）


这是目前最贴近你说的 init_prompt / multi-commits / final outcomes 的论文。它不是把任务当成孤立的一次性求解，而是把 agent 放进一个持续软件演化过程里，按 milestone / dependency DAG 连续推进。论文报告说，很多模型在“单独任务”上能过 80%+，但放进连续演化场景后，总体表现掉到最高也只有 38%，暴露了长期维护、误差传播和回归累积问题。arXiv+1


你如果关心的 schema 是：


init_prompt

milestone_i / commit_i

intermediate checks

final outcome


那 EvoClaw 基本就是最值得先读的。


2) SWE-CI（2026）


SWE-CI 也非常接近你要的第二类，只是它更强调 CI loop / 代码库维护。它从真实仓库的不同时间点抽 base commit 和 reference commit，让 agent 从 base 出发，最终达到 reference 对应的测试状态。平均每个 evolution history 跨 233 天、71 个连续 commits，核心目标是从“静态、一次性功能正确”转向“动态、长期可维护性”的评估。arXiv+1


它特别适合回答这个问题：

agent 能不能在多轮修改中持续保住已有正确性，而不是每次修一个地方坏三个地方？


二、如果你想把 “task_prompt / outcomes / transcript / harness” 概念先理顺


3) Anthropic: Demystifying evals for AI agents（强烈推荐）


这篇博客非常适合搭你的概念框架。它明确区分了：


agent harness / scaffold：让模型变成 agent 的系统，负责输入处理、工具编排、结果返回

evaluation suite：任务集合

隐含地也对应你关心的 transcript / outcomes / environment feedback


它最有价值的点是：评估的不是裸模型，而是 model + harness 的联合作用。这对于你后面设计 task_prompt -> outcomes 或 trajectory -> outcome 很关键，因为 outcome 往往不只是模型能力，还混着工具、环境、反馈设计。Anthropic


4) AgentBoard（2024）


AgentBoard 是比较早但仍然有价值的工作。它明确批评“只看 final success rate 不够”，提出要看 fine-grained progress rate 和多维分析。也就是说，它更接近：


task_prompt

multi-turn trajectory

intermediate progress

final outcome


虽然它不专注软件 commit 序列，但非常适合你建立一个通用的 eval 框架。arXiv+1



三、如果你关心“长周期、多步任务到底怎么量化”


5) METR: Measuring AI Ability to Complete Long Tasks


这篇不是专门讲 transcript schema，但它给你一个非常重要的思想：不要只按任务个数计分，而要按 agent 能独立完成的任务时长/任务跨度来衡量。对于 long-horizon eval 很有启发，因为 multi-commit、本质上就是在测 agent 能稳定撑多长的任务链。metr.org



四、如果你关心“harness 本身怎么设计、怎么影响 outcome”


6) OpenAI: Harness engineering: leveraging Codex in an agent-first world


这篇虽然更偏工程经验，不是 benchmark 论文，但非常值得看。它讨论的是：当 agent 参与真实软件开发时，核心工作会从“写代码”转向“设计环境、表达意图、建立反馈回路”。这和你做 eval 时非常相关，因为 outcome 不只是 agent 本身，还是提示、环境、反馈循环共同产物。而且文中明确提到“从空仓库第一 commit 开始”的 agent-first 开发经验，这跟你说的 init_prompt / multi-commit 很契合。OpenAI


7) OpenAI: Unlocking the Codex harness


这篇更偏 harness 协议与系统稳定性。适合你在做 eval infra 时思考：


工具协议如何统一

agent 状态如何持久化

不同 surface 如何共用同一 harness


如果你想把 transcript 与 harness 绑定起来建 schema，这篇有参考价值。OpenAI



五、如果你想专门分析“trajectory 本身”


8) WebGraphEval（2025）


这是偏 web agent 的，但它很有意思：把多轮 trajectory 抽象成一个图结构，分析重复行为、成功路径、失败路径、奖励传播。它不完全等于你说的 multi-commit，但在“如何分析 transcript / trajectory，而不只看 final outcome”这个角度上很有启发。ChatPaper+1



六、我会怎么给你分层阅读


A. 先建立概念框架


先读：


Anthropic《Demystifying evals for AI agents》Anthropic

AgentBoardarXiv+1


目的：把 task / harness / transcript / outcome 这几个概念分开。


B. 再看连续演化


再读：


EvoClawarXiv+1

SWE-CIarXiv+1


目的：把 eval 从 “单回合成功率” 升级成 “多 commit 演化稳定性”。


C. 最后补工程视角


补：


OpenAI Harness engineeringOpenAI

OpenAI Unlocking the Codex harnessOpenAI

METR long tasksmetr.org


目的：知道为什么同一个模型，在不同 harness 下 outcome 差异会很大。



七、如果按你说的两种 schema 来归类


类型 1：task_prompt -> outcomes


更适合看：


Anthropic demystifying evalsAnthropic

AgentBoardarXiv+1


这类重点是：


final success / failure

progress rate

transcript 质量

工具调用质量

harness 影响


类型 2：init_prompt -> multi-commits -> final outcomes


更适合看：


EvoClawarXiv+1

SWE-CIarXiv+1

OpenAI harness engineeringOpenAI


这类重点是：


每一步 commit/milestone 是否达标

是否引入 regression

是否保住已有能力

error propagation

long-horizon maintainability



八、我的结论


如果你是为了搭建自己的 Agent eval 框架，我建议你直接把文献结构分成两层：


第一层：通用 eval ontology


task

init prompt

harness

transcript / trajectory

intermediate state

outcome


参考：Anthropic + AgentBoard。Anthropic+1


第二层：连续演化 eval


milestone DAG

commit sequence

per-step checks

regression accounting

final repository state


参考：EvoClaw + SWE-CI。arXiv+1


一句话说：
如果你只想找“task_prompt -> outcomes” 的评估框架，看 Anthropic/AgentBoard；如果你想找 “init_prompt, multi-commits, final outcomes” 这一类，EvoClaw 和 SWE-CI 是现在最值得重点看的。 Anthropic+2arXiv+2


下一步我可以直接给你整理一版：


“Agent eval 论文/博客地图”，按
paper/blog -> 评估对象 -> 输入schema -> 过程记录schema -> 输出schema -> 可借鉴点
做成一张结构化表。



Sources:


https://arxiv.org/abs/2603.13428

https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/

https://openai.com/index/harness-engineering/

https://chatpaper.com/zh-CN/paper/202516
