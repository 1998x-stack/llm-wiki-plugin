---
title: "Improving skill-creator: Test, measure, and refine Agent Skills"
source: "https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills"
author:
published: 2001-03-03
created: 2026-04-16
description: "Skill authors now have tools to verify their skills work, catch regressions, and improve descriptions—no coding required."
tags:
  - "clippings"
---
Skill-creator now helps you write evals, run benchmarks, and keep your skills working as models evolve. These updates are available now in Claude.ai and Cowork, as a [plugin for Claude Code](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator), and [within our repo](https://github.com/anthropics/skills/tree/main/skills/skill-creator). Skill-creator 现在可帮助你编写评估、运行基准测试，并确保你的技能随着模型的迭代正常运行。这些更新目前已在 Claude.ai 和 Cowork 中推出，作为 [Claude Code 的插件](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator) ，并可在 [我们的代码仓库](https://github.com/anthropics/skills/tree/main/skills/skill-creator) 中获取。

Since [launching Agent Skills](https://claude.com/blog/skills) last October, we've noticed that most authors are subject matter experts, not engineers. They know their workflows but don't have the tools to tell whether a skill still works with a new model, triggers when it should, or if it actually improved after an edit.自去年10月 [推出智能体技能](https://claude.com/blog/skills) 以来，我们注意到大多数创作者都是领域专家，而非工程师。他们了解自己的工作流程，却没有工具去判断某项技能是否仍适用于新模型、是否在正确的时机触发，或是在编辑后是否真的得到了改进。

Today we're announcing skill-creator enhancements that help authors build with more confidence. We are bringing some of the rigor of software development (testing, benchmarking, iterative improvement) to skill authoring without requiring anyone to write code. 今天我们宣布推出技能创建功能的增强版本，帮助创作者更有信心地进行开发。我们将软件开发中的部分严谨流程（测试、基准测试、迭代优化）引入到技能创作中，且无需任何人编写代码。

## Two kinds of skills 两种技能类型

Skills generally fall into two categories:技能通常分为两类：

**Capability uplift** skills help Claude do something the base model either can't do or can't do consistently. Our [document creation skills](https://github.com/anthropics/skills/tree/main/skills) are good examples. They encode techniques and patterns that produce better output than prompting alone.**能力提升** 技能帮助Claude完成基础模型无法完成或无法稳定完成的任务。我们的 [文档创建技能](https://github.com/anthropics/skills/tree/main/skills) 就是很好的例子。这些技能整合了能产出比单纯提示更好的输出的技巧和模式。

**Encoded preference** skills document workflows where Claude can already do each piece, but the skill sequences them according to your team's process. Examples: a skill that walks through NDA review against set criteria, or one that drafts weekly updates with data from various MCPs.**编码偏好** 技能文档工作流，其中Claude已能完成每个环节，而技能会按照你的团队流程对这些环节进行排序。示例：一项技能可对照设定标准完成保密协议审核流程，或从多个托管控制平台提取数据并撰写每周更新报告。

This distinction matters because these two types of skills may need testing for different reasons:这种区分很重要，因为这两类技能可能出于不同的原因需要进行测试：

- Capability uplift skills may become less necessary as models improve. Evals tell you when that's happened. 随着模型不断优化，能力提升所需的技能可能变得不再那么必要。评估能帮你判断这一情况何时发生。
- Encoded preference skills are more durable, but only as valuable as their fidelity to your actual workflow. Evals verify that fidelity. 编码后的偏好技能更持久，但其价值仅取决于其与实际工作流程的契合度。评估验证了这种契合度。

Either way, testing turns a skill that *seems* to work into one you *know* works. 无论哪种方式，测试都能将一项 *看似* 有效的技能，转化为你 *确认* 真正有效的技能。

## Using evals to test and improve skills利用评估测试并提升技能

Skill-creator now helps you write evals, which are tests that check Claude does what you expect for a given prompt. If you've written software tests, this will feel familiar: define some test prompts (plus files if needed), describe what good looks like, and skill-creator tells you whether the skill holds up.Skill-creator 现在可以帮你编写评估脚本，这类脚本用于测试 Claude 是否能按照预期对特定提示做出正确反应。如果你编写过软件测试，会对此感到很熟悉：定义一些测试提示词（必要时还可加上文件），描述合格的标准，然后 Skill-creator 会告诉你该功能是否符合要求。

Our PDF skill, for instance, previously struggled with non-fillable forms. Claude had to place text at exact coordinates with no defined fields to guide it. Evals isolated the failure, and we shipped a fix that anchors positioning to extracted text coordinates.例如，我们的 PDF 功能此前在处理非可填写表单时一直存在问题。Claude 必须将文本放置在精确的坐标上，而没有可定义的字段来指引它。评估找出了这一故障，我们随后推出了一项修复方案，将定位锚定到提取的文本坐标上。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69a237b02128b691d9e8b2af_skillscreator-PDFevals-1920x840-v1.png)

Evals help in many ways, but two important uses are to catch quality regressions and understand model progress.评估在很多方面都有帮助，但两个重要的用途是发现质量退化并了解模型的进展情况。

First, **catching regressions in quality.** As models and the infrastructure around them evolve, a skill that worked well last month might behave differently today. Running evals against a new model gives you an early signal when something shifts before it impacts your team’s work. 首先， **捕捉质量方面的回归问题。** 随着模型及其周边基础设施的不断演进，上个月效果良好的技能在今天可能会表现出不同的行为。当出现变化时，针对新模型进行评估能让你提前发现信号，避免其影响团队的工作。

Second, **knowing when general model capabilities have outgrown your skill.** This applies mainly to capability uplift skills. If the base model starts passing your evals *without* the skill loaded, that's a signal the skill's techniques may have been incorporated into the model's default behavior. The skill isn't broken; it's just no longer necessary.第二， **了解通用模型能力何时已经超越你的技能水平。** 这主要适用于能力提升类技能。如果基础模型在 *未* 加载该技能的情况下就能通过你的评估，这就表明该技能的相关技术可能已被整合到模型的默认行为中。该技能并未失效，只是不再有必要使用了。

We've also added a **benchmark mode** that runs a standardized assessment using your evals. This is something you can run after model updates or as you iterate on the skill itself. It tracks eval pass rate, elapsed time, and token usage. 我们还新增了 **基准测试模式** ，该模式会使用你的评估项运行标准化评估。你可以在模型更新后或对技能本身进行迭代时运行此模式。它会跟踪评估通过率、耗时和令牌使用量。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69a237f15fbc61e1ccd00a0a_skillscreator-benchmarkmode-1920x1080-v1.png)

Your evals and results stay with you. Store them locally, integrate them with a dashboard, or plug them into a CI system.你的评估内容和结果都由你掌控。你可以将其存储在本地，与仪表板集成，或接入持续集成系统。

## Faster, more consistent evaluation with multi-agent support借助多智能体支持实现更快、更稳定的评估

Running evals sequentially can be slow, and accumulating context can bleed between test runs. Skill-creator now spins up independent agents to run evals in parallel with **multi-agent support** — each in a clean context with its own token and timing metrics. Faster results, no cross-contamination.按顺序运行评估可能会很慢，而且测试运行之间可能会累积上下文并产生干扰。现在，Skill-creator 借助 **多智能体支持** 启动独立智能体来并行运行评估——每个智能体都在干净的上下文中运行，拥有独立的令牌和计时指标。结果更快，且无交叉干扰。

We've also added **comparator agents** for A/B comparisons: two skill versions, or skill vs. no skill. They judge outputs without knowing which is which, so you can tell whether a change actually helped.我们还为 A/B 对比添加了对比智能体</b0：可对比两个技能版本，或技能与无技能的效果。它们在判断输出结果时不会知晓哪个是目标版本，因此你可以判断某一改动是否真正起到了优化作用。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69a74e0afa8435f070120ed9_skillscreator-AB-testing-1920x1080-v1.png)

## Getting skills to trigger at the right time让技能在正确的时机触发

Evals measure output quality, but that only matters if your skill triggers when it should. As your skill count grows, description precision becomes critical: too broad and you get false triggers, too narrow and it never fires. Skill-creator now helps you tune descriptions for more reliable triggering — it analyzes your current description against sample prompts and suggests edits that cut both false positives and false negatives.评估工具会衡量输出质量，但只有当你的技能在正确时机触发时，这一点才重要。随着技能数量的增加，描述的精准度变得至关重要：描述过于宽泛会导致错误触发，过于具体则会让技能永远无法触发。技能创建工具现在能帮你优化描述，实现更可靠的触发——它会对照示例提示词分析你当前的描述，并提出修改建议，同时减少误触发和漏触发的情况。

We ran it across our document-creation skills and saw improved triggering on 5 out of 6 public skills.我们将其应用到文档创建相关技能中，结果显示6项公开技能中有5项的触发效果得到了提升。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69a74e1f72940942cb534904_skillscreator-skill-description-optimization-results.png)

## Looking ahead 展望未来

As models improve, the line between "skill" and "specification" may blur. Today, a SKILL.md file is essentially an implementation plan, providing detailed instructions telling Claude *how* to do something. Over time, a natural-language description of *what* the skill should do may be enough, with the model figuring out the rest.随着模型不断优化，“技能”与“规范”之间的界限可能会变得模糊。如今，一个 SKILL.md 文件本质上是一份实施计划，它会提供详细的指令，告诉 Claude *如何* 完成某项任务。随着时间推移，仅用自然语言描述出 *该技能* 应实现的功能可能就足够了，其余部分由模型自行完成。

The eval framework we're releasing today is a step in that direction. Evals already describe the "what." Eventually, that description may be the skill itself.我们今天发布的评估框架正是朝着这一方向迈出的一步。评估已经明确了“是什么”。最终，这一描述可能会成为技能本身。

## Getting Started 快速开始

All skill-creator updates are available now on Claude.ai and Cowork. Ask Claude to use the skill-creator to get started.Claude.ai 和 Cowork 现已推出所有技能创建器的更新。让 Claude 使用技能创建器开始使用吧。

Claude Code users can install the [plugin](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator) or download from our [repo](https://github.com/anthropics/skills/tree/main/skills/skill-creator). Claude Code 用户可以安装 [插件](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator) 或从我们的 [代码仓库](https://github.com/anthropics/skills/tree/main/skills/skill-creator) 下载。