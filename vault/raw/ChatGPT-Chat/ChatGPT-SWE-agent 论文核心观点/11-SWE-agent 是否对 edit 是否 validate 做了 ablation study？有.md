# SWE-agent 是否对 edit 是否 validate 做了 ablation study？有吗，如果有，结论是什么

> Source: SWE-agent 论文核心观点
> Time: 2026/4/14 19:58:31

## Question

SWE-agent 是否对 edit 是否 validate 做了 ablation study？有吗，如果有，结论是什么

## Answer

已思考几秒

有。


SWE-agent 的 Table 3 专门对 editor interface 做了 ablation，其中就包含了 edit 后是否做 validate / linting 的对比。论文把这组配置分成三档：


w/ linting：带 linting 的 edit

edit action：有专门 edit 动作，但不带 linting

No edit：没有专门 edit 工具，只能靠普通 shell 方式改文件。


对应结果是：


w/ linting：18.0

edit action：15.0

No edit：10.3


这说明两层结论。


第一层，有专门 edit 工具本身就很重要。
从 No edit 10.3 到 edit action 15.0，说明把编辑变成一个紧凑、受约束的专门动作，本身就能显著提升效果。


第二层，edit 后做 validate / linting 进一步显著有益。
从 15.0 到 18.0，说明仅仅“能编辑”还不够，把坏编辑拦下来、把语法/缩进类错误尽早暴露出来，会明显减少错误传播。论文正文对这点的解释也很直接：在编辑函数里加入 linter 后，如果编辑引入语法错误，系统会向 agent 返回错误和代码片段，并把无效编辑丢弃，再让 agent 重新尝试。


所以你的问题可以直接回答成一句话：

SWE-agent 确实对 edit 是否 validate 做了 ablation；结论是：validate（论文里主要体现为 linting）是有效的，能把 resolved rate 从 15.0 提升到 18.0。

再补一句更准确的表述：
论文这里验证的主要是 linting / syntax-level guardrail，不是完整的 LSP/全仓语义检查。也就是说，它证明的是“edit 后做轻量、即时的有效性校验有帮助”，而不是“必须上完整 LSP 才有效”。
