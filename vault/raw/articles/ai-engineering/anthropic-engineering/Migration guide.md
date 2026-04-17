---
title: "Migration guide"
source: "https://platform.claude.com/docs/en/about-claude/models/migration-guide#migrating-to-claude-opus-4-7"
author:
published:
created: 2026-04-17
description: "Guide for migrating to Claude Opus 4.7 and Claude 4.6 models from previous Claude versions"
tags:
  - "clippings"
---
This guide covers migrating [Messages API](https://platform.claude.com/docs/en/build-with-claude/working-with-messages) code. If you use [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview), no changes beyond updating model name are required.本指南涵盖了 [消息 API](https://platform.claude.com/docs/en/build-with-claude/working-with-messages) 代码的迁移。如果你使用 [Claude 托管智能体](https://platform.claude.com/docs/en/managed-agents/overview) ，只需更新模型名称，无需进行其他更改。

## Migrating to Claude Opus 4.7 迁移至 Claude Opus 4.7

Claude Opus 4.7 is our most capable generally available model to date. It is highly autonomous and performs exceptionally well on long-horizon agentic work, knowledge work, vision tasks, and memory tasks. Claude Opus 4.7 should have strong out-of-the-box performance on existing Claude Opus 4.6 prompts and evals at the same `$5 / $25` per MTok pricing, but there are a handful of behavioral and API changes worth knowing about as you migrate. It supports the same set of features as Claude Opus 4.6, including the [1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows) at standard API pricing with no long-context premium, 128k max output tokens, [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking), prompt caching, batch processing, the Files API, PDF support, vision, and the full set of server-side and client-side tools (bash, code execution, computer use, text editor, web search, web fetch, MCP connector, memory).Claude Opus 4.7是我们目前功能最强大的通用模型。它具备高度的自主性，在长周期智能体任务、知识类任务、视觉任务和记忆任务中表现尤为出色。在相同的每百万令牌 `$5 / $25` 定价下，Claude Opus 4.7在现有的Claude Opus 4.6提示词和评估任务上应具备出色的开箱即用性能，但在迁移过程中有一些行为和API变更值得了解。它支持与Claude Opus 4.6相同的功能集，包括标准API定价下 [100万令牌上下文窗口](https://platform.claude.com/docs/en/build-with-claude/context-windows) （无长上下文额外费用）、12.8万最大输出令牌、 [自适应思考](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking) 、提示词缓存、批处理、文件API、PDF支持、视觉功能，以及全套服务端和客户端工具（bash、代码执行、计算机操作、文本编辑器、网络搜索、网络获取、MCP连接器、内存）。

**Automate this migration with the Claude API skill.** In Claude Code, run `/claude-api migrate` to invoke the bundled [Claude API skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model):**使用 Claude API 技能自动完成此迁移。** 在 Claude Code 中，运行 `/claude-api migrate` 以调用内置的 [Claude API 技能](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model) ：

```
/claude-api migrate this project to claude-opus-4-7/claude-api migrate 将此项目迁移至 claude-opus-4-7
```

The skill applies the model ID swap, breaking parameter changes, prefill replacement, and effort calibration described below across your codebase, then produces a checklist of items to verify manually. It asks you to confirm the migration scope (entire working directory, a subdirectory, or a specific file list) before editing any files.该工具会在你的整个代码库中应用下述的模型 ID 替换、参数修改拆解、预填充替换以及效果校准操作，随后生成一份需人工核查的清单。在编辑任何文件之前，它会让你确认迁移范围（整个工作目录、某个子目录还是特定文件列表）。

### Update your model name 更新你的模型名称

```
# Opus migration
model = "claude-opus-4-6"  # Before
model = "claude-opus-4-7"  # After
```

### Breaking changes 破坏性变更

1. **Extended thinking removed:** `thinking: {type: "enabled", budget_tokens: N}` is no longer supported on Claude Opus 4.7 or later models and returns a 400 error. Switch to [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`) and use the [effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort) to control thinking depth. Adaptive thinking is **off by default** on Claude Opus 4.7: requests with no `thinking` field run without thinking, matching Opus 4.6 behavior. Set `thinking: {type: "adaptive"}` explicitly to enable it.**已移除扩展思维功能：** `thinking: {type: "enabled", budget_tokens: N}` 不再受 Claude Opus 4.7 及更高版本模型支持，调用会返回 400 错误。请切换至 [自适应思维](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking) （ `thinking: {type: "adaptive"}` ），并使用 [effort 参数](https://platform.claude.com/docs/en/build-with-claude/effort) 控制思维深度。在 Claude Opus 4.7 中，自适应思维 **默认处于关闭状态** ：未包含 `thinking` 字段的请求将不进行思维推理，行为与 Opus 4.6 一致。需显式设置 `thinking: {type: "adaptive"}` 以启用该功能。
	Before (Claude Opus 4.6): 之前（Claude Opus 4.6）：
	```
	client.messages.create(
	    model="claude-opus-4-6",
	    max_tokens=64000,
	    thinking={"type": "enabled", "budget_tokens": 32000},
	    messages=[{"role": "user", "content": "..."}],
	)
	```
	After (Claude Opus 4.7): （Claude Opus 4.7 之后）：
	```
	client.messages.create(
	    model="claude-opus-4-7",
	    max_tokens=64000,
	    thinking={"type": "adaptive"},
	    output_config={"effort": "high"},  # or "max", "xhigh", "medium", "low"
	    messages=[{"role": "user", "content": "..."}],
	)
	```
	Adaptive thinking is steerable through prompting. For guidance on tuning when the model over- or under-thinks, see [Calibrating effort and thinking depth](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#calibrating-effort-and-thinking-depth).通过提示可以控制自适应思维。有关在模型思考过度或思考不足时进行调整的指导，请参阅 [校准努力程度与思考深度](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#calibrating-effort-and-thinking-depth) 。
2. **Sampling parameters removed:** Setting `temperature`, `top_p`, or `top_k` to any non-default value on Claude Opus 4.7 returns a 400 error. The safest migration path is to omit these parameters entirely from request payloads. Prompting is the recommended way to guide model behavior on Claude Opus 4.7. If you were using `temperature = 0` for determinism, note that it never guaranteed identical outputs on prior models.**已移除的采样参数：** 在 Claude Opus 4.7 上，将 `temperature` 、 `top_p` 或 `top_k` 设置为任何非默认值都会返回 400 错误。最安全的迁移方式是从请求负载中完全省略这些参数。提示工程是在 Claude Opus 4.7 上引导模型行为的推荐方式。如果您曾使用 `temperature = 0` 来保证结果确定性，请注意，在之前的模型中，该设置从未保证输出完全一致。
3. **Thinking content omitted by default:** Thinking blocks still appear in the response stream on Claude Opus 4.7, but their `thinking` field is empty unless you explicitly opt in. This is a silent change from Claude Opus 4.6, where the default was to return summarized thinking text. To restore summarized thinking content on Claude Opus 4.7, set `thinking.display` to `"summarized"`:**默认省略思考内容：** Claude Opus 4.7 的响应流中仍会显示思考块，但除非你明确选择启用，否则它们的 `thinking` 字段为空。这是 Claude Opus 4.6 的一项隐性变更，在 4.6 版本中默认会返回摘要化的思考文本。要在 Claude Opus 4.7 上恢复摘要化的思考内容，请将 `thinking.display` 设置为 `"summarized"` ：
	```
	thinking = {
	    "type": "adaptive",
	    "display": "summarized",
	}
	```
	The default is `"omitted"` on Claude Opus 4.7. If your product streams reasoning to users, the new default appears as a long pause before output begins; set `display: "summarized"` to restore visible progress during thinking. See [Extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking#controlling-thinking-display) for details.在 Claude Opus 4.7 中，默认值为 `"omitted"` 。如果你的产品向用户展示推理过程，新的默认值会表现为输出开始前出现长时间停顿；请设置 `display: "summarized"` 以在思考过程中恢复可见的进度。有关详细信息，请参阅 [扩展思考](https://platform.claude.com/docs/en/build-with-claude/extended-thinking#controlling-thinking-display) 。
4. **Updated token counting:** Claude Opus 4.7 uses a new tokenizer, contributing to its improved performance on a wide range of tasks. This new tokenizer may use roughly 1x to 1.35x as many tokens when processing text compared to previous models (up to ~35% more, varying by content), and [`/v1/messages/count_tokens`](https://platform.claude.com/docs/en/build-with-claude/token-counting) will return a different number of tokens for Claude Opus 4.7 than it did for Claude Opus 4.6. The token efficiency of Claude Opus 4.7 can vary by workload shape. Prompting interventions, `task_budget`, and `effort` can help control costs and ensure appropriate token usage. Keep in mind that these controls may trade off model intelligence. We suggest updating your `max_tokens` parameters to give additional headroom, including compaction triggers. Claude Opus 4.7 provides a 1M context window at standard API pricing with no long-context premium.**更新后的令牌计数：** Claude Opus 4.7 采用了全新的分词器，这使其在各类任务上的性能得到提升。与前代模型相比，这款新分词器处理文本时使用的令牌数量约为其 1 至 1.35 倍（最多多 35% 左右，具体因内容而异），且 [`/v1/messages/count_tokens`](https://platform.claude.com/docs/en/build-with-claude/token-counting) 为 Claude Opus 4.7 返回的令牌数量与 Claude Opus 4.6 不同。Claude Opus 4.7 的令牌效率会因工作负载类型而异。提示干预、 `task_budget` 和 `effort` 有助于控制成本并确保合理的令牌使用。需注意，这些控制措施可能会牺牲模型的智能表现。建议更新 `max_tokens` 参数以预留额外空间，包括压缩触发条件。Claude Opus 4.7 支持 100 万上下文窗口，标准 API 定价且无长上下文额外费用。
5. **Prefill removal (carried over from Opus 4.6):** Prefilling assistant messages returns a 400 error on Claude Opus 4.7. Use [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), system prompt instructions, or `output_config.format` instead.**预填充移除（延续自 Opus 4.6）：** 在 Claude Opus 4.7 中，预填充助手消息会返回 400 错误。请改用 [结构化输出](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) 、系统提示指令或 `output_config.format` 。

### Choosing an effort level 选择投入级别

The [effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort) allows you to tune Claude's intelligence vs. token spend, trading off capability for faster speed and lower costs. Start with the new `xhigh` effort level for coding and agentic use cases, and use a minimum of `high` effort for most intelligence-sensitive use cases. Experiment with other effort levels to further tune token usage and intelligence:[效能参数](https://platform.claude.com/docs/en/build-with-claude/effort) 可用于调整 Claude 的智能水平与令牌消耗之间的平衡，以牺牲部分能力为代价换取更快的速度和更低的成本。对于编码和智能体相关用例，建议从新的 `xhigh` 效能级别开始；对于大多数对智能性敏感的用例，至少使用 `high` 效能级别。可尝试其他效能级别，进一步优化令牌使用和智能性：

- **`max`:** Max effort can deliver performance gains in some use cases, but may show diminishing returns from increased token usage. This setting can also sometimes be prone to overthinking. We recommend testing max effort for intelligence-demanding tasks.**`max` ：** 最大努力在某些用例中能带来性能提升，但随着令牌使用量增加，可能会出现收益递减的情况。此设置有时也容易出现过度思考的问题。我们建议针对需要高智能的任务测试最大努力值。
- **`xhigh` (new):** Extra high effort is the best setting for most coding and agentic use cases.**`xhigh` （新增）：** 超高算力模式是大多数编程和智能体使用场景的最佳设置。
- **`high`:** This setting balances token usage and intelligence. For most intelligence-sensitive use cases, we recommend a minimum of `high` effort.**`high` ：** 此设置会平衡令牌使用与智能性。对于大多数对智能性敏感的使用场景，我们建议至少使用 `high` 力度。
- **`medium`:** Good for cost-sensitive use cases that need to reduce token usage while trading off intelligence.**`medium`:** 适用于需要在降低智能程度的同时减少令牌使用量的成本敏感型场景。
- **`low`:** Reserve for short, scoped tasks and latency-sensitive workloads that are not intelligence-sensitive.**`low` ：** 适用于非智能敏感的短期、范围明确的任务和延迟敏感的工作负载。

We expect effort to be more important for this model than for any prior Opus, and recommend experimenting with it actively when you upgrade.我们认为，与以往任何 Opus 模型相比，这个模型对效果的要求更高，建议你在升级时积极对其进行测试。

### Behavior changes 行为变更

Claude Opus 4.7 has several behavioral differences from Claude Opus 4.6 that are not API breaking changes but may require prompt updates or scaffolding removal.Claude Opus 4.7 与 Claude Opus 4.6 相比存在若干行为差异，这些差异不会破坏 API，但可能需要更新提示词或移除脚手架。

1. **Response length varies by use case:** Claude Opus 4.7 calibrates response length to how complex it judges the task to be, rather than defaulting to a fixed verbosity. This usually means shorter answers on simple lookups and much longer ones on open-ended analysis. If your product depends on a certain style or verbosity of output, you may need to tune your prompts. As an example, to decrease verbosity, you might add: "Provide concise, focused responses. Skip non-essential context, and keep examples minimal." If you see specific examples of kinds of verbosity (i.e. over-explaining), you can add additional instructions in your prompt to prevent them. Positive examples showing how Claude can communicate with the appropriate level of concision tend to be more effective than negative examples or instructions that tell the model what not to do.**响应长度因使用场景而异：** Claude Opus 4.7 会根据其判断的任务复杂程度来调整响应长度，而非默认固定的详细程度。通常情况下，简单查询的回答会更简短，而开放式分析的回答则会更长。如果你的产品依赖特定风格或详细程度的输出，可能需要调整提示词。例如，若想降低详细程度，可添加：“提供简洁、有针对性的响应。跳过非必要的上下文，示例保持最少。”如果发现模型存在特定的详细程度问题（即过度解释），可在提示词中补充额外指令加以避免。展示 Claude 如何以恰当简洁程度沟通的正面示例，往往比负面示例或告知模型“不该做什么”的指令更有效。
2. **More literal instruction following:** Claude Opus 4.7 interprets prompts more literally and explicitly than Claude Opus 4.6, particularly at lower effort levels. It will not silently generalize an instruction from one item to another, and it will not infer requests you didn't make. The upside of this literalism is precision and less thrash. It generally performs better for API use cases with carefully tuned prompts, structured extraction, and pipelines where you want predictable behavior. A prompt and harness review may be especially helpful for migration to Claude Opus 4.7.**更严格的指令遵循：** Claude Opus 4.7 比 Claude Opus 4.6 更严格、更明确地解读提示词，尤其是在低算力级别下。它不会将一个指令的要求无声地泛化到另一个内容上，也不会推断你未提出的需求。这种严格解读的优势在于精准性更高，且更少出现无效输出。对于经过精细调优提示词的 API 用例、结构化提取任务以及需要可预测行为的流水线，它的整体表现通常更优。迁移至 Claude Opus 4.7 时，对提示词和测试框架的审查可能会特别有帮助。
3. **More direct tone:** As with any new model, prose style on long-form writing may shift. Claude Opus 4.7 is more direct and opinionated, with less validation-forward phrasing and fewer emoji than Claude Opus 4.6's warmer style. If your product relies on a specific voice, re-evaluate style prompts against the new baseline.**更直接的语气：** 与任何新模型一样，长篇写作的散文风格可能会发生变化。Claude Opus 4.7 比 Claude Opus 4.6 更温和的风格更直接、更具主见，验证前置性措辞更少，表情符号也更少。如果你的产品依赖特定的语气，请对照新基准重新评估风格提示词。
4. **Built-in progress updates in agentic traces:** Claude Opus 4.7 provides more regular, higher-quality updates to the user throughout long agentic traces. If you've added scaffolding to force interim status messages ("After every 3 tool calls, summarize progress"), try removing it. If you find that the length or contents of Claude Opus 4.7's user-facing updates are not well-calibrated to your use case, explicitly describe what these updates should look like in the prompt and provide examples.**智能体追踪中的内置进度更新：** Claude Opus 4.7 在长时间的智能体追踪过程中，能为用户提供更规律、更高质量的更新。如果你曾添加过框架来强制输出临时状态信息（例如“每调用3次工具后总结一次进度”），可以尝试移除该设置。若你发现 Claude Opus 4.7 面向用户的更新内容长度或形式与你的使用场景不匹配，可在提示词中明确描述这些更新的要求，并附上示例。
5. **Fewer subagents spawned by default:** Claude Opus 4.7 tends to spawn fewer subagents by default. However, this behavior is steerable through prompting; give Claude Opus 4.7 explicit guidance around when subagents are desirable.**默认生成的子智能体数量更少：** Claude Opus 4.7 默认情况下生成的子智能体数量通常更少。不过，可通过提示词来控制这一行为；需为 Claude Opus 4.7 提供明确的指导，说明子智能体在何种情况下适用。
6. **Stricter effort calibration:** Meaningfully changing from Claude Opus 4.6, Claude Opus 4.7 respects [effort levels](https://platform.claude.com/docs/en/build-with-claude/effort) strictly, especially at the low end. At `low` and `medium`, the model scopes its work to what was asked rather than going above and beyond. This is good for latency and cost, but on moderately complex tasks running at `low` effort there is some risk of under-thinking. If you observe shallow reasoning on complex problems, raise effort to `high` or `xhigh` rather than prompting around it. If you need to keep effort at `low` for latency, add targeted guidance: "This task involves multi-step reasoning. Think carefully through the problem before responding." See [Recommended effort levels for Claude Opus 4.7](https://platform.claude.com/docs/en/build-with-claude/effort#recommended-effort-levels-for-claude-opus-4-7).**更严格的努力程度校准：** 与 Claude Opus 4.6 有实质性不同，Claude Opus 4.7 会严格遵循 [努力等级](https://platform.claude.com/docs/en/build-with-claude/effort) ，尤其是在低等级下。在 `low` 和 `medium` 等级时，模型会将工作范围限定在所要求的内容内，而非额外做更多努力。这有利于降低延迟和成本，但在 `low` 努力等级下执行中等复杂度任务时，存在思考不足的风险。若发现模型对复杂问题的推理较为浅显，请将努力等级提升至 `high` 或 `xhigh` ，而非通过提示词调整来规避。若因延迟要求需将努力等级维持在 `low` ，可添加针对性引导：“本任务涉及多步骤推理。请在回复前仔细思考整个问题。”详见 [Claude Opus 4.7 推荐努力等级](https://platform.claude.com/docs/en/build-with-claude/effort#recommended-effort-levels-for-claude-opus-4-7) 。
7. **Fewer tool calls by default:** Claude Opus 4.7 has a tendency to use tools less often than Claude Opus 4.6 and to use reasoning more. This produces better results in most cases. However, increasing the effort setting is a useful lever to increase the level of tool usage, especially in knowledge work. `high` or `xhigh` effort settings show substantially more tool usage in agentic search and coding. For scenarios where you want more tool use, you can also adjust your prompt to explicitly instruct the model about when and how to properly use its tools.**默认减少工具调用：** Claude Opus 4.7 相比 Claude Opus 4.6，更倾向于减少工具使用、增加推理运用。这在大多数情况下能产生更优的结果。不过，调高力度参数是提升工具调用频率的有效手段，在知识类工作中尤为如此。 `high` 或 `xhigh` 力度参数下，智能体搜索和编码场景中的工具调用会显著增多。若希望模型更多地使用工具，也可以调整提示词，明确指示模型何时以及如何正确使用工具。
8. **Real-time cybersecurity safeguards:** Newly added in Claude Opus 4.7, requests that involve prohibited or high-risk topics may lead to refusals. For legitimate security work such as penetration testing, vulnerability research, or red-teaming, apply to the [Cyber Verification Program](https://claude.com/form/cyber-use-case) to request reduced restrictions. See [Safeguards, warnings, and appeals](https://support.claude.com/en/articles/8241253-safeguards-warnings-and-appeals) for background.**实时网络安全防护措施：** 为 Claude Opus 4.7 新增功能，涉及违禁或高风险主题的请求可能会被拒绝。对于渗透测试、漏洞研究或红队演练等合法安全工作，请申请 [网络验证计划](https://claude.com/form/cyber-use-case) 以申请放宽限制。相关背景信息请参阅 [防护措施、警告与申诉](https://support.claude.com/en/articles/8241253-safeguards-warnings-and-appeals) 。
9. **High-resolution image support:** Claude Opus 4.7 is the first Claude model with high-resolution image support, with a maximum image resolution of 2576 pixels on the long edge (up from 1568 pixels on prior models). This unlocks gains on vision-heavy workloads and is particularly valuable for computer use, screenshot understanding, and document analysis. High-resolution support is automatic and requires no beta header or client-side opt-in. Full-resolution images can use up to approximately 3x more image tokens than on prior models (up to 4,784 tokens per image, compared to the previous cap of roughly 1,600 tokens per image), so re-budget `max_tokens` and cost expectations for image-heavy workloads, or downsample before sending if you do not need the additional fidelity. Pointing and bounding-box coordinates returned by the model are 1 **高分辨率图像支持：** Claude Opus 4.7 是首款支持高分辨率图像的 Claude 模型，长边最大图像分辨率达 2576 像素（此前模型为 1568 像素）。这为视觉密集型工作负载带来了性能提升，尤其适用于计算机操作、截图理解和文档分析场景。高分辨率支持为自动启用，无需测试版请求头或客户端主动开启。全分辨率图像可使用的图像令牌数量最多比此前模型多约 3 倍（单张图像可达 4784 个令牌，此前上限约为单张图像 1600 个令牌），因此针对图像密集型工作负载需重新规划 `max_tokens` 配置和成本预期，若无需更高保真度，发送前可对图像进行降采样。模型返回的指向和边界框坐标为 1 with actual image pixels on Claude Opus 4.7, so no scale-factor conversion is required. See [High-resolution image support on Claude Opus 4.7](https://platform.claude.com/docs/en/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7) for details.在 Claude Opus 4.7 上可直接使用实际图像像素，因此无需进行缩放因子转换。有关详细信息，请参阅 [Claude Opus 4.7 上的高分辨率图像支持](https://platform.claude.com/docs/en/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7) 。

These are not required but will improve your experience:这些并非必需，但能提升你的使用体验：

1. **Re-evaluate `max_tokens`:** Because the same text produces a higher token count on Claude Opus 4.7, we suggest updating your `max_tokens` parameters to give additional headroom, including compaction triggers. Prompting interventions, [`task_budget`](https://platform.claude.com/docs/en/build-with-claude/task-budgets), and [`effort`](https://platform.claude.com/docs/en/build-with-claude/effort) can help control costs and ensure appropriate token usage.**重新评估 `max_tokens` ：** 由于同一段文本在 Claude Opus 4.7 上生成的令牌数量更高，我们建议更新你的 `max_tokens` 参数以预留额外空间，包括压缩触发条件。提示干预、 [`task_budget`](https://platform.claude.com/docs/en/build-with-claude/task-budgets) 以及 [`effort`](https://platform.claude.com/docs/en/build-with-claude/effort) 有助于控制成本并确保令牌使用合理。
2. **Audit token-count expectations:** Any code path that estimates tokens client-side or assumes a fixed token-to-character ratio should be re-tested against Claude Opus 4.7. Use the [Token counting endpoint](https://platform.claude.com/docs/en/build-with-claude/token-counting) to verify.**审计令牌计数预期：** 任何在客户端估算令牌或假设固定令牌与字符比例的代码路径，都应针对 Claude Opus 4.7 重新测试。请使用 [令牌计数端点](https://platform.claude.com/docs/en/build-with-claude/token-counting) 进行验证。
3. **Adopt [task budgets](https://platform.claude.com/docs/en/build-with-claude/task-budgets) (beta):** Claude Opus 4.7 introduces task budgets. These budgets let you inform Claude how many tokens it has for a full agentic loop, including thinking, tool calls, tool results, and final output. The model sees a running countdown and uses it to prioritize work and finish the task gracefully as the budget is consumed. To use, set the beta header `task-budgets-2026-03-13` and add the following to your output config:**采用 [任务预算](https://platform.claude.com/docs/en/build-with-claude/task-budgets) （测试版）：** Claude Opus 4.7 推出了任务预算功能。借助这些预算，你可以告知 Claude 完成一整个智能体循环可用的令牌数量，其中包括思考、工具调用、工具结果以及最终输出。模型会查看倒计时，并利用它来优先处理任务，在预算耗尽时优雅地完成任务。要使用此功能，请设置测试版请求头 `task-budgets-2026-03-13` ，并在输出配置中添加以下内容：
	```
	output_config = {
	    "effort": "high",
	    "task_budget": {"type": "tokens", "total": 128000},
	}
	```
	You may need to experiment with different task budgets for your use case. If the model is given a task budget that is too restrictive for a given task, it may complete the task less thoroughly, referencing its budget as the constraint. For open-ended agentic tasks where quality matters more than speed, do not set a task budget; reserve task budgets for workloads where you need the model to scope its work to a token allowance. The minimum value for a task budget is 20k tokens.你可能需要针对你的具体用例尝试不同的任务预算。如果为模型分配的任务预算对某一特定任务而言限制过严，模型可能会因受预算约束而无法彻底完成任务。对于开放式智能体任务，质量比速度更重要时，请勿设置任务预算；仅在需要模型将工作范围限定在令牌额度内的工作负载中使用任务预算。任务预算的最小值为 20,000 个令牌。
	This is not a hard cap; it's a suggestion that the model is aware of. This is distinct from `max_tokens`, which is a hard per-request cap on generated tokens (`max_tokens` is not passed to the model, and the model is not aware of it), while `task_budget` is an advisory cap across the full agentic loop. Use `task_budget` when you want the model to self-moderate, and `max_tokens` as a hard per-request ceiling to cap usage.这并非硬性上限，而是模型会知晓的一个建议值。它与 `max_tokens` 不同，max\_tokens是对生成令牌的每请求硬性上限（ `max_tokens` 不会传递给模型，模型也无法感知到它）；而 `task_budget` 则是适用于整个智能体循环的建议性上限。当你希望模型进行自我节制时，请使用 `task_budget` ；而将 `max_tokens` 作为控制使用量的每请求硬性上限。
4. **Set a large `max_tokens` at `max` or `xhigh` effort:** If you are running Claude Opus 4.7 at `max` or `xhigh` effort, set a large max output token budget so the model has room to think and act across its subagents and tool calls. We recommend starting at 64k tokens and tuning from there.**在 `max` 或 `xhigh` 算力下设置较大的 `max_tokens` ：** 如果你以 `max` 或 `xhigh` 算力运行 Claude Opus 4.7，请设置较大的最大输出令牌预算，以便模型有足够的空间在其子智能体和工具调用中进行思考和行动。我们建议从 64000 个令牌开始，再据此进行调整。
5. **Downsample images if high resolution is unnecessary:** Claude Opus 4.7 supports images up to 2576px / 3.75MP. High-res images use more tokens. If the additional image fidelity is unnecessary, downsample images before sending to Claude to avoid token-usage increases. See [Images and vision](https://platform.claude.com/docs/en/build-with-claude/vision).**若无需高分辨率，请对图像进行下采样：** Claude Opus 4.7 支持的图像最大分辨率为 2576 像素 / 375 万像素。高分辨率图像会消耗更多令牌。如果无需额外的图像保真度，请在发送给 Claude 前对图像进行下采样，以避免令牌使用量增加。详见 [图像与视觉](https://platform.claude.com/docs/en/build-with-claude/vision) 。

### Migration checklist 迁移清单

- Update model name from `claude-opus-4-6` to `claude-opus-4-7` (or update aliases).将模型名称从 `claude-opus-4-6` 更新为 `claude-opus-4-7` （或更新别名）。
- Remove `temperature`, `top_p`, and `top_k` from request payloads.从请求负载中移除 `temperature` 、 `top_p` 和 `top_k` 。
- Replace `thinking: {type: "enabled", budget_tokens: N}` with `thinking: {type: "adaptive"}` plus the [effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort).将 `thinking: {type: "enabled", budget_tokens: N}` 替换为 `thinking: {type: "adaptive"}` 以及 [effort 参数](https://platform.claude.com/docs/en/build-with-claude/effort) 。
- Remove any assistant-message prefills.移除所有助手消息的预填充内容。
- If your UI displays thinking content, explicitly opt in to thinking summarization.如果你的界面显示思考内容，请明确选择启用思考摘要功能。
- Re-benchmark end-to-end cost and latency under the updated tokenization.在更新后的分词规则下，重新对端到端成本和延迟进行基准测试。
- Re-tune `max_tokens` to account for the updated tokenization.重新调整 `max_tokens` 以适应更新后的分词规则。
- Re-test any client-side token-count estimations.重新测试任何客户端的令牌数估算。
- If your application sends images, re-budget for [high-resolution image support](https://platform.claude.com/docs/en/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7) (up to approximately 3x more image tokens per full-resolution image). Downsample before sending if you do not need the additional fidelity. If you consume pointing or bounding-box coordinates from the model, remove any scale-factor conversion; coordinates are 1 如果你的应用需要发送图片，请重新为 [高分辨率图片支持](https://platform.claude.com/docs/en/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7) 分配预算（每张全分辨率图片的图片令牌数量最多增加约3倍）。如果不需要额外的高保真度，请在发送前对图片进行下采样。如果要从模型中获取指向坐标或边界框坐标，请移除任何比例因子转换；坐标为1 with actual image pixels on Claude Opus 4.7.在 Claude Opus 4.7 中对应实际图像像素。
- Review prompts for the behavior changes above (response length, literalism, tone, progress updates, subagents, effort calibration, tool triggering, cyber safeguards, high-resolution image handling).针对上述行为变化（回复长度、字面主义、语气、进度更新、子智能体、工作量校准、工具触发、网络防护、高分辨率图像处理），查看相关提示词。
- Re-baseline response length with existing length-control prompts removed, then tune explicitly.移除现有的长度控制提示词后重新设定回复长度基准，然后进行显式调优。
- If using `xhigh` or `max` effort, raise `max_tokens` to at least 64k as a starting point.如果使用 `xhigh` 或 `max` 级别的算力，建议将 `max_tokens` 至少提升至64k作为起点。
- Consider adopting task budgets (beta) for agentic workflows.考虑为智能体工作流采用任务预算（测试版）。
- If your product does legitimate security work, apply to the [Cyber Verification Program](https://claude.com/form/cyber-use-case) for access to lower restrictions on cyber content.如果你的产品开展合法的安全相关工作，可申请 [网络验证计划](https://claude.com/form/cyber-use-case) 以获得更宽松的网络内容访问限制。

## Migrating to Claude Opus 4.7 from Opus 4.5 or earlier从 Opus 4.5 或更早版本迁移到 Claude Opus 4.7

If you are migrating from Claude Opus 4.5, Opus 4.1, or an earlier model directly to Claude Opus 4.7, apply **all of the [Opus 4.7 changes above](#migrating-to-claude-opus-4-7)** plus the cumulative changes in this section that took effect between Opus 4.5 and Opus 4.7. If you are migrating from Opus 4.6, you only need the [Opus 4.7 section above](#migrating-to-claude-opus-4-7).如果你直接从 Claude Opus 4.5、Opus 4.1 或更早版本迁移到 Claude Opus 4.7，需应用 **上述所有 [Opus 4.7 的变更](#migrating-to-claude-opus-4-7)** ，再加上本节中自 Opus 4.5 至 Opus 4.7 生效的累计变更。若你从 Opus 4.6 迁移，仅需上述 [Opus 4.7 相关部分](#migrating-to-claude-opus-4-7) 即可。

### Update your model name 更新你的模型名称

```
# Opus migration
model = "claude-opus-4-5"  # Before
model = "claude-opus-4-7"  # After
```

### Breaking changes 破坏性变更

1. **Prefill removal** is covered in the [Opus 4.7 breaking changes](#breaking-changes) above.**预填充移除** 包含在上面的 [Opus 4.7 重大变更](#breaking-changes) 中。
2. **Tool parameter quoting:** Claude Opus 4.6 and later models may produce slightly different JSON string escaping in tool call arguments (e.g., different handling of Unicode escapes or forward slash escaping). If you parse tool call `input` as a raw string rather than using a JSON parser, verify your parsing logic. Standard JSON parsers (like `json.loads()` or `JSON.parse()`) handle these differences automatically.**工具参数引用：** Claude Opus 4.6 及更高版本的模型在工具调用参数中可能会生成略有不同的 JSON 字符串转义方式（例如，对 Unicode 转义或正斜杠转义的处理方式不同）。如果将工具调用的 `input` 作为原始字符串解析，而不使用 JSON 解析器，请验证你的解析逻辑。标准 JSON 解析器（如 `json.loads()` 或 `JSON.parse()` ）会自动处理这些差异。

These changes improve your experience on Opus 4.7. Items marked **(required on Opus 4.7)** were optional recommendations when Opus 4.6 launched but are now mandatory; the rest remain recommended.这些改进优化了你在 Opus 4.7 上的使用体验。标有 **（Opus 4.7 版本必需）** 的项目在 Opus 4.6 推出时为可选推荐，如今已成为强制要求；其余项目仍为推荐项。

1. **Migrate to adaptive thinking (required on Opus 4.7):** `thinking: {type: "enabled", budget_tokens: N}` returns a 400 error on Claude Opus 4.7. Switch to `thinking: {type: "adaptive"}` and use the [effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort) to control thinking depth. See [Adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking).**迁移至自适应思维（Opus 4.7 必需）：** `thinking: {type: "enabled", budget_tokens: N}` 在 Claude Opus 4.7 上会返回 400 错误。请切换至 `thinking: {type: "adaptive"}` 并使用 [effort 参数](https://platform.claude.com/docs/en/build-with-claude/effort) 控制思维深度。详见 [自适应思维](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking) 。
	```
	response = client.beta.messages.create(
	    model="claude-opus-4-5",
	    max_tokens=16000,
	    thinking={"type": "enabled", "budget_tokens": 32000},
	    betas=["interleaved-thinking-2025-05-14"],
	    messages=[...],
	)
	```
	Note that the migration also moves from `client.beta.messages.create` to `client.messages.create`. Adaptive thinking and effort are GA features and do not require the beta SDK namespace or any beta headers.请注意，此迁移还将从 `client.beta.messages.create` 改为 `client.messages.create` 。自适应思维和功能是 GA 功能，不需要 beta SDK 命名空间或任何 beta 头文件。
2. **Remove effort beta header:** The effort parameter is now GA. Remove `betas=["effort-2025-11-24"]` from your requests.**移除 effort beta 标头：** effort 参数现已正式发布。请从你的请求中移除 `betas=["effort-2025-11-24"]` 。
3. **Remove fine-grained tool streaming beta header:** Fine-grained tool streaming is now GA. Remove `betas=["fine-grained-tool-streaming-2025-05-14"]` from your requests.**移除细粒度工具流式测试版标头：** 细粒度工具流式现已正式发布。请从你的请求中移除 `betas=["fine-grained-tool-streaming-2025-05-14"]` 。
4. **Remove interleaved thinking beta header:** Adaptive thinking automatically enables interleaved thinking on Claude Opus 4.7, Opus 4.6, and Sonnet 4.6. Remove `betas=["interleaved-thinking-2025-05-14"]` from your requests. The header is still functional on Sonnet 4.6 with manual extended thinking, but manual mode is deprecated.**移除交错思考测试版标头：** 自适应思考会在 Claude Opus 4.7、Opus 4.6 和 Sonnet 4.6 上自动启用交错思考。请从你的请求中移除 `betas=["interleaved-thinking-2025-05-14"]` 。该标头在 Sonnet 4.6 的手动扩展思考模式下仍可使用，但手动模式已被弃用。
5. **Migrate to output\_config.format:** If using structured outputs, update `output_format={...}` to `output_config={"format": {...}}`. The old parameter remains functional but is deprecated and will be removed in a future model release.**迁移至 output\_config.format：** 若使用结构化输出，请将 `output_format={...}` 更新为 `output_config={"format": {...}}` 。旧参数仍可使用，但已弃用，将在未来的模型版本中移除。

### Migrating from Claude 4.1 or earlier从 Claude 4.1 或更早版本迁移

If you're migrating from Opus 4.1, Sonnet 4 (deprecated), or earlier models directly to Claude Opus 4.7, apply the Claude Opus 4.7 changes at the top of this guide and the cumulative changes above plus the additional changes in this section.如果要从 Opus 4.1、Sonnet 4（已弃用）或更早的模型直接迁移到 Claude Opus 4.7，请在本指南顶部应用 Claude Opus 4.7 的变更，同时应用上述所有累积变更以及本节中的额外变更。

```
# From Opus 4.1
model = "claude-opus-4-1-20250805"  # Before
model = "claude-opus-4-7"  # After

# From Sonnet 4
model = "claude-sonnet-4-20250514"  # Before
model = "claude-opus-4-7"  # After

# From Sonnet 3.7
model = "claude-3-7-sonnet-20250219"  # Before
model = "claude-opus-4-7"  # After
```

#### Additional breaking changes 其他重大变更

1. **Remove sampling parameters 移除采样参数**
	This is a breaking change when migrating from Claude 3.x models.从 Claude 3.x 模型迁移时，这是一项破坏性变更。
	Starting with Claude Opus 4.7, setting `temperature`, `top_p`, or `top_k` to any non-default value will return a 400 error. The safest migration path is to omit these parameters entirely from requests, and to use prompting to guide the model's behavior. If you were using `temperature = 0` for determinism, note that it never guaranteed identical outputs.从 Claude Opus 4.7 版本开始，将 `temperature` 、 `top_p` 或 `top_k` 设置为任何非默认值都会返回 400 错误。最安全的迁移方式是在请求中完全省略这些参数，并通过提示词来引导模型的行为。如果你曾使用 `temperature = 0` 来保证结果的确定性，请注意该设置从未确保输出完全一致。
	```
	# Before - This will error in Claude 4+ models
	response = client.messages.create(
	    model="claude-3-7-sonnet-20250219",
	    temperature=0.7,
	    top_p=0.9,  # Non-default sampling params return 400 on Opus 4.7
	    # ...
	)
	# After
	response = client.messages.create(
	    model="claude-opus-4-7",
	    # ...
	)
	```
2. **Update tool versions 更新工具版本**
	This is a breaking change when migrating from Claude 3.x models.从 Claude 3.x 模型迁移时，这是一项破坏性变更。
	Update to the latest tool versions. Remove any code using the `undo_edit` command.更新至最新的工具版本。删除所有使用 `undo_edit` 命令的代码。
	```
	# Before
	tools = [{"type": "text_editor_20250124", "name": "str_replace_editor"}]
	# After
	tools = [{"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"}]
	```
	- **Text editor:** Use `text_editor_20250728` and `str_replace_based_edit_tool`. See [Text editor tool documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool) for details.**文本编辑器：** 使用 `text_editor_20250728` 和 `str_replace_based_edit_tool` 。详细信息请参阅 [文本编辑器工具文档](https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool) 。
		- **Code execution:** Upgrade to `code_execution_20250825`. See [Code execution tool documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool#upgrade-to-latest-tool-version) for migration instructions.**代码执行：** 升级至 `code_execution_20250825` 。迁移说明请参阅 [代码执行工具文档](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool#upgrade-to-latest-tool-version) 。
3. **Handle the `refusal` stop reason 处理拒绝</b>停止原因**
	Update your application to [handle `refusal` stop reasons](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals):将你的应用程序更新为 [能够处理 `refusal` 停止原因](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals) ：
	```
	response = client.messages.create(...)
	if response.stop_reason == "refusal":
	    # Handle refusal appropriately
	    pass
	```
4. **Handle the `model_context_window_exceeded` stop reason 处理 `model_context_window_exceeded` 停止原因**
	Claude 4.5+ models return a `model_context_window_exceeded` stop reason when generation stops due to hitting the context window limit, rather than the requested `max_tokens` limit. Update your application to handle this new stop reason:Claude 4.5及以上模型在生成过程因触及上下文窗口限制而非请求的 `max_tokens` 限制而停止时，会返回 `model_context_window_exceeded` 停止原因。请更新你的应用程序以处理这一新的停止原因：
	```
	response = client.messages.create(...)
	if response.stop_reason == "model_context_window_exceeded":
	    # Handle context window limit appropriately
	    pass
	```
5. **Verify tool parameter handling (trailing newlines) 验证工具参数处理（尾随换行符）**
	Claude 4.5+ models preserve trailing newlines in tool call string parameters that were previously stripped. If your tools rely on exact string matching against tool call parameters, verify your logic handles trailing newlines correctly.Claude 4.5 及更高版本的模型会保留之前被去除的工具调用字符串参数中的尾随换行符。如果你的工具依赖对工具调用参数进行精确字符串匹配，请验证你的逻辑能否正确处理尾随换行符。
6. **Update your prompts for behavioral changes 针对行为变化更新你的提示词**
	Claude 4+ models have a more concise, direct communication style and require explicit direction. Review [prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) for optimization guidance.Claude 4+ 模型采用更简洁、直接的沟通风格，需要明确的指令。请查看 [提示词最佳实践](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) 以获取优化指导。
- **Remove legacy beta headers:** Remove `token-efficient-tools-2025-02-19` and `output-128k-2025-02-19`. All Claude 4+ models have built-in token-efficient tool use and these headers have no effect.**移除旧版 beta 标头：** 移除 `token-efficient-tools-2025-02-19` 和 `output-128k-2025-02-19` 。所有 Claude 4+ 模型均内置高效令牌工具调用功能，这些标头已无任何作用。

### Migration checklist (from Opus 4.5 or earlier)迁移清单（源自 Opus 4.5 或更早版本）

- Update model ID to `claude-opus-4-7` 将模型 ID 更新为 `claude-opus-4-7`
- Apply all [Opus 4.7 breaking changes](#migrating-to-claude-opus-4-7) (extended thinking removed, sampling parameters removed, thinking display omitted by default, updated tokenization) 应用所有 [Opus 4.7 破坏性变更](#migrating-to-claude-opus-4-7) （移除扩展思考、移除采样参数、默认隐藏思考展示、更新分词）
- **BREAKING:** Remove assistant message prefills (returns 400 error); use structured outputs or `output_config.format` instead **重要更新：** 移除助手消息预填充（返回400错误）；请改用结构化输出或 `output_config.format`
- **BREAKING on Opus 4.7:** Replace `thinking: {type: "enabled", budget_tokens: N}` with `thinking: {type: "adaptive"}` plus the [effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort) (returns 400 on Opus 4.7) **Opus 4.7 版本更新：** 将 `thinking: {type: "enabled", budget_tokens: N}` 替换为 `thinking: {type: "adaptive"}` 以及 [effort 参数](https://platform.claude.com/docs/en/build-with-claude/effort) （在 Opus 4.7 版本中返回 400 错误）
- Verify tool call JSON parsing uses a standard JSON parser 验证工具调用 JSON 解析是否使用标准 JSON 解析器
- Remove `effort-2025-11-24` beta header (effort is now GA) 移除 `effort-2025-11-24` 测试版标头（该功能现已正式发布）
- Remove `fine-grained-tool-streaming-2025-05-14` beta header 移除 `fine-grained-tool-streaming-2025-05-14` 测试版标头
- Remove `interleaved-thinking-2025-05-14` beta header (adaptive thinking enables interleaved thinking automatically) 移除 `interleaved-thinking-2025-05-14` 测试版标头（自适应思维可自动启用交替思维）
- Migrate `output_format` to `output_config.format` (if applicable) 将 `output_format` 迁移至 `output_config.format` （如适用）
- If migrating from Claude 4.1 or earlier: remove `temperature`, `top_p`, and `top_k` (non-default values return 400 on Opus 4.7) 若从 Claude 4.1 或更早版本迁移：请移除 `temperature` 、 `top_p` 和 `top_k` （非默认值在 Opus 4.7 上会返回 400 错误）
- If migrating from Claude 4.1 or earlier: update tool versions (`text_editor_20250728`, `code_execution_20250825`) 如果从 Claude 4.1 或更早版本迁移：请更新工具版本（ `text_editor_20250728` 、 `code_execution_20250825` ）
- If migrating from Claude 4.1 or earlier: handle `refusal` stop reason 若从 Claude 4.1 或更早版本迁移：处理拒绝</b>停止原因
- If migrating from Claude 4.1 or earlier: handle `model_context_window_exceeded` stop reason 若从 Claude 4.1 或更早版本迁移：处理 `model_context_window_exceeded` 停止原因
- If migrating from Claude 4.1 or earlier: verify tool string parameter handling for trailing newlines 如果从 Claude 4.1 或更早版本迁移：验证工具字符串参数对尾随换行符的处理方式
- If migrating from Claude 4.1 or earlier: remove legacy beta headers (`token-efficient-tools-2025-02-19`, `output-128k-2025-02-19`) 如果从 Claude 4.1 或更早版本迁移：请移除旧版测试版标头（ `token-efficient-tools-2025-02-19` 、 `output-128k-2025-02-19` ）
- Review and update prompts following [prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) 按照 [提示词最佳实践](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) 审核并更新提示词
- Test in development environment before production deployment 在生产环境部署前于开发环境中进行测试

---

## Migrating to Claude Sonnet 4.6 迁移至 Claude Sonnet 4.6

Claude Sonnet 4.6 combines strong intelligence with fast performance, featuring improved agentic search capabilities and free code execution when used with web search or web fetch. It is ideal for everyday coding, analysis, and content tasks.Claude Sonnet 4.6 融合了强大的智能与快速的性能，其特色是改进了的智能体搜索功能，且在配合网页搜索或网页抓取使用时支持免费代码执行。它非常适合日常编程、数据分析和内容创作类任务。

For a complete overview of capabilities, see the [models overview](https://platform.claude.com/docs/en/about-claude/models/overview).要了解所有功能的完整概览，请查看 [模型概览](https://platform.claude.com/docs/en/about-claude/models/overview) 。

Sonnet 4.6 pricing is $3 per million input tokens, $15 per million output tokens. See [Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing) for details.Sonnet 4.6 的定价为每百万输入标记 3 美元，每百万输出标记 15 美元。详情请查看 [Claude 定价](https://platform.claude.com/docs/en/about-claude/pricing) 。

**Update your model name: 更新你的模型名称：**

```
# From Sonnet 4.5
model = "claude-sonnet-4-5"  # Before
model = "claude-sonnet-4-6"  # After

# From Sonnet 4
model = "claude-sonnet-4-20250514"  # Before
model = "claude-sonnet-4-6"  # After
```

### Breaking changes 破坏性变更

#### When migrating from Sonnet 4.5 从 Sonnet 4.5 迁移时

1. **Prefilling assistant messages is no longer supported 不再支持预填充助手消息**
	This is a breaking change when migrating from Sonnet 4.5 or earlier.从 Sonnet 4.5 或更早版本迁移时，这是一项重大变更。
	Prefilling assistant messages returns a `400` error on Sonnet 4.6. Use [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), system prompt instructions, or `output_config.format` instead.预填充助手消息会在 Sonnet 4.6 上返回 `400` 错误。请改用 [结构化输出](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) 、系统提示指令或 `output_config.format` 。
	**Common prefill use cases and migrations:常见预填充用例及迁移方式：**
	- **Controlling output formatting** (forcing JSON/YAML output): Use [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) or tools with enum fields for classification tasks.**控制输出格式** （强制输出 JSON/YAML 格式）：在分类任务中使用 [结构化输出](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) 或带有枚举字段的工具。
		- **Eliminating preambles** (removing "Here is..." phrases): Add direct instructions in the system prompt: "Respond directly without preamble. Do not start with phrases like 'Here is...', 'Based on...', etc." **删除开场白** （去掉“以下是……”类表述）：在系统提示中添加直接指令：“直接回复，无需开场白。不要以‘以下是……’‘基于……’等表述开头。”
		- **Avoiding bad refusals:** Claude is much better at appropriate refusals now. Clear prompting in the user message without prefill should be sufficient.**避免不当拒绝：** Claude 现在在恰当拒绝方面表现出色得多。用户消息中无需预填的清晰提示应该就足够了。
		- **Continuations** (resuming interrupted responses): Move the continuation to the user message: "Your previous response was interrupted and ended with `[previous_response]`. Continue from where you left off." **继续回复** （恢复被中断的回复）：将继续内容移至用户消息中：“你之前的回复被中断，以 `[previous_response]` 结尾。请从中断处继续回复。”
		- **Context hydration / role consistency** (refreshing context in long conversations): Inject what were previously prefilled-assistant reminders into the user turn instead.**上下文填充/角色一致性** （长对话中刷新上下文）：将之前预设的助手提醒注入到用户轮次中。
2. **Tool parameter JSON escaping may differ 工具参数的 JSON 转义可能存在差异**
	This is a breaking change when migrating from Sonnet 4.5 or earlier.从 Sonnet 4.5 或更早版本迁移时，这是一项重大变更。
	JSON string escaping in tool parameters may differ from previous models. Standard JSON parsers handle this automatically, but custom string-based parsing may need updates.工具参数中的 JSON 字符串转义可能与之前的模型不同。标准 JSON 解析器会自动处理此问题，但基于字符串的自定义解析可能需要更新。

#### When migrating from Claude 3.x 从 Claude 3.x 迁移时

1. **Update sampling parameters 更新采样参数**
	This is a breaking change when migrating from Claude 3.x models.从 Claude 3.x 模型迁移时，这是一项破坏性变更。
	Use only `temperature` OR `top_p`, not both.仅使用 `temperature` 或 `top_p` ，不可同时使用。
2. **Update tool versions 更新工具版本**
	This is a breaking change when migrating from Claude 3.x models.从 Claude 3.x 模型迁移时，这是一项破坏性变更。
	Update to the latest tool versions (`text_editor_20250728`, `code_execution_20250825`). Remove any code using the `undo_edit` command.更新至最新工具版本（ `text_editor_20250728` 、 `code_execution_20250825` ）。删除所有使用 `undo_edit` 命令的代码。
3. **Handle the `refusal` stop reason 处理拒绝</b>停止原因**
	Update your application to [handle `refusal` stop reasons](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).将你的应用程序更新为 [能够处理 `refusal` 停止原因](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals) 。
4. **Update your prompts for behavioral changes 针对行为变化更新你的提示词**
	Claude 4 models have a more concise, direct communication style. Review [prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) for optimization guidance.Claude 4 模型采用更简洁、直接的沟通风格。查看 [提示词最佳实践](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) 获取优化指导。
1. **Remove `fine-grained-tool-streaming-2025-05-14` beta header:** Fine-grained tool streaming is now GA on Sonnet 4.6 and no longer requires a beta header.**移除 `fine-grained-tool-streaming-2025-05-14` 测试版标头：** 细粒度工具流式处理现已在 Sonnet 4.6 版本正式可用，不再需要测试版标头。
2. **Migrate `output_format` to `output_config.format`:** The `output_format` parameter is deprecated. Use `output_config.format` instead.**将 `output_format` 迁移至 `output_config.format` ：** `output_format` 参数已弃用。请改用 `output_config.format` 。

### Migrating from Sonnet 4.5 从 Sonnet 4.5 迁移

Consider migrating from Sonnet 4.5 to Sonnet 4.6, which delivers more intelligence at the same price point.考虑从 Sonnet 4.5 迁移至 Sonnet 4.6，后者在相同价格下能提供更强的智能能力。

Sonnet 4.6 defaults to an effort level of `high`, in contrast to Sonnet 4.5 which had no effort parameter. Consider adjusting the effort parameter as you migrate from Sonnet 4.5 to Sonnet 4.6. If not explicitly set, you may experience higher latency with the default effort level.十四行诗 4.6 默认为 `high` 效率级别，而十四行诗 4.5 没有效率参数。在从十四行诗 4.5 迁移到十四行诗 4.6 时，请考虑调整效率参数。如果未显式设置，默认效率级别可能会导致更高的延迟。

#### If you're not using extended thinking如果你未使用扩展思考

If you're not using extended thinking on Sonnet 4.5, you can continue without it on Sonnet 4.6. You should explicitly set effort to the level appropriate for your use case. At `low` effort with thinking disabled, you can expect similar or better performance relative to Sonnet 4.5 with no extended thinking.如果在 Sonnet 4.5 中未使用扩展思考，那么在 Sonnet 4.6 中也可以继续不使用它。你应明确将\*\*工作量\*\*设置为适合你用例的级别。在 `low` 工作量且禁用思考的情况下，相比未使用扩展思考的 Sonnet 4.5，你可以获得相似或更优的性能。

```
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-6",
    "max_tokens": 8192,
    "output_config": {
        "effort": "low"
    },
    "messages": [
        {
            "role": "user",
            "content": "Your prompt here"
        }
    ]
}'
```

#### If you're using extended thinking 如果你在使用扩展思考

If you're using extended thinking with `budget_tokens` on Sonnet 4.5, it is still functional on Sonnet 4.6 but is deprecated. Migrate to [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking) with the [effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort).如果你在 Sonnet 4.5 中使用了带有 `budget_tokens` 的扩展思维，该功能在 Sonnet 4.6 中仍可使用，但已被弃用。请迁移至带有 [效率参数](https://platform.claude.com/docs/en/build-with-claude/effort) 的 [自适应思维](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking) 功能。

##### Migrating to adaptive thinking 迁移至自适应思维

[Adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking) is the recommended replacement for `budget_tokens` on Sonnet 4.6. It is particularly well suited to the following workload patterns:[自适应思维](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking) 是 Sonnet 4.6 版本中推荐用来替代 `budget_tokens` 的功能。它特别适用于以下工作负载模式：

- **Autonomous multi-step agents:** coding agents that turn requirements into working software, data analysis pipelines, and bug finding where the model runs independently across many steps. Adaptive thinking lets the model calibrate its reasoning per step, staying on path over longer trajectories. For these workloads, start at `high` effort. If latency or token usage is a concern, scale down to `medium`.**自主多步智能体：** 这类编码智能体可将需求转化为可用软件、数据分析流程和漏洞检测工具，模型会独立完成多步操作。自适应思维能力让模型能针对每一步调整推理逻辑，在更长的操作流程中保持正确方向。针对这类工作负载，建议从 `high` 资源投入开始。若存在延迟或令牌使用量方面的顾虑，可将投入调整为 `medium` 。
- **Computer use agents:** Sonnet 4.6 achieved best-in-class accuracy on computer use evaluations using adaptive mode.**计算机使用智能体：** 十四行诗4.6在自适应模式的计算机使用评估中取得了同类最佳的准确率。
- **Bimodal workloads:** a mix of easy and hard tasks where adaptive skips thinking on simple queries and reasons deeply on complex ones.**双峰工作负载：** 由简单任务和复杂任务组成的混合负载，系统会对简单查询自适应跳过思考，对复杂查询进行深度推理。

When using adaptive thinking, evaluate `medium` and `high` effort on your tasks. The right level depends on your workload's tradeoff between quality, latency, and token usage.使用自适应思维时，评估任务的 `medium` 和 `high` 投入程度。合适的投入水平取决于你的工作量在质量、延迟和令牌使用量之间的权衡。

```
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-6",
    "max_tokens": 64000,
    "thinking": {
        "type": "adaptive"
    },
    "output_config": {
        "effort": "medium"
    },
    "messages": [
        {
            "role": "user",
            "content": "Your prompt here"
        }
    ]
}'
```

If you see inconsistent behavior or quality regressions with adaptive thinking, try lowering the [effort](https://platform.claude.com/docs/en/build-with-claude/effort) setting or using `max_tokens` as a hard limit first. Extended thinking with `budget_tokens` is still functional on Sonnet 4.6 but is deprecated and no longer recommended.如果发现自适应思维出现行为不一致或质量下降的情况，请先尝试降低 [工作量](https://platform.claude.com/docs/en/build-with-claude/effort) 设置，或将 `max_tokens` 作为硬性限制。在 Sonnet 4.6 中，使用 `budget_tokens` 的扩展思维功能仍可使用，但已被弃用，不再推荐。

##### Keeping budget\_tokens during migration迁移期间保留 budget\_tokens

If you need to keep `budget_tokens` temporarily while migrating, a budget around 16k tokens provides headroom for harder problems without risk of runaway token usage. This configuration is deprecated and will be removed in a future model release.如果在迁移过程中需要临时保留 `budget_tokens` ，约16000个token的预算能为更复杂的问题留出空间，同时避免token用量失控的风险。此配置已被弃用，将在未来的模型版本中移除。

###### Coding and agentic use cases 编码与智能体使用场景

For agentic coding, frontend design, tool-heavy workflows, and complex enterprise workflows, start with `medium` effort. If you find latency is too high, consider reducing effort to `low`. If you need higher intelligence, consider increasing effort to `high` or migrating to Opus 4.7.对于智能体编程、前端设计、工具密集型工作流以及复杂的企业工作流，从 `medium` 资源投入开始。如果发现延迟过高，可以考虑将资源投入降低至 `low` 。如果需要更高的智能能力，可以考虑将资源投入提升至 `high` 或迁移至 Opus 4.7。

```
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "anthropic-beta: interleaved-thinking-2025-05-14" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-6",
    "max_tokens": 16384,
    "thinking": {
        "type": "enabled",
        "budget_tokens": 16384
    },
    "output_config": {
        "effort": "medium"
    },
    "messages": [
        {
            "role": "user",
            "content": "Your prompt here"
        }
    ]
}'
```

###### Chat and non-coding use cases 聊天与非编码用例

For chat, content generation, search, classification, and other non-coding tasks, start with `low` effort with extended thinking. If you need more depth, increase effort to `medium`.对于聊天、内容生成、搜索、分类以及其他非编码类任务，先以低</b>投入度进行拓展思考。若需要更深入的内容，将投入度提升至中</b>。

```
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "anthropic-beta: interleaved-thinking-2025-05-14" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-6",
    "max_tokens": 8192,
    "thinking": {
        "type": "enabled",
        "budget_tokens": 16384
    },
    "output_config": {
        "effort": "low"
    },
    "messages": [
        {
            "role": "user",
            "content": "Your prompt here"
        }
    ]
}'
```

### Sonnet 4.6 migration checklist Sonnet 4.6 迁移清单

- Update model ID to `claude-sonnet-4-6` 将模型 ID 更新为 `claude-sonnet-4-6`
- **BREAKING:** Remove assistant message prefilling; use structured outputs or `output_config.format` instead **突发消息：** 移除助手消息预填充功能；请改用结构化输出或 `output_config.format`
- **BREAKING:** Verify tool parameter JSON parsing handles escaping differences **重大变更：** 验证工具参数的 JSON 解析是否能处理转义差异
- **BREAKING:** Update tool versions to latest (`text_editor_20250728`, `code_execution_20250825`); legacy versions are not supported (if migrating from 3.x) **突发：** 将工具版本更新至最新版（ `text_editor_20250728` 、 `code_execution_20250825` ）；不支持旧版（若从 3.x 版本迁移）
- **BREAKING:** Remove any code using the `undo_edit` command (if applicable) **重大变更：** 删除所有使用 `undo_edit` 命令的代码（如适用）
- **BREAKING:** Update sampling parameters to use only `temperature` OR `top_p`, not both (if migrating from 3.x) **突发新闻：** 更新采样参数，仅使用 `temperature` 或 `top_p` ，不同时使用两者（若从 3.x 版本迁移）
- Handle new `refusal` stop reason in your application 在你的应用程序中处理新的 `refusal` 停止原因
- Remove `fine-grained-tool-streaming-2025-05-14` beta header (now GA) 移除 `fine-grained-tool-streaming-2025-05-14` 测试版标头（现已正式发布）
- Migrate `output_format` to `output_config.format` 将 `output_format` 迁移至 `output_config.format`
- Review and update prompts following [prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) 按照 [提示词最佳实践](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) 审核并更新提示词
- **Recommended:** Migrate from `thinking: {type: "enabled", budget_tokens: N}` to `thinking: {type: "adaptive"}` with the [effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort) (`budget_tokens` is deprecated and will be removed in a future release) **推荐做法：** 将 `thinking: {type: "enabled", budget_tokens: N}` 迁移至带有 [effort 参数](https://platform.claude.com/docs/en/build-with-claude/effort) 的 `thinking: {type: "adaptive"}` （ `budget_tokens` 已被弃用，将在未来版本中移除）
- Test in development environment before production deployment 在生产环境部署前于开发环境中进行测试

---

## Migrating to Claude Sonnet 4.5 迁移至 Claude 索网 4.5

Claude Sonnet 4.5 combines strong intelligence with fast performance, making it ideal for everyday coding, analysis, and content tasks.Claude Sonnet 4.5 兼具强大的智能与快速的性能，非常适合日常编程、分析和内容创作类任务。

For a complete overview of capabilities, see the [models overview](https://platform.claude.com/docs/en/about-claude/models/overview).要了解所有功能的完整概览，请查看 [模型概览](https://platform.claude.com/docs/en/about-claude/models/overview) 。

Sonnet 4.5 pricing is $3 per million input tokens, $15 per million output tokens. See [Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing) for details.Sonnet 4.5 的定价为每百万输入令牌 3 美元，每百万输出令牌 15 美元。详情请查看 [Claude 定价](https://platform.claude.com/docs/en/about-claude/pricing) 。

**Update your model name: 更新你的模型名称：**

```
# From Sonnet 4
model = "claude-sonnet-4-20250514"  # Before
model = "claude-sonnet-4-5-20250929"  # After

# From Sonnet 3.7
model = "claude-3-7-sonnet-20250219"  # Before
model = "claude-sonnet-4-5-20250929"  # After
```

### Breaking changes 破坏性变更

These breaking changes apply when migrating from Claude 3.x Sonnet models.从 Claude 3.x 系列 Sonnet 模型迁移时，这些重大变更均适用。

1. **Update sampling parameters 更新采样参数**
	This is a breaking change when migrating from Claude 3.x models.从 Claude 3.x 模型迁移时，这是一项破坏性变更。
	Use only `temperature` OR `top_p`, not both.仅使用 `temperature` 或 `top_p` ，不可同时使用。
2. **Update tool versions 更新工具版本**
	This is a breaking change when migrating from Claude 3.x models.从 Claude 3.x 模型迁移时，这是一项破坏性变更。
	Update to the latest tool versions (`text_editor_20250728`, `code_execution_20250825`). Remove any code using the `undo_edit` command.更新至最新工具版本（ `text_editor_20250728` 、 `code_execution_20250825` ）。删除所有使用 `undo_edit` 命令的代码。
3. **Handle the `refusal` stop reason 处理拒绝</b>停止原因**
	Update your application to [handle `refusal` stop reasons](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).将你的应用程序更新为 [能够处理 `refusal` 停止原因](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals) 。
4. **Update your prompts for behavioral changes 针对行为变化更新你的提示词**
	Claude 4 models have a more concise, direct communication style. Review [prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) for optimization guidance.Claude 4 模型采用更简洁、直接的沟通风格。查看 [提示词最佳实践](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) 获取优化指导。

### Sonnet 4.5 migration checklist Sonnet 4.5 迁移清单

- Update model ID to `claude-sonnet-4-5-20250929` 将模型 ID 更新为 `claude-sonnet-4-5-20250929`
- **BREAKING:** Update tool versions to latest (`text_editor_20250728`, `code_execution_20250825`); legacy versions are not supported (if migrating from 3.x) **突发：** 将工具版本更新至最新版（ `text_editor_20250728` 、 `code_execution_20250825` ）；不支持旧版（若从 3.x 版本迁移）
- **BREAKING:** Remove any code using the `undo_edit` command (if applicable) **重大变更：** 删除所有使用 `undo_edit` 命令的代码（如适用）
- **BREAKING:** Update sampling parameters to use only `temperature` OR `top_p`, not both (if migrating from 3.x) **突发新闻：** 更新采样参数，仅使用 `temperature` 或 `top_p` ，不同时使用两者（若从 3.x 版本迁移）
- Handle new `refusal` stop reason in your application 在你的应用程序中处理新的 `refusal` 停止原因
- Review and update prompts following [prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) 按照 [提示词最佳实践](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) 审核并更新提示词
- Consider enabling extended thinking for complex reasoning tasks 考虑为复杂推理任务启用扩展思考功能
- Test in development environment before production deployment 在生产环境部署前于开发环境中进行测试

---

## Migrating to Claude Haiku 4.5 迁移至 Claude Haiku 4.5

Claude Haiku 4.5 is the fastest and most intelligent Haiku model with near-frontier performance, delivering premium model quality for interactive applications and high-volume processing.Claude Haiku 4.5 是速度最快、智能程度最高的 Haiku 模型，具备接近前沿的性能，可为交互式应用和高吞吐量处理场景提供优质的模型体验。

For a complete overview of capabilities, see the [models overview](https://platform.claude.com/docs/en/about-claude/models/overview).要了解所有功能的完整概览，请查看 [模型概览](https://platform.claude.com/docs/en/about-claude/models/overview) 。

Haiku 4.5 pricing is $1 per million input tokens, $5 per million output tokens. See [Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing) for details.Haiku 4.5 的定价为每百万输入令牌1美元，每百万输出令牌5美元。详情请查看 [Claude 定价](https://platform.claude.com/docs/en/about-claude/pricing) 。

**Update your model name: 更新你的模型名称：**

```
# From Haiku 3.5
model = "claude-3-5-haiku-20241022"  # Before
model = "claude-haiku-4-5-20251001"  # After

# From Haiku 3
model = "claude-3-haiku-20240307"  # Before
model = "claude-haiku-4-5-20251001"  # After
```

**Review new rate limits:** Haiku 4.5 has separate rate limits from Haiku 3.5 and Haiku 3. See [Rate limits documentation](https://platform.claude.com/docs/en/api/rate-limits) for details.**查看新的速率限制：** Haiku 4.5 与 Haiku 3.5 和 Haiku 3 拥有独立的速率限制。详情请参阅 [速率限制文档](https://platform.claude.com/docs/en/api/rate-limits) 。

For significant performance improvements on coding and reasoning tasks, consider enabling extended thinking with `thinking: {type: "enabled", budget_tokens: N}`.要在编码和推理任务上获得显著的性能提升，请考虑启用 `thinking: {type: "enabled", budget_tokens: N}` 扩展思考功能。

Extended thinking impacts [prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#caching-with-thinking-blocks) efficiency.扩展思考会影响 [提示词缓存](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#caching-with-thinking-blocks) 的效率。

Extended thinking is deprecated in Claude 4.6 or newer models. If using newer models, use [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking) instead.Claude 4.6 及更新版本已弃用扩展思考。如果使用更新的模型，请改用 [自适应思考](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking) 。

**Explore new capabilities:** See the [models overview](https://platform.claude.com/docs/en/about-claude/models/overview) for details on context awareness, increased output capacity (64k tokens), higher intelligence, and improved speed.**探索新功能：** 查看 [模型概览](https://platform.claude.com/docs/en/about-claude/models/overview) ，了解上下文感知、更高输出容量（64k 令牌）、更强智能以及更快速度的相关详情。

### Breaking changes 破坏性变更

These breaking changes apply when migrating from Claude 3.x Haiku models.从 Claude 3.x Haiku 模型迁移时，这些重大变更均适用。

1. **Update sampling parameters 更新采样参数**
	This is a breaking change when migrating from Claude 3.x models.从 Claude 3.x 模型迁移时，这是一项破坏性变更。
	Use only `temperature` OR `top_p`, not both.仅使用 `temperature` 或 `top_p` ，不可同时使用。
2. **Update tool versions 更新工具版本**
	This is a breaking change when migrating from Claude 3.x models.从 Claude 3.x 模型迁移时，这是一项破坏性变更。
	Update to the latest tool versions (`text_editor_20250728`, `code_execution_20250825`). Remove any code using the `undo_edit` command.更新至最新工具版本（ `text_editor_20250728` 、 `code_execution_20250825` ）。删除所有使用 `undo_edit` 命令的代码。
3. **Handle the `refusal` stop reason 处理拒绝</b>停止原因**
	Update your application to [handle `refusal` stop reasons](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).将你的应用程序更新为 [能够处理 `refusal` 停止原因](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals) 。
4. **Update your prompts for behavioral changes 针对行为变化更新你的提示词**
	Claude 4 models have a more concise, direct communication style. Review [prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) for optimization guidance.Claude 4 模型采用更简洁、直接的沟通风格。查看 [提示词最佳实践](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) 获取优化指导。

### Haiku 4.5 migration checklist Haiku 4.5 迁移清单

- Update model ID to `claude-haiku-4-5-20251001` 将模型 ID 更新为 `claude-haiku-4-5-20251001`
- **BREAKING:** Update tool versions to latest (`text_editor_20250728`, `code_execution_20250825`); legacy versions are not supported **突发消息：** 将工具版本更新至最新版（ `text_editor_20250728` 、 `code_execution_20250825` ）；旧版本不再受支持
- **BREAKING:** Remove any code using the `undo_edit` command (if applicable) **重大变更：** 删除所有使用 `undo_edit` 命令的代码（如适用）
- **BREAKING:** Update sampling parameters to use only `temperature` OR `top_p`, not both **突发消息：** 更新采样参数，仅使用 `temperature` 或 `top_p` ，不同时使用两者
- Handle new `refusal` stop reason in your application 在你的应用程序中处理新的 `refusal` 停止原因
- Review and adjust for new rate limits (separate from Haiku 3.5) 针对新的速率限制进行审核与调整（与 Haiku 3.5 相互独立）
- Review and update prompts following [prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) 按照 [提示词最佳实践](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) 审核并更新提示词
- Consider enabling extended thinking for complex reasoning tasks 考虑为复杂推理任务启用扩展思考功能
- Test in development environment before production deployment 在生产环境部署前于开发环境中进行测试

---

## Get help 获取帮助

- Check the [API documentation](https://platform.claude.com/docs/en/api/overview) for detailed specifications 查看 [API 文档](https://platform.claude.com/docs/en/api/overview) 以获取详细规范
- Review [model capabilities](https://platform.claude.com/docs/en/about-claude/models/overview) for performance comparisons 查看 [模型功能](https://platform.claude.com/docs/en/about-claude/models/overview) 以进行性能对比
- Review [API release notes](https://platform.claude.com/docs/en/release-notes/api) for API updates 查看 [API 版本说明](https://platform.claude.com/docs/en/release-notes/api) 以了解 API 的更新内容
- Contact support if you encounter any issues during migration 如果在迁移过程中遇到任何问题，请联系技术支持

Was this page helpful? 此页面是否有帮助？