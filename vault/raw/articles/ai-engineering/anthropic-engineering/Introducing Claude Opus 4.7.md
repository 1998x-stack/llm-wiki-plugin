---
title: "Introducing Claude Opus 4.7"
source: "https://www.anthropic.com/news/claude-opus-4-7"
author:
published:
created: 2026-04-17
description: "Anthropic is an AI safety and research company that's working to build reliable, interpretable, and steerable AI systems."
tags:
  - "clippings"
---
Product 产品 Announcements 公告

## Introducing Claude Opus 4.7 推出 Claude Opus 4.7

2026年4月16日

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F96ea2509a90e527642c822303e56296a07bcfce4-1920x1080.png&w=3840&q=75)

Our latest model, Claude Opus 4.7, is now generally available.我们的最新模型 Claude Opus 4.7 现已全面开放使用。

Opus 4.7 is a notable improvement on Opus 4.6 in advanced software engineering, with particular gains on the most difficult tasks. Users report being able to hand off their hardest coding work—the kind that previously needed close supervision—to Opus 4.7 with confidence. Opus 4.7 handles complex, long-running tasks with rigor and consistency, pays precise attention to instructions, and devises ways to verify its own outputs before reporting back.Opus 4.7 是高级软件工程领域中对 Opus 4.6 的显著改进版本，在难度最高的任务上取得了尤为突出的提升。用户反馈，他们可以放心地将最棘手的编码工作——这类工作此前需要密切监督——交给 Opus 4.7 处理。Opus 4.7 能严谨且稳定地处理复杂的长期运行任务，精准遵循指令，并在反馈结果前制定方法验证自身的输出。

The model also has substantially better vision: it can see images in greater resolution. It’s more tasteful and creative when completing professional tasks, producing higher-quality interfaces, slides, and docs. And—although it is less broadly capable than our most powerful model, Claude Mythos Preview—it shows better results than Opus 4.6 across a range of benchmarks:该模型的视觉能力也有显著提升：能够以更高分辨率识别图像。在完成专业任务时，它的表现更具品味和创意，能生成更高质量的界面、幻灯片和文档。此外——尽管它的综合能力不如我们最强大的模型 Claude Mythos Preview——但在一系列基准测试中，它的表现优于 Opus 4.6：

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fd434d15757c6abac1122af483617741776d5a114-2600x2638.png&w=3840&q=75)

Last week we announced [Project Glasswing](https://www.anthropic.com/glasswing), highlighting the risks—and benefits—of AI models for cybersecurity. We stated that we would keep Claude Mythos Preview’s release limited and test new cyber safeguards on less capable models first. Opus 4.7 is the first such model: its cyber capabilities are not as advanced as those of Mythos Preview (indeed, during its training we experimented with efforts to differentially reduce these capabilities). We are releasing Opus 4.7 with safeguards that automatically detect and block requests that indicate prohibited or high-risk cybersecurity uses. What we learn from the real-world deployment of these safeguards will help us work towards our eventual goal of a broad release of Mythos-class models.上周我们发布了Project Glasswing</b>，重点介绍了人工智能模型在网络安全领域的风险与益处。我们表示，将对Claude Mythos预览版的发布保持有限制，并先在性能较低的模型上测试新的网络安全防护措施。Opus 4.7是首款此类模型：其网络安全功能不如Mythos预览版先进（事实上，在训练过程中，我们尝试通过差异化手段削弱这些功能）。我们发布Opus 4.7时配备了防护机制，可自动检测并拦截表明存在违规或高风险网络安全用途的请求。从这些防护措施的实际部署中获得的经验，将助力我们朝着最终广泛发布Mythos级模型的目标迈进。

Security professionals who wish to use Opus 4.7 for legitimate cybersecurity purposes (such as vulnerability research, penetration testing, and red-teaming) are invited to join our new [Cyber Verification Program](https://claude.com/form/cyber-use-case).希望出于合法网络安全目的（如漏洞研究、渗透测试和红队演练）使用 Opus 4.7 的安全专业人士，欢迎加入我们全新的 [网络验证计划](https://claude.com/form/cyber-use-case) 。

Opus 4.7 is available today across all Claude products and our API, Amazon Bedrock, Google Cloud’s Vertex AI, and Microsoft Foundry. Pricing remains the same as Opus 4.6: $5 per million input tokens and $25 per million output tokens. Developers can use `claude-opus-4-7` via the [Claude API](https://platform.claude.com/docs/en/about-claude/models/overview).Opus 4.7 现已在所有 Claude 产品以及我们的 API、Amazon Bedrock、Google Cloud 的 Vertex AI 和 Microsoft Foundry 上线。定价与 Opus 4.6 保持一致：每百万输入令牌 5 美元，每百万输出令牌 25 美元。开发者可通过 `claude-opus-4-7` 借助 [Claude API](https://platform.claude.com/docs/en/about-claude/models/overview) 使用该模型。

## Testing Claude Opus 4.7 测试 Claude Opus 4.7

Claude Opus 4.7 has garnered strong feedback from our early-access testers:Claude Opus 4.7 已获得我们早期访问测试者的积极反馈：

04 / 28

Below are some highlights and notes from our early testing of Opus 4.7:以下是我们对 Opus 4.7 早期测试的一些重点和说明：

- *Instruction following*. Opus 4.7 is substantially better at following instructions. Interestingly, this means that prompts written for earlier models can sometimes now produce unexpected results: where previous models interpreted instructions loosely or skipped parts entirely, Opus 4.7 takes the instructions literally. Users should re-tune their prompts and harnesses accordingly.*指令遵循* 。Opus 4.7 在遵循指令方面表现显著更出色。有趣的是，这意味着为早期模型编写的提示词有时现在会产生意想不到的结果：以往的模型会宽松地解读指令或直接跳过部分内容，而 Opus 4.7 会严格按字面理解指令。用户应据此重新调整他们的提示词和工具。
- *Improved multimodal support*. Opus 4.7 has better vision for high-resolution images: it can accept images up to 2,576 pixels on the long edge (~3.75 megapixels), more than three times as many as prior Claude models. This opens up a wealth of multimodal uses that depend on fine visual detail: computer-use agents reading dense screenshots, data extractions from complex diagrams, and work that needs pixel-perfect references.<sup>1</sup> *多模态支持升级* 。Opus 4.7 对高分辨率图像的视觉处理能力更出色：其可接收长边像素达2576（约375万像素）的图像，是此前Claude模型的三倍多。这为依赖精细视觉细节的多模态应用场景打开了广阔空间：包括读取密集截图的计算机操作智能体、从复杂图表中提取数据，以及需要像素级精准参考的各类工作。1
- *Real-world work*. As well as its state-of-the-art score on the Finance Agent evaluation (see table above), our internal testing showed Opus 4.7 to be a more effective finance analyst than Opus 4.6, producing rigorous analyses and models, more professional presentations, and tighter integration across tasks. Opus 4.7 is also state-of-the-art on [GDPval-AA](https://artificialanalysis.ai/evaluations/gdpval-aa), a third-party evaluation of economically valuable knowledge work across finance, legal, and other domains.*实际工作表现* 。除了在金融智能体评估中取得顶尖分数（见上表）外，我们的内部测试显示，Opus 4.7 作为金融分析师比 Opus 4.6 更高效，能生成更严谨的分析和模型、更专业的演示文稿，并实现各任务间更紧密的整合。Opus 4.7 在 [GDPval-AA](https://artificialanalysis.ai/evaluations/gdpval-aa) 评估中也处于顶尖水平，该第三方评估针对金融、法律及其他领域具有经济价值的知识型工作展开。
- *Memory*. Opus 4.7 is better at using file system-based memory. It remembers important notes across long, multi-session work, and uses them to move on to new tasks that, as a result, need less up-front context.*记忆* 。4.7 版本在使用基于文件系统的记忆功能上表现更出色。它能在漫长的多会话工作中记住重要笔记，并利用这些笔记推进新任务，从而让新任务所需的前期背景信息更少。

The charts below display more evaluation results from our pre-release testing, across a range of different domains:以下图表展示了我们预发布测试中来自多个不同领域的更多评估结果：

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F9299f8b86c69359c31d15dbece4545e628bddc34-1920x1080.png&w=3840&q=75)

## Safety and alignment 安全性与对齐性

Overall, Opus 4.7 shows a similar safety profile to Opus 4.6: our evaluations show low rates of concerning behavior such as deception, sycophancy, and cooperation with misuse. On some measures, such as honesty and resistance to malicious “prompt injection” attacks, Opus 4.7 is an improvement on Opus 4.6; in others (such as its tendency to give overly detailed harm-reduction advice on controlled substances), Opus 4.7 is modestly weaker. Our alignment assessment concluded that the model is “largely well-aligned and trustworthy, though not fully ideal in its behavior”. Note that Mythos Preview remains the best-aligned model we’ve trained according to our evaluations. Our safety evaluations are discussed in full in the [Claude Opus 4.7 System Card](https://anthropic.com/claude-opus-4-7-system-card).总体而言，Opus 4.7 展现出与 Opus 4.6 相似的安全表现：我们的评估显示，其出现欺骗、阿谀奉承、配合滥用等不良行为的概率较低。在诚实度以及抵御恶意“提示注入”攻击等指标上，Opus 4.7 较 Opus 4.6 有所提升；但在部分方面（如对管制物质给出过于详细的减害建议的倾向），Opus 4.7 的表现则稍逊一筹。我们的对齐评估得出结论，该模型“整体对齐度良好且值得信赖，不过行为并非完全完美”。需注意的是，根据我们的评估，Mythos Preview 仍是我们训练过的对齐效果最佳的模型。我们的安全评估详情可参见 [Claude Opus 4.7 系统卡片](https://anthropic.com/claude-opus-4-7-system-card) 。

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F3a5b5c3eedb539fe20bc8dd1ecfc952c447000b8-1920x1080.png&w=3840&q=75)

Overall misaligned behavior score from our automated behavioral audit. On this evaluation, Opus 4.7 is a modest improvement on Opus 4.6 and Sonnet 4.6, but Mythos Preview still shows the lowest rates of misaligned behavior. 我们自动化行为审计得出的整体行为偏差分数。在本次评估中，Opus 4.7 相比 Opus 4.6 和 Sonnet 4.6 有小幅改进，但 Mythos Preview 的行为偏差率仍为最低。

## Also launching today 今日同步推出

In addition to Claude Opus 4.7 itself, we’re launching the following updates:除了 Claude Opus 4.7 本身，我们还推出了以下更新：

- *More effort control*: Opus 4.7 introduces a new `xhigh` (“extra high”) [effort level](https://platform.claude.com/docs/en/build-with-claude/effort) between `high` and `max`, giving users finer control over the tradeoff between reasoning and latency on hard problems. In Claude Code, we’ve raised the default effort level to `xhigh` for all plans. When testing Opus 4.7 for coding and agentic use cases, we recommend starting with `high` or `xhigh` effort.*更强的效果控制* ：Opus 4.7 新增了一个介于 `high` 和 `max` 之间的 `xhigh` （“超高”） [效果等级](https://platform.claude.com/docs/en/build-with-claude/effort) ，让用户能更精细地控制复杂问题上推理能力与延迟之间的权衡。在 Claude Code 中，我们已将所有计划的默认效果等级提升至 `xhigh` 。在针对编码和智能体用例测试 Opus 4.7 时，我们建议从 `high` 或 `xhigh` 效果等级开始尝试。
- *On the Claude Platform (API)*: as well as support for higher-resolution images, we’re also launching task budgets in public beta, giving developers a way to guide Claude’s token spend so it can prioritize work across longer runs.*在 Claude 平台（API 端）* ：除了支持更高分辨率的图像外，我们还将推出任务预算的公开测试版，为开发者提供一种方式来指导 Claude 的令牌消耗，使其能够在长时间运行的任务中优先处理各项工作。
- *In Claude Code*: The new `/ultrareview` [slash command](https://code.claude.com/docs/en/commands) produces a dedicated review session that reads through changes and flags bugs and design issues that a careful reviewer would catch. We’re giving Pro and Max Claude Code users three free ultrareviews to try it out. In addition, we’ve extended [auto mode](https://claude.com/blog/auto-mode) to Max users. Auto mode is a new permissions option where Claude makes decisions on your behalf, meaning that you can run longer tasks with fewer interruptions—and with less risk than if you had chosen to skip all permissions.*在 Claude Code 中* ：全新的 `/ultrareview` [斜杠命令](https://code.claude.com/docs/en/commands) 可生成专属的审核会话，全面检视代码变更并标记出细心审核人员会发现的 bug 与设计问题。我们为 Pro 和 Max 版 Claude Code 用户提供了三次免费超量审核机会，供大家体验。此外，我们还向 Max 用户开放了 [自动模式](https://claude.com/blog/auto-mode) 。自动模式是一项全新的权限选项，由 Claude 代你做出决策，这意味着你可以运行更长的任务，中断次数更少，且相比选择跳过所有权限的情况，风险也更低。

## Migrating from Opus 4.6 to Opus 4.7从 Opus 4.6 迁移到 Opus 4.7

Opus 4.7 is a direct upgrade to Opus 4.6, but two changes are worth planning for because they affect token usage. First, Opus 4.7 uses an updated tokenizer that improves how the model processes text. The tradeoff is that the same input can map to more tokens—roughly 1.0–1.35× depending on the content type. Second, Opus 4.7 thinks more at higher effort levels, particularly on later turns in agentic settings. This improves its reliability on hard problems, but it does mean it produces more output tokens. Opus 4.7 是 Opus 4.6 的直接升级版本，但有两项更改值得提前规划，因为它们会影响令牌使用量。首先，Opus 4.7 采用了更新的分词器，优化了模型处理文本的方式。代价是相同的输入可能对应更多的令牌——具体倍数约为 1.0–1.35 倍，取决于内容类型。其次，Opus 4.7 在高算力模式下的思考能力更强，尤其是在智能体场景的后续交互回合中。这提升了它在难题上的可靠性，但也意味着它会生成更多的输出令牌。

Users can control token usage in various ways: by using the effort parameter, adjusting their task budgets, or prompting the model to be more concise. In our own testing, the net effect is favorable—token usage across all effort levels is improved on an internal coding evaluation, as shown below—but we recommend measuring the difference on real traffic. We’ve written a [migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide#migrating-to-claude-opus-4-7) that provides further advice on upgrading from Opus 4.6 to Opus 4.7.用户可以通过多种方式控制 token 用量：使用努力参数、调整任务预算，或提示模型更简洁。在我们的测试中，最终效果是积极的——如下所示，在一项内部编码评估中，所有努力等级下的 token 用量都得到了优化——但我们建议在实际流量中衡量这一差异。我们编写了一份 [迁移指南](https://platform.claude.com/docs/en/about-claude/models/migration-guide#migrating-to-claude-opus-4-7) ，其中提供了从 Opus 4.6 升级到 Opus 4.7 的进一步建议。

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fff97ab0f2a5f3a243da02398f97dec1ac99b526a-3840x2160.png&w=3840&q=75)

Score on an internal agentic coding evaluation as a function of token usage at each effort level. In this evaluation, the model works autonomously from a single user prompt, and results may not be representative of token usage in interactive coding. See the migration guide for more on tuning effort levels. 在不同努力水平下，内部智能体编码评估的得分与令牌使用量的关系。在该评估中，模型需根据单个用户提示自主完成任务，其结果可能无法代表交互式编码中的令牌使用情况。有关调整努力水平的更多信息，请参阅 迁移指南 。

#### Footnotes 脚注

<sup>1</sup> This is a [model-level change](https://platform.claude.com/docs/en/build-with-claude/vision) rather than an API parameter, so images users send to Claude will simply be processed at higher fidelity. Because higher-resolution images consume more tokens, users who don’t require the extra detail can downsample images before sending them to the model.1 这是一项 [模型级别的更改](https://platform.claude.com/docs/en/build-with-claude/vision) ，而非 API 参数，因此用户发送给 Claude 的图像将直接以更高的保真度进行处理。由于高分辨率图像会消耗更多的 token，不需要额外细节的用户可以在将图像发送给模型前对其进行下采样。

- For GPT-5.4 and Gemini 3.1 Pro, we compared against the best reported model version available via API in the charts and table.对于 GPT-5.4 和 Gemini 3.1 Pro，我们将其与图表和表格中通过 API 可获取的最佳已报告模型版本进行了对比。
- MCP-Atlas: The Opus 4.6 score has been updated to reflect revised grading methodology from Scale AI.MCP-Atlas：已更新 Opus 4.6 分数，以反映 Scale AI 修订后的评分方法。
- SWE-bench Verified, Pro, and Multilingual: Our memorization screens flag a subset of problems in these SWE-bench evals. Excluding any problems that show signs of memorization, Opus 4.7’s margin of improvement over Opus 4.6 holds.SWE-bench 验证版、专业版和多语言版：我们的记忆筛查工具会标记这些 SWE-bench 评估中的部分题目。排除任何显示出记忆迹象的题目后，Opus 4.7 相较于 Opus 4.6 的性能提升幅度依然成立。
- Terminal-Bench 2.0: We used the Terminus-2 harness with thinking disabled. All experiments used 1× guaranteed/3× ceiling resource allocation averaged over five attempts per task.Terminal-Bench 2.0：我们使用了禁用思考功能的 Terminus-2 测试框架。所有实验均采用 1 倍保证/3 倍上限资源分配方案，每个任务的五次尝试结果取平均值。
- CyberGym: Opus 4.6’s score has been updated from the originally reported 66.6 to 73.8, as we updated our harness parameters to better elicit cyber capability.赛博健身馆：Opus 4.6 的评分已从最初公布的 66.6 分更新为 73.8 分，原因是我们更新了测试框架参数，以更好地激发赛博能力。
- SWE-bench Multimodal: We used an internal implementation for both Opus 4.7 and Opus 4.6. Scores are not directly comparable to public leaderboard scores.SWE-bench 多模态：我们为 Opus 4.7 和 Opus 4.6 均采用了内部实现。其分数无法与公开排行榜上的分数直接进行比较。